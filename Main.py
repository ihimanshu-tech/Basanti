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
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=3, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
            return command
    except sr.WaitTimeoutError:
        print("Error: listening timed out while waiting for phrase to start")
        return ""
    except sr.UnknownValueError:
        print("Error: could not understand audio")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

command_file = 'commands.json'
contact_file = 'contacts.json'

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

def save_contact(contact_name, phone_number, alternative_name):
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

def handle_add_alternative_name(command):
    parts = command.split('for')
    if len(parts) == 2: 
        alternative_name = parts[0].replace('add alternative name', '').strip()
        main_command = parts[1].strip()
        save_alternative_names(main_command, alternative_name)
        talk("Added Alternative name")
    else:
        talk('Please provide the command and the alternative name in the format: "add alternative name [alternative] for [command]"')

def handle_add_contact(command):
    parts = command.split('as')
    if len(parts) == 2:
        contact_info = parts[0].replace('set', '').strip().split('phone')
        if len(contact_info) == 2:
            contact_name = contact_info[0].strip()
            phone_number = contact_info[1].strip()
            alternative_name = parts[1].strip()
            save_contact(contact_name, phone_number, alternative_name)
        else:
            talk('Please provide the contact name and phone number in the format: "set [contact] phone [number] as [alternative]"')
            print('Please provide the contact name and phone number in the format: "set [contact] phone [number] as [alternative]"')
    else:
        talk('Please provide the contact name and the alternative name in the format: "set [contact] phone [number] as [alternative]"')

def run_alexa():
    command = take_command()
    if not command:
        return

    if 'basanti' in command:
        command = command.replace('basanti', '').strip()

        if 'add alternative name' in command:
            handle_add_alternative_name(command)
        elif 'set' in command and 'as' in command:
            handle_add_contact(command)
        elif 'play' in command:
            song = command.replace('play', '').strip()
            talk(f'Playing {song}')
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%H:%M')
            talk('Current time is ' + time)
        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            info = wikipedia.summary(person, 1)
            talk(info)
        elif 'are you single' in command:
            talk('I am in a relationship with WIFI')
        elif 'alternative name for' in command:
            contact_name = command.replace('alternative name for', '').strip()
            alt_name = get_contact_from_alternatives(contact_name)
            if alt_name:
                talk(f'The alternative name for {contact_name} is {alt_name}')
            else:
                talk(f'No alternative name found for {contact_name}')

load_data()

while True:
    run_alexa()
