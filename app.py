# streamlit run mixed_language_app_openai.py
import streamlit as st
import openai
import re
import json
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load configuration
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# Get API key from environment variable
# API_KEY = os.getenv('OPEN_ROUTER_KEY')
API_KEY = st.secrets["OPEN_ROUTER_KEY"]
if not API_KEY:
    raise ValueError("OPEN_ROUTER_KEY environment variable is not set")

# Set up OpenAI client for OpenRouter
client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=API_KEY,
)
# Set default headers for OpenRouter
openai.default_headers = {
    "HTTP-Referer": "http://localhost:8501",  # Streamlit default port
}

def detect_language(text):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a language detection tool. Respond with only the language name."},
            {"role": "user", "content": f"Detect the language of this text: '{text}'. Respond with only the language name from this list: {', '.join(config['supported_languages'])}"}
        ],
        max_tokens=10,
        temperature=0,
    )
    return response.choices[0].message.content.strip()
    
def translate_text(text, target_language):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
            {"role": "user", "content": text}
        ],
        max_tokens=1000,
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()

def convert_to_mixed_language(input_text, primary_language, target_language):
    system_prompt = f"""You are a language learning assistant. Convert the input text from {primary_language} into a mixed-language content where important vocabulary or phrases are in the {target_language} language, surrounded by curly braces {{}}.

Rules:
1. Identify words or phrases that are valuable for language learners to focus on.
2. Convert ONLY these identified words/phrases to the {target_language}.
3. Surround the translated {target_language} words/phrases with curly braces {{}}.
4. Ensure that ALL content within curly braces {{}} is in the {target_language}.
5. Maintain the original sentence structure and grammar for non-translated parts.
6. The text outside the curly braces should remain in the original language.
7. Ensure the mixed output is still readable and understandable.

For example:
If the target language is Chinese and the input is "I love to eat apples", a correct output would be:
"I {{喜欢}} to eat {{苹果}}."

An incorrect output would be:
"I {{love}} to eat {{apples}}." (because the words inside braces are not translated)

Remember: Always translate the content inside the curly braces to the target language.
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ],
        max_tokens=1000,
        temperature=0.8,
    )
    
    mixed_language_output = response.choices[0].message.content.strip()
    return mixed_language_output

def post_process_output(mixed_output, primary_language, target_language):
    def translate_if_needed(match):
        content = match.group(1)
        detected_lang = detect_language(content)
        if detected_lang != target_language:
            return "{" + translate_text(content, target_language) + "}"
        return match.group(0)
    
    return re.sub(r'\{([^}]+)\}', translate_if_needed, mixed_output)

def main():
    st.title("Learn-Vocabulary-in-Context")
    """
    #### Click the [Convert] button and see the result!
    """
    # Language selection
    target_language = st.selectbox("Select the target language your are learning:", config['supported_languages'])
    primary_language = st.selectbox("Select context language:", [lang for lang in config['supported_languages'] if lang != target_language])
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["Example Sentences", "Custom Text"])

    if input_method == "Custom Text":
        input_text = st.text_area("Enter your text:", "")
    else:
        example_sentences = config['example_sentences'].get(primary_language, ["No examples available for this language."])
        input_text = st.selectbox("Choose an example sentence:", example_sentences)

    if st.button("Convert"):
        if input_text:
            detected_lang = detect_language(input_text)
            if detected_lang != primary_language:
                input_text = translate_text(input_text, primary_language)
                st.info(f"Input text has been translated to {primary_language}:")

            mixed_output = convert_to_mixed_language(input_text, primary_language, target_language)
            mixed_output = post_process_output(mixed_output, primary_language, target_language)
            st.subheader("Primary-Language Content:")
            st.write(input_text)
            st.subheader("Mixed-Language Output:")
            st.write(mixed_output)
        else:
            st.warning("Please enter some text or select an example sentence.")

    # Add a footer with the Venmo QR code
    st.markdown("---")
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
        <style>
            .github-link {
                text-decoration: none;
                color: #333;
                font-size: 1.2rem;
            }
            .github-link:hover {
                color: #0366d6;
            }
        </style>
    """, unsafe_allow_html=True)    
    col1, col2, col3 = st.columns(3)
    with col1:
    # Add GitHub link with icon
        st.markdown("""
            <a href="https://github.com/Wonderfon/Learn-Vocabulary-in-Context" target="_blank" class="github-link">
                <i class="fab fa-github"></i> Source Code
            </a>
        """, unsafe_allow_html=True)

        st.markdown("""
            <a href="https://github.com/Wonderfon
                    " target="_blank" class="github-link">
                <i class="fab fa-github"></i> My Github Profile
            </a>
        """, unsafe_allow_html=True)

        st.markdown("""
            <a href="https://notion-next-chi-eight-85.vercel.app/en?theme=simple
                    " target="_blank" class="github-link">
                 My Personal Website
            </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("###### Buy me an A100  -->_-->")

    with col3:
        st.image("venmo.png", width=150)

# run
if __name__ == "__main__":
    main()
