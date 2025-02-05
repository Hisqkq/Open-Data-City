import plotly.express as px
from services.data.process_data_immo import process_data_immo

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