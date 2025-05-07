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
        # id картинок хранятся в сессии, но правильный ответ для каждой картинки хранится в базе. Сами картинки хранятся в static/user_data/
        game_cards_id = []
        for i in range(3):
            time.sleep(1)
            '''a = random.randint(0, 1)
            if a == 0:
                id = api.get_real_image()
                card_db = CardsDB(
                    id=id,
                    corr_answer=Answer.REAL
                )
                repository.create_new_card(card_db)
                game_cards_id.append(id)

            if a == 211:
                id = api.get_ai_image()
                card_db = CardsDB(
                    id=id,
                    corr_answer=Answer.AI
                )
                repository.create_new_card(card_db)
                game_cards_id.append(id)

            if a == 1:
                random_card = repository.get_random_card()
                id = random_card.id
                game_cards_id.append(id)

            if 1 == 1:
                random_card = repository.get_random_card()
                id = random_card.id
                game_cards_id.append(id)'''

            id = api.get_real_image()
            card_db = CardsDB(
                id=id,
                corr_answer=Answer.REAL
            )
            repository.create_new_card(card_db)
            game_cards_id.append(id)

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


