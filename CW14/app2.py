from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pickle
import numpy as np

df = px.data.iris()

# Загрузка запиклинной модели
with open('linear_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Dash()

app.layout = [
    html.Div(children='My First App with Graph and Controls'),
    dcc.RadioItems(options=['sepal_width', 'petal_length', 'petal_width'], value='sepal_width', id='controls-and-radio-item'),
    html.Label('Введите число:'),
    dcc.Input(
        id='input-number',
        type='number',
        value=0,
        style={'width': '200px', 'height': '40px', 'fontSize': '20px', 'marginRight': '10px'}
    ),
    html.Div(id='output-div'),
    dcc.Graph(figure={}, id='controls-and-graph'),

]

@app.callback(
    Output('output-div', 'children'),
    Input('input-number', 'value')
)
def update_output(value):
    if value is not None:
        # Использование модели для предсказания
        prediction = model.predict(np.array([[value]]))[0]
        return f'Введенное число: {value}, Предсказанное значение: {prediction:.2f}'
    else:
        return 'Введите число'

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.scatter(df, x=col_chosen, y='sepal_length', color='species')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)