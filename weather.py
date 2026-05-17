import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # set window title and size of the window respectively
        self.setWindowTitle("weather app")
        self.resize(700,500)

        self.city_label = QLabel("Enter city name: ",self)

        # input field
        self.city_input = QLineEdit(self)
        # placeholder text
        self.city_input.setPlaceholderText("Enter city")

        # get weather button
        self.get_weather_btn = QPushButton("Get Weather",self)
        
        # result label
        self.temperature_label = QLabel(self)

        # emoji label
        self.emoji_label = QLabel(self)

        # description laber
        self.description_label = QLabel(self)


        # vertical layout
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label) # add city label widget into layout
        vbox.addWidget(self.city_input) # add city input widget into layout
        vbox.addWidget(self.get_weather_btn) # add city get_weather_btn widget into layout
        vbox.addWidget(self.temperature_label) # add city input result_label into layout
        vbox.addWidget(self.emoji_label) # add city input emoji_label into layout
        vbox.addWidget(self.description_label) # add city input description_label into layout

        # set layout
        self.setLayout(vbox)

        # center align widgets
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # style 
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.get_weather_btn.setObjectName("get_weather_btn")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")


        self.setStyleSheet("""
           
           QLabel, QPushButton {
            font-family: verdana;
           }
           QLabel#city_label{
            font-size: 40px;
            font-style: italic;
           }
           
            QLineEdit#city_input{
             font-size: 40px;
            }
                           
            QPushButton#get_weather_btn{
               font-size: 30px;
               font-weight: bold;
               margin-bottom:10px;
            }

            QLabel#temperature_label{
                font-size: 70px;
            }
                           
            QLabel#emoji_label{
                font-size: 100px;
                font-family: segoe UI emoji;
            }
                           
            QLabel#description_label{
                font-size: 50px;
                font-weight: bold;
            }
     """)

        # connect button to get_weather function
        self.get_weather_btn.clicked.connect(self.get_weather)

        # make when pressed "enter" then weather is searched
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        # get input field entered text i.e, city
        city = self.city_input.text()

        # check if request is not empty
        if not city.strip():
         self.display_error("Please enter a city name")
         return

        # base url
        base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        

        try:
            # get response back using get() method
            response = requests.get(base_url)
            response.raise_for_status()

            # convert response to json
            weather_data = response.json()

            if weather_data["cod"] == 200:
                self.temperature_label.setStyleSheet("font-size: 70px;")
                print(weather_data)

                # access temperature from json 
                temperature = weather_data['main']['temp']

                # access weather id from json
                weather_id = weather_data['weather'][0]['id']

                # set result label with temperature
                self.temperature_label.setText(f"Temp: {temperature:.0f}°C")

                # set emoji label
                self.emoji_label.setText(self.get_weather_icon(weather_id))

                 # set description label with temperature
                self.description_label.setText(f"{weather_data['weather'][0]['description']}")

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\n please check your input")
                case 401:
                    self.display_error("Unauthorized:\n Invalid API key")
                case 403:
                    self.display_error("Forbidden:\n Access is denied")
                case 404:
                    self.display_error("Not found:\n City not found")
                case 500:
                    self.display_error("Internal server error:\n please try again later")
                case 502:
                    self.display_error("Bad Gateway:\n Invalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\n Server is down")
                case 504:
                    self.display_error("Gateway Timeout:\n No response from the server")
                case _:
                    self.display_error(f"HTTP error occured: {http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\n check your internet connection")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\n check the URL")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\n request timed out")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n {req_error}")

    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.description_label.clear()
        self.emoji_label.clear()

    @staticmethod
    def get_weather_icon(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return '☁️'
        else:
            return ""
        


        

        





if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = WeatherApp()
    window.show()

    sys.exit(app.exec_())