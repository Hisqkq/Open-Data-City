import plotly.express as px
from services.data.process_education_data import get_aggregated_data

def create_bar_chart_figure(detail_level="global", parent_value=None, year=2022, template="mantine_light"):
    """
    Crée une figure Plotly Express (bar chart) en fonction du niveau de détail.
    Les barres sont coloriées en fonction de la moyenne du taux d'emploi overall (entre 70 et 100).
    """
    df_agg = get_aggregated_data(detail_level, parent_value, year)
    
    # Définir la colonne x selon le niveau
    if detail_level == "global":
        x_col = "university"
    elif detail_level == "university":
        x_col = "school"
    elif detail_level == "school":
        x_col = "degree"
    else:
        x_col = "university"
    
    fig = px.bar(
        df_agg,
        x=x_col,
        y="gross_monthly_median",
        color="employment_rate_overall",
        color_continuous_scale=px.colors.sequential.deep_r,
        range_color=[70, 100],
        labels={
            x_col: x_col.capitalize(),
            "gross_monthly_median": "Gross Salary (S$)",
            "employment_rate_overall": "Employment Rate (%)"
        },
        title=f"Median Gross Salary by {x_col.capitalize()}",
        template=template  # Utilise le template fourni
    )
    fig.update_layout(xaxis_tickangle=-7)
    return fig
