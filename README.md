# Amore Marketing Agent

A professional AI-powered marketing agent system designed to generate personalized marketing content using advanced RAG (Retrieval Augmented Generation) technology.

## Overview

The Amore Marketing Agent leverages LLM technology to create targeted marketing messages based on product information, customer personas, and communication tones. The system combines vector database search capabilities with intelligent agent-based content generation.

## Features

- **Data Crawling**: Automated data collection and processing
- **RAG System**: Vector database-powered retrieval for contextual marketing
- **AI Agents**: LLM-based persona management and message generation
- **Interactive Dashboard**: Streamlit-powered UI for easy interaction
- **Modular Architecture**: Clean, maintainable code structure

## Project Structure

```
Amore_Marketing_Agent/
├── data/                          # Raw CSV data storage
│   ├── products.csv              # Product information
│   ├── personas.csv              # Customer personas
│   └── tones.csv                 # Communication tones
├── src/                          # Core source code
│   ├── crawling/                 # Data collection scripts
│   ├── rag/                      # Vector DB and retrieval logic
│   ├── agent/                    # LLM persona and message generation
│   └── ui/                       # Streamlit dashboard
├── config/                       # Configuration files
│   └── .env                      # Environment variables
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites

- Python 3.11
- GOOGLE_API_KEY

### Installation

1. Clone or download this repository

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Open `config/.env`
   - Add your GOOGLE_API_KEY:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Technology Stack

- **LLM Framework**: LangChain, OpenAI
- **Vector Database**: ChromaDB
- **Data Processing**: Pandas
- **UI Framework**: Streamlit
- **Utilities**: python-dotenv, Faker

## Usage

(Usage instructions will be added as features are implemented)

## Development

This project follows a modular architecture:
- Each module in `src/` is a separate package
- Configuration is centralized in `config/`
- Data files are stored in `data/`

## License

This project is proprietary.

## Contact

For questions or support, please contact the development team.
