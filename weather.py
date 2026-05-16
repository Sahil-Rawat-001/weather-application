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
        self.resize(500,500)

        # input field
        self.city_input = QLineEdit(self)
        # get weather button
        self.get_weather_btn = QPushButton("Weather")
        
        # result label
        self.result_label = QLabel("Temperature: ")


        # vertical layout
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_input) # add city input widget into layout
        vbox.addWidget(self.result_label) # add city input result_label into layout
        vbox.addWidget(self.get_weather_btn) # add city get_weather_btn widget into layout

        # set layout
        self.setLayout(vbox)

        # connect button to get_weather function
        self.get_weather_btn.clicked.connect(self.get_weather)

    def get_weather(self):
        # get input field entered text i.e, city
        city = self.city_input.text()

        # base url
        base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        # get response back using get() method
        response = requests.get(base_url)

        # convert response to json
        weather_data = response.json()

        if response.status_code == 200:
            # access temperature from json 
            temperature = weather_data['main']['temp']
            # set result label with temperature
            self.result_label.setText(f"Temperature: {temperature}")
        else:
            print("error")


        

        





if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = WeatherApp()
    window.show()

    sys.exit(app.exec_())