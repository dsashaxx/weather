import json
import urllib.parse
import urllib.request
class WeatherData:
    def __init__(self, city, temperature, country):
        self.city = city
        self.temperature = temperature
        self.country = country
def read(filename):
    with open(filename, "r", encoding="utf-8") as file:
        cities = []
        for line in file:
            city = line.strip()
            if city != "" and city not in cities:
                cities.append(city)

        return cities
def get(city):
    city_for_url = urllib.parse.quote(city)
    url = "https://wttr.in/" + city_for_url + "?format=j1"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        text = response.read().decode("utf-8")
    data = json.loads(text)
    temperature = int(data["current_condition"][0]["temp_C"])
    area = data["nearest_area"][0]
    country = area["country"][0]["value"]
    return WeatherData(city, temperature, country)


def printt(weather):
    sign = "+"
    if weather.temperature < 0:
        sign = ""
    print(
        weather.city + ", " +
        weather.country + " " +
        sign + str(weather.temperature) + " °C"
    )
def statistics(weather_list):
    countries = {}

    for weather in weather_list:
        if weather.country not in countries:
            countries[weather.country] = []

        countries[weather.country].append(weather.temperature)

    print()
    print("Statistics by country:")

    for country in countries:
        temperatures = countries[country]

        count = len(temperatures)
        average = sum(temperatures) / count
        minimum = min(temperatures)
        maximum = max(temperatures)

        print(
            country +
            " — " + str(count) + " cities, " +
            "avg: " + format(average) + ", " +
            "min: " + format(minimum) + ", " +
            "max: " + format(maximum)
        )


def format(temperature):
    if temperature > 0:
        return "+" + str(round(temperature, 1)) + " °C"
    return str(round(temperature, 1)) + " °C"


def main():
    cities = read("cities.txt")
    weather_list = []

    for city in cities:
        try:
            weather = get(city)
            weather_list.append(weather)
            printt(weather)
        except Exception as error:
            print(city + " — error: " + str(error))

    statistics(weather_list)


main()
