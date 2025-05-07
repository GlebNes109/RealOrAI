import time
from pathlib import Path

from flask import session, render_template, redirect, url_for, request, flash, jsonify

from app.src.blueprints.game_bp.forms import AnswerForm
from app.src.database.repository import Repository
from app.src.blueprints.game_bp import game_bp
from app.src.services.game_service import GameService

repository = Repository()
game_service = GameService()
@game_bp.route('/game/new') # генерация новой игры
def new_game():
    if 'user_id' in session:
        user_id = session['user_id']
        # user_db = repository.get_user_by_id(user_id)
        game_service.generate_new_game()
        return redirect(url_for('game_bp.game_question'))
    return redirect(url_for('auth_bp.signin'))

@game_bp.route('/game/question')
def game_question():
    form = AnswerForm()
    card_id = game_service.get_current_card()
    BASE_DIR = Path(__file__).resolve().parents[3]
    USER_DATA_DIR = BASE_DIR / 'static/user_data'
    image_url = url_for('user_data', filename=f"{card_id}.jpg")
    if card_id:
        return render_template('gamecards.html', image_path=image_url, form=form)
    else:
        return redirect(url_for('game_bp.game_result'))

@game_bp.route('/game/answer', methods=['POST'])
def game_answer():
    print(request.data)
    try:
        data = request.get_json()
        user_answer = data.get('answer')
        is_correct = game_service.check_answer(user_answer)
        response = {
            "message": "Правильно!" if is_correct else "Неправильно!",
            "is_correct": is_correct
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": f"Ошибка сервера: {str(e)}", "is_correct": False}), 500

@game_bp.route('/game/result')
def game_result():
    correct = session.get('correct_answers', 0)
    incorrect = len(session.get('game_cards')) - correct
    total_questions = len(session.get('game_cards'))
    return render_template('result.html', correct=correct, incorrect=incorrect, total_questions=total_questions)