import requests

class EconEnvironment:
   POOR_ENV = "POOR_ENV"
   INTERMEDIATE_ENV = "INTERMEDIATE_ENV"
   EXCELLENT_ENV = "EXCELLENT_ENV"
   UNEMPLOYMENT_THRESHOLD = 4 # percent
   INFLATION_THRESHOLD = 7 # percent
   
   KEY = "registrationkey=9161024e13354d91b75d021708f62f3e"
   BLS_UNEMPLOYMENT_URL = f"https://api.bls.gov/publicAPI/v2/timeseries/data/LNS14000000?latest=true&{KEY}"
   BLS_INFLATION_URL = f"https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?{KEY}"

   def __init__(self):
      self.inflation_rate = 0.0
      self.unemployment_rate = 0.0
      self.calc_inflation_rate()
      self.calc_unemployment_rate()

   def get_econ_env(self):
      if self.unemployment_rate > 0 and self.unemployment_rate < self.UNEMPLOYMENT_THRESHOLD \
         and self.inflation_rate > 0 and self.inflation_rate < self.INFLATION_THRESHOLD:
         return self.EXCELLENT_ENV
      elif (self.unemployment_rate > 0 and self.unemployment_rate < self.UNEMPLOYMENT_THRESHOLD) \
         or (self.inflation_rate > 0 and self.inflation_rate < self.INFLATION_THRESHOLD):
         return self.INTERMEDIATE_ENV
      else:
         return self.POOR_ENV
   
   def calc_inflation_rate(self):
       cpi, prev_year_cpi = self.fetch_cpis()
       self.inflation_rate = self.compute_inflation_rate(cpi, prev_year_cpi)
       return self.inflation_rate

   def compute_inflation_rate(self, cpi: float, prev_year_cpi: float):
      return 100 * (cpi - prev_year_cpi) / prev_year_cpi

   @classmethod
   def fetch_cpis(cls):
      res = requests.get(cls.BLS_INFLATION_URL)
      res_dict = res.json()

      arr = res_dict["Results"]["series"][0]["data"]

      def search_cpi(arr: list, year: str, month: str)->str:
         ans = ""
         for cpi_obj in arr:
            if cpi_obj["year"] == year and cpi_obj["periodName"] == month:
               ans = cpi_obj["value"]
               break
         return ans

      # extract the CPI
      cpi_recent_obj = arr[0]
      prev_year = str(int(cpi_recent_obj["year"]) - 1)
      month = cpi_recent_obj["periodName"]
      cpi_recent = float(cpi_recent_obj["value"])

      cpi_prev = float(search_cpi(arr, prev_year, month))

      return cpi_recent, cpi_prev

   def calc_unemployment_rate(self):
      self.unemployment_rate = self.fetch_unemployment_rate()
      return self.unemployment_rate
   
   @classmethod
   def fetch_unemployment_rate(cls):
      res = requests.get(cls.BLS_UNEMPLOYMENT_URL)
      res_dict = res.json()

      arr = res_dict["Results"]["series"][0]["data"]

      return float(arr[0]["value"])
