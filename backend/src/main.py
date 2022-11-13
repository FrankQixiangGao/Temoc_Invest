from .macroeconomics import EconEnvironment
from .assets.bonds import TreasuryBond
from .assets.stocks import Stocks
from .assets.currency import Currencies

if __name__ == '__main__':
   # macro_econ = EconEnvironment()
   # print(macro_econ.get_econ_env())

   # bond = TreasuryBond()
   # print(bond.avg_interest_rate, bond.date)

   cur = Currencies()
   cur.optimize()





