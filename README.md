# Basanti
Basanti- My Own Alexa


Basanti is a Python-based voice assistant capable of performing various tasks such as playing music, telling the current time, providing Wikipedia summaries, and managing contacts with alternative names. It leverages several libraries for speech recognition, text-to-speech, and interaction with external APIs.

Features

Speech Recognition: Converts spoken words into text using the speech_recognition library.

Text-to-Speech: Provides verbal feedback using the pyttsx3 library.

Dynamic Command Management: Allows users to add alternative names for commands.

Contact Management: Saves and retrieves contacts with alternative names.

Persistent Storage: Stores commands and contacts in JSON files for persistence across sessions.

Music Playback: Plays songs on YouTube using the pywhatkit library.

Time Reporting: Tells the current time.

Wikipedia Search: Provides summaries from Wikipedia.

Error Handling: Handles various exceptions during command recognition and execution.

Installation
Clone the repository:

bash
Copy code
git clone https://github.com/ihimanshu_tech/basanti.git
cd basanti-voice-assistant
Install the required libraries:

bash
Copy code
pip install -r requirements.txt
Create JSON files for storing commands and contacts (if not already present):

bash
Copy code
echo "{}" > commands.json
echo "{}" > contacts.json
Usage
Run the script:

bash
Copy code
python basanti.py
Interacting with Basanti:

Play Music:
css
Copy code
Basanti, play [song name]
Get Current Time:
csharp
Copy code
Basanti, what time is it?
Search Wikipedia:
vbnet
Copy code
Basanti, who is [person's name]?
Add Alternative Name for Command:
css
Copy code
Basanti, add alternative name [alternative name] for [command]
Save Contact:
css
Copy code
Basanti, set [contact name] phone [phone number] as [alternative name]
Ask Relationship Status:
sql
Copy code
Basanti, are you single?
File Structure
basanti.py: Main script for the voice assistant.
commands.json: JSON file to store commands and their alternative names.
contacts.json: JSON file to store contacts and their alternative names.
requirements.txt: List of required Python libraries.
Contributing
Fork the repository.
Create a new branch:
bash
Copy code
git checkout -b feature-branch
Make your changes and commit them:
bash
Copy code
git commit -m "Add some feature"
Push to the branch:
bash
Copy code
git push origin feature-branch
Submit a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Python Speech Recognition: speech_recognition
Text-to-Speech: pyttsx3
YouTube Control: pywhatkit
Wikipedia API: wikipedia
