import typing
from typing import Tuple
import numpy as np
import pandas as pd


# mean
def mean(data: pd.DataFrame, col: str = None) -> float:
    
    try:
        #converting to numpy, calculating the mean of a split array
        returns_numpy = data.loc[:, col].copy().to_numpy() 
        return returns_numpy.mean()
    except TypeError as te:
        print(f'Column data type is missing or is an incompatible data type of int or str. The data type required is a float.\nError is {te}')
        return None
    except KeyError as ke:
        print(f"The column {col} is not a valid column name within the dataframe.\nError is {ke}")
        return None
    except UFuncTypeError as ufte:
        print(f'Column data type of dtype is not accepted. A float is required.\nError is {ufte}')
        return None


# variance
def variance(data: pd.DataFrame, col: str = None) -> float:
    
    try:
        # converting to numpy, calculating the std (ddof = 0)
        numpy_column = (data.loc[:, col]).copy().to_numpy() 
        variance = numpy_column.var(ddof = 0)
        return variance
    except TypeError as te:
        print(f'Column data type is missing or is an incompatible data type of int or str. The data type required is a float.\nError is {te}')
        return None
    except KeyError as ke:
        print(f"The column {col} is not a valid column name within the dataframe.\nError is {ke}")
        return None
    except UFuncTypeError as ufte:
        print(f'Column data type of dtype is not accepted. A float is required.\nError is {ufte}')
        return None

# covariance
def covariance_daily_returns(data: pd.DataFrame, ticker: str, benchmark_ticker: str) -> float:
    
    # create merged dataframe to ensure series size of daily returns data per stock is the same
    merged_data = pd.merge(
        data.loc[data['Ticker'] == ticker, ('Date','Daily Returns %')], 
        data.loc[data['Ticker'] == benchmark_ticker, ('Date','Daily Returns %')], 
        on = 'Date',
        how = 'inner'
    )
    
    # calculating the covariance
    covariance = np.cov(merged_data['Daily Returns %_x'], merged_data['Daily Returns %_y'])
    return covariance[0][1] #returning the covariance value only.

# correlation: covariance / (standard deviation of x * standard deviation of y)
def correlation_daily_returns(data: pd.DataFrame, ticker: str, benchmark_ticker: str) -> float:
    
    #merging dataframes to match date range
    merged_data = pd.merge(
        data.loc[data['Ticker'] == ticker, ('Date','Daily Returns %')], 
        data.loc[data['Ticker'] == benchmark_ticker, ('Date','Daily Returns %')], 
        on = 'Date',
        how = 'inner'
    )
    
    correlation = np.corrcoef(x = merged_data['Daily Returns %_x'], y = merged_data['Daily Returns %_y'])
    return correlation[0][1]


# Beta 
def beta_daily_returns(data: pd.DataFrame, ticker: str, benchmark_ticker: str) -> float:
    
    # create merged dataframe to ensure series size of daily returns data per stock is the same
    # all we need fromt this merged data is the variance of 'Daily Returns %_y' column, which is the ticker 2 data
    merged_data = pd.merge(
        data.loc[data['Ticker'] == ticker, ('Date','Daily Returns %')], 
        data.loc[data['Ticker'] == benchmark_ticker, ('Date','Daily Returns %')], 
        on = 'Date',
        how = 'inner'
)
    
    # calculating beta, using the variance and covariance functions already defined
    # beta = cov(x,y) / var(y), where y is the benchmark data
    beta = covariance_daily_returns(data, ticker, benchmark_ticker) / merged_data['Daily Returns %_y'].std(ddof = 0)
    return beta
    
# 5% ETL - In future we can vary the % within an input and callback. See RiskMetrics file in Code/Stock Data folder
def etl_5_percent_daily_returns(data: pd.DataFrame) -> float:
    
    #ceiling division using upside-down floor division
    num_tail_losses = int(-(len(data) // -(100/5)))
    
    #converting to numpy, sorting the array, calculating the mean of a split array
    day_returns_numpy = data.loc[:, 'Daily Returns %'].copy().to_numpy() 
    day_returns_numpy.sort()
    etl_5_percent =  day_returns_numpy[:num_tail_losses].mean()
    return etl_5_percent
        
    
def trading_days(data: pd.DataFrame, ticker: str, benchmark_ticker: str  = None) -> Tuple[int, int, int, int, int]:
    '''
    Function provides count of trading days over the timeseries provided (simply the count).
    The function also provides a comparison of closing price to open price for both the ticker and the benchmark ticker.
    This is essentially understanding the daily movements because more people can trade during active market hours
    thank after or pre market hours given broker access.
    '''  
    
    if benchmark_ticker is None:
        
        ticker_trading_days = data.loc[data['Ticker'] == ticker, 'Date'].copy().count()
        return ticker_trading_days, None, None, None, None
    
    else:
        
        # creating individual datframes
        ticker_data = data.loc[data['Ticker'] == ticker, ('Ticker', 'Date', 'Daily Returns %')].copy()
        benchmark_data = data.loc[data['Ticker'] == benchmark_ticker, ('Ticker', 'Date', 'Daily Returns %')].copy()
        
        # merge both dataframes and count the number of dates (total trading days for both stocks)
        merged_data = pd.merge(
            ticker_data.loc[:, 'Date'], 
            benchmark_data.loc[:, 'Date'], 
            on = 'Date',
            how = 'inner'
        )
        
        # slice dataframes for 'Daily Returns %' being lower or higher than 0, that is (Close - Open)/Open than 0
        filtered_ticker_data_high = ticker_data.loc[ticker_data['Daily Returns %'] > 0]
        filtered_benchmark_data_high = benchmark_data.loc[benchmark_data['Daily Returns %'] > 0]
        filtered_ticker_data_low_or_zero = ticker_data.loc[ticker_data['Daily Returns %'] <= 0]
        filtered_benchmark_data_low_or_zero = benchmark_data.loc[benchmark_data['Daily Returns %'] <= 0]
        
        # merging dataframes
        both_high = pd.merge(
            filtered_ticker_data_high.loc[:, 'Date'],  
            filtered_benchmark_data_high.loc[:, 'Date'], 
            on = 'Date',
            how = 'inner'
        )
        
        both_low = pd.merge(
            filtered_ticker_data_low_or_zero.loc[:, 'Date'],  
            filtered_benchmark_data_low_or_zero.loc[:, 'Date'], 
            on = 'Date',
            how = 'inner'
        )
        
        ticker_high_benchmark_low = pd.merge(
            filtered_ticker_data_high.loc[:, 'Date'],  
            filtered_benchmark_data_low_or_zero.loc[:, 'Date'], 
            on = 'Date',
            how = 'inner'
        )
        
        ticker_low_benchmark_high = pd.merge(
            filtered_ticker_data_low_or_zero.loc[:, 'Date'],  
            filtered_benchmark_data_high.loc[:, 'Date'],
            on = 'Date',
            how = 'inner'
        )
        
        # counts
        trading_days_count = merged_data.count()
        both_high_count = both_high.count()
        both_low_count = both_low.count()
        ticker_high_benchmark_low_count = ticker_high_benchmark_low.count()
        ticker_low_benchmark_high_count = ticker_low_benchmark_high.count()
        
        return trading_days_count, both_high_count, both_low_count, ticker_high_benchmark_low_count, ticker_low_benchmark_high_count
