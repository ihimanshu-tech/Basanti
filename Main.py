import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import json
import os

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say('Me basanti hu')

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
            return command
    except Exception as e:
        print(f"Error: {e}")
        return ""

# Paths for data files
command_file = 'commands.json'
contact_file = 'contacts.json'

# Load existing data or initialize empty dictionaries
def load_data():
    global command_dict, contact_dict
    if os.path.exists(command_file):
        with open(command_file, 'r') as file:
            command_dict = json.load(file)
    else:
        command_dict = {
            'play': ['play song', 'play music'],
            'time': ['current time', 'what time is it'],
            'who is': ['who the heck is', 'who is']
        }

    if os.path.exists(contact_file):
        with open(contact_file, 'r') as file:
            contact_dict = json.load(file)
    else:
        contact_dict = {}

def save_data():
    with open(command_file, 'w') as file:
        json.dump(command_dict, file, indent=4)
    with open(contact_file, 'w') as file:
        json.dump(contact_dict, file, indent=4)

def save_alternative_names(main_command, alternative_name):
    if main_command in command_dict:
        command_dict[main_command].append(alternative_name)
    else:
        command_dict[main_command] = [alternative_name]
    save_data()
    talk(f'Alternative name "{alternative_name}" added for the command "{main_command}".')

def save_contact(contact_name, alternative_name):
    contact_dict[alternative_name] = contact_name
    save_data()
    talk(f'Contact name "{contact_name}" saved as "{alternative_name}".')

def get_command_from_alternatives(command):
    for key, values in command_dict.items():
        if command in values:
            return key
    return None

def get_contact_from_alternatives(contact_name):
    return contact_dict.get(contact_name, contact_name)

def run_alexa():
    command = take_command()
    if 'basanti' in command:
        command = command.replace('basanti', '').strip()

        # Check if the command is to add an alternative name for a command
        if 'add alternative name' in command:
            parts = command.split('for')
            if len(parts) == 2:
                alternative_name = parts[0].replace('add alternative name', '').strip()
                main_command = parts[1].strip()
                save_alternative_names(main_command, alternative_name)
                print (f"Added {alternative_name} for {main_command}")
                talk ("Added Alternative name")
            else:
                talk('Please provide the command and the alternative name in the format: "add alternative name [alternative] for [command]"')
            return

        # Check if the command is to save a contact
        if 'save' in command and 'as' in command:
            parts = command.split('as')
            if len(parts) == 2:
                contact_name = parts[0].replace('save', '').strip()
                alternative_name = parts[1].strip()
                save_contact(contact_name, alternative_name)
            else:
                talk('Please provide the contact name and the alternative name in the format: "save [contact] as [alternative]"')
            return

        # Check if the command is to use a contact's alternative name
        main_command = get_command_from_alternatives(command)
        if main_command == 'play':
            song = command.replace('play', '').strip()
            talk(f'Playing {song}')
            pywhatkit.playonyt(song)
        elif main_command == 'time':
            time = datetime.datetime.now().strftime('%H:%M')
            print(time)
            talk('Current time is ' + time)
        elif main_command == 'who is':
            person = command.replace('who the heck is', '').strip()
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        elif 'are you single' in command:
            talk('I am in a relationship with WIFI')
            print("I am in a relationship with WIFI")

        # Handle contact names
        contact_name = get_contact_from_alternatives(command)
        if contact_name != command:
            talk(f'Contact recognized: {contact_name}')
            print(f'Contact recognized: {contact_name}')

# Load data from files before running the loop
load_data()

while True:
    run_alexa()
