import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.animation import Animation
import asyncio
import edge_tts
import playsound
import speech_recognition as sr
import csv
import os
import re

kivy.require('2.0.0')

# ---------------------------
# 🔹 Register Tamil Font
# ---------------------------
FONT_PATH = "C:\\Users\\vnrth\\Downloads\\NotoSansTamil-VariableFont_wdth,wght.ttf"
if os.path.exists(FONT_PATH):
    LabelBase.register(name="TamilFont", fn_regular=FONT_PATH)
else:
    print("⚠ Tamil Font Not Found!")

# ---------------------------
# 🔹 Language Selection
# ---------------------------
LANGUAGES = {"Tamil": "ta-IN", "English": "en-US"}
selected_language = "Tamil"

def set_language(lang):
    global selected_language
    selected_language = lang

# ---------------------------
# 🔹 TTS: Convert text to speech
# ---------------------------
async def speak_text(text):
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")
    tts = edge_tts.Communicate(text, voice="ta-IN-ValluvarNeural" if selected_language == "Tamil" else "en-US-JennyNeural")
    await tts.save("output.mp3")
    playsound.playsound("output.mp3")

def speak(prompt):
    asyncio.run(speak_text(prompt))

# ---------------------------
# 🔹 Speech Recognition
# ---------------------------
def listen(prompt):
    speak(prompt)
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
                text = r.recognize_google(audio, language=LANGUAGES[selected_language])
                return text
            except sr.UnknownValueError:
                speak("மன்னிக்கவும், நான் புரிந்துகொள்ளவில்லை. மீண்டும் சொல்லவும்." if selected_language == "Tamil" else "Sorry, I didn't catch that. Please say it again.")
            except sr.RequestError:
                speak("சேவையகத்துடன் தொடர்பு கொள்ள முடியவில்லை." if selected_language == "Tamil" else "Unable to reach the service.")
            except Exception as e:
                print("Speech recognition error:", e)
                return ""

# ---------------------------
# 🔹 Regular Expressions for Validation
# ---------------------------
FIELD_PATTERNS_TAMIL = {
    "பெயர்": (r'^[\u0B80-\u0BFF\s]+$', "⚠️ பெயர் தவறாக உள்ளது. மீண்டும் சொல்லவும்."),
    "வயது": (r'^\d{1,3}$', "⚠️ வயது 1 முதல் 3 இலக்கங்கள் வரை இருக்க வேண்டும்."),
    "பாலினம்": (r'^(ஆண்|பெண்|பிற)$', "⚠️ பாலினம் 'ஆண்', 'பெண்' அல்லது 'பிற' ஆக இருக்க வேண்டும்."),
    "முகவரி": (r'^[\u0B80-\u0BFF\s,0-9]+$', "⚠️ முகவரி தவறாக உள்ளது. சரியாக உள்ளிடவும்."),
    "தொலைபேசி": (r'^\d{10}$', "⚠️ தொலைபேசி எண் 10 இலக்கங்கள் இருக்க வேண்டும்."),
    "மின்னஞ்சல்": (r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$', "⚠️ சரியான மின்னஞ்சல் (example@mail.com) வழங்கவும்.")
}

FIELD_PATTERNS_ENGLISH = {
    "Name": (r'^[A-Za-z\s]+$', "Invalid name! Please try again."),
    "Age": (r'^\d{1,3}$', "Invalid age! Please enter 1 to 3 digits."),
    "Gender": (r'^(male|female|other)$', "Invalid gender! Choose Male, Female, or Other."),
    "Address": (r'^[A-Za-z0-9\s,]+$', "Invalid address! Please enter a valid address."),
    "Phone": (r'^\d{10}$', "Invalid phone number! Enter a 10-digit number."),
    "Email": (r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$', "Invalid email! Enter a valid email address.")
}

def get_field_input(field_name):
    field_patterns = FIELD_PATTERNS_TAMIL if selected_language == "Tamil" else FIELD_PATTERNS_ENGLISH
    pattern, warning_message = field_patterns[field_name]
    
    while True:
        # Listen for the input
        user_input = listen(f"{field_name} சொல்லவும்:" if selected_language == "Tamil" else f"Please say your {field_name}.")
        
        # Normalize the input for case insensitivity and stripping extra spaces
        normalized_input = user_input.strip().lower()
        
        if re.match(pattern, normalized_input):
            return user_input
        else:
            speak(warning_message)

# ---------------------------
# 🔹 Save Form Data to CSV
# ---------------------------
def save_to_csv(data, filename="form_data.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# ---------------------------
# 🔹 Kivy App
# ---------------------------
class VoiceAssistantApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        
        # Title Label
        self.title_label = Label(text="Voice Assistant", font_size=30, bold=True, color=(0, 0, 0, 1))
        layout.add_widget(self.title_label)
        
        # Language Buttons
        self.tamil_button = Button(text="தமிழ்", font_size=20, on_press=lambda x: set_language("Tamil"))
        self.english_button = Button(text="English", font_size=20, on_press=lambda x: set_language("English"))
        layout.add_widget(self.tamil_button)
        layout.add_widget(self.english_button)
        
        # Microphone Button
        self.mic_button = Button(text="🎤", font_size=50, size_hint=(None, None), size=(120, 120), background_color=(0.2, 0.6, 1, 1))
        self.mic_button.bind(on_press=self.start_session)
        layout.add_widget(self.mic_button)
        
        # Response Label (Fading Text)
        self.response_label = Label(text="", font_size=20, color=(0, 0, 0, 1))
        layout.add_widget(self.response_label)
        
        return layout

    def start_session(self, instance):
        self.fade_text("உங்கள் தகவல்களை சொல்லுங்கள்." if selected_language == "Tamil" else "Please provide your details.")
        
        field_patterns = FIELD_PATTERNS_TAMIL if selected_language == "Tamil" else FIELD_PATTERNS_ENGLISH
        
        # Collecting data for each field
        form_data = {}
        for field in field_patterns.keys():
            field_input = get_field_input(field)
            form_data[field] = field_input
        
        self.fade_text("உங்கள் தகவல்கள் சேமிக்கப்பட்டன!" if selected_language == "Tamil" else "Your details have been saved!")
        save_to_csv(form_data)
        
    def fade_text(self, text):
        # Fading in and out animation for response text
        self.response_label.text = text
        anim_in = Animation(opacity=1, duration=1)
        anim_out = Animation(opacity=0, duration=1)
        anim_in.start(self.response_label)
        anim_out.start(self.response_label)

if __name__ == '__main__':
    VoiceAssistantApp().run()
