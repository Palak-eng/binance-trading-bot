📌 Binance Futures Testnet Trading Bot (CLI)

A Python-based CLI trading bot that interacts with the Binance Futures Testnet (USDT-M) to place MARKET and LIMIT orders with proper validation, logging, and error handling.

🚀 Features

✅ Place MARKET and LIMIT orders

✅ Supports both BUY and SELL

✅ CLI-based input using argparse

✅ Input validation (symbol, side, type, quantity, price)

✅ Structured code (client, orders, validators)

✅ Logging of API requests, responses, and errors

✅ Exception handling (API errors, network issues, invalid input)

✅ Test mode (--test) for safe order validation

✅ Enhanced CLI UI with colorized output

📂 Project Structure
trading_bot/
│
├── bot/
│   ├── client.py          # Binance API client
│   ├── orders.py          # Order logic
│   ├── validators.py      # Input validation
│   ├── logging_config.py  # Logging setup
│   ├── exceptions.py
│
├── cli.py                 # CLI entry point
├── requirements.txt
├── README.md
├── .env.example
├── sample_logs/           # Example logs (for submission)
⚙️ Setup Instructions
1. Clone repository
git clone https://github.com/Palak-eng/binance-trading-bot.git
cd binance-trading-bot
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
BINANCE_BASE_URL=https://testnet.binancefuture.com
▶️ Usage Examples
🟢 Market Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
🔵 Limit Order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 80000
🧪 Test Order (No Execution)
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002 --test
📊 Sample Output
=== ORDER REQUEST SUMMARY ===
Symbol      : BTCUSDT
Side        : BUY
Order Type  : MARKET
Quantity    : 0.002
Mode        : TEST

Processing order...

=== ORDER RESPONSE ===
Test order successful (not executed)
📁 Logs

The application logs:

API requests

API responses

Errors

Sample logs are included in:

sample_logs/
⚠️ Assumptions

Uses Binance Futures Testnet

Minimum notional value must be ≥ 100 USDT

API keys must have Futures trading permissions enabled

🛠️ Technologies Used

Python 3.x

Requests

python-dotenv

Colorama (CLI UI)

📌 Notes

This project is designed for learning and testing purposes only

Test mode is available to validate orders safely without execution

👨‍💻 Author

Palak Barsaiyan