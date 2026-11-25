"""unsafe_allow_html 로 들어가는 값이 모두 이스케이프되는지 확인한다 (4-10).

AI 출력(result['title']/['body'])과 CSV 값(persona, product, brand_tone)이 그대로 HTML 로
들어가면 <img onerror=...> 같은 태그가 브라우저에서 실행된다.
"""
import ast
import html
import pathlib
import unittest

APP = pathlib.Path(__file__).resolve().parents[1] / "src" / "ui" / "app.py"


def _unsafe_html_interpolations(tree):
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "markdown"):
            continue
        if not any(
            kw.arg == "unsafe_allow_html" and getattr(kw.value, "value", False) is True
            for kw in node.keywords
        ):
            continue
        for arg in node.args:
            for sub in ast.walk(arg):
                if isinstance(sub, ast.FormattedValue):
                    expr = sub.value
                    # esc() 로 감싼 값, 또는 int()/float() 로 숫자만 뽑는 식은 안전하다
                    if "esc(" in ast.unparse(expr):
                        continue
                    if isinstance(expr, ast.Call) and getattr(expr.func, "id", "") in ("int", "float"):
                        continue
                    offenders.append(ast.unparse(expr))
    return offenders


class HtmlEscapingTest(unittest.TestCase):
    def test_every_value_in_raw_html_is_escaped(self):
        tree = ast.parse(APP.read_text(encoding="utf-8"), str(APP))
        self.assertEqual(_unsafe_html_interpolations(tree), [])

    def test_escape_helper_escapes_angle_brackets(self):
        namespace = {"html": html}
        source = APP.read_text(encoding="utf-8")
        module = ast.parse(source, str(APP))
        esc_def = next(
            node for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name == "esc"
        )
        exec(compile(ast.Module(body=[esc_def], type_ignores=[]), str(APP), "exec"), namespace)
        escaped = namespace["esc"]("<img src=x onerror=alert(1)>")
        self.assertEqual(escaped, "&lt;img src=x onerror=alert(1)&gt;")


if __name__ == "__main__":
    unittest.main()
