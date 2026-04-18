import requests
import logging

logger = logging.getLogger(__name__)

class WeatherSkill:
    def __init__(self):
        self.base_url = "https://wttr.in"

    def get_weather(self, city):
        """
        Fetches the current weather for a given city.
        """
        try:
            # format=3 gives a one-line output like: "London: ⛅️ +13°C"
            url = f"{self.base_url}/{city}?format=3"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
            else:
                return f"Sorry, I couldn't get the weather for {city}."
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return "I'm having trouble connecting to the weather service."
