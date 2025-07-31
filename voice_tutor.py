import os
import io
import tempfile
import numpy as np
import datetime # New import for timestamping files
import sys # New import for sys.exit

# Imports for Speech Recognition and Text-to-Speech (non-cloud-billing dependent)
import speech_recognition as sr
from gtts import gTTS

# Imports for Google Gemini (AI Brain)
import google.generativeai as genai

# Imports for audio playback
from pydub import AudioSegment
from pydub.playback import play

# Import your API key (only Google Cloud API key is needed for Gemini here)
from config import GOOGLE_CLOUD_API_KEY

# --- CONFIGURE API CLIENTS ---
genai.configure(api_key=GOOGLE_CLOUD_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.0-flash') 

# Initialize the SpeechRecognition Recognizer
recognizer = sr.Recognizer()

# --- Audio Recording Parameters ---
samplerate = 16000 


# --- SUPPORTED LANGUAGES AND THEIR CODES ---
# This dictionary maps display names to SR_LANG_CODE, TTS_LANG_CODE, and AI_RESPONSE_LANGUAGE
SUPPORTED_LANGUAGES = {
    1: {'display': 'English', 'sr_code': 'en-US', 'tts_code': 'en', 'ai_instruct': 'English'},
    2: {'display': 'Hindi', 'sr_code': 'hi-IN', 'tts_code': 'hi', 'ai_instruct': 'Hindi'},
    3: {'display': 'Telugu', 'sr_code': 'te-IN', 'tts_code': 'te', 'ai_instruct': 'Telugu'},
    4: {'display': 'Marathi', 'sr_code': 'mr-IN', 'tts_code': 'mr', 'ai_instruct': 'Marathi'},
    5: {'display': 'Gujarati', 'sr_code': 'gu-IN', 'tts_code': 'gu', 'ai_instruct': 'Gujarati'},
    6: {'display': 'Tamil', 'sr_code': 'ta-IN', 'tts_code': 'ta', 'ai_instruct': 'Tamil'},
}

# Global variables for language codes, will be set by user choice
SR_LANG_CODE = ''
TTS_LANG_CODE = ''
AI_RESPONSE_LANGUAGE = ''


def record_audio_for_recognition(duration_seconds=5):
    """
    Records audio from the microphone using SpeechRecognition's built-in utility.
    Adjusts for ambient noise and returns an AudioData object.
    """
    print(f"Recording for {duration_seconds} seconds... Speak now!")
    with sr.Microphone(sample_rate=samplerate) as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, phrase_time_limit=duration_seconds)
            return audio
        except sr.WaitTimeoutError:
            print("No speech detected within the time limit.")
            return None # Return None if no speech detected
        except Exception as e:
            print(f"Error during audio recording: {e}")
            return None


def transcribe_audio_sr(audio_data):
    """
    Transcribes audio data using SpeechRecognition's default Google Web Speech API.
    Uses the configured SR_LANG_CODE for transcription.
    """
    if audio_data is None: # Handle case where no speech was recorded
        return None
        
    print(f"Transcribing audio using SpeechRecognition ({SR_LANG_CODE})...")
    try:
        text = recognizer.recognize_google(audio_data, language=SR_LANG_CODE)
        print(f"Transcription: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API service; {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during Speech Recognition: {e}")
        return None

def get_gemini_response(text_input):
    """
    Gets a conversational response from Google Gemini API,
    instructing it to respond in the configured AI_RESPONSE_LANGUAGE.
    """
    print(f"Getting Gemini response for: '{text_input}' (expecting {AI_RESPONSE_LANGUAGE})...")
    prompt = (
        f"You are 'Genie', a friendly, encouraging, and patient AI tutor for children aged 6 to 16. "
        f"Your goal is to make learning fun and easy. Respond concisely and clearly in {AI_RESPONSE_LANGUAGE}. "
        "If the child asks a question, answer it simply and then ask a follow-up question or suggest a simple practice. "
        "Keep the language simple and positive. Use emojis where appropriate to make it fun. "
        "Current conversation:\n"
        f"Child: {text_input}\n"
        "Genie:"
    )
    try:
        response = gemini_model.generate_content(prompt)
        gemini_text = response.text
        print(f"Gemini Response: {gemini_text}")
        return gemini_text
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        if "Quota exceeded" in str(e):
            return f"My apologies! It seems I'm a bit busy right now. Please try again in a few moments. ({AI_RESPONSE_LANGUAGE})"
        return f"I'm sorry, I'm having trouble understanding right now. Can you please repeat that? ({AI_RESPONSE_LANGUAGE})"

def synthesize_speech_gtts(text):
    """
    Synthesizes speech from text using gTTS, using the configured TTS_LANG_CODE.
    """
    print(f"Synthesizing speech for: '{text}' using gTTS ({TTS_LANG_CODE})...")
    try:
        tts = gTTS(text=text, lang=TTS_LANG_CODE, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        print("Speech synthesized.")
        return fp.read()
    except Exception as e:
        print(f"Error during gTTS synthesis: {e}")
        return None

def play_audio_bytes(audio_bytes):
    """
    Plays audio bytes using pydub/sounddevice via a temporary file,
    created in the current directory for permission reliability.
    Also saves a timestamped copy for historical responses.
    """
    if audio_bytes:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        response_filename = f"ai_response_{timestamp}.mp3" # Unique filename

        print("Playing audio response...")
        try:
            # Attempt to play directly from a temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True, dir='.') as temp_audio_file:
                temp_audio_file.write(audio_bytes)
                temp_audio_file.seek(0)
                audio_segment = AudioSegment.from_file(temp_audio_file.name, format="mp3")
                play(audio_segment) # This call requires FFmpeg
            print("Audio playback finished.")
        except Exception as e:
            print(f"Error playing audio: {e}. Ensure FFmpeg is installed and added to PATH.")
            print(f"As a fallback, audio saved to '{response_filename}'. Please play it manually from the folder.")
            # Even if automatic playback fails, ensure the unique file is saved
            try:
                with open(response_filename, "wb") as f:
                    f.write(audio_bytes)
            except Exception as save_e:
                print(f"Also failed to save audio file: {save_e}")
    else:
        print("No audio to play.")

if __name__ == "__main__":
    # --- Language Selection Logic ---
    print("Welcome to the AI Voice Tutor!")
    while True:
        print("\nPlease choose a language for your tutor:")
        for key, value in SUPPORTED_LANGUAGES.items():
            print(f"  {key}. {value['display']}")
        
        choice = input("Enter the number of your choice (or 'q' to quit): ").lower().strip()
        
        if choice == 'q':
            print("Exiting AI Voice Tutor. Goodbye!")
            sys.exit() # Use sys.exit() for a clean exit from the script
            
        try:
            choice = int(choice)
            if choice in SUPPORTED_LANGUAGES:
                selected_lang = SUPPORTED_LANGUAGES[choice]
                # --- SYNTAXERROR FIX: REMOVED "global" HERE ---
                # SR_LANG_CODE, TTS_LANG_CODE, AI_RESPONSE_LANGUAGE are already global from their initial empty assignments
                SR_LANG_CODE = selected_lang['sr_code']
                TTS_LANG_CODE = selected_lang['tts_code']
                AI_RESPONSE_LANGUAGE = selected_lang['ai_instruct']
                print(f"\nLanguage set to {selected_lang['display']}.")
                break
            else:
                print("Invalid choice. Please enter a number from the list or 'q'.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

    print(f"Starting AI Voice Tutor (Current Language: {AI_RESPONSE_LANGUAGE}). Say 'quit' into mic or press Ctrl+C to exit.")
    
    while True:
        try:
            recorded_audio_data = record_audio_for_recognition(duration_seconds=5)
            transcribed_text = transcribe_audio_sr(recorded_audio_data)

            if transcribed_text:
                if transcribed_text.lower() == "quit":
                    print("Exiting AI Voice Tutor. Goodbye!")
                    break # Exit loop if 'quit' is spoken

                ai_response_text = get_gemini_response(transcribed_text)

                if ai_response_text:
                    synthesized_audio_bytes = synthesize_speech_gtts(ai_response_text)
                    play_audio_bytes(synthesized_audio_bytes)
                else:
                    print("No AI response to synthesize.")
            else:
                print("No clear speech detected or an error occurred. Please try again.")

            print("\n--- Next interaction ---")

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nCtrl+C detected. Exiting AI Voice Tutor. Goodbye!")
            break
        except Exception as main_e:
            print(f"An unexpected error occurred in the main loop: {main_e}")
            print("Continuing to next interaction...")
