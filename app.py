import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import seaborn as sns
import dash_table
import mysql.connector
import pandas as pd
from dash.dependencies import Input, Output, State

mydb = mysql.connector.connect(host = 'localhost', user='root', passwd='rootpassword')

cursor = mydb.cursor(dictionary = True)
cursor.execute('SELECT * FROM tsa.tsa_claims_dashboard_ujian')
result = cursor.fetchall()
df = pd.DataFrame(result)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def generate_table(dataframe, page_size = 10):
    return dash_table.DataTable(
        id = 'datatable',
        columns = [{
            'name' : i,
            'id' : i
        } for i in dataframe.columns],
        data = dataframe.to_dict('records'),
        page_action = 'native',
        page_current = 0,
        page_size = page_size,
    )

app.layout = html.Div([
    html.Div([
        html.H1('Ujian Modul 2 Dashboard TSA'),
        html.P('Created by: Stevanus')
    ]),

    html.Div([
        dcc.Tabs([

            dcc.Tab(value = 'Tab-1', label = 'DataFrame Table', children = [
                
                html.Div([
                    html.H1('DATAFRAME TSA', style = {'textAlign' : 'center'})
                ]),

                html.Div([
                    
                    html.Div([

                        html.P('Claim Site:'),

                        dcc.Dropdown(value = 'All', id = 'Claim Site',
                        options = [{'label':i, 'value':i} for i in ['Checkpoint', 'Other', 'Checked Baggage', 'Motor Vehicle','Bus Station']])

                    ], className = 'three columns')

                        
                ], className = 'row'),

                html.Div([

                    html.Div([

                        html.P('Max Rows'),

                        dcc.Input(
                            id = 'input', type = 'number'
                    )
                    ], className = 'three columns')



                ],className = 'row'),

                html.Div([
                    html.Button(id='submit-button', children='Search', type = 'submit'),
                ]),

                html.Br(),

                html.Div(id = 'div-table', children = [generate_table(df)])

            ]),

            dcc.Tab(value = 'Tab-2', label = 'Bar-Chart', children = [

                html.Div([
                    
                    html.Div([
                        html.H6('Y1'),

                        dcc.Dropdown(value = 'Claim Amount', id = 'y1',
                        options = [{'label':i, 'value':i} for i in ['Claim Amount', 'Close Amount']])
                    ], className = 'three columns'),

                    html.Div([
                        html.H6('Y2'),

                        dcc.Dropdown(value = 'Close Amount', id = 'y2',
                        options = [{'label':i, 'value':i} for i in ['Claim Amount', 'Close Amount']])
                    ], className = 'three columns'),

                    html.Div([
                        html.H6('X'),

                        dcc.Dropdown(value = 'Claim Type', id = 'y3',
                        options = [{'label':i, 'value':i} for i in ['Claim Type', 'Close Site', 'Disposition']])


                    ], className = 'three columns'),

                    html.Div([
                        dcc.Graph( id='example-graph', figure={ 'data': [ {'x': df['Claim Type'], 'y': df['Claim Amount'], 'type': 'bar', 'name': 'Claim Amount'}, {'x': df['Claim Type'], 'y': df['Close Amount'], 'type': 'bar', 'name' : 'Claim Amount'} ], 'layout': { 'title': 'Bar-Chart' } } ) 
                    ], className = 'eleven columns')                    

                ], className = 'row')
                

            ]),

            dcc.Tab(value = 'Tab-3', label = 'Scatter-Chart', children = [

                html.Div([
                    dcc.Graph( id = 'graph-scatter', figure = {'data': [ go.Scatter( x = df[df['Claim Type'] == i]['Claim Amount'], y = df[df['Claim Type'] == i]['Close Amount'], mode='markers', name = '{}'.format(i) ) for i in df['Claim Type'].unique()], 'layout':go.Layout( xaxis= {'title': 'Claim Amount'}, yaxis={'title': 'Close Amount'}, title= '', hovermode='closest' ) } ) 
                ], className = 'eleven columns')

            ]),

            dcc.Tab(value = 'Tab-4', label = 'Pie-Chart', children = [

                html.Br(),

                html.Div([
                    dcc.Dropdown(value = 'Claim Amount', id = 'dropdown1',
                    options = [{'label':i, 'value':i} for i in ['Claim Amount', 'Close Amount', 'Day Differences', 'Amount Differences']])
                ], className = 'three columns'),

                html.Div([
                    dcc.Graph( id = 'pie-chart', figure = 
                    { 
                        'data':[
                            go.Pie(labels = ['{}'.format(i) for i in list(df['Claim Type'].unique())],
                            values = [df.groupby('Claim Type').mean()['Claim Amount'][i] for i in df['Claim Type'].unique()], sort = True)
                        ],
                        'layout' : go.Layout(title = 'Mean Pie Chart')

                    })

                ], className = 'eleven columns')
                
            ])






        ])
    ])
])


@app.callback(
    Output('example-graph', 'figure'),
    [Input('y1', 'value'),
    Input('y2', 'value'),
    Input('y3', 'value')]
)
def bargraph(y1,y2,y3):
    figure = {
        'data' : [{'x' : df[y3], 'y' : df[y1], 'type' : 'bar', 'name' : 'Claim Amount'},
        {'x' : df[y3], 'y' : df[y2], 'type' : 'bar', 'name' : 'Close Amount'}]
    }
    return figure


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('dropdown1', 'value')]   
)
def chart(x):
    figure = { 
        'data':[
            go.Pie(labels = ['{}'.format(i) for i in list(df['Claim Type'].unique())],
            values = [df.groupby('Claim Type').mean()[x][i] for i in df['Claim Type'].unique()], sort = True)
        ],
        'layout' : go.Layout(title = 'Mean Pie Chart')
    }
    return figure





if __name__ == '__main__':
    app.run_server(debug=True)