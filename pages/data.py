import dash
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, callback, State
from dash_iconify import DashIconify
import math
from utils.data_config import get_grouped_dataset_options, get_dataset_by_id, load_dataset

dash.register_page(__name__, path="/data")

layout = dmc.Container(
    fluid=True,
    p="xl", 
    children=[
        dmc.Group(
            align="center",
            justify="center",
            children=[
                DashIconify(icon="mdi:table", height=40, color="#228be6"),
                dmc.Title("Open Data Table", order=1),
            ],
            style={"marginBottom": "1rem"},
        ),
        dmc.Text(
            "Explore the datasets we used in this project. Click on a dataset to view its description and data.",
            size="md",
            style={"marginTop": "0.5rem", "margin" : "auto", "textAlign": "center",  "marginBottom": "0.5rem"},
        ),
        dmc.Space(h="md"),

        dmc.Select(
            id="dataset-select",
            data=get_grouped_dataset_options(),
            placeholder="Search for a dataset",
            searchable=True,
            style={"width": "30%", "margin": "auto", "marginBottom": "1rem"}
        ),
        
        dmc.Space(h="md"),
        
        html.Div(
            dmc.Table(
                id="data-table",
                striped=True,
                highlightOnHover=True,
                withColumnBorders=True,
                data={}  
            ),
            style={"overflowX": "auto", "width": "100%"}
        ),
        
        dmc.Space(h="md"),
        
        dmc.Pagination(
            id="table-pagination",
            total=1,  
            boundaries=1,
            value=1,  
            style={"margin": "auto"}
        ),
        
        dmc.Space(h="md"),
        
        html.Div(
            id="dataset-description",
            style={"width": "100%", "margin": "auto", "padding": "1rem", "border": "1px solid #ccc", "borderRadius": "8px"}
        ),
    ],
    style={"padding": "1rem"}
)

@callback(
    Output("data-table", "data"),
    Output("table-pagination", "total"),
    Output("dataset-description", "children"),
    Input("dataset-select", "value"),
    Input("table-pagination", "value")
)
def update_data_table(dataset_id, page):
    if not dataset_id:
        return {}, 1, "Please select a dataset from the dropdown above."
    
    dataset = get_dataset_by_id(dataset_id)
    if not dataset:
        return {}, 1, "Dataset not found."
    
    try:
        df = load_dataset(dataset_id)
    except Exception as e:
        return {}, 1, f"Error loading data: {e}"
    
    head = list(df.columns)
    body = df.values.tolist()
    
    rows_per_page = 10
    total_pages = math.ceil(len(body) / rows_per_page)
    page = max(1, page)
    start = (page - 1) * rows_per_page
    end = start + rows_per_page
    body_paginated = body[start:end]
    
    description_text = [
        dmc.Text("Dataset description", size="lg"),
        dcc.Markdown(
            dataset["description"],
            style={"textAlign": "justify", "lineHeight": "1.6"}
        ),
        dmc.Space(h="sm"),
        dmc.Anchor("Data Source", href=dataset["source_link"], target="_blank", size="md")
    ]
    
    table_data = {
        "caption": "",
        "head": head,
        "body": body_paginated
    }
    
    return table_data, total_pages, description_text
