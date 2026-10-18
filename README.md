# AI Stock Researcher

I built this project to improve my Python programming skills while also exploring my interest in stock trading and quantitative analysis. Through coding this project, I've gained valuable experience working with real financial data, integrating APIs, and building a program that can analyse companies automatically.


## Features

- Retrieves company information and historical stock prices using Yahoo Finance.
- Analyses revenue growth, profit margins, free cash flow, and P/E ratios.
- Calculates a financial score based on available metrics.
- Measures changes in stock prices between trading sessions.
- Uses Gemini AI to explain financial strengths and potential risks.
- Allows users to analyse multiple companies in one session.
- Handles invalid stock tickers, missing data, and API errors.

## Technologies Used

- Python
- yfinance
- Google Gemini API
- Pandas (through yfinance)
- python-dotenv

## Installation

1. Clone this repository and open the project folder.

2. Install the required Python packages:

```bash
python3 -m pip install yfinance google-genai python-dotenv
```

3. Create a `.env` file in the project folder and add your own Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

4. Run the program:

```bash
python3 main.py
```

## Usage

Enter a stock ticker when prompted, such as `AAPL`, `NVDA`, or `MSFT`.

The program retrieves financial information, calculates a simplified financial score, and generates a structured AI analysis using Gemini.

After each report, users can choose whether to analyse another company.

## Disclaimer

This project was developed for educational purposes. Its financial scoring system uses simplified rules and should not be considered professional investment advice. The AI-generated reports are based on the financial data provided and may contain inaccuracies.