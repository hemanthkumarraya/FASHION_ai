# app.py
import streamlit as st
import streamlit.components.v1 as components
from avatar_3d import get_avatar_html  # Import the function

st.set_page_config(
    page_title="Fashion AI - 3D Avatar",
    page_icon="👗",
    layout="wide"
)

st.title("🎨 Photorealistic 3D Saree Avatar")

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Avatar Customization")
    
    st.subheader("Colors")
    saree_color = st.color_picker("Saree Color", "#D32F2F", key="saree")
    blouse_color = st.color_picker("Blouse Color", "#C62828", key="blouse")
    border_color = st.color_picker("Border/Zari Color", "#FFD700", key="border")
    
    st.subheader("Skin & Hair")
    skin_tone = st.color_picker("Skin Tone", "#D4A373", key="skin")
    hair_color = st.color_picker("Hair Color", "#1a1a1a", key="hair")
    lip_color = st.color_picker("Lip Color", "#C13C3C", key="lips")
    
    st.subheader("Style")
    hairstyle = st.selectbox(
        "Hairstyle",
        ["long_braid", "bun", "wavy"],
        index=0
    )
    
    pose = st.selectbox(
        "Pose",
        ["dance_pose", "standing", "namaste"],
        index=0
    )

# Main area
col1, col2 = st.columns([3, 1])

with col1:
    st.info("🖱️ **Drag** to rotate • 📸 **Click button** to capture screenshot")
    
    # Generate and display avatar
    try:
        avatar_html = get_avatar_html(
            hairstyle=hairstyle,
            hair_color=hair_color,
            skin_tone=skin_tone,
            saree_color=saree_color,
            blouse_color=blouse_color,
            border_color=border_color,
            lip_color=lip_color,
            pose=pose
        )
        
        components.html(avatar_html, height=700, scrolling=False)
        
    except Exception as e:
        st.error(f"Error rendering avatar: {str(e)}")
        st.exception(e)

with col2:
    st.subheader("📋 Current Settings")
    st.json({
        "hairstyle": hairstyle,
        "pose": pose,
        "saree_color": saree_color,
        "blouse_color": blouse_color,
        "border_color": border_color,
        "skin_tone": skin_tone,
        "hair_color": hair_color,
        "lip_color": lip_color
    })
    
    st.markdown("---")
    st.subheader("💡 Tips")
    st.markdown("""
    - **Drag** avatar to rotate
    - **Auto-rotate** toggles on button click
    - **Screenshot** saves PNG to downloads
    - Try different color combinations!
    """)
