from textblob import TextBlob
import streamlit as st
from deep_translator import GoogleTranslator
import json

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Sentiment Lab",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #111936 55%, #17142e 100%);
        color: #f5f7ff;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero {
        padding: 2.2rem 2.5rem;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(102, 78, 255, .28), rgba(25, 203, 255, .12));
        border: 1px solid rgba(255,255,255,.10);
        box-shadow: 0 20px 60px rgba(0,0,0,.25);
        margin-bottom: 1.5rem;
    }

    .eyebrow {
        color: #8be9ff;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .18em;
        text-transform: uppercase;
        margin-bottom: .5rem;
    }

    .hero h1 {
        font-size: 3.1rem;
        line-height: 1;
        margin: 0;
        background: linear-gradient(90deg, #ffffff, #8be9ff, #b79cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #b8c1dd;
        font-size: 1.05rem;
        margin-top: .9rem;
        max-width: 700px;
    }

    .info-card {
        background: rgba(255,255,255,.055);
        border: 1px solid rgba(255,255,255,.09);
        border-radius: 20px;
        padding: 1.2rem;
        height: 100%;
    }

    .info-title {
        font-size: .8rem;
        text-transform: uppercase;
        letter-spacing: .12em;
        color: #8be9ff;
        font-weight: 800;
        margin-bottom: .5rem;
    }

    .info-text {
        color: #cbd2e8;
        font-size: .92rem;
        line-height: 1.55;
    }

    .result-card {
        padding: 1.5rem;
        border-radius: 24px;
        background: rgba(255,255,255,.06);
        border: 1px solid rgba(255,255,255,.10);
        margin-top: 1rem;
    }

    .sentiment {
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: .4rem;
    }

    .positive { color: #58f5b0; }
    .negative { color: #ff718d; }
    .neutral { color: #8be9ff; }

    .small-label {
        color: #8993b2;
        font-size: .78rem;
        text-transform: uppercase;
        letter-spacing: .1em;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.045);
        border: 1px solid rgba(255,255,255,.08);
        padding: 1rem;
        border-radius: 18px;
    }

    .stTextInput input {
        background: rgba(255,255,255,.07) !important;
        color: white !important;
        border: 1px solid rgba(139,233,255,.25) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
    }

    .footer {
        text-align: center;
        color: #68718e;
        margin-top: 3rem;
        font-size: .8rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ANIMACIÓN LOTTIE
# ---------------------------------------------------------
def load_lottie_animation(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

lottie_animation = load_lottie_animation("Cute Mascot Jumping Character.json")

# ---------------------------------------------------------
# CABECERA
# ---------------------------------------------------------
col_title, col_animation = st.columns([2.2, 1])

with col_title:
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">TEXT ANALYSIS · SENTIMENT AI</div>
        <h1>Sentiment Lab</h1>
        <p>
            Explora la emoción detrás de un texto mediante
            <b>polaridad</b> y <b>subjetividad</b>.
            Escribe una frase y descubre cómo se comporta su lenguaje.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_animation:
    if lottie_animation:
        from streamlit_lottie import st_lottie
        st_lottie(lottie_animation, height=220, key="mascot")
    else:
        st.warning("No se encontró el archivo JSON de la animación.")

# ---------------------------------------------------------
# EXPLICACIÓN
# ---------------------------------------------------------
info1, info2 = st.columns(2)

with info1:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">Polaridad</div>
        <div class="info-text">
            Indica la orientación emocional del texto.
            Su valor va de <b>-1</b> a <b>1</b>:
            los valores negativos representan emociones negativas,
            mientras que los positivos representan emociones positivas.
        </div>
    </div>
    """, unsafe_allow_html=True)

with info2:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">Subjetividad</div>
        <div class="info-text">
            Mide cuánto contenido subjetivo existe en el texto.
            Va de <b>0</b> a <b>1</b>: 0 es completamente objetivo
            y 1 es completamente subjetivo.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# ANALIZADOR
# ---------------------------------------------------------
st.markdown("### ✦ Analiza una frase")

text = st.text_input(
    "Escribe el texto que deseas analizar:",
    placeholder="Ejemplo: Me encanta esta experiencia, es increíble..."
)

if text:

    try:
        trans_text = GoogleTranslator(
            source="es",
            target="en"
        ).translate(text)

        blob = TextBlob(trans_text)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        if polarity > 0:
            sentiment = "POSITIVO"
            css_class = "positive"
            description = "El texto presenta una orientación emocional favorable."

        elif polarity < 0:
            sentiment = "NEGATIVO"
            css_class = "negative"
            description = "El texto presenta una orientación emocional desfavorable."

        else:
            sentiment = "NEUTRAL"
            css_class = "neutral"
            description = "El texto no presenta una orientación emocional marcada."

        st.markdown(f"""
        <div class="result-card">
            <div class="small-label">Resultado del análisis</div>
            <div class="sentiment {css_class}">{sentiment}</div>
            <div style="color:#b8c1dd;">{description}</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric("Polaridad", polarity)
            st.progress((polarity + 1) / 2)

        with metric2:
            st.metric("Subjetividad", subjectivity)
            st.progress(subjectivity)

        with st.expander("Ver información técnica"):
            st.write("Texto original:", text)
            st.write("Texto traducido:", trans_text)
            st.write("Polaridad:", polarity)
            st.write("Subjetividad:", subjectivity)

    except Exception as error:
        st.error(
            "No fue posible analizar el texto. "
            "Verifica tu conexión a internet y vuelve a intentarlo."
        )

else:
    st.markdown("""
    <div style="
        margin-top:1rem;
        padding:2rem;
        text-align:center;
        border:1px dashed rgba(139,233,255,.2);
        border-radius:22px;
        color:#7f89a8;
    ">
        ✦ Escribe una frase arriba para comenzar el análisis.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------
st.markdown("""
<div class="footer">
    SENTIMENT LAB · TextBlob + Google Translate + Streamlit
</div>
""", unsafe_allow_html=True)
