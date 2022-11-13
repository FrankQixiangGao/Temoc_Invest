import requests
from datetime import datetime

class TreasuryBond:
   API_AVG_US_SECURITIES = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?sort=-record_date'
   BOND_NAME = 'Treasury Bonds'

   def __init__(self):
      self.avg_interest_rate = 0.0 # percent
      self.date = datetime.today()
      self.calc_rate()
   
   def calc_rate(self):
      self.avg_interest_rate, self.date = self.fetch_avg_interest_rate()
      return self.avg_interest_rate, self.date
   
   @classmethod
   def fetch_avg_interest_rate(cls):
      res = requests.get(cls.API_AVG_US_SECURITIES)
      res_dict = res.json()

      def search_most_recent_value(arr: list):
         rate = 0.0
         date = None
         for obj in arr:
            if obj["security_desc"] == cls.BOND_NAME:
               rate = float(obj["avg_interest_rate_amt"])
               date = datetime.strptime(obj["record_date"], "%Y-%m-%d")
               break
         return rate, date
      
      return search_most_recent_value(res_dict["data"])