import json
import os
import requests
import random

from datetime import datetime

    

class Repository:
    def __init__(self, data_file, api_key):
        self.data_file = data_file
        self.api_key = api_key
        self.use_api = api_key != ""
        if self.use_api:
            print("API-ключ не предоставлен, используется генератор случайных ответов")
        else:
            print(f"Получен API-ключ {self.api_key}")
        os.makedirs(os.path.dirname(data_file), exist_ok=True)


    # API-методы

    def get_sentiment(self, text):
        data = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": "Определи настроение отзыва (позитивное, нейтральное, негативное), дай ответ одним английским словом (positive/neutral/negative). Отзыв:" + text
                }
            ]
        }
        headers =  {
            'Authorization': 'Bearer ' + self.api_key,
            'Content-Type': 'application/json'
        }
        if self.use_api:
            try:
                response = requests.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    json= data,
                    headers=headers
                ).json()
                return response['choices'][0]['message']['content']
            except BaseException:
                print("Ошибка отправки запроса")
                pass 
        
        return random.choice(["positive", "negative", "neutral"])
    
    #CRUD

    def load_messages(self):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_messages(self, messages):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

    def add_message(self, name, text):
        messages = self.load_messages()
        sentiment = self.get_sentiment(text)  # Вызов API
        
        messages.append({
            "id": len(messages) + 1,
            "name": name,
            "text": text,
            "sentiment": sentiment,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.save_messages(messages)

    def delete_message(self, message_id):
        messages = self.load_messages()
        messages = [m for m in messages if m["id"] != message_id]
        self.save_messages(messages)

    
