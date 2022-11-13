from flask import Flask, request
from ..assets.stocks import Stocks
from ..assets.currency import Currencies
from ..assets.bonds import TreasuryBond
from ..macroeconomics import EconEnvironment
import numpy as np

app = Flask(__name__)

equity = ["stocks", "currencies", "bonds"]

stocks_g = Stocks()
stocks_g.optimize()
currencies_g = Currencies()
currencies_g.optimize()
bonds_g = TreasuryBond()


def stock_mix(ann_risk, return_eff, idx):
    pairs = np.c_[return_eff, ann_risk]
    sorted(pairs, key=lambda x: x[0])
    return pairs[idx][0], pairs[idx][1] # return vs risk


def get_mix(equity_arr: list[str], interest: float, risk: float, stocks: Stocks, currencies: Currencies, bonds: TreasuryBond):
    mixture = {}
    idx = 0
    for equity_name in equity_arr:
        if equity_name == "stocks":
            ann_risk_list, return_eff = stocks.cpo
            ret, ri = stock_mix(return_eff, ann_risk_list, idx)
            next_interest = interest - ret
            pass
        elif equity_name == "currencies":
            ann_risk_list, return_eff = currencies.cpo
            ret, ri = stock_mix(return_eff, ann_risk_list, idx)
            next_interest = interest - ret
            pass
        elif equity_name == "bonds":
            return_eff = bonds.avg_interest_rate
            pass
        else:
            pass
        idx += 1
        pass

def get_risk(s: float, cur: float, bon: float, stocks: Stocks, currencies: Currencies, bonds: TreasuryBond):
    risk = 0
    assignment = [s, cur]
    idx = 0
    for equity in [stocks, currencies]:
        ann_risk, return_eff = equity.cpo
        pairs = np.c_[ann_risk, return_eff]
        sorted(pairs, key=lambda x: x[0])
        risk += pairs[0][0] * assignment[idx]
        idx += 1
    risk += 0 # bonds we do not assume risks
    return risk


@app.route("/api/stock-companies", methods=["GET"])
def get_stock_companies():
    return Stocks.get_dji_stock_info()

@app.route("/api/get-risk", methods=["POST"])
def get_portfolio_risk():
    req_body = request.get_json()
    print(req_body)
    s = req_body["stocks"]
    c = req_body["currencies"]
    b = req_body["bonds"]
    return get_risk(s, c, b, stocks_g, currencies_g, bonds_g)

@app.route("/api/get-mixture", methods=["POST"])
def get_equity_mixture():
    req_body = request.get_json()
    ann_interest_goal = req_body["annual_interest"]
    risk_level_goal = req_body["risk_level"]

    macro_econ = EconEnvironment()
    macro_env = macro_econ.get_econ_env()
    if EconEnvironment.POOR_ENV == macro_env:
        # poor env
        # start with low risk equity investment
        equity_order = equity[::-1]

        pass
    elif EconEnvironment.INTERMEDIATE_ENV == macro_env:
        # intermediate
        # start with high risk equity investment

        pass
    else:
        # excellent env
        # start with high risk equity investment

        pass

app.run()
