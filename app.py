import streamlit as st
from components.avatar_component import get_avatar_html
from components.chatbot import render_chat_tab

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fashion AI Studio",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import Google Font */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');

  /* Global */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* Hide Streamlit default elements */
  #MainMenu, footer, header { visibility: hidden; }

  /* Sidebar styling */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0D0D 0%, #1A1A2E 100%);
    border-right: 1px solid rgba(233,30,140,0.2);
  }

  section[data-testid="stSidebar"] * {
    color: #ffffff !important;
  }

  /* Selectbox & slider labels */
  .stSelectbox label, .stSlider label {
    color: #E91E8C !important;
    font-weight: 500;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
  }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
    background: #1A1A2E;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #aaa !important;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.95rem;
    padding: 8px 24px;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #E91E8C, #9C27B0) !important;
    color: white !important;
  }

  /* Quick starter buttons */
  .stButton button {
    background: rgba(233,30,140,0.12) !important;
    border: 1px solid rgba(233,30,140,0.35) !important;
    color: #E91E8C !important;
    border-radius: 20px !important;
    font-size: 0.75rem !important;
    padding: 4px 8px !important;
    transition: all 0.2s !important;
  }
  .stButton button:hover {
    background: rgba(233,30,140,0.3) !important;
    transform: scale(1.03) !important;
  }

  /* Chat messages */
  .stChatMessage {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    margin-bottom: 8px !important;
  }

  /* Chat input */
  .stChatInput textarea {
    background: #1A1A2E !important;
    border: 1px solid rgba(233,30,140,0.4) !important;
    border-radius: 12px !important;
    color: white !important;
  }

  /* Divider */
  hr { border-color: rgba(233,30,140,0.2) !important; }

  /* Color swatch display */
  .color-swatch {
    display: inline-block;
    width: 18px; height: 18px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.3);
    margin-right: 6px;
    vertical-align: middle;
  }
</style>
""", unsafe_allow_html=True)


# ─── SIDEBAR — AVATAR CONTROLS ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1rem 0;'>
        <div style='font-size:2.2rem;'>✨</div>
        <h2 style='color:#E91E8C; font-size:1.3rem; margin:0; letter-spacing:1px;'>
            FASHION STUDIO
        </h2>
        <p style='color:#666; font-size:0.75rem; margin:4px 0 0 0;'>
            3D Avatar Customizer
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Hairstyle ──────────────────────────────────────────────────────────
    st.markdown("#### 💇‍♀️ Hairstyle")
    hairstyle = st.selectbox(
        "Choose hairstyle",
        options=["bun", "long", "wavy"],
        format_func=lambda x: {
            "bun":  "🌸 Elegant Bun",
            "long": "💫 Long Straight",
            "wavy": "🌊 Wavy Bob"
        }[x],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Hair Color ─────────────────────────────────────────────────────────
    st.markdown("#### 🎨 Hair Color")
    hair_color_name = st.selectbox(
        "Choose hair color",
        options=["Jet Black", "Dark Brown", "Warm Chestnut",
                 "Auburn Red", "Deep Burgundy", "Midnight Blue"],
        label_visibility="collapsed"
    )
    hair_color_map = {
        "Jet Black":      "#0A0A0A",
        "Dark Brown":     "#2C1810",
        "Warm Chestnut":  "#6B2D0E",
        "Auburn Red":     "#8B2500",
        "Deep Burgundy":  "#4A0010",
        "Midnight Blue":  "#0D1B4B"
    }
    hair_color = hair_color_map[hair_color_name]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skin Tone ──────────────────────────────────────────────────────────
    st.markdown("#### 🌸 Skin Tone")
    skin_tone_name = st.selectbox(
        "Choose skin tone",
        options=["Fair Porcelain", "Warm Ivory", "Golden Wheatish",
                 "Warm Caramel", "Deep Mocha", "Rich Ebony"],
        label_visibility="collapsed"
    )
    skin_tone_map = {
        "Fair Porcelain":  "#FDECD0",
        "Warm Ivory":      "#F5CBA7",
        "Golden Wheatish": "#D4A76A",
        "Warm Caramel":    "#C68642",
        "Deep Mocha":      "#8D5524",
        "Rich Ebony":      "#4A2912"
    }
    skin_tone = skin_tone_map[skin_tone_name]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Outfit Color ───────────────────────────────────────────────────────
    st.markdown("#### 👗 Saree / Outfit Color")
    outfit_color_name = st.selectbox(
        "Choose outfit color",
        options=["Rose Pink", "Royal Purple", "Emerald Green",
                 "Deep Red", "Sapphire Blue", "Marigold Gold",
                 "Coral Orange", "Midnight Teal"],
        label_visibility="collapsed"
    )
    outfit_color_map = {
        "Rose Pink":      "#E91E8C",
        "Royal Purple":   "#7B1FA2",
        "Emerald Green":  "#1B5E20",
        "Deep Red":       "#B71C1C",
        "Sapphire Blue":  "#0D47A1",
        "Marigold Gold":  "#F57F17",
        "Coral Orange":   "#E64A19",
        "Midnight Teal":  "#004D40"
    }
    outfit_color = outfit_color_map[outfit_color_name]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Lip Color ──────────────────────────────────────────────────────────
    st.markdown("#### 💄 Lip Color")
    lip_color_name = st.selectbox(
        "Choose lip color",
        options=["Classic Red", "Deep Berry", "Nude Pink",
                 "Coral", "Plum", "Rose Gold"],
        label_visibility="collapsed"
    )
    lip_color_map = {
        "Classic Red":  "#C62828",
        "Deep Berry":   "#6A1B4D",
        "Nude Pink":    "#C48B7A",
        "Coral":        "#E64A19",
        "Plum":         "#4A148C",
        "Rose Gold":    "#C2748A"
    }
    lip_color = lip_color_map[lip_color_name]

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── Info Card ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:rgba(233,30,140,0.08); border:1px solid rgba(233,30,140,0.25);
                border-radius:10px; padding:12px; font-size:0.78rem; color:#ccc;'>
        <strong style='color:#E91E8C;'>Current Look</strong><br><br>
        💇 {hairstyle.title()} · {hair_color_name}<br>
        🌸 {skin_tone_name}<br>
        👗 {outfit_color_name}<br>
        💄 {lip_color_name}
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN HEADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:0.5rem 0 1rem 0;'>
    <h1 style='font-family:"Playfair Display",serif;
               background:linear-gradient(90deg,#E91E8C,#9C27B0,#E91E8C);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;
               font-size:2.6rem; margin:0; letter-spacing:2px;'>
        Fashion AI Studio
    </h1>
    <p style='color:#888; font-size:0.88rem; letter-spacing:3px; margin:4px 0 0 0;'>
        3D AVATAR  ·  STYLE AI  ·  FASHION TECH
    </p>
</div>
""", unsafe_allow_html=True)


# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🧍 3D Fashion Avatar", "💬 Priya — Fashion AI"])


# ── TAB 1: 3D AVATAR ─────────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <p style='text-align:center; color:#888; font-size:0.82rem; margin-bottom:8px;'>
        🖱️ Drag to rotate · Customize using the sidebar · 📸 Screenshot to save
    </p>
    """, unsafe_allow_html=True)

    avatar_html = get_avatar_html(
        hairstyle=hairstyle,
        hair_color=hair_color,
        skin_tone=skin_tone,
        outfit_color=outfit_color,
        lip_color=lip_color
    )

    st.components.v1.html(avatar_html, height=620, scrolling=False)

    st.markdown("<br>", unsafe_allow_html=True)

    # Export info
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='background:rgba(255,215,0,0.06); border:1px solid rgba(255,215,0,0.2);
                    border-radius:10px; padding:12px; text-align:center; color:#ccc; font-size:0.82rem;'>
            💡 Use the <strong style='color:#FFD700;'>📸 Screenshot</strong> button inside
            the 3D canvas to export your avatar as a PNG image
        </div>
        """, unsafe_allow_html=True)


# ── TAB 2: CHATBOT ───────────────────────────────────────────────────────────
with tab2:
    render_chat_tab()