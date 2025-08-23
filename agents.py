from tools import CalculatorTool, StringTool, WeatherTool
import re
import streamlit as st
from huggingface_hub import InferenceClient

class CalculatorAgent:
    def __init__(self):
        self.tool = CalculatorTool()

    def perform_task(self, request: str):
        if any(word in request.lower() for word in ["plus", "add", "+", "multiply", "times", "*"]):
            numbers = list(map(int, re.findall(r'\d+', request)))
            if len(numbers) < 2:
                return "Not enough numbers for calculator."

            if any(word in request.lower() for word in ["plus", "add", "+"]):
                return self.tool.add(numbers[0], numbers[1])
            elif any(word in request.lower() for word in ["times", "multiply", "*"]):
                return self.tool.multiply(numbers[0], numbers[1])

        return None


class StringAgent:
    def __init__(self):
        self.tool = StringTool()

    def perform_task(self, query: str):
        if "reverse" in query.lower():
            text = query.replace("reverse", "").strip()
            return self.tool.reverse(text)
        elif "uppercase" in query.lower():
            text = query.replace("uppercase", "").strip()
            return self.tool.uppercase(text)
        return None


class WeatherAgent:
    def __init__(self):
        api_key = st.secrets["API_KEY"]
        self.tool = WeatherTool(api_key)

    def perform_task(self, request: str):
        if any(word in request.lower() for word in ["weather", "temperature"]):
            city_match = re.search(r'(?:weather|temperature) in ([\w\s]+)', request, re.IGNORECASE)
            if city_match:
                city = city_match.group(1).strip()
                return self.tool.get_weather(city)
            else:
                return "Please specify a city for the weather."
        return None
    
class MasterAgent:
    def __init__(self):
        self.agents = [CalculatorAgent(), StringAgent(), WeatherAgent()]
        # ✅ Hugging Face client
        self.llm = InferenceClient(token=st.secrets["HF_TOKEN"])

    def route(self, query: str):
        # Step 1: Try each agent first
        for agent in self.agents:
            response = agent.perform_task(query)
            if response:
                return response

        # Step 2: If no agent handled it → fallback to Mistral
        try:
            completion = self.llm.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.2",
                messages=[{"role": "user", "content": query}],
                max_tokens=200
            )
            return completion.choices[0].message["content"]
        except Exception as e:
            return f"🤖 Sorry, I couldn't fetch an answer. ({e})"
    


    