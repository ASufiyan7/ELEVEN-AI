import smtplib
import pyttsx3
import datetime
import requests
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from MusicLibrary import Music

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I’m ELEVEN, the Enhanced Learning Entity. Let's get started.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
        except Exception as e:
            print(f"Error accessing microphone: {e}")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"Error recognizing speech: {e}")
        return "None"
    
    return query

def get_weather():
    city = "Surat" 
    api_key = "0ed358efaf2839cef0c242d6ab41325b" 
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temp = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        weather_report = (f"Temperature: {temp}°C\n"
                          f"Atmospheric pressure: {pressure} hPa\n"
                          f"Humidity: {humidity}%\n"
                          f"Description: {description}")
        speak(weather_report)
        print(weather_report)
    else:
        speak("City not found.")

def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)
    speak(f"Here are the search results for {query} on YouTube.")


def play_music(song_name):
    song_name = song_name.lower()
    if song_name in Music:
        song_url = Music[song_name]
        webbrowser.open(song_url)
        return True
    return False

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'open facebook' in query:
            webbrowser.open("https://facebook.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")  

        
        if 'weather' in query:
            get_weather() 

        elif 'search youtube' in query:
            search_query = query.replace('search youtube for', '').strip()
            search_youtube(search_query)

        elif 'play music' in query:
            music_dir = "D:\\Python\\MusicLibrary.py"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'play' in query:
            song_name = query.replace('play', '').strip()
            if not play_music(song_name):
                speak("Song not found in the library")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"The time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\sufiyan ansari\\AppData\\Local\\Programs\\Microsoft VS Code"
            os.startfile(codePath)

        elif 'news' in query:
            try:
                r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=267f5ef7b2d849cfbe77d55ee93ad659")
                if r.status_code == 200:
                    data = r.json()
                    articles = data.get('articles', [])
                    for index, article in enumerate(articles, start=1):
                        speak(f"{index}. {article.get('title')}")
                else:
                    speak("I'm sorry, I couldn't fetch the news right now.")
            except Exception as e:
                print(f"Failed to fetch news: {e}")
                speak("There was an error fetching the news.")
