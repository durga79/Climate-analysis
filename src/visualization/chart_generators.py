import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChartGenerator:
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff6b6b',
            'info': '#17becf',
            'sequential': px.colors.sequential.Viridis,
            'diverging': px.colors.diverging.RdYlGn
        }
        
    def create_time_series_chart(self, df: pd.DataFrame, 
                                 countries: List[str],
                                 metric: str,
                                 title: str) -> go.Figure:
        fig = go.Figure()
        
        for country in countries:
            country_data = df[df['country_code'] == country].sort_values('year')
            
            fig.add_trace(go.Scatter(
                x=country_data['year'],
                y=country_data[metric],
                mode='lines+markers',
                name=country,
                hovertemplate=f'<b>{country}</b><br>' +
                             'Year: %{x}<br>' +
                             f'{metric}: %{{y:.2f}}<br>' +
                             '<extra></extra>'
            ))
            
        fig.update_layout(
            title=title,
            xaxis_title='Year',
            yaxis_title=metric.replace('_', ' ').title(),
            hovermode='x unified',
            template='plotly_white',
            font=dict(size=12),
            legend=dict(
                orientation='v',
                yanchor='top',
                y=1,
                xanchor='left',
                x=1.02
            )
        )
        
        logger.info(f"Created time series chart: {title}")
        return fig
        
    def create_scatter_plot(self, df: pd.DataFrame,
                           x_metric: str,
                           y_metric: str,
                           size_metric: str = None,
                           color_metric: str = None,
                           title: str = None) -> go.Figure:
        if title is None:
            title = f'{y_metric} vs {x_metric}'
            
        if color_metric and color_metric in df.columns:
            fig = px.scatter(
                df,
                x=x_metric,
                y=y_metric,
                size=size_metric if size_metric and size_metric in df.columns else None,
                color=color_metric,
                hover_data=['country_name', 'year'],
                title=title,
                labels={
                    x_metric: x_metric.replace('_', ' ').title(),
                    y_metric: y_metric.replace('_', ' ').title()
                },
                template='plotly_white',
                color_continuous_scale='Viridis'
            )
        else:
            fig = px.scatter(
                df,
                x=x_metric,
                y=y_metric,
                size=size_metric if size_metric and size_metric in df.columns else None,
                hover_data=['country_name', 'year'],
                title=title,
                labels={
                    x_metric: x_metric.replace('_', ' ').title(),
                    y_metric: y_metric.replace('_', ' ').title()
                },
                template='plotly_white'
            )
            
        fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
        
        logger.info(f"Created scatter plot: {title}")
        return fig
        
    def create_correlation_heatmap(self, correlation_matrix: pd.DataFrame,
                                   title: str = 'Correlation Matrix') -> go.Figure:
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=[col.replace('_', ' ').title() for col in correlation_matrix.columns],
            y=[col.replace('_', ' ').title() for col in correlation_matrix.index],
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            colorbar=dict(title='Correlation')
        ))
        
        fig.update_layout(
            title=title,
            xaxis=dict(tickangle=-45),
            template='plotly_white',
            height=600,
            width=800
        )
        
        logger.info(f"Created correlation heatmap: {title}")
        return fig
        
    def create_bar_chart(self, df: pd.DataFrame,
                        x_col: str,
                        y_col: str,
                        title: str,
                        orientation: str = 'v') -> go.Figure:
        if orientation == 'h':
            fig = go.Figure(go.Bar(
                x=df[y_col],
                y=df[x_col],
                orientation='h',
                marker=dict(color=self.color_scheme['primary'])
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=y_col.replace('_', ' ').title(),
                yaxis_title=x_col.replace('_', ' ').title(),
                template='plotly_white'
            )
        else:
            fig = go.Figure(go.Bar(
                x=df[x_col],
                y=df[y_col],
                marker=dict(color=self.color_scheme['primary'])
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title(),
                template='plotly_white'
            )
            
        logger.info(f"Created bar chart: {title}")
        return fig
        
    def create_box_plot(self, df: pd.DataFrame,
                       category_col: str,
                       value_col: str,
                       title: str) -> go.Figure:
        fig = px.box(
            df,
            x=category_col,
            y=value_col,
            title=title,
            labels={
                category_col: category_col.replace('_', ' ').title(),
                value_col: value_col.replace('_', ' ').title()
            },
            template='plotly_white',
            color=category_col
        )
        
        logger.info(f"Created box plot: {title}")
        return fig
        
    def create_choropleth_map(self, df: pd.DataFrame,
                             metric: str,
                             title: str,
                             year: int = None) -> go.Figure:
        if year:
            data = df[df['year'] == year].copy()
        else:
            data = df.copy()
            
        fig = px.choropleth(
            data,
            locations='country_code',
            color=metric,
            hover_name='country_name',
            hover_data={metric: ':.2f'},
            title=title,
            color_continuous_scale='Viridis',
            labels={metric: metric.replace('_', ' ').title()}
        )
        
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True),
            template='plotly_white'
        )
        
        logger.info(f"Created choropleth map: {title}")
        return fig
        
    def create_grouped_bar_chart(self, df: pd.DataFrame,
                                 x_col: str,
                                 y_cols: List[str],
                                 title: str) -> go.Figure:
        fig = go.Figure()
        
        for y_col in y_cols:
            fig.add_trace(go.Bar(
                name=y_col.replace('_', ' ').title(),
                x=df[x_col],
                y=df[y_col]
            ))
            
        fig.update_layout(
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title='Value',
            barmode='group',
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        logger.info(f"Created grouped bar chart: {title}")
        return fig
        
    def create_histogram(self, df: pd.DataFrame,
                        metric: str,
                        title: str,
                        bins: int = 30) -> go.Figure:
        fig = px.histogram(
            df,
            x=metric,
            nbins=bins,
            title=title,
            labels={metric: metric.replace('_', ' ').title()},
            template='plotly_white',
            marginal='box'
        )
        
        fig.update_traces(marker=dict(line=dict(width=1, color='white')))
        
        logger.info(f"Created histogram: {title}")
        return fig
        
    def create_line_chart_with_confidence_interval(self, df: pd.DataFrame,
                                                   x_col: str,
                                                   y_col: str,
                                                   group_col: str,
                                                   title: str) -> go.Figure:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=group_col,
            title=title,
            labels={
                x_col: x_col.replace('_', ' ').title(),
                y_col: y_col.replace('_', ' ').title()
            },
            template='plotly_white'
        )
        
        fig.update_traces(mode='lines+markers')
        
        logger.info(f"Created line chart with groups: {title}")
        return fig
        
    def save_chart(self, fig: go.Figure, filename: str, format: str = 'html'):
        if format == 'html':
            fig.write_html(f"{filename}.html")
        elif format == 'png':
            fig.write_image(f"{filename}.png")
        elif format == 'svg':
            fig.write_image(f"{filename}.svg")
            
        logger.info(f"Saved chart to {filename}.{format}")


