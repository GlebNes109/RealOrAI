import base64
import os
import random
import uuid
import time
from pathlib import Path

import requests

from app.src.config import settings

BASE_DIR = Path(__file__).resolve().parents[2]
USER_DATA_DIR = BASE_DIR / 'static/user_data'

class ApiService:
    def get_yandex_token(self, oauth_token):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        response = requests.post(url, json={"yandexPassportOauthToken": oauth_token}, timeout=10)
        if response.status_code == 200:
            return response.json()["iamToken"]
        else:
            return None

    def get_real_image(self):
        USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

        proxies = {
            "http": "http://EXvG1OT9o2:hPjgoPWSUt@193.176.153.72:21596",
            "https": "http://EXvG1OT9o2:hPjgoPWSUt@193.176.153.72:21596"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://picsum.photos/"
        }
        url = "https://picsum.photos/600/700"

        response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        if response.status_code == 200:
            id = str(uuid.uuid4())
            filename = f"{id}.jpg"
            filepath = USER_DATA_DIR / filename
            with open(filepath, "wb") as f:
                f.write(response.content)

            return id
        else:
            return None

    def get_ai_image(self):
        '''text = "Сгененируй максимально реалистичное изображение в стиле абстракционизма"
        IAM_TOKEN = self.get_yandex_token(settings.yandex_api_token)

        #Отправка запроса на генерацию
        generation_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
        headers = {
            "Authorization": f"Bearer {IAM_TOKEN}",
            "Content-Type": "application/json"
        }

        data = {
            "model_uri": "art://b1gd0h2v4hrmolvm843f/yandex-art/latest",
            "messages": [{"text": text, "weight": 1}],
            "generation_options": {"mime_type": "image/jpeg", "seed": random.randint(1, 2**63 - 1)}
        }

        gen_response = requests.post(generation_url, json=data, headers=headers)
        gen_response.raise_for_status()
        operation_id = gen_response.json()["id"]

        #Ожидание завершения операции
        operation_url = f"https://operation.api.cloud.yandex.net/operations/{operation_id}"
        while True:
            op_response = requests.get(operation_url, headers=headers)
            op_data = op_response.json()
            if op_data.get("done"):
                break
            time.sleep(2)

        # Декодирование и сохранение изображения
        image_b64 = op_data["response"]["image"]
        image_bytes = base64.b64decode(image_b64)

        filename = f"{uuid.uuid4()}.jpg"
        filepath = USER_DATA_DIR / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return str(filepath)'''
        return 0