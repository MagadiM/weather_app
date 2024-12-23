from django.shortcuts import render
from .models import City
import requests
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=cea773c705cafef55170ce24bf4f16e1'

    # Query all cities from the database
    cities = City.objects.all()

    if request.method == 'POST':  # Handle form submission
        form = CityForm(request.POST)  # Bind form with POST data
        #form validation and city extraction
        if form.is_valid():
            new_city = form.cleaned_data['name']
            # Check if city already existsand saves only if the city is new
            if not City.objects.filter(name=new_city).exists():
                form.save() 
            else:
                # Optional: Add a message to inform the user about duplicates(message in the console)
                print(f"City {new_city} already exists!")

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city.name)).json()  # Fetch weather data
        if 'main' in city_weather:  # Check if the API returned valid data
            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
            }
            weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)