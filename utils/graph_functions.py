'''
GRAPH CREATIONS
'''
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import dash_table
import numpy as np
import pandas as pd
from utils import calculation_functions as cf


# candlestick graph figure
def create_candlestick_graph(stock_df: pd.DataFrame) -> go.Candlestick:
    
    #declaring figure comprised of subplots
    price_figure = make_subplots(
                        rows=2, 
                        cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.05
                    ) #shared x axis & distance between subplots 
    
    #first subplot
    price_figure.add_trace(
        go.Candlestick(x=stock_df['Date'],
                    open=stock_df['Open'],
                    high=stock_df['High'],
                    low=stock_df['Low'],
                    close=stock_df['Close'],
                    name="Price"),
        row=1,col=1
    )
    
    #second subplot, using the marker argument to determine the bar colour based on closing lower or higher
    price_figure.add_trace(
        go.Bar(x=stock_df['Date'],
            y=stock_df['Volume'],
            name="Volume",
            marker=dict(color = ['green' if x>0 else 'red' for x in stock_df['Close'] - stock_df['Open']])),
        row=2,col=1
    )
    
    # removing rangeslider
    price_figure.update_layout(xaxis_rangeslider_visible=False)
    
    # hide weekends
    price_figure.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    
    # update gridlines and automargin scaling
    price_figure.update_xaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    price_figure.update_yaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    
    #naming and decorating
    price_figure.update_layout(
        yaxis1_title="Price (Exchange CCY)",
        yaxis2_title="Daily Volume",
        showlegend=False,
        template="plotly_white",
        font=dict( 
                size=14,
                color='Navy'
        ),
        autosize=True, #graph size adjusts with screen
        margin=dict(l=10, r=10, t=30, b=0) #margins within figure
    )
    
    # return graph
    return price_figure

# labelling subplot axes: https://community.plotly.com/t/subplots-with-shared-x-axes-but-show-x-axis-for-each-plot/34800/2

# Line graph comparing one ticker's rebase closee prices to another ticker's (benchmark) over time
def create_price_line_graph(stock_df: pd.DataFrame, ticker: str, benchmark_ticker: str) -> go.Scatter:
    '''
    creating plotly line graph comparing two tickers results over time. We will use the close price only
    '''
    if benchmark_ticker is None:
        # slicing df for plotting
        sliced_stock_df = stock_df.loc[stock_df['Ticker'] == ticker, ('Ticker', 'Date', 'Close')].set_index('Date')
        # plotting line figure
        line_figure = go.Figure()
        line_figure.add_trace(go.Scatter(x = sliced_stock_df.index, y = sliced_stock_df['Close'], name = f'{ticker} price'))
    
        # updating figure titles and labels
        line_figure.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            yaxis_title="Price (Exchange CCY)",
            template="plotly_white",
            font=dict( 
                size=14,
                color='Navy'
            ),
            autosize=True, #graph size adjusts with screen
            margin=dict(l=10, r=10, t=30, b=0) #margins within figure
            )
        
    else:
        # creating a merged dataframe using copies of the individual ticker dataframes. This ensures the same date range (inner merge)
        merged_df = pd.merge(
            stock_df.loc[stock_df['Ticker'] == ticker, ('Ticker', 'Date', 'Close')].set_index('Date'),
            stock_df.loc[stock_df['Ticker'] == benchmark_ticker, ('Ticker', 'Date', 'Close')].set_index('Date'),     
            on = 'Date',
            how = 'inner'
        )
        
        ## first find factor for which to rebase Close values by per ticker
        rebasing_factor_ticker = round(100/(merged_df.loc[merged_df['Ticker_x'] == ticker, 'Close_x'].iloc[0]),10) # identifies first close value in dataframe for ticker
        rebasing_factor_benchmark = round(100/(merged_df.loc[merged_df['Ticker_y'] == benchmark_ticker, 'Close_y'].iloc[0]),10) # identifies first close value in dataframe for ticker
        
        ## rebase using pandas.apply()
        merged_df.loc[merged_df['Ticker_x'] == ticker, 'Close_x'] = merged_df['Close_x'][merged_df['Ticker_x'] == ticker].apply(lambda x: round(x * rebasing_factor_ticker, 4))
        merged_df.loc[merged_df['Ticker_y'] == benchmark_ticker, 'Close_y'] = merged_df['Close_y'][merged_df['Ticker_y'] == benchmark_ticker].apply(lambda x: round(x * rebasing_factor_benchmark, 4))
        
        ## plotting the line graphs, make 'color' ticker to create distinct coloured lines
        line_figure = go.Figure()
        # add ticker trace
        line_figure.add_trace(go.Scatter(x = merged_df.index, y = merged_df['Close_x'], name = f'{ticker} price'))
        # add benchmark trace
        line_figure.add_trace(go.Scatter(x = merged_df.index, y = merged_df['Close_y'], name = f'{benchmark_ticker} price'))
    
        # updating figure titles and labels
        line_figure.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            yaxis_title="Price rebased to 100",
            template="plotly_white",
            font=dict( 
                size=14,
                color='Navy'
            ),
            autosize=True, #graph size adjusts with screen
            margin=dict(l=10, r=10, t=30, b=0) #margins within figure
            )
    
    # update gridlines and automargin scaling
    line_figure.update_xaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    line_figure.update_yaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    
    return line_figure

# stock returns time series scatter graph
def create_returns_line_graph(stock_df: pd.DataFrame, ticker: str, benchmark_ticker: str) -> go.Scatter:
    
    if benchmark_ticker is None:
        # slicing df for plotting
        sliced_stock_df = stock_df.loc[stock_df['Ticker'] == ticker, ('Ticker', 'Date', 'Daily Returns %')].set_index('Date')
        # adding ETL 5% df column
        sliced_stock_df['ETL_5'] = round(cf.etl_5_percent_daily_returns(sliced_stock_df), 2)
        
        # creating returns figure
        returns_figure = go.Figure()
        returns_figure.add_trace(go.Scatter(x = sliced_stock_df.index, y = sliced_stock_df['Daily Returns %'], name = f'{ticker} Daily Returns %', line = dict(color = 'dodgerblue')))
        returns_figure.add_trace(go.Scatter(x = sliced_stock_df.index, y = sliced_stock_df['ETL_5'], name = f'{ticker} Expected Tail Loss of 5%', line = dict(dash = 'longdash', color = 'limegreen')))
    
        # updating figure titles and labels
        returns_figure.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            yaxis_title="Returns %",
            template="plotly_white",
            font=dict( 
                size=14,
                color='Navy'
            ),
            autosize=True, #graph size adjusts with screen
            margin=dict(l=10, r=10, t=30, b=0) #margins within figure
            )
    
    else:
        ticker_df = stock_df.loc[stock_df['Ticker'] == ticker, ('Ticker', 'Date', 'Daily Returns %')].set_index('Date')
        benchmark_df = stock_df.loc[stock_df['Ticker'] == benchmark_ticker, ('Ticker', 'Date', 'Daily Returns %')].set_index('Date')
        
        # calculating ETL 5% for tikcer & benchmark
        ETL_5_ticker = round(cf.etl_5_percent_daily_returns(ticker_df), 2)
        ETL_5_benchmark = round(cf.etl_5_percent_daily_returns(benchmark_df), 2)
        
        # creating a merged dataframe using copies of the individual ticker dataframes. This ensures the same date range (inner merge)
        merged_df = pd.merge(
            ticker_df,
            benchmark_df,     
            on = 'Date',
            how = 'inner'
        )
        # adding ETL columns for ticker and benchmark (now referred to as '..._x' and '..._y' respectively since pandas merging)
        merged_df['ETL_x'] = ETL_5_ticker
        merged_df['ETL_y'] = ETL_5_benchmark
        
        # creating returns figure
        returns_figure = go.Figure()
        returns_figure.add_trace(go.Scatter(x = merged_df.index, y = merged_df['Daily Returns %_x'], name = f'{ticker} Daily Returns %', line = dict(color = 'dodgerblue')))
        returns_figure.add_trace(go.Scatter(x = merged_df.index, y = merged_df['Daily Returns %_y'], name = f'{benchmark_ticker} Daily Returns %', line = dict(color = 'limegreen')))
        returns_figure.add_trace(go.Scatter(x = merged_df.index, y = merged_df['ETL_x'], name = f'{ticker} Expected Tail Loss of 5%', line = dict(dash = 'longdash', color = 'dodgerblue')))
        returns_figure.add_trace(go.Scatter(x = merged_df.index, y = merged_df['ETL_y'], name = f'{benchmark_ticker} Expected Tail Loss of 5%', line = dict(dash = 'longdash', color = 'limegreen')))
    
        # updating figure titles and labels
        returns_figure.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            yaxis_title="Returns %",
            template="plotly_white",
            font=dict( 
                size=14,
                color='Navy'
            ),
            autosize=True, #graph size adjusts with screen
            margin=dict(l=10, r=10, t=30, b=0) #margins within figure
            )
    # update gridlines and automargin scaling
    returns_figure.update_xaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    returns_figure.update_yaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    
    return returns_figure


# returns histogram graph
def create_returns_histogram(stock_df: pd.DataFrame, ticker: str, benchmark_ticker: str) -> go.Histogram:
    
    if benchmark_ticker is None:
        # slicing df for plotting
        sliced_stock_df = stock_df.loc[stock_df['Ticker'] == ticker, ('Ticker', 'Date', 'Daily Returns %')].set_index('Date')
        
        # Calculating ETL 5%
        ETL_5 = round(cf.etl_5_percent_daily_returns(sliced_stock_df), 2)
        
        # create histogram
        histogram_figure = go.Figure()
        
        # colour trace for <= ETL 5%, rounded (so histogram boundary is conitinuous)
        histogram_figure.add_trace(go.Histogram(
            x = sliced_stock_df.loc[sliced_stock_df['Daily Returns %'] <= round(ETL_5, 0), 'Daily Returns %'],
            marker_color= 'limegreen',
            xbins = dict(size = 1),
            legendgroup='1',
            name = f"{ticker} lowest 5%",
            showlegend=True
        ))
        
        # colour trace for > ETL 5%, rounded (so histogram boundary is conitinuous)
        histogram_figure.add_trace(go.Histogram(
            x = sliced_stock_df.loc[sliced_stock_df['Daily Returns %'] > round(ETL_5, 0), 'Daily Returns %'],
            marker_color= 'dodgerblue',
            xbins = dict(size = 1),
            legendgroup='1',
            name = f"{ticker} highest 95%",
            showlegend=True
        ))
        
        
        # updating histogram titles and labels
        histogram_figure.update_layout(
            xaxis_title=f"{ticker} Daily Returns %",
            yaxis_title="Frequency",
            template="plotly_white",
            font=dict( 
                size=14,
                color='Navy'
            ),
            autosize=True, #graph size adjusts with screen
            margin=dict(l=10, r=10, t=30, b=0) #margins within figure
            )
        
        
    else:
        # slicing dataframes for plotting
        ticker_df = stock_df.loc[stock_df['Ticker'] == ticker, ('Ticker', 'Date', 'Daily Returns %')].set_index('Date')
        benchmark_df = stock_df.loc[stock_df['Ticker'] == benchmark_ticker, ('Ticker', 'Date', 'Daily Returns %')].set_index('Date')
        
        # calculating ETL 5% for ticker & benchmark
        ETL_5_ticker = round(cf.etl_5_percent_daily_returns(ticker_df), 2)
        ETL_5_benchmark = round(cf.etl_5_percent_daily_returns(benchmark_df), 2)
        
        # creating a merged dataframe using copies of the individual ticker dataframes. This ensures the same date range (inner merge)
        merged_df = pd.merge(
            ticker_df,
            benchmark_df,     
            on = 'Date',
            how = 'inner'
        )
        
        # create histogram
        histogram_figure = go.Figure()
        histogram_figure.add_trace(go.Histogram(x = merged_df['Daily Returns %_x'], name = f'{ticker} Daily Returns Frequency', marker_color = 'dodgerblue', xbins = dict(size = 1)))
        histogram_figure.add_trace(go.Histogram(x = merged_df['Daily Returns %_y'], name = f'{benchmark_ticker} Daily Returns Frequency', marker_color = 'limegreen', xbins = dict(size = 1)))
        
        # updating histogram titles and labels
        histogram_figure.update_layout(
            xaxis_title="Daily Returns %",
            yaxis_title="Frequency",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            template="plotly_white",
            font=dict( 
                size=14,
                color='Navy'
            ),
            autosize=True, #graph size adjusts with screen
            margin=dict(l=10, r=10, t=30, b=0) #margins within figure
            )
    # update gridlines and automargin scaling
    histogram_figure.update_xaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    histogram_figure.update_yaxes(showgrid=True, gridcolor='Dark Blue', automargin=True)
    
    return histogram_figure
