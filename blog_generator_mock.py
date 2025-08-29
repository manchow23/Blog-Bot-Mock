import streamlit as st

# -------------------------
# Mock OpenAI client
# -------------------------
class MockChoice:
    def __init__(self, content):
        self.message = {"content": content}

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockOpenAIClient:
    class chat:
        class completions:
            @staticmethod
            def create(model, messages):
                user_message = next((m["content"] for m in messages if m["role"] == "user"), "")
                reply = f"Simulated paragraph about: '{user_message}'"
                return MockResponse(reply)

client = MockOpenAIClient()

# -------------------------
# Function to generate paragraph
# -------------------------
def generate_blog(paragraph_topic):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes blog paragraphs."},
            {"role": "user", "content": paragraph_topic}
        ]
    )
    return response.choices[0].message["content"].strip()

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="📝 BlogBot Studio", layout="wide")

# Header
st.markdown("<h1 style='color: #4CAF50;'>📝 BlogBot Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: grey;'>Enter a topic and get a simulated AI-written paragraph instantly!</p>", unsafe_allow_html=True)

# Input and button in columns
col1, col2 = st.columns([3, 1])
with col1:
    paragraph_topic = st.text_input("Enter a topic for your paragraph:", placeholder="e.g., Benefits of Meditation")
with col2:
    generate_btn = st.button("✨ Generate")

# Example topics
with st.expander("💡 Example Topics"):
    st.write("- The future of AI in healthcare")
    st.write("- How to start a successful blog")
    st.write("- Benefits of learning Python")
    st.write("- Travel tips for solo travelers")

# Generate paragraph
if generate_btn:
    if paragraph_topic:
        with st.spinner("Generating your paragraph... 🪄"):
            paragraph = generate_blog(paragraph_topic)
        st.success("Paragraph generated successfully!")
        st.markdown("### 🖋️ Generated Paragraph:")
        st.info(paragraph)
        st.download_button("📥 Download Paragraph", paragraph, file_name="blog_paragraph.txt")
    else:
        st.warning("⚠️ Please enter a topic first!")

