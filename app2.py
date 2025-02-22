import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
import speech_recognition as sr
import pyttsx3
import re
import csv

kivy.require('1.11.1')  # specify the Kivy version

# Speech-to-Text engine (Text-to-Speech)
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # speed
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech Recognition (Tamil)
recognizer = sr.Recognizer()

def listen_to_user():
    with sr.Microphone() as source:
        print("தயவுசெய்து பேசவும்...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Timeout for better UX
            text = recognizer.recognize_google(audio, language="ta-IN")
            print(f"நீங்கள் சொன்னது: {text}")
            return text
        except (sr.UnknownValueError, sr.RequestError):
            speak("மன்னிக்கவும், உங்கள் பதில் புரியவில்லை. மீண்டும் சொல்லவும்.")
            return ""
        
        try:
            # Tamil speech-to-text
            text = recognizer.recognize_google(audio, language="ta-IN")  # Tamil language
            print(f"நீங்கள் சொன்னது: {text}")
            return text
        except sr.UnknownValueError:
            speak("மன்னிக்கவும், நான் அதைப் புரிந்துகொள்ள முடியவில்லை.")
        except sr.RequestError:
            speak("மன்னிக்கவும், பேச்சு பொழிப்புத் தொலைபேசி சேவையில் பிரச்சினை உள்ளது.")
        return ""

# Regular expressions for validation (Phone, Email, etc.)
def validate_phone_number(phone):
    pattern = r"^[6-9]\d{9}$"  # Indian phone number format (6-9 and 9 digits)
    return re.match(pattern, phone)

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def validate_age(age):
    return age.isdigit() and 0 < int(age) <= 120

# Function to save data to a CSV file
def save_to_csv(data):
    header = ["பெயர்", "மின்னஞ்சல்", "தொலைபேசி எண்", "முகவரி", "பாலினம்", "வயது", "தொழில்", "பிறந்த தேதி", "நகரம்", "நாடு"]
    
    # Open the CSV file in append mode, so that it adds to the file without overwriting.
    with open("form_data.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # If file is empty, write the header
        if file.tell() == 0:
            writer.writerow(header)
        
        # Write the data as a row in the CSV
        writer.writerow(data)
    speak("உங்கள் தகவல்கள் வெற்றிகரமாக சேமிக்கப்பட்டுள்ளன.")

# Kivy App for Form Filling with Enhanced UI
class TamilFormFillApp(App):
    def build(self):
        self.title = "தமிழ் படிவம் பூர்த்தி செய்யுங்கள்"
        
        # Create the root layout for the app
        root_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Add an image/logo to the header
        header_layout = BoxLayout(size_hint_y=None, height=200)
        img = Image(source='your_logo.png')  # Replace 'your_logo.png' with your image path
        header_layout.add_widget(img)
        root_layout.add_widget(header_layout)

        # Scrollable content area
        scroll_view = ScrollView()
        form_layout = GridLayout(cols=1, padding=10, spacing=15, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Labels and TextInputs for the form fields with custom styling
        self.name_input = TextInput(hint_text="பெயர்", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.email_input = TextInput(hint_text="மின்னஞ்சல்", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.phone_input = TextInput(hint_text="தொலைபேசி எண்", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.address_input = TextInput(hint_text="முகவரி", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.gender_input = TextInput(hint_text="பாலினம்", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.age_input = TextInput(hint_text="வயது", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.occupation_input = TextInput(hint_text="தொழில்", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.dob_input = TextInput(hint_text="பிறந்த தேதி", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.city_input = TextInput(hint_text="நகரம்", multiline=False, size_hint_y=None, height=40, font_size=18)
        self.country_input = TextInput(hint_text="நாடு", multiline=False, size_hint_y=None, height=40, font_size=18)
        
        # Add all inputs to the layout
        form_layout.add_widget(self.name_input)
        form_layout.add_widget(self.email_input)
        form_layout.add_widget(self.phone_input)
        form_layout.add_widget(self.address_input)
        form_layout.add_widget(self.gender_input)
        form_layout.add_widget(self.age_input)
        form_layout.add_widget(self.occupation_input)
        form_layout.add_widget(self.dob_input)
        form_layout.add_widget(self.city_input)
        form_layout.add_widget(self.country_input)

        # Add ScrollView to the root layout
        scroll_view.add_widget(form_layout)
        root_layout.add_widget(scroll_view)

        # Button to start form filling
        self.fill_button = Button(text="பフォーム பூர்த்தி செய்யவும்", size_hint_y=None, height=50, font_size=20, background_color=(0.2, 0.6, 0.2, 1))
        self.fill_button.bind(on_press=self.fill_form)

        # Add button to root layout
        root_layout.add_widget(self.fill_button)

        return root_layout
    
    # Function to start the form filling process
    def fill_form(self, instance):
        speak("உங்கள் பெயர் என்ன?")
        name = listen_to_user()
        self.name_input.text = name  # Set the name in the text input field
        
        speak("தயவுசெய்து உங்கள் மின்னஞ்சல் சொல்க.")
        email = listen_to_user()
        while not validate_email(email):
            speak("மின்னஞ்சல் வடிவம் தவறாக உள்ளது. மீண்டும் உங்கள் மின்னஞ்சலை சொல்லவும்.")
            email = listen_to_user()
        self.email_input.text = email  # Set the email in the text input field
        
        speak("தயவுசெய்து உங்கள் தொலைபேசி எண்ணை சொல்லவும்.")
        phone = listen_to_user()
        while not validate_phone_number(phone):
            speak("தொலைபேசி எண் தவறாக உள்ளது. மீண்டும் உங்கள் தொலைபேசி எண்ணை சொல்லவும்.")
            phone = listen_to_user()
        self.phone_input.text = phone  # Set the phone number in the text input field
        
        speak("தயவுசெய்து உங்கள் முகவரியை சொல்லவும்.")
        address = listen_to_user()
        self.address_input.text = address  # Set the address in the text input field
        
        speak("உங்கள் பாலினம் என்ன? (ஆண்/பெண்/மற்றது)")
        gender = listen_to_user()
        self.gender_input.text = gender  # Set the gender in the text input field
        
        speak("உங்கள் வயது எவ்வளவு?")
        age = listen_to_user()
        while not validate_age(age):
            speak("வயது தவறாக உள்ளது. தயவுசெய்து சரியான வயதை சொல்லவும்.")
            age = listen_to_user()
        self.age_input.text = age  # Set the age in the text input field
        
        speak("உங்கள் தொழில் என்ன?")
        occupation = listen_to_user()
        self.occupation_input.text = occupation  # Set the occupation in the text input field
        
        speak("உங்கள் பிறந்த தேதி என்ன? (DD/MM/YYYY வடிவத்தில்)")
        dob = listen_to_user()
        self.dob_input.text = dob  # Set the date of birth in the text input field
        
        speak("உங்கள் நகரம் என்ன?")
        city = listen_to_user()
        self.city_input.text = city  # Set the city in the text input field
        
        speak("உங்கள் நாடு என்ன?")
        country = listen_to_user()
        self.country_input.text = country  # Set the country in the text input field

        # Prepare the data as a list
        form_data = [name, email, phone, address, gender, age, occupation, dob, city,country]
    save_to_csv(form_data)
        
    speak(f"உங்கள் தகவல்கள் பூர்த்தி செய்யப்பட்டுள்ளன:\nபெயர்: {name}\nமின்னஞ்சல்: {email}\nதொலைபேசி எண்: {phone}\nமுகவரி: {address}\nபாலினம்: {gender}\nவயது: {age}\nதொழில்: {occupation}\nபிறந்த தேதி: {dob}\nநகரம்: {city}\nநாடு: {country}")

# Run the app
if __name__ == "__main__":
    TamilFormFillApp().run()