from dash import html

# APP DATA TABLE
# create table head
table_header = [
    html.Thead(html.Tr([html.Th("Data Point"), html.Th("Value")], style = {'background-color':'#010521', 'color':'#f2f4f7'}))
]

# create table body. Values updated via a callback function
table_body = [
    html.Tbody([
        html.Tr([html.Th('Ticker', scope = 'col'), html.Td(id = 'ticker')]),
        html.Tr([html.Th('Mean Daily Return %', scope = 'col'), html.Td(id = 'mean_daily_return')]),
        html.Tr([html.Th('Var Daily Return %', scope = 'col'), html.Td(id = 'var_daily_return')]),
        html.Tr([html.Th('Mean Volume', scope = 'col'), html.Td(id = 'mean_volume')]),
        html.Tr([html.Th('ETL 5%', scope = 'col'), html.Td(id = 'etl_5_percent')]),
        html.Tr([html.Th('Benchmark', scope = 'col'), html.Td(id = 'benchmark_ticker')]),
        html.Tr([html.Th('Covariance', scope = 'col'), html.Td(id = 'covariance')]),
        html.Tr([html.Th('Correlation', scope = 'col'), html.Td(id = 'correlation')]),
        html.Tr([html.Th('Beta', scope = 'col'), html.Td(id = 'beta')]),
        html.Tr([html.Th('Days Traded', scope = 'col'), html.Td(id = 'trading_day_count')]),
        html.Tr([html.Th('Count - both stocks closed high', scope = 'col'), html.Td(id = 'both_open_high')]),
        html.Tr([html.Th('Count - both stocks closed low or even', scope = 'col'), html.Td(id = 'both_open_low')]),
        html.Tr([html.Th('Count - stock closed high, benchmark low', scope = 'col'), html.Td(id = 'stock_high_benchmark_low')]),
        html.Tr([html.Th('Count - stock closed low, benchmark high', scope = 'col'), html.Td(id = 'stock_low_benchmark_high')])
    ])
]