USE_ROUNDED_COORDS = False

OPENWEATHER_API_KEY = 'Your Api key OPENWEATHERMAP'
OPENWEATHER_URL = ("https://api.openweathermap.org/data/2.5/weather?"
                   "lat={latitude}&lon={longitude}&"
                   "appid=" + OPENWEATHER_API_KEY + "&lang=ru&units=metric")
