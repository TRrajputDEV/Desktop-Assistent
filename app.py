import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import openai
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

openai.api_key = ''
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

def get_and_display_weather():
    # Replace these coordinates with the desired location
    latitude = 28.9034473
    longitude = 76.5719414

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m"
    }

    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    speak(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    speak(f"Elevation {response.Elevation()} m asl")
    print(f"Elevation {response.Elevation()} m asl")
    speak(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    speak(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    speak(hourly_dataframe)
    print(hourly_dataframe)

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
        # else:
        #     # Use OpenAI API for general responses
        #     prompt = f"You said: {query}"
        #     response = openai.Completion.create(
        #         engine="gpt-3.5-turbo",
        #         prompt=prompt,
        #         max_tokens=150  # You can adjust this based on your preference
        #     )
        #     ai_response = response.choices[0].text.strip()

        #     # Speak the AI response
        #     speak(ai_response)

        #     # Optionally, you can also print the AI response to the console
        #     print("AI:", ai_response)

