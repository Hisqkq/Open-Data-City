from dash import html

def create_colorbar(theme="dark"):
    text_color = "#ffffff" if theme == "dark" else "#000000"
    border_color = "#ffffff" if theme == "dark" else "#000000"

    return html.Div(
        children=[
            html.Div(
                style={
                    "width": "200px",
                    "height": "20px",
                    "background": "linear-gradient(to right, #0000FF, #FFFFFF, #FF0000)",
                    "border": f"1px solid {border_color}",
                }
            ),
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "width": "200px"},
                children=[
                    html.Span("-1", style={"color": text_color}),
                    html.Span("0", style={"color": text_color}),
                    html.Span("1", style={"color": text_color}),
                ],
            ),
        ],
        style={"display": "flex", "flexDirection": "column", "alignItems": "center"},
    )