# Learn-Vocabulary-in-Context
This small web app uses GPT-4o-mini to convert whatever you input into a mixed-language content and marks those words worth learning.
A free demo is here: https://fakeforeigner-jiayangguizi.streamlit.app/


## Overview

The Learn-Vocabulary-in-Context App is an interactive tool designed to help language learners practice and improve their skills. It uses AI-powered translation and language mixing to create custom learning content across multiple languages.

Key features:
- Support for multiple languages including English, Chinese, Spanish, French, German, Japanese, Korean
- AI-powered translation and language mixing
- Custom text input or pre-defined example sentences
- Interactive web interface built with Streamlit

The original motivation for this project is to develop a tool for creating datasets to improve the Whisper's ability to transcribe mixed-language speeches through fine-tuning.
Based on fine-tuned Whisper, We are also working on a meeting assisant product. It is still an on-going project.

Welcome to star and discuss!

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have a Python 3.7+ environment
- You have an OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/learn-vocabulary-in-context.git
   cd learn-vocabulary-in-context
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).

3. Use the app:
   - Select your primary language and target language
   - Choose to enter custom text or use an example sentence
   - Click "Convert" to generate mixed-language content

## Configuration

You can customize the supported languages and example sentences by editing the `config.json` file.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenAI for providing the AI models used in this project
- Streamlit for the web app framework

## Contact

If you have any questions or feedback, please open an issue on this GitHub repository.
