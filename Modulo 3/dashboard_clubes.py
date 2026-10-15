import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# Configuração da página
# ============================================================
st.set_page_config(
    page_title="Dashboard Brasileirão - Clubes 2008-2017",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# Carregamento e limpeza dos dados (adaptado ao seu CSV)
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("Tabela_Clubes.csv")

    # Remove a coluna de índice se existir (Unnamed: 0)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Garante que ficamos só com as 13 colunas relevantes
    colunas_esperadas = [
        "Ano", "Pos.", "Clubes", "Vitorias", "Derrotas", "Empates",
        "GolsF/S", "Saldo", "Qtd_Jogadores", "Idade_Media",
        "Estrangeiros", "Valor_total", "Media_Valor"
    ]
    colunas_existentes = [c for c in colunas_esperadas if c in df.columns]
    df = df[colunas_existentes]

    # Converter Idade_Media (vírgula → ponto)
    df["Idade_Media"] = (
        df["Idade_Media"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )

    # Separar Gols Pró e Gols Contra
    gols = df["GolsF/S"].str.split(":", expand=True)
    df["Gols_Pro"] = gols[0].astype(int)
    df["Gols_Contra"] = gols[1].astype(int)

    # Pontos aproximados (3*V + E)
    df["Pontos"] = 3 * df["Vitorias"] + df["Empates"]

    # Valor em milhões
    df["Valor_total_mi"] = df["Valor_total"] / 1_000_000
    df["Media_Valor_mi"] = df["Media_Valor"] / 1_000_000

    return df


df = load_data()


# ============================================================
# Sidebar - Filtros
# ============================================================
st.sidebar.title("⚽ Filtros")
st.sidebar.markdown("---")

anos = sorted(df["Ano"].unique())
ano_sel = st.sidebar.multiselect("Ano(s)", anos, default=anos)

clubes = sorted(df["Clubes"].unique())
clube_sel = st.sidebar.multiselect("Clube(s)", clubes, default=[])

# Aplicar filtros
df_f = df[df["Ano"].isin(ano_sel)]
if clube_sel:
    df_f = df_f[df_f["Clubes"].isin(clube_sel)]

st.sidebar.markdown("---")
st.sidebar.info(
    f"**Registros filtrados:** {len(df_f)}\n\n"
    "Dados do Campeonato Brasileiro Série A (2008–2017)."
)


# ============================================================
# Header + KPIs
# ============================================================
st.markdown(
    '<p class="main-header">⚽ Dashboard Brasileirão – Clubes</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Visualização interativa com Plotly Express | 2008 – 2017</p>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Clubes únicos", df_f["Clubes"].nunique())
with col2:
    st.metric("Temporadas", df_f["Ano"].nunique())
with col3:
    st.metric("Média Vitórias", f"{df_f['Vitorias'].mean():.1f}")
with col4:
    st.metric("Valor Médio (M€)", f"{df_f['Valor_total_mi'].mean():.1f}")
with col5:
    st.metric("Idade Média", f"{df_f['Idade_Media'].mean():.1f} anos")

st.markdown("---")


# ============================================================
# Abas
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visão Geral",
    "🏆 Ranking & Posição",
    "💰 Valor de Mercado",
    "📈 Desempenho por Clube",
    "📋 Dados Brutos"
])


# ---------- TAB 1: Visão Geral ----------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribuição de Vitórias por Ano")
        fig = px.box(
            df_f,
            x="Ano",
            y="Vitorias",
            color="Ano",
            points="all",
            title="Boxplot de Vitórias",
            labels={"Vitorias": "Vitórias", "Ano": "Ano"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Saldo de Gols por Ano")
        fig = px.violin(
            df_f,
            x="Ano",
            y="Saldo",
            box=True,
            points="all",
            title="Distribuição do Saldo de Gols",
            labels={"Saldo": "Saldo de Gols"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Relação: Vitórias × Saldo de Gols")
    fig = px.scatter(
        df_f,
        x="Vitorias",
        y="Saldo",
        color="Ano",
        size="Valor_total_mi",
        hover_name="Clubes",
        hover_data=["Pos.", "Pontos", "Idade_Media"],
        title="Vitórias vs Saldo (tamanho = Valor de Mercado)",
        labels={"Vitorias": "Vitórias", "Saldo": "Saldo de Gols"},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Mapa de calor – Média de Pontos por Clube e Ano")
    pivot = df_f.pivot_table(
        index="Clubes", columns="Ano", values="Pontos", aggfunc="mean"
    )
    fig = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="YlGnBu",
        title="Pontos médios (3×V + E)",
        labels=dict(color="Pontos"),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------- TAB 2: Ranking ----------
with tab2:
    st.subheader("Posição Final por Temporada")
    fig = px.line(
        df_f.sort_values(["Ano", "Pos."]),
        x="Ano",
        y="Pos.",
        color="Clubes",
        markers=True,
        title="Evolução da Posição (1 = Campeão)",
        labels={"Pos.": "Posição", "Ano": "Ano"},
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 Clubes – Mais Títulos (Pos. 1)")
        titulos = (
            df_f[df_f["Pos."] == 1]
            .groupby("Clubes")
            .size()
            .reset_index(name="Títulos")
            .sort_values("Títulos", ascending=False)
            .head(10)
        )
        if not titulos.empty:
            fig = px.bar(
                titulos,
                x="Clubes",
                y="Títulos",
                color="Títulos",
                color_continuous_scale="Greens",
                text="Títulos",
            )
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum título encontrado com os filtros atuais.")

    with c2:
        st.subheader("Clubes que mais ficaram no G4 (Pos. ≤ 4)")
        g4 = (
            df_f[df_f["Pos."] <= 4]
            .groupby("Clubes")
            .size()
            .reset_index(name="Vezes no G4")
            .sort_values("Vezes no G4", ascending=False)
            .head(10)
        )
        if not g4.empty:
            fig = px.bar(
                g4,
                x="Clubes",
                y="Vezes no G4",
                color="Vezes no G4",
                color_continuous_scale="Blues",
                text="Vezes no G4",
            )
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum clube no G4 com os filtros atuais.")

    st.subheader("Distribuição de Posições (Histograma)")
    fig = px.histogram(
        df_f,
        x="Pos.",
        nbins=20,
        color_discrete_sequence=["#636EFA"],
        title="Frequência de cada posição final",
        labels={"Pos.": "Posição"},
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------- TAB 3: Valor de Mercado ----------
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Evolução do Valor Total de Mercado")
        valor_ano = df_f.groupby("Ano")["Valor_total_mi"].mean().reset_index()
        fig = px.area(
            valor_ano,
            x="Ano",
            y="Valor_total_mi",
            title="Valor médio dos elencos (M€)",
            labels={"Valor_total_mi": "Valor (M€)"},
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Valor vs Posição")
        fig = px.scatter(
            df_f,
            x="Valor_total_mi",
            y="Pos.",
            color="Ano",
            hover_name="Clubes",
            size="Qtd_Jogadores",
            title="Valor de Mercado × Posição Final",
            labels={"Valor_total_mi": "Valor (M€)", "Pos.": "Posição"},
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 15 Clubes por Valor Médio de Mercado")
    top_valor = (
        df_f.groupby("Clubes")["Valor_total_mi"]
        .mean()
        .reset_index()
        .sort_values("Valor_total_mi", ascending=False)
        .head(15)
    )
    fig = px.bar(
        top_valor,
        x="Valor_total_mi",
        y="Clubes",
        orientation="h",
        color="Valor_total_mi",
        color_continuous_scale="Viridis",
        text=top_valor["Valor_total_mi"].round(1),
        title="Valor médio do elenco (M€)",
        labels={"Valor_total_mi": "Valor (M€)"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Correlação: Valor × Desempenho")
    corr_cols = [
        "Valor_total_mi", "Vitorias", "Saldo", "Pos.",
        "Idade_Media", "Estrangeiros"
    ]
    corr = df_f[corr_cols].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Matriz de Correlação",
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------- TAB 4: Por Clube ----------
with tab4:
    lista_clubes = sorted(df["Clubes"].unique())
    indice_padrao = (
        lista_clubes.index("Flamengo")
        if "Flamengo" in lista_clubes
        else 0
    )
    clube_unico = st.selectbox(
        "Selecione um clube para análise detalhada",
        lista_clubes,
        index=indice_padrao,
    )
    df_clube = df[df["Clubes"] == clube_unico].sort_values("Ano")

    if len(df_clube) == 0:
        st.warning("Nenhum dado para o clube selecionado com os filtros atuais.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Temporadas", len(df_clube))
        with c2:
            st.metric("Melhor posição", int(df_clube["Pos."].min()))
        with c3:
            st.metric("Média de vitórias", f"{df_clube['Vitorias'].mean():.1f}")
        with c4:
            st.metric("Valor médio (M€)", f"{df_clube['Valor_total_mi'].mean():.1f}")

        g1, g2 = st.columns(2)
        with g1:
            st.subheader("Posição por temporada")
            fig = px.line(
                df_clube,
                x="Ano",
                y="Pos.",
                markers=True,
                title=f"{clube_unico} – posição final (1 = Campeão)",
                labels={"Pos.": "Posição"},
            )
            fig.update_yaxes(autorange="reversed")
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            st.subheader("Vitórias, empates e derrotas")
            resultados = df_clube.melt(
                id_vars="Ano",
                value_vars=["Vitorias", "Empates", "Derrotas"],
                var_name="Resultado",
                value_name="Jogos",
            )
            fig = px.bar(
                resultados,
                x="Ano",
                y="Jogos",
                color="Resultado",
                barmode="stack",
                color_discrete_map={
                    "Vitorias": "#2ca02c",
                    "Empates": "#7f7f7f",
                    "Derrotas": "#d62728",
                },
                title=f"{clube_unico} – campanha por ano",
            )
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)

        g3, g4 = st.columns(2)
        with g3:
            st.subheader("Gols pró × contra")
            gols_long = df_clube.melt(
                id_vars="Ano",
                value_vars=["Gols_Pro", "Gols_Contra"],
                var_name="Tipo",
                value_name="Gols",
            )
            fig = px.line(
                gols_long,
                x="Ano",
                y="Gols",
                color="Tipo",
                markers=True,
                title=f"{clube_unico} – gols marcados e sofridos",
            )
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)

        with g4:
            st.subheader("Valor de mercado do elenco")
            fig = px.bar(
                df_clube,
                x="Ano",
                y="Valor_total_mi",
                text=df_clube["Valor_total_mi"].round(1),
                title=f"{clube_unico} – valor do elenco (M€)",
                labels={"Valor_total_mi": "Valor (M€)"},
            )
            fig.update_traces(textposition="outside")
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Tabela do clube")
        st.dataframe(
            df_clube.drop(columns=["Valor_total_mi", "Media_Valor_mi"]),
            use_container_width=True,
            hide_index=True,
        )


# ---------- TAB 5: Dados Brutos ----------
with tab5:
    st.subheader("Dados filtrados")
    st.dataframe(df_f, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Baixar dados filtrados (CSV)",
        data=df_f.to_csv(index=False).encode("utf-8"),
        file_name="clubes_filtrados.csv",
        mime="text/csv",
    )

    st.subheader("Estatísticas descritivas")
    st.dataframe(
        df_f[["Vitorias", "Derrotas", "Empates", "Saldo", "Qtd_Jogadores",
              "Idade_Media", "Estrangeiros", "Valor_total_mi"]].describe().T,
        use_container_width=True,
    )