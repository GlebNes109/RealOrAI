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
        w = random.randint(300, 900)
        h = random.randint(300, 900)
        url = f"https://picsum.photos/{w}/{h}"

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
        prompts = [
            # природные
            "Сгенерируй фотореалистичное изображение совы в полёте на фоне полной луны",
            "Создай гиперреалистичный портрет тигра в джунглях при закатном освещении",
            "Сгенерируй изображение коалы на эвкалипте с мельчайшей детализацией шерсти",
            "Сделай фотореалистичный кадр подводного мира с акулой и коралловым рифом",
            "Сделай реалистичное изображение с водопадом и горами",

            # техника
            "Создай реалистичное изображение робота-гуманоида, чинящего автомобиль в гараже",
            "Сгенерируй фото городского пейзажа будущего с летающими машинами и неоновой рекламой",
            "Сделай максимально реалистичный 3D-рендер киберпанкового рынка с людьми и роботами",
            "Сделай реалистичное изображение старинного города, сделай как будто это старое фото",
            "Сгененируй максимально реалистичное изображение советского автомобиля 50-х годов",
            "Сгененируй суперреалистичное изображение электропоезда, 60-70-х годов",
            "Сгененируй гиперреалистичное изображение самолета, 60-70-х годов",

            # история
            "Создай изображение древнеримского форума с людьми в тогах, как историческая реконструкция",
            "Сгенерируй фотореалистичную сцену средневекового рынка с лошадьми и торговыми лавками",
            "Сделай реалистичное старое фото первой железной дороги 19 века с паровозом",

            # Еда, напитки
            "Сгенерируй гиперреалистичное изображение куска растаявшего сыра на гриле",
            "Создай фото настоящего итальянского пирога с моцареллой и базиликом крупным планом",
            "Сделай макросъёмку капель воды на бутылке дорогого вина с бликами света",

            # Захватывающие фото)
            "Сгенерируй реалистичный кадр вулкана во время извержения ночью",
            "Создай фото торнадо в прерии с детализацией пыли и летящих обломков",
            "Сделай реалистичное изображение альпиниста на отвесной ледяной скале",

            # Обычные повседневные
            "Сгенерируй фото пожилой пары, пьющей чай на балконе с видом на город",
            "Создай реалистичный кадр детских рук, запускающих бумажного змея на пляже",
            "Сделай изображение заправочной станции 70-х годов с винтажными автомобилями",

            # Немного разбавим очевидным ИИ контентом
            "Сгенерируй фотореалистичное изображение дракона, спящего в современной библиотеке",
            "Создай реалистичный портрет инопланетянина в скафандре с текстурой металла",
            "Сделай изображение гигантских механических часов, растущих из поля пшеницы",
            "Сделай изображение толпы людей, поклоняющихся соцсети ВКонтакте как своему священному божеству",

            # Спорт
            "Сгенерируй реалистичный кадр футбольного матча под дождём с брызгами грязи",
            "Создай фото велосипедиста в горах с эффектом motion blur на колёсах",
            "Сделай изображение боксёра в момент удара с каплей пота в замедленной съёмке",

            # Архитектура, здания
            "Сгенерируй фото заброшенного замка в тумане с обвалившейся стеной",
            "Создай реалистичный ночной вид небоскрёба с освещёнными окнами-пикселями",
            "Сделай изображение деревянной церкви в русской деревне с инеем на крыше",

            # Необычные ракурсы
            "Сгенерируй фото зеркального шара с отражением лесного пейзажа",
            "Создай реалистичный кадр капли воды на стекле с преломлением городского пейзажа",

            # Природа, по сезонам
            "Сгенерируй фото заснеженного леса с лучом света сквозь ветки елей",
            "Создай реалистичное изображение осеннего парка с ковром из жёлтых листьев",
            "Сделай летний пейзаж с грозовым небом и одиноким деревом на холме",

            # Арт и абстракция
            "Сгенерируй реалистичное изображение масляной краски, растекающейся по мрамору",
            "Создай фото сюрреалистичной скульптуры из расплавленного стекла и стали",
            "Сделай гиперреалистичный натюрморт с фруктами и разбитой вазой в стиле голландских мастеров"
        ]

        text = random.choice(prompts)

        IAM_TOKEN = self.get_yandex_token(settings.yandex_api_token)
        text = prompts[random.randint(0, 5)]
        # отправка запроса на генерацию
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

        # Ожидание завершения операции (апи не возвращает картинку сразу, надо проверять готовность с помощью operation_id
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
        id = str(uuid.uuid4())
        filename = f"{id}.jpg"
        filepath = USER_DATA_DIR / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return id