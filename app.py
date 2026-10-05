import streamlit as st

from backend.rag_engine import PrerequisiteFinder
from backend.whisper_service import transcribe_audio


# -------------------------------
# Streamlit Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Prerequisite Finder",
    page_icon="🎓",
    layout="wide"
)


# -------------------------------
# Application Title
# -------------------------------

st.title("🎓 AI Prerequisite Finder for Learning")

st.caption(
    "Find the concepts you should learn before starting "
    "a new Data Science or AI topic."
)


# -------------------------------
# Load AI Prerequisite Finder
# -------------------------------

@st.cache_resource
def load_finder():
    return PrerequisiteFinder()


finder = load_finder()


# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:

    st.header("📚 Learning Settings")

    st.write(
        "Enter a topic and let the AI identify "
        "the prerequisites you should learn first."
    )

    st.info(
        "Examples:\n"
        "• Random Forest\n"
        "• Transformers\n"
        "• CNN\n"
        "• Pandas\n"
        "• RAG"
    )

    st.markdown("### 🎙️ Voice Input")

    audio = st.file_uploader(
        "Upload an audio question",
        type=["wav", "mp3", "m4a", "ogg"]
    )

    if audio:

        if st.button("🎤 Transcribe Audio"):

            with st.spinner("Transcribing audio..."):

                try:

                    text = transcribe_audio(audio)

                    st.session_state["topic"] = text

                    st.success("Transcription completed!")

                except Exception as e:

                    st.error(
                        f"Whisper error: {e}"
                    )


# -------------------------------
# Topic Input
# -------------------------------

topic = st.text_input(
    "🔎 What do you want to learn?",
    value=st.session_state.get("topic", ""),
    placeholder="Example: Machine Learning"
)


# -------------------------------
# Find Prerequisites
# -------------------------------

if st.button(
    "🚀 Find Prerequisites",
    type="primary"
):

    if not topic.strip():

        st.warning(
            "Please enter a topic."
        )

    else:

        with st.spinner(
            "AI is finding your learning prerequisites..."
        ):

            try:

                result = finder.find_prerequisites(
                    topic.strip()
                )

                st.session_state["result"] = result

            except Exception as e:

                st.error(
                    "Could not generate the result.\n\n"
                    "Make sure Ollama is running and "
                    "Llama 3.2 is installed.\n\n"
                    f"Error: {e}"
                )


# -------------------------------
# Display Result
# -------------------------------

if "result" in st.session_state:

    st.divider()

    st.subheader(
        "🧭 Your Learning Roadmap"
    )

    st.markdown(
        st.session_state["result"]
    )


# -------------------------------
# Footer
# -------------------------------

st.divider()

st.markdown(
    """
    💡 **How it works**

    Your topic → ChromaDB retrieves related knowledge →
    LangChain prepares the prompt → Ollama generates
    a personalized prerequisite roadmap.
    """
)