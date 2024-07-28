import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os


engine = pyttsx3.init('sapi5')
voices=engine.getProperty("voices")
# print(voices[1].id)
engine.setProperty('voices',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning sir")

    elif hour>=12 and hour<18:
        speak("Good Afternoon sir")
    
    else:
        speak("Good Evening sir")

    speak("THIS IS YOUR VIRTYAL ASSISTENT 1.0.0, How can I help You Today!") #MY name is Jarvis, How can I help You Today!"

def takecommand():
    #it will take microphone input
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        # print(e)
        print("say that again....")
        return "None"
    return query

if __name__=="__main__":
    speak("")
    wishMe()
    while True:
        query= takecommand().lower()
    #logic for executing tasks
        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences= 5)
            speak("Accourding to wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak('opening Youtube..')
            webbrowser.open("youtube.com")

        elif 'weather' in query:
            speak('Todays weather is:')
            get_and_display_weather()

        elif 'open google' in query:
            speak('opening google..')
            webbrowser.open("google.com")

        elif 'open lpu live' in query:
            speak('opening lpulive...')
            webbrowser.open("https://lpulive.lpu.in/lpu-demo1/messages/0")

        elif 'the time' in  query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open ums' in query:
            speak('opening University Management system')
            webbrowser.open("https://ums.lpu.in/lpuums/")

        elif 'open chat GPT' in query:
            speak('opening chatgpt')
            webbrowser.open("https://chat.openai.com/")

        elif 'open vs code' in query:
            speak("openning VScode")
            codepath = "C:\\Users\\lenovo\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)

        elif 'open valorant' in query:
            speak("openning valorent")
            codepath = "C:\\Riot Games\\Riot Client\\RiotClientServices.exe"
            os.startfile(codepath)

        #     # Optionally, you can also print the AI response to the console
        #     print("AI:", ai_response)

