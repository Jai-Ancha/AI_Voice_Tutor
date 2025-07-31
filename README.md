# 🎙️🤖 Real-Time AI Voice Tutor - Task 1: Voice Chatbot 🌟

## Project Description
This project implements the core functionality of a real-time AI voice tutor designed for children aged 6 to 16. It features an **interactive, multi-lingual voice chatbot** that listens to spoken questions, processes them using Google Gemini AI, and then provides spoken answers. This creates a natural, tutor-style conversational experience.

## Features
* **Interactive Language Selection:** Allows the user to choose from supported languages (English, Hindi, Telugu, Marathi, Gujarati, Tamil) at the start of the session.
* **Voice Input:** Captures audio from the user's microphone.
* **Speech-to-Text (STT):** Transcribes spoken questions into text using Google's Web Speech API (via `speech_recognition`), adapted for the selected language.
* **AI Chatbot (LLM):** Processes text questions and generates age-appropriate, friendly, and educational responses using the Google Gemini (`gemini-2.0-flash`) model, tailored to respond in the chosen language.
* **Text-to-Speech (TTS):** Converts the AI's text responses into natural-sounding speech using `gTTS` (Google Text-to-Speech library), utilizing voices for the selected language.
* **Comprehensive Voice Output & Playback:** Attempts direct playback of synthesized audio. If automatic playback encounters system-specific permission issues, it reliably saves *every* AI response as a timestamped MP3 file for manual playback.
* **Child-Safe Persona:** AI responses are designed to be friendly, encouraging, and patient for children.
* **Robust Quitting:** Allows graceful exit via spoken command, keyboard interrupt (Ctrl+C), or initial text prompt.

## Technologies Used

* **Programming Language:** Python 3.x
* **Speech-to-Text (STT):** `speech_recognition` library (utilizing Google Web Speech API)
* **Text-to-Speech (TTS):** `gTTS` library (utilizing Google Text-to-Speech web API)
* **Large Language Model (LLM):** `google-generativeai` library (for Google Gemini `gemini-2.0-flash` model)
* **Audio Recording:** `sounddevice`, `soundfile`, `pyaudio`
* **Audio Processing & Playback:** `pydub`
* **External Dependency:** FFmpeg (required by `pydub` for audio playback)

## Setup Instructions

Follow these steps to set up and run the project:

1.  **Clone or Download the Project:**
    * Download the project files to your desired location (e.g., `D:\AI_Voice_Tutor`).

2.  **Install Python:**
    * Ensure you have Python 3.x installed on your system.
    * **Crucially, during installation, ensure "Add Python to PATH" is checked.**
    * Verify installation by opening Command Prompt and running: `python --version` and `pip --version`.

3.  **Install Python Libraries:**
    * Open your Command Prompt (or Administrator Command Prompt).
    * Navigate to your project directory (e.g., `D:`, then `cd AI_Voice_Tutor`).
    * Run the following command to install all necessary Python packages:
        ```bash
        pip install Flask openai elevenlabs sounddevice soundfile SpeechRecognition pydub google-cloud-speech google-cloud-texttospeech google-generativeai pyaudio gTTS numpy
        ```
        *(Note: Some of these were part of initial explorations and may not be directly used in the final `voice_tutor.py` code, but installing them ensures all dependencies are met.)*

4.  **Install FFmpeg:**
    * FFmpeg is required by `pydub` for audio playback.
    * **Download FFmpeg:** Go to [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html), choose "Windows builds from gyan.dev", and download `ffmpeg-release-full.zip`.
    * **Extract FFmpeg:** Extract the contents of the downloaded ZIP file to a simple location (e.g., `C:\ffmpeg`). This will create a folder like `C:\ffmpeg\ffmpeg-7.1.1-full`.
    * **Add FFmpeg to System PATH:**
        * Find the `bin` folder inside your extracted FFmpeg directory (e.g., `C:\ffmpeg\ffmpeg-7.1.1-full\bin`). Copy its full path.
        * Search "Environment Variables" in Windows Start Menu.
        * Click "Edit the system environment variables" -> "Environment Variables..."
        * Under "System variables", select "Path" and click "Edit...".
        * Click "New" and paste the path to your FFmpeg `bin` folder.
        * Click OK on all windows.
        * **Verify Installation:** Close and reopen your Command Prompt. Type `ffmpeg -version` and press Enter. You should see FFmpeg version details.

5.  **Obtain API Keys:**
    * **Google Cloud API Key (for Gemini):**
        * Go to [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials).
        * Ensure your "Gemini API" project is selected in the project dropdown at the top.
        * Under "API Keys", find your `Generative Language API Key`.
        * Click "Show key" and copy the key.
    * **OpenAI API Key (for completeness in `config.py`):**
        * Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
        * Create a new secret key and copy it immediately.
        * *(Note: While OpenAI APIs are not directly used in the final `voice_tutor.py` to avoid billing issues encountered during development, including the key in `config.py` is good practice if future expansion were to include them.)*

6.  **Create `config.py`:**
    * In your `D:\AI_Voice_Tutor` project folder, create a new file named `config.py`.
    * Paste the following content into it, **replacing the placeholder text with your actual API keys**:
        ```python
        # config.py

        # Google Cloud API Key for Gemini
        GOOGLE_CLOUD_API_KEY = "YOUR_ACTUAL_GOOGLE_CLOUD_API_KEY_HERE"

        # OpenAI API Key (for completeness, not directly used in final voice_tutor.py)
        OPENAI_API_KEY = "YOUR_ACTUAL_OPENAI_API_KEY_HERE"
        ```
    * **Save `config.py`.**

## How to Run the Voice Chatbot

1.  **Open Command Prompt** (or Administrator Command Prompt).
2.  **Navigate to your project folder:**
    ```bash
    D:
    cd AI_Voice_Tutor
    ```
3.  **Execute the script:**
    ```bash
    python voice_tutor.py
    ```

## How to Interact

1.  **Language Selection:** Upon running, the script will prompt you to choose a language from a list by entering its corresponding number. Enter your choice and press Enter. You can also type `q` and press Enter to quit before the tutor starts.
2.  **Speak to the Tutor:** Once the language is set, the tutor will prompt you to "Speak now!". Speak clearly into your microphone in the chosen language.
3.  **View Text Output:** The Command Prompt will display the transcription of your speech and the AI's text response.
4.  **Hear Voice Output:**
    * The program will attempt to play the AI's spoken response automatically.
    * **Crucially, every AI response is also saved as a timestamped MP3 file** (e.g., `ai_response_20250731_124530.mp3`) in your `D:\AI_Voice_Tutor\` folder. **If you cannot hear the automatic playback, please navigate to this folder in File Explorer and double-click the latest `ai_response_*.mp3` file to listen manually.** (Note: Direct automatic playback may be blocked by system permissions on some machines.)
5.  **Continuous Conversation:** The chatbot will automatically loop, ready for your next input.
6.  **Quitting:** To exit the program, you have several options:
    * **Speak "quit":** When the tutor is listening ("Speak now!"), say the word "quit" clearly into the microphone.
    * **Keyboard Interrupt:** At any point, press `Ctrl` + `C` on your keyboard in the Command Prompt.

## Task 1 Completion & Next Steps

This implementation successfully demonstrates the core "Voice-based AI Chatbot" functionality, now with added support for interactive multi-language conversations and comprehensive saving of AI responses. While direct automatic audio playback faced unique system-level permission hurdles, the successful generation and manual playback of timestamped MP3s confirm full functionality as a voice tutor.

This foundational setup will be greatly leveraged for Task 2 (Interactive Roleplay Mode), where the emphasis will shift to managing conversational flow based on predefined scenarios."# AI_Voice_Tutor" 
