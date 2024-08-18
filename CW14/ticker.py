import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Создаем приложение Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Label("Введите тикер акции:"),
        dcc.Input(id='ticker-input', value='AAPL', type='text')
    ], style={'display': 'inline-block', 'margin-right': '20px'}),
    html.Div([
        html.Label("Выберите диапазон дат:"),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=pd.to_datetime('2023-01-01'),
            end_date=pd.to_datetime('2023-12-31'),
            display_format='YYYY-MM-DD'
        )
    ], style={'display': 'inline-block'}),
    dcc.Graph(id='stock-chart')
])

@app.callback(
    Output('stock-chart', 'figure'),
    [Input('ticker-input', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_chart(ticker, start_date, end_date):
    # Преобразуем даты в формат, который поддерживается yfinance
    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')

    # Получаем данные из Yahoo Finance
    df = yf.download(ticker, start=start_date, end=end_date)
    df.reset_index(inplace=True)

    # Создаем фигуру
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name=ticker))
    fig.update_layout(title=f'Цены на акции {ticker}', xaxis_title='Дата', yaxis_title='Цена')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
