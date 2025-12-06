import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.postgres_handler import PostgresHandler

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Climate Analytics Dashboard"

postgres_handler = PostgresHandler()

@app.callback(
    Output('data-store', 'data'),
    Input('interval-component', 'n_intervals')
)
def load_data(n):
    if postgres_handler.connect():
        try:
            df = postgres_handler.read_table('combined_analysis')
            return df.to_json(date_format='iso', orient='split')
        finally:
            postgres_handler.disconnect()
    return None

app.layout = dbc.Container([
    dcc.Store(id='data-store'),
    dcc.Interval(id='interval-component', interval=60*60*1000, n_intervals=0),
    
    html.Div([
        html.H1("Climate Analytics & Economic Development Dashboard", 
               className="text-center my-4",
               style={'color': '#2c3e50', 'fontWeight': 'bold'}),
        html.P("Analyzing the relationship between energy use, renewable energy adoption, and economic indicators across 30 countries (2000-2023)",
              className="text-center text-muted mb-4",
              style={'fontSize': '18px'})
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🌍 Filters", style={'color': '#fff'}), 
                              style={'backgroundColor': '#3498db'}),
                dbc.CardBody([
                    html.Label("Select Countries:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='country-selector',
                        multi=True,
                        placeholder="Select countries (leave empty for top 5)...",
                        style={'marginBottom': '20px'}
                    ),
                    html.Label("Select Year Range:", style={'fontWeight': 'bold'}),
                    dcc.RangeSlider(
                        id='year-slider',
                        min=2000,
                        max=2023,
                        step=1,
                        value=[2015, 2023],
                        marks={i: str(i) for i in range(2000, 2024, 3)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ])
            ], className="shadow")
        ], width=12, className="mb-4")
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("⚡ Energy Use Over Time", style={'color': '#fff'}),
                              style={'backgroundColor': '#e74c3c'}),
                dbc.CardBody([
                    dcc.Graph(id='energy-time-series', config={'displayModeBar': True})
                ])
            ], className="shadow")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🌱 Renewable Energy Adoption Over Time", style={'color': '#fff'}),
                              style={'backgroundColor': '#27ae60'}),
                dbc.CardBody([
                    dcc.Graph(id='renewable-time-series', config={'displayModeBar': True})
                ])
            ], className="shadow")
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("💰 GDP per Capita vs Energy Use", style={'color': '#fff'}),
                              style={'backgroundColor': '#9b59b6'}),
                dbc.CardBody([
                    dcc.Graph(id='scatter-gdp-energy', config={'displayModeBar': True})
                ])
            ], className="shadow")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📊 Renewable Energy by Country (Latest Year)", style={'color': '#fff'}),
                              style={'backgroundColor': '#16a085'}),
                dbc.CardBody([
                    dcc.Graph(id='bar-renewable', config={'displayModeBar': True})
                ])
            ], className="shadow")
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🔥 Correlation Heatmap: Key Indicators", style={'color': '#fff'}),
                              style={'backgroundColor': '#f39c12'}),
                dbc.CardBody([
                    dcc.Graph(id='correlation-heatmap', config={'displayModeBar': True})
                ])
            ], className="shadow")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📈 Economic Growth vs Renewable Energy", style={'color': '#fff'}),
                              style={'backgroundColor': '#34495e'}),
                dbc.CardBody([
                    dcc.Graph(id='scatter-growth-renewable', config={'displayModeBar': True})
                ])
            ], className="shadow")
        ], width=6)
    ], className="mb-4"),
    
    html.Footer([
        html.Hr(),
        html.P("Climate Analytics Project | Data Source: World Bank API | 30 Countries, 2000-2023",
              className="text-center text-muted",
              style={'fontSize': '14px'})
    ])
    
], fluid=True, style={'backgroundColor': '#ecf0f1', 'padding': '20px'})

@app.callback(
    Output('country-selector', 'options'),
    Input('data-store', 'data')
)
def update_country_options(json_data):
    if json_data is None:
        return []
    
    df = pd.read_json(json_data, orient='split')
    countries = df['country_name'].dropna().unique()
    
    return [{'label': country, 'value': country} for country in sorted(countries)]

@app.callback(
    Output('energy-time-series', 'figure'),
    [Input('data-store', 'data'),
     Input('country-selector', 'value'),
     Input('year-slider', 'value')]
)
def update_energy_time_series(json_data, selected_countries, year_range):
    if json_data is None:
        return go.Figure()
    
    df = pd.read_json(json_data, orient='split')
    df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    if selected_countries:
        df = df[df['country_name'].isin(selected_countries)]
    else:
        top_countries = df.groupby('country_name')['climate_energy_use'].mean().nlargest(5).index
        df = df[df['country_name'].isin(top_countries)]
    
    fig = px.line(
        df,
        x='year',
        y='climate_energy_use',
        color='country_name',
        title='Energy Use per Capita Over Time',
        labels={'climate_energy_use': 'Energy Use (kg of oil equivalent per capita)', 
                'year': 'Year',
                'country_name': 'Country'},
        template='plotly_white'
    )
    
    fig.update_traces(mode='lines+markers', line=dict(width=2.5))
    fig.update_layout(hovermode='x unified', height=400)
    
    return fig

@app.callback(
    Output('renewable-time-series', 'figure'),
    [Input('data-store', 'data'),
     Input('country-selector', 'value'),
     Input('year-slider', 'value')]
)
def update_renewable_time_series(json_data, selected_countries, year_range):
    if json_data is None:
        return go.Figure()
    
    df = pd.read_json(json_data, orient='split')
    df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    if selected_countries:
        df = df[df['country_name'].isin(selected_countries)]
    else:
        top_countries = df.groupby('country_name')['renewable_renewable_energy_consumption_pct'].mean().nlargest(5).index
        df = df[df['country_name'].isin(top_countries)]
    
    fig = px.line(
        df,
        x='year',
        y='renewable_renewable_energy_consumption_pct',
        color='country_name',
        title='Renewable Energy Consumption Over Time',
        labels={'renewable_renewable_energy_consumption_pct': 'Renewable Energy (%)', 
                'year': 'Year',
                'country_name': 'Country'},
        template='plotly_white'
    )
    
    fig.update_traces(mode='lines+markers', line=dict(width=2.5))
    fig.update_layout(hovermode='x unified', height=400)
    
    return fig

@app.callback(
    Output('scatter-gdp-energy', 'figure'),
    [Input('data-store', 'data'),
     Input('year-slider', 'value')]
)
def update_scatter_plot(json_data, year_range):
    if json_data is None:
        return go.Figure()
    
    df = pd.read_json(json_data, orient='split')
    df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    latest_year = df['year'].max()
    df_latest = df[df['year'] == latest_year].dropna(subset=['economic_gdp_per_capita', 'climate_energy_use'])
    
    fig = px.scatter(
        df_latest,
        x='economic_gdp_per_capita',
        y='climate_energy_use',
        size='economic_population',
        color='renewable_renewable_energy_consumption_pct',
        hover_name='country_name',
        title=f'GDP per Capita vs Energy Use ({latest_year})',
        labels={
            'economic_gdp_per_capita': 'GDP per Capita (USD)',
            'climate_energy_use': 'Energy Use (kg oil eq per capita)',
            'economic_population': 'Population',
            'renewable_renewable_energy_consumption_pct': 'Renewable Energy %'
        },
        color_continuous_scale='Viridis',
        template='plotly_white'
    )
    
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(height=400)
    
    return fig

@app.callback(
    Output('bar-renewable', 'figure'),
    [Input('data-store', 'data'),
     Input('year-slider', 'value')]
)
def update_bar_chart(json_data, year_range):
    if json_data is None:
        return go.Figure()
    
    df = pd.read_json(json_data, orient='split')
    
    latest_year = df['year'].max()
    df_latest = df[df['year'] == latest_year].dropna(subset=['renewable_renewable_energy_consumption_pct'])
    
    df_top = df_latest.nlargest(10, 'renewable_renewable_energy_consumption_pct')
    
    fig = px.bar(
        df_top.sort_values('renewable_renewable_energy_consumption_pct'),
        y='country_name',
        x='renewable_renewable_energy_consumption_pct',
        orientation='h',
        title=f'Top 10 Countries by Renewable Energy Consumption ({latest_year})',
        labels={
            'country_name': 'Country',
            'renewable_renewable_energy_consumption_pct': 'Renewable Energy (%)'
        },
        color='renewable_renewable_energy_consumption_pct',
        color_continuous_scale='Greens',
        template='plotly_white'
    )
    
    fig.update_layout(showlegend=False, height=400)
    
    return fig

@app.callback(
    Output('correlation-heatmap', 'figure'),
    [Input('data-store', 'data'),
     Input('year-slider', 'value')]
)
def update_heatmap(json_data, year_range):
    if json_data is None:
        return go.Figure()
    
    df = pd.read_json(json_data, orient='split')
    df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    corr_cols = [
        'climate_energy_use',
        'climate_fossil_fuel_consumption',
        'economic_gdp_per_capita',
        'economic_gdp_growth',
        'renewable_renewable_energy_consumption_pct',
        'economic_population'
    ]
    
    df_corr = df[corr_cols].corr()
    
    labels = {
        'climate_energy_use': 'Energy Use',
        'climate_fossil_fuel_consumption': 'Fossil Fuel %',
        'economic_gdp_per_capita': 'GDP per Capita',
        'economic_gdp_growth': 'GDP Growth',
        'renewable_renewable_energy_consumption_pct': 'Renewable %',
        'economic_population': 'Population'
    }
    
    fig = go.Figure(data=go.Heatmap(
        z=df_corr.values,
        x=[labels.get(col, col) for col in df_corr.columns],
        y=[labels.get(col, col) for col in df_corr.index],
        colorscale='RdBu',
        zmid=0,
        text=df_corr.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Correlation Matrix of Key Indicators',
        xaxis={'side': 'bottom'},
        height=400,
        template='plotly_white'
    )
    
    return fig

@app.callback(
    Output('scatter-growth-renewable', 'figure'),
    [Input('data-store', 'data'),
     Input('year-slider', 'value')]
)
def update_growth_renewable_scatter(json_data, year_range):
    if json_data is None:
        return go.Figure()
    
    df = pd.read_json(json_data, orient='split')
    df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    df_filtered = df.dropna(subset=['economic_gdp_growth', 'renewable_renewable_energy_consumption_pct'])
    
    fig = px.scatter(
        df_filtered,
        x='renewable_renewable_energy_consumption_pct',
        y='economic_gdp_growth',
        color='country_name',
        hover_data=['year', 'country_name'],
        title='Economic Growth vs Renewable Energy Consumption',
        labels={
            'renewable_renewable_energy_consumption_pct': 'Renewable Energy (%)',
            'economic_gdp_growth': 'GDP Growth (%)',
            'country_name': 'Country'
        },
        template='plotly_white'
    )
    
    fig.update_traces(marker=dict(size=8, opacity=0.6))
    fig.update_layout(height=400)
    
    return fig

if __name__ == '__main__':
    print("\n" + "="*80)
    print("CLIMATE ANALYTICS DASHBOARD")
    print("="*80)
    print("\nDashboard is starting...")
    print("Access the dashboard at: http://127.0.0.1:8050")
    print("\nPress Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    app.run_server(debug=True, host='127.0.0.1', port=8050)
