import telebot
import requests
import os
import datetime as dt
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    bot.send_message(message.chat.id, text="Hi!\n"
                                           "I'm your weather bot.\n"
                                           "Type in your city name to get the weather report of that city.")


@bot.message_handler(func=lambda msg: True)
def handle_start(message):
    API_KEY = os.getenv("API_KEY")
    CITY = message.text
    URL = f"https://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={CITY}"
    response = requests.get(URL)

    def kelvin_to_celsius(kelvin):
        celsius = kelvin - 273.15
        return celsius

    if response.status_code == 200:
        response = response.json()
        temp_kelvin = response["main"]["temp"]
        temp_celsius = kelvin_to_celsius(temp_kelvin)
        feels_like_kelvin = response["main"]["feels_like"]
        feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)
        humidity = response["main"]["humidity"]
        description = response["weather"][0]["description"]
        sunrise_time = dt.datetime.utcfromtimestamp(response["sys"]["sunrise"] + response["timezone"])
        sunset_time = dt.datetime.utcfromtimestamp(response["sys"]["sunset"] + response["timezone"])
        wind_speed = response["wind"]["speed"]

        bot.send_message(message.chat.id, text=f"Temperature in {CITY}: {temp_celsius:.2f}C\n"
                                               f"Temperature in {CITY} feels like: {feels_like_celsius:.2f}C\n"
                                               f"Humidity in {CITY}: {humidity}%\n"
                                               f"Wind Speed in {CITY}: {wind_speed}m/s\n"
                                               f"Description in {CITY}: {description}\n"
                                               f"Sun rises in {CITY}: {sunrise_time} local time\n"
                                               f"Sun sets in {CITY}: {sunset_time} local time\n")
    elif response.status_code == 400:
        bot.send_message(message.chat.id, text="There is no city with this name in my data base or"
                                               " you write the name wrong")
    else:
        bot.send_message(message.chat.id, text="Something went wrong.\nPlease try again later")


bot.infinity_polling()
