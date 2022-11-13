from .model.cpo import ConstrainedPortfolioOptimization

class Currencies:
   CUR = [
      "CAD=X",
      "EUR=X",
      "GBP=X",
      "HKD=X",
      "JPY=X"
   ]

   def __init__(self):
      self.cpo = ()
      pass

   def optimize(self):
      self.cpo = ConstrainedPortfolioOptimization.train_non_stocks(self.CUR)
