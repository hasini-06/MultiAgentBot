import requests
import re
class CalculatorTool:
  def add(self,a,b):
    return a+b
  def subtract(self,a,b):
    return a-b
  def multiply(self,a,b):
    return a*b
  def divide(self,a,b):
    if b==0:
      return "Error: Division by zero"
    return a/b
  
class StringTool:
  def reverse(self, text):
    return text[::-1]    # slice notation to reverse a string

  def uppercase(self, text):
    return text.upper()  # built-in str method to uppercase
  
class WeatherTool:
  def __init__(self,api_key):
    self.api_key = api_key
  def get_weather(self,city):
    # API Call
    url=f"https://api.tomorrow.io/v4/timelines?location={city}&fields=temperature,weatherCode&units=metric&timesteps=1d&apikey={self.api_key}"
  
    try:
      res=requests.get(url)   #sends a GET request
      data=res.json()   #converts response to JSON
      # return data
    except Exception as e:
      return f"Error fetching weather : {e}"
    
    try:
      timelines=data.get('data',{}).get('timelines',[])
      if not timelines:
        return f"No weather data found for {city}"
      #Extracts timelines from JSON.
      # If no timelines, return error message.

      intervals=timelines[0].get('intervals',[])

      if not intervals:
        return f"No interval data found for {city}"
      # Gets first timeline's intervals.
      # If none, return error message.

      values=intervals[0].get('values',{})
      temperature=values.get('temperature','N/A')
      weather=values.get('weatherCode','N/A')
       #return a user-friendly string
      return f"The weather in {city} is {weather} with {temperature}°C."

    except Exception as e:
      return f"Error reading weather data : {e}"
      # Catches errors during parsing.