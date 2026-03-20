# Binance Futures Testnet Trading Bot

A beginner-friendly Python CLI app that places **MARKET** and **LIMIT** orders on **Binance USDⓈ-M Futures Testnet**.

## Features
- Place `MARKET` and `LIMIT` orders
- Supports both `BUY` and `SELL`
- CLI input validation
- Structured code with separate layers:
  - `bot/client.py` → API client
  - `bot/orders.py` → order logic
  - `bot/validators.py` → validation
  - `cli.py` → command entry point
- Logging to `logs/trading_bot.log`
- Error handling for validation, API, config, and network failures

## Project Structure
```text
trading_bot_project/
  bot/
    __init__.py
    client.py
    exceptions.py
    logging_config.py
    orders.py
    validators.py
  cli.py
  README.md
  requirements.txt
  .env.example
```

## Setup
1. Create a Binance Futures Testnet account.
2. Generate API credentials.
3. Clone/download this project.
4. Create and activate a virtual environment.
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```

## Run Examples
### MARKET BUY
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### MARKET SELL
```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### LIMIT BUY
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 20000
```

### LIMIT SELL
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

## Output
The CLI prints:
- order request summary
- order response details
- success/failure message

## Logging
Logs are written to:
```text
logs/trading_bot.log
```
The log includes:
- request method/url/payload
- response status/body
- validation or runtime errors

## Important Note About Testnet Base URL
The assignment says to use:
```text
https://testnet.binancefuture.com
```
Binance official USDⓈ-M Futures docs currently show the testnet REST base URL as:
```text
https://demo-fapi.binance.com
```
This project keeps the base URL configurable through `BINANCE_BASE_URL` so you can match the assignment or switch to the official current doc value if needed.

## Assumptions
- Only `MARKET` and `LIMIT` orders are required.
- LIMIT orders use `timeInForce=GTC`.
- Credentials are stored in environment variables via `.env`.
- The bot is for **testnet only**, not mainnet.

## Deliverables Checklist
Before sending your submission, add these real files from your own run:
- public GitHub repo or zip
- source code
- README
- requirements.txt
- log file containing one MARKET order
- log file containing one LIMIT order

## Suggested Submission Steps
1. Run one MARKET order and save the generated log.
2. Run one LIMIT order and save the generated log.
3. Push everything to GitHub.
4. Email your resume + GitHub link + logs.

## Common Errors
- `Missing Binance API credentials` → fill `.env`
- `price is required for LIMIT orders` → pass `--price`
- Binance API error about precision/minQty → try a smaller or valid quantity/price for that symbol

## Bonus Idea
A simple optional bonus is to add a menu-based CLI using `Typer` or `Click` after the base version works.
