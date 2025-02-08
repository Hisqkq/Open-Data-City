import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from services.data.process_education_data import get_aggregated_data, get_line_chart_data, get_admission_trade_data

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
    fig.update_layout(hovermode="x unified")

    return fig

def create_line_chart_figure(metric="intake", gender="both", template="mantine_light", csv_path="services/data/processed/course_data.csv", hover_mode="closest"):
    """
    Crée un graphique linéaire interactif avec Plotly Graph Objects pour l'évolution des cours selon la métrique sélectionnée.
    
    Paramètres:
      - metric : "intake", "enrolment", "graduates", ou "intake_rate"
      - gender : "both", "women" ou "men"
      - template : template Plotly (ex. "plotly_white" ou "plotly_dark")
      - csv_path : chemin vers le fichier CSV prétraité
      - hover_mode : mode de survol pour le graphique ("closest" pour un point précis, "x unified" pour des infos année par année)
      
    Retourne une figure Plotly.
    """
    df_pivot = get_line_chart_data(metric=metric, gender=gender, csv_path=csv_path)
    fig = go.Figure()
    
    # Utiliser une palette qualitative avec de nombreuses couleurs (par exemple Alphabet)
    color_palette = px.colors.qualitative.Alphabet  # 26 couleurs disponibles
    colors = {course: color_palette[i % len(color_palette)] for i, course in enumerate(df_pivot.columns)}
    
    # Ajouter une trace par cours avec une couleur assignée
    for course in df_pivot.columns:
        fig.add_trace(
            go.Scatter(
                x=df_pivot.index,
                y=df_pivot[course],
                mode='lines+markers',
                name=course,
                line=dict(color=colors[course])
            )
        )
    
    fig.update_layout(
        template=template,
        title=f"Evolution of {metric.capitalize()} by Course ({gender.capitalize()})",
        xaxis_title="Year",
        yaxis_title=metric.capitalize(),
        legend=dict(
            orientation="h",      
            yanchor="bottom",
            y=-0.6,  # Baisser un peu plus la légende
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=50, t=80, b=100),
        hovermode=hover_mode  # On choisit le mode de survol passé en paramètre
    )

    if hover_mode == "closest":
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)

    return fig


def create_admission_trends_figure(template="mantine_light"):
    """
    Crée un graphique à lignes multiples illustrant l'évolution des indicateurs d'admission (intake, enrolment et intake_rate)
    sur les années. Les indicateurs absolus (intake et enrolment) sont affichés sur l'axe principal,
    tandis que le taux d'admission (intake_rate) est affiché sur un axe secondaire.
    
    Paramètres:
      - csv_path: chemin vers le fichier CSV contenant les colonnes: 
          year, intake, enrolment, intake_rate
      
    Retourne:
      - Une figure Plotly avec un axe secondaire pour le taux d'admission.
    """
    # Charger et convertir les données
    df = get_admission_trade_data()
    
    # Créer un graphique avec un axe secondaire
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Trace pour l'intake
    fig.add_trace(
        go.Scatter(x=df["year"], y=df["intake"], mode="lines+markers", name="Intake"),
        secondary_y=False,
    )
    # Trace pour l'enrolment
    fig.add_trace(
        go.Scatter(x=df["year"], y=df["enrolment"], mode="lines+markers", name="Enrolment"),
        secondary_y=False,
    )
    # Trace pour le taux d'admission, sur l'axe secondaire
    fig.add_trace(
        go.Scatter(x=df["year"], y=df["intake_rate"], mode="lines+markers", name="Intake Rate (%)"),
        secondary_y=True,
    )
    
    # Mise à jour des axes et de la légende
    fig.update_layout(
        title="University Admissions Trends Over the Years",
        xaxis_title="Year",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=50, t=80, b=100),
        template=template
    )
    fig.update_layout(hovermode="x unified")
    
    fig.update_yaxes(title_text="Absolute Numbers", secondary_y=False)
    fig.update_yaxes(title_text="Intake Rate (%)", secondary_y=True)
    
    return fig
