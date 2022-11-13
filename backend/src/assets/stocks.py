from .model.cpo import ConstrainedPortfolioOptimization
import pandas as pd
import json

class Stocks:
   DJI_STOCKS = [
      "MMM",
      "AXP",
      "AMGN",
      "AAPL",
      "BA",
      "CAT",
      "CVX",
      "CSCO",
      "KO",
      "DIS",
      "GS",
      "HD",
      "HON",
      "IBM",
      "INTC",
      "JNJ",
      "JPM",
      "MCD",
      "MRK",
      "MSFT",
      "NKE",
      "PG",
      "CRM",
      "TRV",
      "UNH",
      "VZ",
      "V",
      "WBA",
      "WMT"
   ]

   DJI_STOCK_DF = pd.read_csv("https://wavta-nlp-data.s3.us-east-2.amazonaws.com/dji30.csv")
   
   def __init__(self):
      pass

   @classmethod
   def get_dji_stock_info(cls):
      return json.loads(cls.DJI_STOCK_DF.to_json(orient='records'))


   def optimize(self):
      cpo = ConstrainedPortfolioOptimization.train(self.DJI_STOCKS)



