import plotly.express as px
import plotly.graph_objects as go
from services.data.process_data_immo import process_data_immo, process_data_table_intro

def create_line_chart_figure_introduction():
    """
    Crée une figure Plotly Express (line chart) pour l'introduction.
    """
    df_agg = process_data_immo()
    
    fig = px.line(
        df_agg,
        x="Date",
        y="price_m2",
        title="Prix au m2 en fonction de la date",
    )
    return fig

def create_table_figure_introduction():
    """
    Crée une figure Plotly Express (table) pour l'introduction.
    """
    df_agg = process_data_table_intro()
    
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df_agg.columns), 
                    fill_color="lightgrey",
                    align="center"
                ),
                cells=dict(
                    values=[df_agg[col] for col in df_agg.columns], 
                    fill_color="white",
                    align="center"
                )
            )
        ]
    )
    return fig