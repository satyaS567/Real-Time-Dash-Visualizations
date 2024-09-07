import dash
from dash import dcc, html  # Updated imports
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
import plotly.graph_objects as go  # Import graph_objects for table creation

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Setup SQLAlchemy engine
engine = create_engine('sqlite:///example.db')

# Define app layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Dashboard"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H2("Total Amount Spent by Top 3 Users"), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='top-3-users-graph'))
        ]),
        dbc.Row([
            dbc.Col(html.H2("Transaction Amounts Over Time"), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='transactions-time-graph'))
        ]),
        dbc.Row([
            dbc.Col(html.H2("User Report"), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='user-report-table'))
        ]),
        dbc.Row([
            dbc.Col(html.H2("Users With No Transactions"), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='no-transactions-table'))
        ])
    ])
])

# Callback to update top 3 users graph
@app.callback(
    Output('top-3-users-graph', 'figure'),
    [Input('top-3-users-graph', 'id')]
)
def update_top_3_users_graph(_):
    df = pd.read_sql_query('''
        SELECT u.name, SUM(t.amount) AS total_spent
        FROM users u
        JOIN transactions t ON u.user_id = t.user_id
        GROUP BY u.user_id
        ORDER BY total_spent DESC
        LIMIT 3
    ''', engine)
    if df.empty:
        return {}
    fig = px.bar(df, x='name', y='total_spent', title='Total Amount Spent by Top 3 Users')
    return fig

# Callback to update transactions over time graph
@app.callback(
    Output('transactions-time-graph', 'figure'),
    [Input('transactions-time-graph', 'id')]
)
def update_transactions_time_graph(_):
    df = pd.read_sql_query('''
        SELECT transaction_date, amount
        FROM transactions
    ''', engine)
    if df.empty:
        return {}
    fig = px.scatter(df, x='transaction_date', y='amount', title='Transaction Amounts Over Time')
    return fig

# Callback to update user report table
@app.callback(
    Output('user-report-table', 'figure'),
    [Input('user-report-table', 'id')]
)
def update_user_report_table(_):
    df = pd.read_sql_query('''
        SELECT u.name, u.email, COALESCE(SUM(t.amount), 0) AS total_spent
        FROM users u
        LEFT JOIN transactions t ON u.user_id = t.user_id
        GROUP BY u.user_id
    ''', engine)
    if df.empty:
        return {}
    # Create table using graph_objects
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.name, df.email, df.total_spent],
                   fill_color='lavender',
                   align='left'))
    ])
    fig.update_layout(title='User Report')
    return fig

# Callback to update no transactions table
@app.callback(
    Output('no-transactions-table', 'figure'),
    [Input('no-transactions-table', 'id')]
)
def update_no_transactions_table(_):
    df = pd.read_sql_query('''
        SELECT u.user_id, u.name, u.email
        FROM users u
        LEFT JOIN transactions t ON u.user_id = t.user_id
        WHERE t.transaction_id IS NULL
    ''', engine)
    if df.empty:
        return {}
    # Create table using graph_objects
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.user_id, df.name, df.email],
                   fill_color='lavender',
                   align='left'))
    ])
    fig.update_layout(title='Users With No Transactions')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
