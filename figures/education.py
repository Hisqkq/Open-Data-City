import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

from services.data.process_education_data import get_aggregated_data, get_line_chart_data, get_admission_trade_data, get_institution_trends_data, compute_corr_institution

def create_bar_chart_figure(detail_level="global", parent_value=None, year=2022, template="mantine_light"):
    """
    Crée une figure Plotly avec des barres arrondies et une légende de couleur personnalisée pour `employment_rate_overall`.
    
    Paramètres :
      - detail_level (str) : Niveau d'agrégation ("global", "university", "school").
      - parent_value (str ou None) : Valeur du parent (ex: université pour afficher les écoles).
      - year (int) : Année de référence.
      - template (str) : Thème graphique Plotly.

    Retourne :
      - Une figure Plotly avec barres arrondies et une légende de couleur pour `employment_rate_overall`.
    """
    df_agg = get_aggregated_data(detail_level, parent_value, year)

    # Déterminer la colonne à afficher sur l'axe X
    if detail_level == "global":
        x_col = "university"
    elif detail_level == "university":
        x_col = "school"
    elif detail_level == "school":
        x_col = "degree"
    else:
        x_col = "university"

    # Création de la figure avec des barres arrondies
    fig = go.Figure(layout=dict(barcornerradius=15))

    fig.add_trace(go.Bar(
        x=df_agg[x_col],
        y=df_agg["gross_monthly_median"],
        marker=dict(
            color=df_agg["employment_rate_overall"],
            colorscale="deep_r",
            cmin=70, cmax=100,  # Échelle de couleur de 70% à 100%
            line=dict(color="white", width=1.5),  # Contour blanc pour effet arrondi
            colorbar=dict(
                title=dict(
                    text="Employment Rate (%)",
                    side="top",
                ),
                orientation="h",
                len=0.5,  # Longueur de la barre de couleur
            )
        ),
        opacity=0.8,  # Légère transparence pour améliorer l'effet visuel
        hoverinfo="x+y+text",
        text=df_agg["employment_rate_overall"].apply(lambda x: f"Employment Rate: {x:.1f}%"),  # Ajout dans le hover
    ))

    # Mise en forme des axes et légende
    fig.update_layout(
        title=f"Median Gross Starting Salary by {x_col.capitalize()}",
        xaxis_title=x_col.capitalize(),
        yaxis_title="Gross Salary (S$)",
        template=template,
        xaxis_tickangle=-7,
        hovermode="x unified",
        height=550,
    )

    fig.update_xaxes(showspikes=False)

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

    # On augmente la hauteur du graphique pour laisser de la place à la légende
    fig.update_layout(height=450)

    if hover_mode == "closest":
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)

    return fig

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_admission_trends_figure(show_regression=False, marker_size=8, template="mantine_light"):
    """
    Crée un graphique interactif illustrant l'évolution des admissions universitaires à Singapour.
    Connecte les points historiques et les prédictions sur une seule ligne continue.

    Paramètres :
      - show_regression (bool) : Afficher ou non les courbes de régression des prédictions.
      - marker_size (int) : Taille des points de données.
      - template (str) : Thème graphique pour Plotly.
      
    Retourne :
      - Une figure Plotly avec les admissions réelles et prédites, ainsi qu'une séparation entre historique et prévisions.
    """
    # Charger les données
    df = get_admission_trade_data()

    # Déterminer l'année de séparation des données réelles et des prédictions
    last_real_year = df.dropna(subset=["intake"]).iloc[-1]["year"]
    
    # Création du graphique avec un axe secondaire
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Ajout des courbes connectant les points historiques et prévisions
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["intake"], mode="lines+markers", name="Intake",
        marker=dict(color="blue", size=marker_size), line=dict(color="blue", dash="solid")
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["enrolment"], mode="lines+markers", name="Enrolment",
        marker=dict(color="green", size=marker_size), line=dict(color="green", dash="solid")
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df["year"], y=df["intake_rate"], mode="lines+markers", name="Intake Rate (%)",
        marker=dict(color="red", size=marker_size), line=dict(color="red", dash="solid")
    ), secondary_y=True)

    # Affichage des prédictions si demandé
    if show_regression:
        fig.add_trace(go.Scatter(
            x=df["year"], y=df["intake_pred"], mode="lines+markers", name="Intake (Forecast)",
            marker=dict(color="blue", symbol="circle-open", size=marker_size), line=dict(color="blue", dash="dot")
        ), secondary_y=False)

        fig.add_trace(go.Scatter(
            x=df["year"], y=df["enrolment_pred"], mode="lines+markers", name="Enrolment (Forecast)",
            marker=dict(color="green", symbol="circle-open", size=marker_size), line=dict(color="green", dash="dot")
        ), secondary_y=False)

        fig.add_trace(go.Scatter(
            x=df["year"], y=df["intake_rate_pred"], mode="lines+markers", name="Intake Rate (Forecast)",
            marker=dict(color="red", symbol="circle-open", size=marker_size), line=dict(color="red", dash="dot")
        ), secondary_y=True)

        # Ajout d'une ligne verticale pour séparer les données réelles et prédites
        fig.add_shape(type="line", x0=last_real_year+0.5, x1=last_real_year+0.5, y0=0, y1=1, xref='x', yref='paper',
                    line=dict(color="black", width=2, dash="dash"))
        
        # Ajout d'annotations pour différencier les périodes historiques et prédites
        fig.add_annotation(x=last_real_year-1, y=0.97, xref="x", yref="paper", text="Historical", showarrow=False, font=dict(size=12))
        fig.add_annotation(x=last_real_year+2, y=0.97, xref="x", yref="paper", text="Forecast", showarrow=False, font=dict(size=12))
        fig.update_xaxes(range=[2004.8, 2028.2])

    else:
        # On met l'axe des y jusqu'en 2023 pour ne pas étirer le graphique
        fig.update_xaxes(range=[2004.8, 2023.2])


    # Mise à jour des axes et de la légende
    fig.update_layout(
        title="University Admissions Trends Over the Years",
        xaxis_title="Year",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=50, r=50, t=80, b=100),
        template=template,
        hovermode="x unified"
    )

    fig.update_yaxes(title_text="Absolute Numbers", secondary_y=False)
    fig.update_yaxes(title_text="Intake Rate (%)", secondary_y=True)

    return fig




def create_institution_trends_figure(metric="enrolment", institutions=None, template="mantine_light", csv_path="services/data/processed/institution_data.csv", hover_mode="closest"):
    """
    Crée un graphique linéaire interactif avec Plotly Graph Objects pour l'évolution de la métrique sélectionnée par institution.
    
    Paramètres:
      - metric : "enrolment", "intake" ou "intake_rate".
      - institutions : Liste d'institutions à afficher (pour un multiselect). Si None, on affiche toutes.
      - template : Template Plotly, par exemple "plotly_white" ou "plotly_dark".
      - csv_path : Chemin vers le fichier CSV.
      
    Retourne:
      Une figure Plotly avec une trace par institution et la légende positionnée en bas.
    """
    # Récupérer les données agrégées
    df = get_institution_trends_data(metric=metric, institutions=institutions, csv_path=csv_path)
    
    # Obtenir la liste des institutions présentes
    institutions_list = sorted(df["institution"].unique())
    
    # Définir une palette de couleurs étendue (par exemple, "Plotly" qualitative ou une autre)
    color_palette = px.colors.qualitative.Plotly
    color_dict = {inst: color_palette[i % len(color_palette)] for i, inst in enumerate(institutions_list)}
    
    fig = go.Figure()
    
    # Pour chaque institution, ajouter une trace avec ses données (triées par année)
    for inst in institutions_list:
        df_inst = df[df["institution"] == inst]
        fig.add_trace(
            go.Scatter(
                x=df_inst["year"],
                y=df_inst[metric],
                mode="lines+markers",
                name=inst,
                line=dict(color=color_dict[inst])
            )
        )
    
    # Mettre à jour le layout
    fig.update_layout(
        template=template,
        title=f"Evolution of {metric.capitalize()} by Institution",
        xaxis_title="Year",
        yaxis_title=metric.capitalize(),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=60, t=80, b=120)
    )
    fig.update_xaxes(tickangle=-45)

    if hover_mode == "closest":
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
    
    return fig

def create_corr_institution_figure(institutions=["sit", "smu", "suss", "sutd", "nus", "ntu"], template="mantine_light", mode="intake"):
    intake_corr, enrolment_corr, corr_intake_rate = compute_corr_institution()

    if mode == "intake":
        corr = intake_corr
    elif mode == "enrolment":
        corr = enrolment_corr
    else:
        corr = corr_intake_rate
    corr = corr.loc[institutions, institutions]

    fig = go.Figure(data=go.Heatmap(
        z=corr,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu'))
    
    # On force l'echelle de colorscale entre -1 et 1 pour les coorélations
    fig.update_traces(zmin=-1, zmax=1)
        
    fig.update_layout(
        title=f"Correlation between Institutions ({mode.capitalize()})",
        template=template,
        margin=dict(l=50, r=50, t=80, b=100),
    )

    # on met un background transparent pour la figure
    fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', 
    plot_bgcolor = 'rgba(0,0,0,0)')    

    return fig