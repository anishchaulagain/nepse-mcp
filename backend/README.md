# NEPSE AI — Stock Prediction Backend

A production-grade **FastAPI** backend for the Nepal Stock Exchange (NEPSE) analysis platform, integrating **Clean Architecture**, **Modular Services**, and **Model Context Protocol (MCP)**.

## 🚀 Features

- **Indicator Engine**: Real-time calculation of SMA, RSI, MACD, and Bollinger Bands using `pandas` and `numpy`.
- **Rule-Based Prediction**: Comprehensive scoring system for trend forecasting, confidence ranking, and signal analysis.
- **Breakout Detection**: Automated pattern recognition for resistance breaks, volume spikes, and Bollinger squeezes.
- **AI Analysis**: Integration with **Groq LLM (LLama 3.3 70B)** for human-readable quantified explanations.
- **MCP Server**: Full tool exposure for LLM-based agentic tools:
  - `get_stock_candles`: Fetch historical OHLCV.
  - `calculate_indicators`: Multi-indicator data.
  - `predict_trend`: Signal-based trend forecasting.
  - `detect_breakout`: Automated pattern detection.
  - `analyze_stock`: Complete AI analysis with explanations.
- **Backtesting Service**: Full quantitative strategy simulation with trade history and performance metrics.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Data processing**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) (Model-driven via SQLAlchemy)
- **Cache**: [Redis](https://redis.io/)
- **AI Integration**: [Groq](https://groq.com/)
- **Protocol**: [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

## 🏁 Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (for Postgres/Redis)
- Groq API Key

### Installation

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure environment:
    Create a `.env` file from the example:
    ```bash
    cp .env.example .env
    # Add your GROQ_API_KEY
    ```

5.  Run the application:
    ```bash
    python -m uvicorn app.main:app --reload --port 8000
    ```

## 🏗 Backend Architecture

```
app/
├── main.py                    # Entry point & CORS
├── config/                    # Settings & env vars
├── core/                      # Business logic & indicators
├── api/routes/                # API endpoints
├── services/                  # Orchestration & third-party integrations
├── mcp/                       # MCP server & tools
├── schemas/                   # Pydantic models
├── models/                    # DB models
└── utils/                     # Helpers & logging
```

## 📜 API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
