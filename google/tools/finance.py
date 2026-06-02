"""Financial tools for Google ADK agents using yfinance."""

from datetime import datetime
from typing import Dict, List

import yfinance as yf


def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """
    Fetches the current stock price and daily change for a list of stock tickers
    using the yfinance library.

    Args:
        tickers: A list of stock market tickers (e.g., ["GOOG", "NVDA"]).

    Returns:
        A dictionary mapping each ticker to its formatted financial data string.
    """
    financial_data: Dict[str, str] = {}
    for ticker_symbol in tickers:
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info

            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")

            if price is not None and change_percent is not None:
                change_str = f"{change_percent * 100:+.2f}%"
                financial_data[ticker_symbol] = f"${price:.2f} ({change_str})"
            else:
                financial_data[ticker_symbol] = "Price data not available."

        except Exception:
            financial_data[ticker_symbol] = "Invalid Ticker or Data Error"

    return financial_data


def get_market_summary() -> Dict[str, str]:
    """
    Fetches current values and daily changes for major US market indices:
    S&P 500, NASDAQ Composite, and Dow Jones Industrial Average.

    Returns:
        A dictionary mapping each index name to its current value and daily change.
    """
    indices = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI",
    }
    summary: Dict[str, str] = {}
    for name, symbol in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")

            if price is not None and change_percent is not None:
                change_str = f"{change_percent * 100:+.2f}%"
                summary[name] = f"{price:,.2f} ({change_str})"
            else:
                summary[name] = "Data not available."
        except Exception:
            summary[name] = "Error fetching data."

    summary["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    return summary


def get_company_info(ticker: str) -> Dict[str, str]:
    """
    Fetches key company details for a given US-listed stock ticker,
    including sector, headquarters, CEO, employee count, and market cap.

    Args:
        ticker: A stock market ticker symbol (e.g., "GOOG").

    Returns:
        A dictionary with company information fields.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        market_cap = info.get("marketCap")
        market_cap_str = (
            f"${market_cap / 1e9:.1f}B" if market_cap else "N/A"
        )

        return {
            "name": info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "headquarters": f"{info.get('city', 'N/A')}, {info.get('state', 'N/A')}",
            "ceo": info.get("companyOfficers", [{}])[0].get("name", "N/A")
            if info.get("companyOfficers")
            else "N/A",
            "employees": f"{info.get('fullTimeEmployees', 'N/A'):,}"
            if info.get("fullTimeEmployees")
            else "N/A",
            "market_cap": market_cap_str,
            "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        }
    except Exception:
        return {"error": f"Could not fetch info for ticker: {ticker}"}
