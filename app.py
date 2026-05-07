import streamlit as st
from components.avatar_component import get_avatar_html
from components.chatbot import render_chat_tab

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fashion AI Studio", page_icon="👗", layout="wide")

# --- (Keep your existing CSS markdown block here) ---

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align:center;'><h2>FASHION STUDIO</h2></div>", unsafe_allow_html=True)
    
    # 1. Hairstyle
    hairstyle = st.selectbox("Hairstyle", options=["bun", "long", "wavy"])

    # 2. NEW: Outfit Style Selection
    st.markdown("#### 👗 Outfit Style")
    outfit_style = st.selectbox(
        "Choose outfit type",
        options=["saree", "kurta", "western"],
        format_func=lambda x: {
            "saree": "🥻 Traditional Saree",
            "kurta": "🧥 Designer Kurta",
            "western": "👗 Evening Gown"
        }[x],
        label_visibility="collapsed"
    )

    # 3. Outfit Color
    st.markdown("#### 🎨 Outfit Color")
    outfit_color_name = st.selectbox("Color", options=["Rose Pink", "Royal Purple", "Emerald Green", "Deep Red"])
    outfit_color_map = {"Rose Pink": "#E91E8C", "Royal Purple": "#7B1FA2", "Emerald Green": "#1B5E20", "Deep Red": "#B71C1C"}
    outfit_color = outfit_color_map[outfit_color_name]

    # (Keep your other selectors: Skin Tone, Lip Color, etc.)

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["🧍 3D Fashion Avatar", "💬 Priya — Fashion AI"])

with tab1:
    # Pass the outfit_style to the component
    avatar_html = get_avatar_html(
        hairstyle=hairstyle,
        hair_color="#2C1810", # Example static or linked variable
        skin_tone="#FDECD0",   # Example static or linked variable
        outfit_style=outfit_style,  # <--- CRITICAL ADDITION
        outfit_color=outfit_color,
        lip_color="#C62828"    # Example static or linked variable
    )
    st.components.v1.html(avatar_html, height=620)

with tab2:
    render_chat_tab()
