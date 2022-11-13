from flask import Flask
from ..assets.stocks import Stocks

app = Flask(__name__)

@app.route("/api/stock-companies", methods=["GET"])
def get_stock_companies():
    return Stocks.get_dji_stock_info()

app.run()