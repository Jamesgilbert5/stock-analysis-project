# packages
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json
from components import html_table as ht
from utils import graph_functions as gf
from utils import calculation_functions as cf


#ading an example stylesheet taken from the following, https://community.plotly.com/t/dash-bootstrap-components-in-ie-chrome/34362/6
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/flatly/bootstrap.min.css']

#creating an instance of the dash class. This is similar to Flask, where you initialize a WSGI application (Web Server Gateway Interface)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Defining the layout of the application
colours = {
    'deep blue': '#010521',
    'off white':'#f2f4f7',
    'funky stuff':'#04b1c4'
}

text_colours = {
    'deep blue': '#010521',
    'off white':'#f2f4f7',
    'silver':'#C0C0C0'
}

# DATA
# Data
all_tickers_stock_data = pd.read_csv('assets/data/master_data_2022-11-03.csv')   
all_tickers_stock_data['Date'] = all_tickers_stock_data['Date'].astype("Datetime64") #set the datatype of the date column

# getting tickers from dataframe for labels
unique_tickers = sorted(list(all_tickers_stock_data['Ticker'].unique()))



# APP
# app visual layout. Layout structure uses dash bootstrap components (for which we must have a defined stylesheet for expected rendering)
app.layout = dbc.Container(children = [
    html.Br(),
        dbc.Row([ 
        dbc.Col([ # row 1, col 1
            dbc.Card([
                dbc.CardBody([
                    html.Div(children = [
                        dbc.Tabs([
                                dbc.Tab(label="Candlestick Graph", id="candlestick_graph_tab", tab_id="candlestick_graph_tab", style = {'padding-left':'5px', 'padding-right':'5px', 'height':'100%'}),
                                dbc.Tab(label="Price Line Graph", id="price_line_graph_tab", tab_id="price_line_graph_tab", style = {'padding-left':'5px', 'padding-right':'5px', 'height':'100%'}),
                                dbc.Tab(label="Returns Line Graph", id="returns_line_graph_tab", tab_id="returns_line_graph_tab", style = {'padding-left':'5px', 'padding-right':'5px', 'height':'100%'}),
                                dbc.Tab(label="Returns Distribution Graph", id="returns_histogram_graph_tab", tab_id="returns_histogram_graph_tab", style = {'padding-left':'5px', 'padding-right':'5px', 'height':'100%'})
                            ],
                            id="tabs",
                            active_tab="candlestick_graph_tab"
                        ),
                    ],
                    style = {"height":"40px"}     
                    ),
                ],
                ),
            ],
            style = {"background-color":colours["off white"]}
            ),  
        ], md = 12
        ),
    ],
    align = "center"
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([ #row 2, col 1
            dbc.Card( #row 2, col 1 card container
                dbc.CardBody([
                    html.Div(children = [
                        html.H5(
                            children = "Ticker & Date Picker", 
                            style = {'color':text_colours['off white'], 'display':'inline-block', 'vertical-align':'middle', 'padding':'5px'}
                        ),
                        html.Div([
                            dcc.Dropdown(
                                id = 'ticker_dropdown',
                                options = unique_tickers,
                                value = unique_tickers[0],
                                style = {'height':'40px'}
                            ), 
                        ],
                        style = {'display':'inline-block', 'vertical-align':'middle', 'padding':'5px', 'width':'35%'}
                        ),
                        html.Div([
                            dcc.DatePickerRange(
                                id = 'date_picker',
                                min_date_allowed = all_tickers_stock_data['Date'].min(),
                                max_date_allowed = all_tickers_stock_data['Date'].max(),
                                start_date = all_tickers_stock_data['Date'].min(),
                                end_date = all_tickers_stock_data['Date'].max(),
                                display_format = 'DD MMM YY',
                                start_date_placeholder_text = 'DD MMM YY',
                                style = {'height':'40px'} #https://community.plotly.com/t/change-size-of-datepicker/25286/3
                            ),
                        ],
                        style = {'display':'inline-block', 'vertical-align':'middle', 'padding':'5px'}
                        ),
                    ],
                    style = {'display':'inline', 'height':'60px'}
                    ),                    
                ],
                ), 
                style = {"background-color":colours["deep blue"]},
            )
        ], md = 9
        ),
        dbc.Col([ #row 2, col 2
            dbc.Card( #row 2, col 2 card container
                dbc.CardBody([
                    html.Div(children = [
                        html.Div([
                            dcc.Dropdown(
                                id = 'benchmark_dropdown',
                                placeholder = 'Benchmark Ticker',
                                style = {'height':'40px'}
                            ), 
                        ],
                        style = {'display':'inline-block', 'vertical-align':'middle', 'padding':'5px', 'width':'100%'}
                        ),
                    ],
                    style = {'display':'inline', 'height': '60px'}
                    ),
                ]), 
                style = {"background-color":colours["off white"]},
            )
        ], md = 3
        ),
    ],
    align = "center",
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([ #row 3, col 1
            dbc.Card( #row 3, col 1 card container
                dbc.CardBody([
                    html.Div(children = [
                        dcc.Graph(
                            id = "candlestick_graph", 
                            responsive = True, 
                            config={"displaylogo": True,
                                    'modeBarButtonsToRemove': [
                                        'zoom2d',
                                        'toggleSpikelines',
                                        'pan2d',
                                        'select2d',
                                        'lasso2d',
                                        'autoScale2d',
                                        'hoverClosestCartesian',
                                        'hoverCompareCartesian']
                                   },
                            style = {'height':'450px', 'width':'100%'}
                        ),
                    ],
                    id = 'candlestick_graph_div',
                    style = {'height':'400px', 'margin':'5px', 'display':'block'}
                    ),
                    html.Div(children = [
                        dcc.Graph(
                            id = 'price_line_graph', 
                            responsive = True, 
                            config={
                                "displaylogo": True,
                                'modeBarButtonsToRemove': [
                                    'zoom2d',
                                    'toggleSpikelines',
                                    'pan2d',
                                    'select2d',
                                    'lasso2d',
                                    'autoScale2d',
                                    'hoverClosestCartesian',
                                    'hoverCompareCartesian']
                            },
                            style = {'height':'450px', 'width':'100%'}
                        ),
                    ],
                    id = 'price_line_graph_div',         
                    style = {'height':'450px', 'margin':'5px', 'display':'none'}
                    ),
                    html.Div(children = [
                        dcc.Graph(
                            id = 'returns_line_graph', 
                            responsive = True, 
                            config={
                                "displaylogo": True,
                                'modeBarButtonsToRemove': [
                                    'zoom2d',
                                    'toggleSpikelines',
                                    'pan2d',
                                    'select2d',
                                    'lasso2d',
                                    'autoScale2d',
                                    'hoverClosestCartesian',
                                    'hoverCompareCartesian']
                            },
                            style = {'height':'450px', 'width':'100%'}
                        ), 
                    ],
                    id = 'returns_line_graph_div',         
                    style = {'height':'450px', 'margin':'5px', 'display':'none'} 
                    ),
                    html.Div(children = [
                        dcc.Graph(
                            id = 'returns_histogram_graph', 
                            responsive = True, 
                            config={
                                "displaylogo": True,
                                'modeBarButtonsToRemove': [
                                    'zoom2d',
                                    'toggleSpikelines',
                                    'pan2d',
                                    'select2d',
                                    'lasso2d',
                                    'autoScale2d',
                                    'hoverClosestCartesian',
                                    'hoverCompareCartesian']
                            },
                            style = {'height':'450px', 'width':'100%'}
                        ), 
                    ],
                    id = 'returns_histogram_graph_div',         
                    style = {'height':'450px', 'margin':'5px', 'display':'none'}
                    ),
                ],
                ),
            style = {"background-color":colours["funky stuff"]}
            ),
        ], md = 9
        ),
        dbc.Col([ #row 3, col 2
            dbc.Card( #row 3, col 2 card container
                dbc.CardBody([
                    html.Div(children = [
                        dbc.Table(
                            ht.table_header + ht.table_body, 
                            id = 'all_tickers_df',
                            bordered = True, 
                            striped = True, 
                            style = {'padding':'5px', 'height': '100%', 'width':'100%'}
                        ),
                    ],
                    style = {'color':text_colours['off white'], 'height':'450px', 'overflow':'scroll'}
                    ),
                    
                ]), 
            style = {"background-color":colours["off white"]}
            ),
        ], md = 3
        ),
    ],
    align = "center",
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([ #row 4, col 1
            dbc.Card( #row 4, col 1 card container
                   dbc.CardBody([
                       html.Div([
                           html.Pre(id='selected_data', style={'border': 'thin lightgrey solid', 'overflowX': 'scroll'})
                       ],
                       ),  
                   ],
                   style = {"background-color":colours["off white"]}
                   ),
            ),
        ],
        ),
    ],
    ),
    
], 
#style = {'overflow':'scroll'}
)

# CALLBACKS
# updating start and end dates when users drag over graphs. Zoom out to return to original dates
@app.callback(
    Output('selected_data', 'children'),
    Output('date_picker', 'start_date'),
    Output('date_picker', 'end_date'),
    Input('tabs', 'active_tab'),
    Input('candlestick_graph', 'relayoutData'),
    Input('price_line_graph', 'relayoutData'),
    Input('returns_line_graph', 'relayoutData'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date')
)
def display_selected_data(active_tab, candlestick_relayout_data, price_line_relayout_data, returns_line_relayout_data, start_date, end_date):
    '''
    Logic in this function:
    
    - upon app initialisation start and end dates are none, so we don't want to throw an error
    - once active tab is selected we want to update start and end date values if a user has dragged over the graph, i.e., xaxis.range[0] value is present in the relayoutData
    - if the user hasn't dragged over the graph then the start and end dates should still be the min and max limits respectively. RelayoutData contains only "autosize":true
    - if the user has double clicked on the graph to reset the axes then we want to reset the dates to the min and max limits. RelayoutData contains "xaxis.autorange":true at this point
    
    '''
    if start_date is None and end_date is None:
        start_date = all_tickers_stock_data['Date'].min()
        end_date = all_tickers_stock_data['Date'].max()
        return None, start_date, end_date
    
    elif active_tab == 'candlestick_graph_tab':
        min_start_date = all_tickers_stock_data['Date'].min()
        max_end_date = all_tickers_stock_data['Date'].max()
        
        # user dragged over graph
        try:
            start_date = candlestick_relayout_data['xaxis.range[0]']
            end_date = candlestick_relayout_data['xaxis.range[1]']
            return json.dumps(candlestick_relayout_data, indent=2), start_date, end_date 
            
        except KeyError:
            #double clicked graph
            try: 
                # test for KeyError
                key_test = candlestick_relayout_data['xaxis.autorange']
                # returning date limits
                return json.dumps(candlestick_relayout_data, indent=2), min_start_date, max_end_date
            
            # no/other graph action
            except KeyError:
                return json.dumps(candlestick_relayout_data, indent=2), start_date, end_date
        
    elif active_tab == 'price_line_graph_tab':
        min_start_date = all_tickers_stock_data['Date'].min()
        max_end_date = all_tickers_stock_data['Date'].max()
        
        try:
            start_date = price_line_relayout_data['xaxis.range[0]']
            end_date = price_line_relayout_data['xaxis.range[1]']
            return json.dumps(price_line_relayout_data, indent=2), start_date, end_date
            
        except KeyError:
            try:
                key_test = price_line_relayout_data['xaxis.autorange']
                return json.dumps(price_line_relayout_data, indent=2), min_start_date, max_end_date
            except KeyError:
                return json.dumps(price_line_relayout_data, indent=2), start_date, end_date
    
    elif active_tab == 'returns_line_graph_tab':
        min_start_date = all_tickers_stock_data['Date'].min()
        max_end_date = all_tickers_stock_data['Date'].max()
        
        try:
            start_date = returns_line_relayout_data['xaxis.range[0]']
            end_date = returns_line_relayout_data['xaxis.range[1]']
            return json.dumps(returns_line_relayout_data, indent=2), start_date, end_date
            
        except KeyError:
            try:
                key_test = returns_line_relayout_data['xaxis.autorange']
                return json.dumps(returns_line_relayout_data, indent=2), min_start_date, max_end_date
            
            except KeyError:
                return json.dumps(returns_line_relayout_data, indent=2), start_date, end_date
            
    else:
        return None, start_date, end_date
        

# updating colour of active label (Tabs)
@app.callback(
    Output('candlestick_graph_tab', 'label_style'),
    Output('price_line_graph_tab', 'label_style'),
    Output('returns_line_graph_tab', 'label_style'),
    Output('returns_histogram_graph_tab', 'label_style'),
    Input('tabs', 'active_tab')
)
def update_label_style(active_tab):
    
    candlestick_tab_color = {"background-color":colours["deep blue"], "color":text_colours['off white']}
    price_line_tab_color = {"background-color":colours["deep blue"], "color":text_colours['off white']}
    returns_line_tab_color = {"background-color":colours["deep blue"], "color":text_colours['off white']}
    returns_histogram_tab_color = {"background-color":colours["deep blue"], "color":text_colours['off white']}
    
    if active_tab == 'candlestick_graph_tab':
        candlestick_tab_color = {"background-color":colours["funky stuff"], "color":text_colours['off white']}
    elif active_tab == 'price_line_graph_tab':
        price_line_tab_color = {"background-color":colours["funky stuff"], "color":text_colours['off white']}
    elif active_tab == 'returns_line_graph_tab':
        returns_line_tab_color = {"background-color":colours["funky stuff"], "color":text_colours['off white']}
    elif active_tab == 'returns_histogram_graph_tab':
        returns_histogram_tab_color = {"background-color":colours["funky stuff"], "color":text_colours['off white']}

    return candlestick_tab_color, price_line_tab_color, returns_line_tab_color, returns_histogram_tab_color


#updating the candlestick graph based on date and ticker parameters
@app.callback(
    Output('candlestick_graph', 'figure'), # need to parse the in the arguments needed to generate the graph (this is a 'figure')
    Input('ticker_dropdown', 'value'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date'),
)
def candlestick_graph_display(ticker, start_date, end_date):
    '''
    first create the required dataframe, then returned outputs based on buttons will return the graphs/tables.
    
    we slice the dataframe according to date parameters within this callback function, instead of the graph generation function.
    '''

    # create filtered dataframe from all stocks dataframe read in from CSV
    returned_df = all_tickers_stock_data.loc[all_tickers_stock_data['Ticker'] == ticker].set_index('Date') # set index on date for slicing. used to be all_tickers_stock_data[all_tickers_stock_data['Ticker'] == ticker].set_index('Date')
    returned_df = returned_df[start_date : end_date] # filter dataframe on start and end date
    
    # dropping index so that the dataframe in Dash displays the date column
    returned_df.reset_index(inplace = True)
    
    # candlestick figure
    candlestick_figure = gf.create_candlestick_graph(returned_df)
    
    # return figure
    return candlestick_figure

# updating the price line graph figure based on dates, ticker and benchmark ticker parameters
@app.callback(
    Output('price_line_graph', 'figure'),
    Input('ticker_dropdown', 'value'),
    Input('benchmark_dropdown', 'value'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date')
)
def price_line_graph_display(ticker, benchmark_ticker, start_date, end_date):
    '''
    first create the required dataframe, then returned outputs based on buttons will return the graphs/tables.
    
    we slice the dataframe according to date parameters within this callback function, instead of within the graph generation function.
    '''
    # create filtered dataframe from all stocks dataframe read in from CSV
    returned_df = all_tickers_stock_data.loc[:, ['Date', 'Ticker', 'Close']].set_index('Date') # set index on date for slicing on dataframe copy (.loc[])
    returned_df = returned_df[start_date : end_date] # filter dataframe on start and end date
    
    # dropping index so that the dataframe in Dash displays the date column
    returned_df.reset_index(inplace = True)
    
    # price line graph figure
    price_line_graph_figure = gf.create_price_line_graph(returned_df, ticker, benchmark_ticker)
    
    return price_line_graph_figure

# updating the returns line graph figure based on dates, ticker and benchmark ticker parameters
@app.callback(
    Output('returns_line_graph', 'figure'),
    Input('ticker_dropdown', 'value'),
    Input('benchmark_dropdown', 'value'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date')
)
def returns_line_graph_display(ticker, benchmark_ticker, start_date, end_date):
    '''
    first create the required dataframe, then returned outputs based on buttons will return the graphs/tables.
    
    we slice the dataframe according to date parameters within this callback function, instead of within the graph generation function.
    '''
    # create filtered dataframe from all stocks dataframe read in from CSV
    returned_df = all_tickers_stock_data.loc[:, ['Date', 'Ticker', 'Daily Returns %']].set_index('Date') # set index on date for slicing on dataframe copy (.loc[])
    returned_df = returned_df[start_date : end_date] # filter dataframe on start and end date
    
    # dropping index so that the dataframe in Dash displays the date column
    returned_df.reset_index(inplace = True)
    
    # returns line graph figure
    returns_line_graph_figure = gf.create_returns_line_graph(returned_df, ticker, benchmark_ticker)
    
    return returns_line_graph_figure

# updating the returns histogram figure based on dates, ticker and benchmark ticker parameters
@app.callback(
    Output('returns_histogram_graph', 'figure'),
    Input('ticker_dropdown', 'value'),
    Input('benchmark_dropdown', 'value'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date')
)
def returns_histogram_graph_display(ticker, benchmark_ticker, start_date, end_date):
    '''
    first create the required dataframe, then returned outputs based on buttons will return the graphs/tables.
    
    we slice the dataframe according to date parameters within this callback function, instead of within the graph generation function.
    '''
    # create filtered dataframe from all stocks dataframe read in from CSV
    returned_df = all_tickers_stock_data.loc[:, ['Date', 'Ticker', 'Daily Returns %']].set_index('Date') # set index on date for slicing on dataframe copy (.loc[])
    returned_df = returned_df[start_date : end_date] # filter dataframe on start and end date
    
    # dropping index so that the dataframe in Dash displays the date column
    returned_df.reset_index(inplace = True)
    
    # histogram graph figure
    returns_histogram_graph_figure = gf.create_returns_histogram(returned_df, ticker, benchmark_ticker)
    
    return returns_histogram_graph_figure


# disabling primary ticker from benchmark ticker options
@app.callback(
    Output('benchmark_dropdown', 'options'), #determining the values of the benchmark dropdown. Everything exlcuding the primary selected ticker
    Input('ticker_dropdown', 'value')
)

def benchmark_ticker_options(primary_ticker):
    
    # list comprehension creating list of dictionaries that form the argument for the dcc.Dropdown function
    ticker_options = [{'label': ticker, 'value': ticker} if ticker != primary_ticker else {'label': ticker, 'value': ticker, 'disabled': True} for ticker in unique_tickers]
    
    return ticker_options


# tab selection determining displayed graph
@app.callback(
    Output('candlestick_graph_div', 'style'),
    Output('price_line_graph_div', 'style'),
    Output('returns_line_graph_div', 'style'),
    Output('returns_histogram_graph_div', 'style'),
    Input('tabs', 'active_tab')
)
def show_candlestick_or_line_graph(active_tab):
    candlestick_style = {'display': 'none'}
    price_line_graph_style = {'display': 'none'}
    returns_line_graph_style = {'display': 'none'}
    returns_histogram_graph_style = {'display': 'none'}   
    
    if active_tab == 'candlestick_graph_tab':
        candlestick_style = {'display': 'block'}
        
    elif active_tab == 'price_line_graph_tab':
        price_line_graph_style = {'display': 'block'}
    
    elif active_tab == 'returns_line_graph_tab':
        returns_line_graph_style = {'display': 'block'}
    
    elif active_tab == 'returns_histogram_graph_tab':
        returns_histogram_graph_style = {'display': 'block'}
        
    return candlestick_style, price_line_graph_style, returns_line_graph_style, returns_histogram_graph_style

# table values being updated
@app.callback(
    Output('ticker', 'children'),
    Output('mean_daily_return', 'children'),
    Output('var_daily_return', 'children'),
    Output('mean_volume', 'children'),
    Output('etl_5_percent', 'children'),
    Output('benchmark_ticker', 'children'),
    Output('covariance', 'children'),
    Output('correlation', 'children'),
    Output('beta', 'children'),
    Output('trading_day_count', 'children'),
    Output('both_open_high', 'children'),
    Output('both_open_low', 'children'),
    Output('stock_high_benchmark_low', 'children'),
    Output('stock_low_benchmark_high', 'children'),
    Input('ticker_dropdown', 'value'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date'),
    Input('benchmark_dropdown', 'value')
)
def update_table_values(ticker, start_date, end_date, benchmark_ticker):
    
    '''
    could adapt this to only recalculate depending on what values change (e.g. if benchmark ticker changes then no
    need to recalculate the data points pertaining to the primary ticker only metrics such as mean return or volume.)
    '''
        
    # create filtered dataframe from all stocks dataframe read in from CSV
    stock_data = all_tickers_stock_data.set_index('Date') # set index on date for slicing
    stock_data = stock_data[start_date : end_date] # filter dataframe on start and end date
    # dropping index so that the dataframe in Dash displays the date column
    stock_data.reset_index(inplace = True)
    
    if benchmark_ticker == None:
        
        mean_daily_return = round(cf.mean(data = stock_data[stock_data['Ticker'] == ticker], col = 'Daily Returns %'), 2)
        var_daily_return = round(cf.variance(data = stock_data[stock_data['Ticker'] == ticker], col = 'Daily Returns %'), 4)
        mean_volume = round(cf.mean(data = stock_data[stock_data['Ticker'] == ticker], col = 'Volume'), 0)
        etl_5_percent = round(cf.etl_5_percent_daily_returns(stock_data[stock_data['Ticker'] == ticker]), 2)
        
        return ticker, mean_daily_return, var_daily_return, mean_volume, etl_5_percent, None, None, None, None, None, None, None, None, None
    
    else:
        
        mean_daily_return = round(cf.mean(data = stock_data[stock_data['Ticker'] == ticker], col = 'Daily Returns %'), 2)
        var_daily_return = round(cf.variance(data = stock_data[stock_data['Ticker'] == ticker], col = 'Daily Returns %'), 4)
        mean_volume = round(cf.mean(data = stock_data[stock_data['Ticker'] == ticker], col = 'Volume'), 0)
        etl_5_percent = round(cf.etl_5_percent_daily_returns(stock_data[stock_data['Ticker'] == ticker]), 2)
        covariance = round(cf.covariance_daily_returns(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker), 4)
        correlation = round(cf.correlation_daily_returns(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker), 4)
        beta = round(cf.beta_daily_returns(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker), 4)
        trading_day_count = cf.trading_days(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker)[0]
        both_open_high = cf.trading_days(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker)[1]
        both_open_low = cf.trading_days(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker)[2]
        stock_high_benchmark_low = cf.trading_days(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker)[3]
        stock_low_benchmark_high = cf.trading_days(data = stock_data, ticker = ticker, benchmark_ticker = benchmark_ticker)[4]
        
        return ticker, mean_daily_return, var_daily_return, mean_volume, etl_5_percent, benchmark_ticker, covariance, correlation, beta, trading_day_count, both_open_high, both_open_low, stock_high_benchmark_low, stock_low_benchmark_high
    
  
# running the app
app.run_server(debug=True, use_reloader=False)  # Turn off reloading of the web app when the code changes

if __name__ == '__main__':
    app.run_server(debug=True)