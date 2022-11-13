import numpy as np
import pandas as pd
from scipy import optimize
from .. import util

class ConstrainedPortfolioOptimization:
   HIGH_VAL_BOUND = (0.0, 0.1)
   LOW_VAL_BOUND = (0.0, 1.0)

   def __init__(self):
      pass

   @classmethod
   def train(cls, symbols: list[str], upper_selection_constraint=[0.5,0.5], lower_selection_constraint=[0.01,0.01]):
      # reference: https://www.kaggle.com/code/vijipai/lesson-7-constrained-portfolio-optimization/notebook
      # function computes asset returns 
      def StockReturnsComputing(StockPrice, Rows, Columns):         
         StockReturn = np.zeros([Rows-1, Columns])
         for j in range(Columns):        # j: Assets
            for i in range(Rows-1):     # i: Daily Prices
                  StockReturn[i,j]=((StockPrice[i+1, j]-StockPrice[i,j])/StockPrice[i,j])*100
         return StockReturn

      #compute stock returns for k-portfolio 1 and market returns to compute asset betas

      #input k portfolio 1 dataset  comprising 15 Dow stocks and DJIA market dataset 
      #over a 3 Year period (April 2016 to April 2019)
      stockColumns = len(symbols)  #excluding date of stock dataset 

      #read stock prices and closing prices of market data (column index 4),  into dataframes
      stockData = util.read_stock_prices(symbols)
      marketData = util.read_market_prices()

      #extract asset labels in the portfolio
      assetLabels = stockData.columns.tolist()
      print('Asset labels of k-portfolio 1: \n', assetLabels)

      #compute asset returns
      arStockPrices = np.asarray(stockData)
      [sRows, sCols]=arStockPrices.shape
      arStockReturns = StockReturnsComputing(arStockPrices, sRows, sCols)

      #compute market returns
      arMarketPrices = np.asarray(marketData)
      [mRows, mCols]=arMarketPrices.shape
      arMarketReturns = StockReturnsComputing(arMarketPrices, mRows, mCols)

      #compute betas of the assets in k-portfolio 1
      beta= []
      Var = np.var(arMarketReturns, ddof =1)
      for i in range(stockColumns):
         CovarMat = np.cov(arMarketReturns[:,0], arStockReturns[:,i])
         Covar  = CovarMat[1,0]
         beta.append(Covar/Var)

      #display results
      print('Asset Betas:\n')
      for data in beta:
         print('{:9.3f}'.format(data))

      selection_matrix1 = []
      selection_matrix2 = []
      bounds = []
      for data in beta:
         if data >= 1:
            selection_matrix1.append(1)
            selection_matrix2.append(0)
            bounds.append(cls.HIGH_VAL_BOUND)
         else:
            selection_matrix1.append(0)
            selection_matrix2.append(1)
            bounds.append(cls.LOW_VAL_BOUND)
      
      selection = [selection_matrix2, selection_matrix1]


      #input k portfolio 1 dataset comprising 15 Dow stocks
      Columns = stockColumns

      #compute asset returns
      arStockPrices = np.asarray(stockData)
      [Rows, Cols]=arStockPrices.shape
      arReturns = StockReturnsComputing(arStockPrices, Rows, Cols)

      #set precision for printing data
      np.set_printoptions(precision=3, suppress = True)

      #compute mean returns and variance covariance matrix of returns
      meanReturns = np.mean(arReturns, axis = 0)
      covReturns = np.cov(arReturns, rowvar=False)
      print('\nMean Returns:\n', meanReturns)
      print('\nVariance-Covariance Matrix of Returns:\n', covReturns)

      #function to handle bi-criterion portfolio optimization with constraints
      def BiCriterionFunctionOptmzn(MeanReturns, CovarReturns, RiskAversParam, PortfolioSize):
         def  f(x, MeanReturns, CovarReturns, RiskAversParam, PortfolioSize):
            PortfolioVariance = np.matmul(np.matmul(x, CovarReturns), x.T) 
            PortfolioExpReturn = np.matmul(np.array(MeanReturns),x.T)
            func = RiskAversParam * PortfolioVariance - (1-RiskAversParam)*PortfolioExpReturn
            return func

         def ConstraintEq(x):
            A=np.ones(x.shape)
            b=1
            constraintVal = np.matmul(A,x.T)-b 
            return constraintVal
         
         def ConstraintIneqUpBounds(x):
            A=selection
            bUpBounds =np.array(upper_selection_constraint).T
            constraintValUpBounds = bUpBounds-np.matmul(A,x.T)    # type: ignore
            return constraintValUpBounds

         def ConstraintIneqLowBounds(x):
            A=selection
            bLowBounds =np.array(lower_selection_constraint).T
            constraintValLowBounds = np.matmul(A,x.T)-bLowBounds    # type: ignore
            return constraintValLowBounds
         
         xinit=np.repeat(0.01, PortfolioSize)
         cons = ({'type': 'eq', 'fun':ConstraintEq}, \
                  {'type':'ineq', 'fun': ConstraintIneqUpBounds},\
                  {'type':'ineq', 'fun': ConstraintIneqLowBounds})

         opt = optimize.minimize(f, x0 = xinit, args = ( MeanReturns, CovarReturns,\
                                                         RiskAversParam, PortfolioSize), \
                                 method = 'SLSQP',  bounds = bounds, constraints = cons, \
                                 tol = 10**-3)
         print(opt)
         return opt


      #obtain optimal portfolios for the constrained portfolio optimization model
      #Maximize returns and Minimize risk with fully invested, bound and 
      #class constraints

      #set portfolio size 
      portfolioSize = Columns

      #initialization
      xOptimal =[]
      minRiskPoint = []
      expPortfolioReturnPoint =[]

      for points in range(0,60):
         riskAversParam = points/60.0
         result = BiCriterionFunctionOptmzn(meanReturns, covReturns, riskAversParam, portfolioSize)
         xOptimal.append(result.x)

      #compute annualized risk and return  of the optimal portfolios for trading days = 251
      trading_days = 251

      xOptimalArray = np.array(xOptimal)
      minRiskPoint = np.diagonal(np.matmul((np.matmul(xOptimalArray,covReturns)), np.transpose(xOptimalArray)))
      riskPoint =   np.sqrt(minRiskPoint*trading_days) 
      expPortfolioReturnPoint= np.matmul(xOptimalArray, meanReturns )
      retPoint = trading_days*np.array(expPortfolioReturnPoint) 

      #set precision for printing results
      np.set_printoptions(precision=3, suppress = True)

      #display optimal portfolio results
      print("Optimal weights of the efficient set portfolios\n:", xOptimalArray)
      print("\nAnnualized Risk and Return of the efficient set portfolios:\n", np.c_[riskPoint, retPoint])
      return riskPoint, retPoint

   @classmethod
   def train_non_stocks(cls, symbols: list[str], upper_selection_constraint=[0.5,0.5], lower_selection_constraint=[0.01,0.01]):
      # reference: https://www.kaggle.com/code/vijipai/lesson-7-constrained-portfolio-optimization/notebook
      # function computes asset returns 
      def StockReturnsComputing(StockPrice, Rows, Columns):         
         StockReturn = np.zeros([Rows-1, Columns])
         for j in range(Columns):        # j: Assets
            for i in range(Rows-1):     # i: Daily Prices
                  StockReturn[i,j]=((StockPrice[i+1, j]-StockPrice[i,j])/StockPrice[i,j])*100
         return StockReturn

      #compute stock returns for k-portfolio 1 and market returns to compute asset betas

      #input k portfolio 1 dataset  comprising 15 Dow stocks and DJIA market dataset 
      #over a 3 Year period (April 2016 to April 2019)
      stockColumns = len(symbols)  #excluding date of stock dataset 

      #read stock prices and closing prices of market data (column index 4),  into dataframes
      stockData = util.read_stock_prices(symbols)

      #extract asset labels in the portfolio
      assetLabels = stockData.columns.tolist()
      print('Asset labels of k-portfolio 1: \n', assetLabels)

      #compute asset returns
      arStockPrices = np.asarray(stockData)
      [sRows, sCols]=arStockPrices.shape
      arStockReturns = StockReturnsComputing(arStockPrices, sRows, sCols)

      selection_matrix1 = []
      selection_matrix2 = []
      bounds = []
      for i in range(stockColumns):
            selection_matrix1.append(1)
            selection_matrix2.append(0)
            bounds.append(cls.HIGH_VAL_BOUND)
      
      selection = [selection_matrix2, selection_matrix1]


      #input k portfolio 1 dataset comprising 15 Dow stocks
      Columns = stockColumns

      #compute asset returns
      arStockPrices = np.asarray(stockData)
      [Rows, Cols]=arStockPrices.shape
      arReturns = StockReturnsComputing(arStockPrices, Rows, Cols)

      #set precision for printing data
      np.set_printoptions(precision=3, suppress = True)

      #compute mean returns and variance covariance matrix of returns
      meanReturns = np.mean(arReturns, axis = 0)
      covReturns = np.cov(arReturns, rowvar=False)
      print('\nMean Returns:\n', meanReturns)
      print('\nVariance-Covariance Matrix of Returns:\n', covReturns)

      #function to handle bi-criterion portfolio optimization with constraints
      def BiCriterionFunctionOptmzn(MeanReturns, CovarReturns, RiskAversParam, PortfolioSize):
         def  f(x, MeanReturns, CovarReturns, RiskAversParam, PortfolioSize):
            PortfolioVariance = np.matmul(np.matmul(x, CovarReturns), x.T) 
            PortfolioExpReturn = np.matmul(np.array(MeanReturns),x.T)
            func = RiskAversParam * PortfolioVariance - (1-RiskAversParam)*PortfolioExpReturn
            return func

         def ConstraintEq(x):
            A=np.ones(x.shape)
            b=1
            constraintVal = np.matmul(A,x.T)-b 
            return constraintVal
         
         def ConstraintIneqUpBounds(x):
            A=selection
            bUpBounds =np.array(upper_selection_constraint).T
            constraintValUpBounds = bUpBounds-np.matmul(A,x.T)    # type: ignore
            return constraintValUpBounds

         def ConstraintIneqLowBounds(x):
            A=selection
            bLowBounds =np.array(lower_selection_constraint).T
            constraintValLowBounds = np.matmul(A,x.T)-bLowBounds    # type: ignore
            return constraintValLowBounds
         
         xinit=np.repeat(0.01, PortfolioSize)
         cons = ({'type': 'eq', 'fun':ConstraintEq}, \
                  {'type':'ineq', 'fun': ConstraintIneqUpBounds},\
                  {'type':'ineq', 'fun': ConstraintIneqLowBounds})

         opt = optimize.minimize(f, x0 = xinit, args = ( MeanReturns, CovarReturns,\
                                                         RiskAversParam, PortfolioSize), \
                                 method = 'SLSQP',  bounds = bounds, constraints = cons, \
                                 tol = 10**-3)
         print(opt)
         return opt


      #obtain optimal portfolios for the constrained portfolio optimization model
      #Maximize returns and Minimize risk with fully invested, bound and 
      #class constraints

      #set portfolio size 
      portfolioSize = Columns

      #initialization
      xOptimal =[]
      minRiskPoint = []
      expPortfolioReturnPoint =[]

      for points in range(0,60):
         riskAversParam = points/60.0
         result = BiCriterionFunctionOptmzn(meanReturns, covReturns, riskAversParam, portfolioSize)
         xOptimal.append(result.x)

      #compute annualized risk and return  of the optimal portfolios for trading days = 251
      trading_days = 251

      xOptimalArray = np.array(xOptimal)
      minRiskPoint = np.diagonal(np.matmul((np.matmul(xOptimalArray,covReturns)), np.transpose(xOptimalArray)))
      riskPoint =   np.sqrt(minRiskPoint*trading_days) 
      expPortfolioReturnPoint= np.matmul(xOptimalArray, meanReturns )
      retPoint = trading_days*np.array(expPortfolioReturnPoint) 

      #set precision for printing results
      np.set_printoptions(precision=3, suppress = True)

      #display optimal portfolio results
      print("Optimal weights of the efficient set portfolios\n:", xOptimalArray)
      print("\nAnnualized Risk and Return of the efficient set portfolios:\n", np.c_[riskPoint, retPoint])
      return riskPoint, retPoint
