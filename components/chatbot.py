import streamlit as st
from groq import Groq

SYSTEM_PROMPT = """You are Priya 👗, an elite AI fashion consultant specializing 
in Indian ethnic wear — sarees, blouses, lehengas, dupattas and accessories.

Your expertise includes:
- Saree styles: Banarasi, Kanjivaram, Chiffon, Georgette, Silk, Cotton, Linen
- Blouse designs: Backless, Boat neck, Halter, Off-shoulder, Puff sleeve, Mirror work
- Occasion-based styling: Bridal, Festive, Casual, Office, Party, Reception
- Color theory: Skin tone matching, seasonal palettes, contrasts
- Accessories: Jewelry, footwear, handbags, bindis, bangles

Guidelines:
- Be warm, stylish, and conversational
- Give specific, actionable recommendations
- Ask clarifying questions about occasion, skin tone, or preferences when needed
- Use emojis occasionally to keep it lively
- Keep responses concise but helpful (3–5 sentences max unless asked for more)
- If asked about non-fashion topics, gently redirect to your expertise"""


def initialize_chat():
    """Initialize chat session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_initialized" not in st.session_state:
        st.session_state.chat_initialized = True


def get_groq_response(user_message: str) -> str:
    """
    Send message history to Groq and stream the response.
    Returns the full response string.
    """
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        # Build full message history for context
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += st.session_state.messages
        messages.append({"role": "user", "content": user_message})

        # Streaming response
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.75,
            max_tokens=512,
            stream=True
        )

        full_response = ""
        response_placeholder = st.empty()

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                response_placeholder.markdown(
                    f"<div class='chat-bubble assistant'>{full_response}▌</div>",
                    unsafe_allow_html=True
                )

        # Final render without cursor
        response_placeholder.markdown(
            f"<div class='chat-bubble assistant'>{full_response}</div>",
            unsafe_allow_html=True
        )

        return full_response

    except Exception as e:
        error_msg = f"⚠️ Connection issue: {str(e)}"
        st.error(error_msg)
        return error_msg


def render_chat_tab():
    """Render the full chatbot tab UI."""
    initialize_chat()

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
        <h2 style='color:#E91E8C; font-size:2rem; margin:0;'>👗 Priya — Fashion AI</h2>
        <p style='color:#aaa; font-size:0.9rem; margin:0;'>
            Your personal Indian ethnic wear stylist
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Quick Starter Chips ──────────────────────────────────────────────────
    st.markdown("<p style='color:#ccc; font-size:0.82rem;'>✨ Quick starters:</p>",
                unsafe_allow_html=True)

    starters = [
        "Saree for a wedding?",
        "Best colors for wheatish skin?",
        "Bridal blouse designs?",
        "Casual cotton saree ideas?",
        "Lehenga vs saree for reception?"
    ]

    cols = st.columns(len(starters))
    for i, starter in enumerate(starters):
        with cols[i]:
            if st.button(starter, key=f"starter_{i}", use_container_width=True):
                _process_message(starter)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat History ─────────────────────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style='text-align:center; padding:3rem; color:#666;'>
                <div style='font-size:3rem;'>👗</div>
                <p style='margin-top:0.5rem;'>Namaste! I'm Priya, your fashion AI.<br>
                Ask me anything about sarees, blouses, or ethnic styling!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="🧑"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="👗"):
                        st.markdown(msg["content"])

    # ── Chat Input ───────────────────────────────────────────────────────────
    if user_input := st.chat_input("Ask Priya about sarees, blouses, styling..."):
        _process_message(user_input)

    # ── Clear Chat ───────────────────────────────────────────────────────────
    if st.session_state.messages:
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def _process_message(user_input: str):
    """Add user message, get response, update state, rerun."""
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message immediately
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Get and display assistant response
    with st.chat_message("assistant", avatar="👗"):
        response = get_groq_response(user_input)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()