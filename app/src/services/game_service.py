import random
import time

from flask import session

from app.src.database.db_models import Answer, CardsDB
from app.src.database.repository import Repository
from app.src.services.api_service import ApiService

api = ApiService()
repository = Repository()
class GameService():
    def generate_new_game(self):
        game_cards_id = []

        # 5 случайных карточек из базы
        existing_cards = repository.get_random_cards(5)
        if existing_cards:
            game_cards_id.extend([card.id for card in existing_cards])

        # 3 новых реальных изображения
        for _ in range(3):
            time.sleep(1)  # Перерыв между запросами
            id = api.get_real_image()
            card_db = CardsDB(
                id=id,
                corr_answer=Answer.REAL
            )
            if card_db.id:
                repository.create_new_card(card_db)
                game_cards_id.append(id)

        # 2 изображения из нейросети
        for _ in range(0):
            time.sleep(1)
            id = api.get_ai_image()
            card_db = CardsDB(
                id=id,
                corr_answer=Answer.AI
            )
            if card_db.id:
                repository.create_new_card(card_db)
                game_cards_id.append(id)

        #  рандомное перемешивание
        random.shuffle(game_cards_id)

        # в сессии только id карточек - текущая игра
        session['game_cards'] = game_cards_id
        session['current_index'] = 0
        session['correct_answers'] = 0

    def get_current_card(self):
        index = session.get('current_index', 0)
        game_cards_id = session.get('game_cards', [])

        if index >= len(game_cards_id):
            return None # Игра закончена

        card_id = game_cards_id[index]
        return card_id

    def check_answer(self, user_answer):
        index = session.get('current_index', 0)
        card_ids = session.get('game_cards', [])
        if index >= len(card_ids):
            return None

        card_id = card_ids[index]
        card_db = repository.get_card_by_id(card_id)

        # проверка ответа
        is_correct = user_answer == card_db.corr_answer
        if is_correct:
            session['correct_answers'] += 1

        # Переход к следующему вопросу
        session['current_index'] += 1
        return is_correct


