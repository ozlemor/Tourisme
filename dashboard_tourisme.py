# ============================================================
# DASHBOARD TOURISME — Streamlit
# 4 vues : Executive, Data Quality, Forecast, Recommandation
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title='Tourisme — Tableau de bord',
    layout='wide'
)

C = {
    'blue':   '#4361ee',
    'red':    '#ef4444',
    'green':  '#22c55e',
    'orange': '#f59e0b',
    'purple': '#8b5cf6',
    'teal':   '#14b8a6',
    'gray':   '#6b7280',
    'dark':   '#1a1f36',
}

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #f8f9fc; }
    .block-container { padding: 1.5rem 2rem; }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border-left: 4px solid;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1f36;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-top: 0.2rem;
    }

    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #4361ee;
    }

    .piege-card {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        color: #1a1f36;
    }
    .piege-card strong {
        color: #1a1f36;
    }

    .decision-card {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        color: #1a1f36;
    }
    .decision-card strong {
        color: #1a1f36;
    }

    .hausse-card {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
        color: #1a1f36;
    }
    .hausse-card strong { color: #1a1f36; }
    .hausse-card .val { color: #16a34a; font-weight: 700; }

    .baisse-card {
        background: #fff1f2;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
        color: #1a1f36;
    }
    .baisse-card strong { color: #1a1f36; }
    .baisse-card .val { color: #dc2626; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# CHARGEMENT DES DONNÉES
# ------------------------------------------------------------
@st.cache_data
def load_data():
    gold_dest    = pd.read_csv('data/gold/gold_destinations.csv')
    gold_signaux = pd.read_csv('data/gold/gold_signaux.csv')
    gold_signaux['month'] = pd.to_datetime(gold_signaux['month'])
    reco         = pd.read_csv('data/gold/recommandations_finales.csv')
    with open('data/gold/ml_results_final.json', encoding='utf-8') as f:
        ml_results = json.load(f)
    return gold_dest, gold_signaux, reco, ml_results

gold_dest, gold_signaux, reco, ml_results = load_data()

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
st.sidebar.title('Tourisme Analytics')
st.sidebar.markdown('---')

vue = st.sidebar.radio(
    'Navigation',
    ['Vue Executive', 'Data Quality', 'Forecast', 'Recommandation']
)

st.sidebar.markdown('---')
pays_list = sorted(gold_dest['country'].unique().tolist())
pays_sel  = st.sidebar.multiselect('Pays', pays_list, default=pays_list)

st.sidebar.markdown('---')
st.sidebar.markdown(
    '<p style="color:#6b7280;font-size:0.8rem">EPITA Master — Gouvernance IM<br>Examen Final AED + MPE</p>',
    unsafe_allow_html=True
)

# Filtres
gold_dest_f    = gold_dest[gold_dest['country'].isin(pays_sel)]
gold_signaux_f = gold_signaux[gold_signaux['country'].isin(pays_sel)]
reco_f         = reco[reco['country'].isin(pays_sel)]

# ------------------------------------------------------------
# VUE 1 — EXECUTIVE
# ------------------------------------------------------------
if vue == 'Vue Executive':
    st.title('Vue Executive — Synthese Tourisme')
    st.markdown('---')

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['blue']}">
            <div class="metric-value">{len(gold_dest_f['country'].unique())}</div>
            <div class="metric-label">Pays analyses</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['green']}">
            <div class="metric-value">{len(gold_dest_f)}</div>
            <div class="metric-label">Destinations</div></div>""", unsafe_allow_html=True)
    with c3:
        demand_moy = gold_signaux_f['demand_index'].mean()
        st.markdown(f"""<div class="metric-card" style="border-color:{C['orange']}">
            <div class="metric-value">{demand_moy:.1f}</div>
            <div class="metric-label">Demand index moyen</div></div>""", unsafe_allow_html=True)
    with c4:
        nb_opport = int(gold_dest_f['flag_opportunite'].sum())
        st.markdown(f"""<div class="metric-card" style="border-color:{C['purple']}">
            <div class="metric-value">{nb_opport}</div>
            <div class="metric-label">Opportunites detectees</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['teal']}">
            <div class="metric-value">{len(reco_f)}</div>
            <div class="metric-label">Destinations recommandees</div></div>""", unsafe_allow_html=True)

    st.markdown('---')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>Evolution demand index par pays</div>", unsafe_allow_html=True)
        fig = px.line(gold_signaux_f, x='month', y='demand_index', color='country',
                      color_discrete_sequence=list(C.values()))
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend=dict(orientation='h', y=-0.2, font=dict(color='#ffffff')),
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'))
        fig.update_xaxes(showgrid=False, tickfont=dict(color='#ffffff'))
        fig.update_yaxes(gridcolor='#f0f0f0', tickfont=dict(color='#ffffff'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>Score promotion moyen par pays</div>", unsafe_allow_html=True)
        agg = gold_dest_f.groupby('country')['score_promotion'].mean().reset_index()
        agg = agg.sort_values('score_promotion', ascending=True)
        fig = px.bar(agg, x='score_promotion', y='country', orientation='h',
                     color='score_promotion', color_continuous_scale='Blues',
                     text=agg['score_promotion'].round(2))
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          coloraxis_showscale=False,
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'))
        fig.update_xaxes(showgrid=False, tickfont=dict(color='#ffffff'))
        fig.update_yaxes(showgrid=False, tickfont=dict(color='#ffffff'))
        fig.update_traces(textfont=dict(color='#ffffff'))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-title'>Attractivite vs Visiteurs</div>", unsafe_allow_html=True)
        fig = px.scatter(gold_dest_f, x='visitors', y='attractiveness',
                         color='country', size='cost',
                         hover_data=['destination', 'rating'],
                         color_discrete_sequence=list(C.values()))
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#1a1f36'),
                          legend=dict(font=dict(color='#ffffff')))
        fig.update_xaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>Opportunites et bizarres par pays</div>", unsafe_allow_html=True)
        opport = gold_dest_f.groupby('country').agg(
            opportunites=('flag_opportunite', 'sum'),
            bizarres=('flag_bizarre', 'sum')
        ).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Opportunites', x=opport['country'],
                             y=opport['opportunites'], marker_color=C['green'],
                             text=opport['opportunites'], textposition='outside',
                             textfont=dict(color='#ffffff')))
        fig.add_trace(go.Bar(name='Bizarres', x=opport['country'],
                             y=opport['bizarres'], marker_color=C['orange'],
                             text=opport['bizarres'], textposition='outside',
                             textfont=dict(color='#ffffff')))
        fig.update_layout(barmode='group', height=350,
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend=dict(orientation='h', y=-0.2, font=dict(color='#ffffff')),
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'))
        fig.update_xaxes(tickfont=dict(color='#ffffff'))
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# VUE 2 — DATA QUALITY
# ------------------------------------------------------------
elif vue == 'Data Quality':
    st.title('Data Quality — AED et Nettoyage')
    st.markdown('---')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['green']}">
            <div class="metric-value">160</div>
            <div class="metric-label">Lignes GOLD DATA</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['blue']}">
            <div class="metric-value">24</div>
            <div class="metric-label">Variables documentees</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['green']}">
            <div class="metric-value">0</div>
            <div class="metric-label">Anomalies residuelles</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['orange']}">
            <div class="metric-value">15</div>
            <div class="metric-label">Pieges detectes</div></div>""", unsafe_allow_html=True)

    st.markdown('---')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>Pieges detectes dans les donnees</div>", unsafe_allow_html=True)
        pieges = [
            ('01_destinations', 'france / FRANCE / France — standardisation requise'),
            ('01_destinations', '9 destinations attract. haute + peu visiteurs'),
            ('01_destinations', '13 destinations attract. faible + beaucoup visiteurs'),
            ('02_signaux',      'Formats date mixtes : tiret et slash dans meme fichier'),
            ('03_reviews',      '68 lignes positive + score < 2 — incoherence'),
            ('03_reviews',      '71 lignes negative + score > 4 — incoherence'),
            ('03_reviews',      '458 doublons sur (country, destination)'),
            ('04_facteurs',     'Separateur point-virgule non standard'),
            ('04_facteurs',     '93 doublons — weather contradictoire meme destination'),
            ('05_cible',        'Fichier intentionnellement vide — message du prof'),
            ('06_campaign',     'budget=unknown — string au lieu de numerique'),
            ('06_campaign',     'budget=0 + ROI=80K — impossible'),
            ('06_campaign',     'ROI negatif + status=SUCCESS — incoherence'),
            ('06_campaign',     'FAIL + ROI=220K — status non fiable'),
            ('Coherence',       'USA vs Usa — standardisation entre fichiers'),
        ]
        for source, desc in pieges:
            st.markdown(f"""<div class="piege-card">
                <strong>{source}</strong> — {desc}</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-title'>Decisions de nettoyage</div>", unsafe_allow_html=True)
        decisions = [
            ('Standardisation', 'france/FRANCE → France, Usa → USA'),
            ('Format date',     'format=mixed pour gerer tiret et slash'),
            ('Reviews',         'Sentiment corrige selon score numerique'),
            ('Reviews',         '800 → 342 lignes apres agregation'),
            ('Facteurs',        'sep=; pour lecture correcte'),
            ('Facteurs',        '300 → 207 lignes apres dedoublonnage'),
            ('Campaign',        'budget/status/ROI exclus — non fiables'),
            ('Campaign',        'Seul conversion_rate conserve'),
            ('Cible',           'Construite manuellement — 2 tables'),
            ('GOLD DATA',       '160 x 24 — 0 anomalie residuelle'),
        ]
        for action, detail in decisions:
            st.markdown(f"""<div class="decision-card">
                <strong>{action}</strong> — {detail}</div>""", unsafe_allow_html=True)

    st.markdown('---')
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-title'>Distribution score promotion</div>", unsafe_allow_html=True)
        fig = px.histogram(gold_dest_f, x='score_promotion', color='country',
                           nbins=20, color_discrete_sequence=list(C.values()))
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'),
                          legend=dict(orientation='h', y=-0.3, font=dict(color='#ffffff')))
        fig.update_xaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>Distribution attractivite par pays</div>", unsafe_allow_html=True)
        fig = px.box(gold_dest_f, x='country', y='attractiveness',
                     color='country', color_discrete_sequence=list(C.values()))
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'),
                          showlegend=False)
        fig.update_xaxes(tickfont=dict(color='#ffffff'))
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# VUE 3 — FORECAST
# ------------------------------------------------------------
elif vue == 'Forecast':
    st.title('Forecast — Prevision de la demande')
    st.markdown('---')

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['blue']}">
            <div class="metric-value">SARIMA</div>
            <div class="metric-label">Modele retenu</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['green']}">
            <div class="metric-value">30</div>
            <div class="metric-label">Mois d'entrainement</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['orange']}">
            <div class="metric-value">6</div>
            <div class="metric-label">Mois de test</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card" style="border-color:{C['purple']}">
            <div class="metric-value">8/8</div>
            <div class="metric-label">Pays meilleurs que Baseline</div></div>""", unsafe_allow_html=True)

    st.markdown('---')

    resultats = pd.DataFrame(ml_results['resultats'])
    resultats_f = resultats[resultats['pays'].isin(pays_sel)].copy()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>MAE — Comparaison modeles par pays</div>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Baseline A (Naive)', x=resultats_f['pays'],
            y=resultats_f['mae_baseline_a'],
            marker_color=C['gray'], opacity=0.6,
            text=resultats_f['mae_baseline_a'].round(1),
            textposition='outside', textfont=dict(color='#ffffff')
        ))
        fig.add_trace(go.Bar(
            name='SARIMA optimise', x=resultats_f['pays'],
            y=resultats_f['mae_final'],
            marker_color=C['blue'],
            text=resultats_f['mae_final'].round(1),
            textposition='outside', textfont=dict(color='#ffffff')
        ))
        fig.update_layout(barmode='group', height=350,
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend=dict(orientation='h', y=-0.2, font=dict(color='#ffffff')),
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'))
        fig.update_xaxes(tickfont=dict(color='#ffffff'))
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>Prevision Janvier 2025 par pays</div>", unsafe_allow_html=True)
        resultats_f['variation'] = (
            resultats_f['prevision_jan25'] - resultats_f['demand_dernier']
        ).round(2)
        couleurs = resultats_f['variation'].apply(
            lambda x: C['green'] if x > 0 else C['red']
        ).tolist()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=resultats_f['pays'], y=resultats_f['variation'],
            marker_color=couleurs,
            text=resultats_f['variation'].apply(
                lambda x: f'+{x:.1f}' if x > 0 else f'{x:.1f}'
            ),
            textposition='outside', textfont=dict(color='#ffffff')
        ))
        fig.add_hline(y=0, line_color='gray', line_dash='dash')
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          showlegend=False,
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'))
        fig.update_xaxes(tickfont=dict(color='#ffffff'))
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')
    st.markdown("<div class='section-title'>Previsions detaillees par pays</div>", unsafe_allow_html=True)

    pays_detail = st.selectbox('Selectionner un pays', [p for p in pays_sel])

    if pays_detail and pays_detail in ml_results.get('predictions', {}):
        pred_data = ml_results['predictions'][pays_detail]
        mois = pred_data['mois']
        reel = pred_data['reel']
        pred = pred_data['pred']

        df_pays = gold_signaux[
            gold_signaux['country'] == pays_detail
        ].sort_values('month')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_pays['month'], y=df_pays['demand_index'],
            name='Historique', line=dict(color='#ffffff', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(mois), y=reel,
            name='Reel (test)', line=dict(color='#f59e0b', width=2, dash='dot')
        ))
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(mois), y=pred,
            name='SARIMA', line=dict(color='#4361ee', width=2),
            mode='lines+markers', marker=dict(size=6, color='#4361ee')
        ))
        fig.add_vrect(x0='2024-07-01', x1='2024-07-15',
                      fillcolor='gray', opacity=0.3, line_width=0,
                      annotation_text='Split', annotation_position='top left',
                      annotation_font_color='#1a1f36')
        fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend=dict(orientation='h', y=-0.2, font=dict(color='#ffffff')),
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'))
        fig.update_xaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

        row = resultats[resultats['pays'] == pays_detail].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric('MAE SARIMA', f"{row['mae_final']:.2f}")
        with c2:
            st.metric('R2', f"{row['r2_final']:.3f}")
        with c3:
            st.metric('Demand actuel', f"{row['demand_dernier']:.1f}")
        with c4:
            variation = row['prevision_jan25'] - row['demand_dernier']
            st.metric('Prevision Jan 2025',
                      f"{row['prevision_jan25']:.1f}",
                      delta=f"{variation:+.1f}")

# ------------------------------------------------------------
# VUE 4 — RECOMMANDATION
# ------------------------------------------------------------
elif vue == 'Recommandation':
    st.title('Recommandation Metier')
    st.markdown('---')

    pays_hausse = ['France', 'Germany', 'Morocco', 'Italy', 'Portugal', 'Spain']
    pays_baisse = ['Japan', 'USA']
    resultats   = pd.DataFrame(ml_results['resultats'])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>Pays en hausse — Priorite haute</div>", unsafe_allow_html=True)
        for pays in pays_hausse:
            if pays not in pays_sel:
                continue
            row = resultats[resultats['pays'] == pays].iloc[0]
            variation = row['prevision_jan25'] - row['demand_dernier']
            st.markdown(f"""<div class="hausse-card">
                <strong>{pays}</strong> — {row['demand_dernier']:.1f} →
                <span class="val">{row['prevision_jan25']:.1f} (+{variation:.1f})</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-title'>Pays en baisse — Priorite basse</div>", unsafe_allow_html=True)
        for pays in pays_baisse:
            if pays not in pays_sel:
                continue
            row = resultats[resultats['pays'] == pays].iloc[0]
            variation = row['prevision_jan25'] - row['demand_dernier']
            st.markdown(f"""<div class="baisse-card">
                <strong>{pays}</strong> — {row['demand_dernier']:.1f} →
                <span class="val">{row['prevision_jan25']:.1f} ({variation:.1f})</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('---')
    st.markdown("<div class='section-title'>Top 5 destinations par pays</div>", unsafe_allow_html=True)

    pays_reco    = st.selectbox('Selectionner un pays', pays_sel)
    df_pays_reco = reco_f[reco_f['country'] == pays_reco].sort_values(
        'score_final', ascending=False
    ).head(5)

    if len(df_pays_reco) == 0:
        st.warning('Aucune recommandation disponible pour ce pays.')
    else:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_pays_reco['destination'],
            y=df_pays_reco['score_final'],
            marker_color=[
                C['green'] if f == 1 else C['blue']
                for f in df_pays_reco.get('flag_opportunite', [0]*len(df_pays_reco))
            ],
            text=df_pays_reco['score_final'].round(2),
            textposition='outside',
            textfont=dict(color='#ffffff')
        ))
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          showlegend=False,
                          margin=dict(l=10, r=10, t=10, b=10),
                          font=dict(color='#ffffff'))
        fig.update_xaxes(tickfont=dict(color='#ffffff'))
        fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
        st.plotly_chart(fig, use_container_width=True)

        cols_show = [c for c in [
            'destination', 'attractiveness', 'cost', 'rating',
            'weather', 'flight_price', 'score_promotion',
            'score_final', 'flag_opportunite'
        ] if c in df_pays_reco.columns]
        st.dataframe(df_pays_reco[cols_show].reset_index(drop=True),
                     use_container_width=True)

    st.markdown('---')
    st.markdown("<div class='section-title'>Score final — toutes destinations</div>", unsafe_allow_html=True)

    fig = px.scatter(reco_f, x='attractiveness', y='score_final',
                     color='country', size='cost',
                     hover_data=['destination'],
                     color_discrete_sequence=list(C.values()))
    fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=10, r=10, t=10, b=10),
                      font=dict(color='#1a1f36'),
                      legend=dict(orientation='h', y=-0.2, font=dict(color='#ffffff')))
    fig.update_xaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
    fig.update_yaxes(tickfont=dict(color='#ffffff'), gridcolor='#2d3748')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')
    st.markdown("<div class='section-title'>Pourquoi l'IA generative seule est insuffisante</div>",
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="piege-card">
            <strong>Donnees non structurees</strong><br>
            L'IA generative ne peut pas lire, nettoyer et croiser
            6 fichiers heterogenes avec des pieges intentionnels
            (separateurs, formats mixtes, incoherences).
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="piege-card">
            <strong>Modelisation temporelle</strong><br>
            SARIMA requiert un split chronologique strict,
            une optimisation des parametres par pays et une
            evaluation rigoureuse — impossible sans code.
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="piege-card">
            <strong>Decisions metier</strong><br>
            Les contraintes business (max 5 dest., meteo, budget)
            necessitent un raisonnement analytique que l'IA
            generative ne peut pas garantir sans donnees reelles.
        </div>""", unsafe_allow_html=True)