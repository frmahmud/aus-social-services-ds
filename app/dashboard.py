import os
import pandas as pd
import numpy as np
import plotly.express       as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
import warnings
warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

# ── Load data ──────────────────────────────────────────────────────────────
def safe_load(filename):
    path = os.path.join(PROCESSED_DIR, filename)
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

df_seifa     = safe_load("seifa_with_risk_tier.csv")
df_sentiment = safe_load("sentiment_results.csv")
df_topics    = safe_load("topic_model_results.csv")

COLOR_MAP = {"High": "#993C1D", "Medium": "#BA7517", "Low": "#1D9E75"}

# ── App layout ─────────────────────────────────────────────────────────────
app = Dash(__name__, title="Social Services Risk Dashboard")

app.layout = html.Div([

    html.Div([
        html.H1("Social Services Demand Risk Predictor",
                style={"color": "#1D9E75", "marginBottom": "4px"}),
        html.P("Australian Public Sector — Department of Social Services",
               style={"color": "#5F5E5A", "marginTop": "0"}),
    ], style={"padding": "1.5rem 2rem 0.5rem", "borderBottom": "2px solid #E0E0E0"}),

    html.Div([

        # ── Panel 1: Risk Tier Distribution ────────────────────────────────
        html.Div([
            html.H3("SA2 Risk Tier Distribution",
                    style={"color": "#185FA5", "marginBottom": "8px"}),
            html.P("Regions classified as High / Medium / Low welfare demand risk "
                   "based on IRSD socioeconomic disadvantage score.",
                   style={"color": "#5F5E5A", "fontSize": "13px"}),
            dcc.Graph(id="risk-tier-chart", style={"height": "380px"}),

            html.Div([
                html.Label("Filter by State / Territory:",
                           style={"fontWeight": "bold", "fontSize": "13px"}),
                dcc.Dropdown(
                    id      = "state-filter",
                    options = (
                        [{"label": "All States", "value": "All"}] +
                        [{"label": s, "value": s}
                         for s in sorted(df_seifa.get(
                             next((c for c in df_seifa.columns
                                   if "state" in c.lower()), ""), pd.Series()
                         ).dropna().unique())]
                    ) if len(df_seifa) > 0 else [{"label": "All", "value": "All"}],
                    value      = "All",
                    clearable  = False,
                    style      = {"marginTop": "6px"}
                ),
            ], style={"marginTop": "12px"}),

        ], style={"background": "white", "borderRadius": "10px",
                  "padding": "1.2rem", "border": "1px solid #E0E0E0",
                  "marginBottom": "1rem"}),

        # ── Panel 2: Sentiment Trend ───────────────────────────────────────
        html.Div([
            html.H3("Policy Sentiment Trend 2018–2023",
                    style={"color": "#185FA5", "marginBottom": "8px"}),
            html.P("VADER compound sentiment score from DSS Annual Reports. "
                   "Positive = constructive language. Negative = urgent/crisis language.",
                   style={"color": "#5F5E5A", "fontSize": "13px"}),
            dcc.Graph(id="sentiment-chart", style={"height": "340px"}),
        ], style={"background": "white", "borderRadius": "10px",
                  "padding": "1.2rem", "border": "1px solid #E0E0E0",
                  "marginBottom": "1rem"}),

        # ── Panel 3: Topic Evolution ───────────────────────────────────────
        html.Div([
            html.H3("Policy Topic Evolution Over Time",
                    style={"color": "#185FA5", "marginBottom": "8px"}),
            html.P("LDA topic proportions per year. Each colour represents "
                   "a distinct policy theme discovered from DSS Annual Reports.",
                   style={"color": "#5F5E5A", "fontSize": "13px"}),
            dcc.Graph(id="topic-chart", style={"height": "340px"}),
        ], style={"background": "white", "borderRadius": "10px",
                  "padding": "1.2rem", "border": "1px solid #E0E0E0",
                  "marginBottom": "1rem"}),

    ], style={"padding": "1rem 2rem", "maxWidth": "1000px", "margin": "0 auto"}),

    html.Div([
        html.P("Data sources: ABS SEIFA 2021 · DSS Payment Data · DSS Annual Reports "
               "2018–2023 · All open data under CC BY 4.0",
               style={"color": "#9E9E9E", "fontSize": "12px", "textAlign": "center"})
    ], style={"padding": "1rem", "borderTop": "1px solid #E0E0E0", "marginTop": "1rem"}),

], style={"fontFamily": "Arial, sans-serif", "background": "#F8F8F5",
          "minHeight": "100vh"})


# ── Callbacks ──────────────────────────────────────────────────────────────
@app.callback(
    Output("risk-tier-chart", "figure"),
    Input("state-filter", "value")
)
def update_risk_chart(selected_state):
    if len(df_seifa) == 0:
        return go.Figure().add_annotation(text="No data loaded",
                                          showarrow=False, font_size=16)

    state_col = next((c for c in df_seifa.columns if "state" in c.lower()), None)
    df = df_seifa.copy()

    if selected_state != "All" and state_col:
        df = df[df[state_col] == selected_state]

    counts = df["risk_tier"].value_counts().reindex(
        ["High", "Medium", "Low"], fill_value=0
    ).reset_index()
    counts.columns = ["Risk Tier", "Count"]

    fig = px.bar(
        counts, x="Risk Tier", y="Count",
        color="Risk Tier",
        color_discrete_map=COLOR_MAP,
        text="Count"
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=20, b=20), yaxis_title="SA2 Regions"
    )
    return fig


@app.callback(
    Output("sentiment-chart", "figure"),
    Input("state-filter", "value")   # dummy input to wire the callback
)
def update_sentiment_chart(_):
    if len(df_sentiment) == 0:
        return go.Figure().add_annotation(text="No sentiment data loaded",
                                          showarrow=False, font_size=16)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sentiment["year"], y=df_sentiment["compound"],
        mode="lines+markers+text",
        line=dict(color="#534AB7", width=2.5),
        marker=dict(size=8),
        text=df_sentiment["compound"].round(3).astype(str),
        textposition="top center",
        name="Compound score"
    ))
    fig.add_hrect(y0=0.05,  y1=1,   fillcolor="#1D9E75", opacity=0.08, line_width=0)
    fig.add_hrect(y0=-1,    y1=-0.05, fillcolor="#993C1D", opacity=0.08, line_width=0)
    fig.add_hline(y=0, line_dash="dot", line_color="gray", line_width=1)
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=20, b=20),
        yaxis=dict(title="Compound score", range=[-0.5, 0.5]),
        xaxis_title="Year"
    )
    return fig


@app.callback(
    Output("topic-chart", "figure"),
    Input("state-filter", "value")   # dummy input
)
def update_topic_chart(_):
    if len(df_topics) == 0:
        return go.Figure().add_annotation(text="No topic data loaded",
                                          showarrow=False, font_size=16)

    topic_cols = [c for c in df_topics.columns if c != "year"]
    year_col   = "year" if "year" in df_topics.columns else df_topics.index.name

    df_t = df_topics.reset_index() if year_col == df_topics.index.name else df_topics
    colors = ["#1D9E75","#534AB7","#BA7517","#993C1D",
              "#185FA5","#3B6D11","#5F5E5A","#D4537E"]

    fig = go.Figure()
    for i, col in enumerate(topic_cols):
        fig.add_trace(go.Bar(
            name=col, x=df_t.get("year", df_t.index),
            y=df_t[col], marker_color=colors[i % len(colors)]
        ))

    fig.update_layout(
        barmode="stack", plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=20, b=20),
        yaxis=dict(title="Topic proportion",
                   tickformat=".0%", range=[0, 1]),
        xaxis_title="Year",
        legend=dict(orientation="v", x=1.01, y=1, font_size=9)
    )
    return fig


if __name__ == "__main__":
    print("Starting Social Services Risk Dashboard...")
    print("Open your browser at: http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
