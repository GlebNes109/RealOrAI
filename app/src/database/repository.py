import uuid
from sqlalchemy import create_engine, func
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session, select

from app.src.config import settings
from app.src.database.db_models import UsersDB, CardsDB
from app.src.utility_services import create_hash

# DATABASE_URL = settings.postgres_url
engine = create_engine(settings.database_url)


class Repository:
    def __init__(self):
        try:
            # SQLModel.metadata.drop_all(engine)
            SQLModel.metadata.create_all(engine)
            self.add_super_admin() # супер админ создается в самом начале

        except Exception as e:
            print(e)

    def add_super_admin(self):
        with Session(engine) as session:
            query = select(UsersDB).where(UsersDB.role == "SUPER_ADMIN")
            res = session.exec(query).first()  # получить айдишник юзера. None если такой нет
            if not res:
                user_id = str(uuid.uuid4())
                user_db = UsersDB(
                    id=user_id,
                    login=settings.admin_login,
                    password_hash=create_hash(settings.admin_password),
                    role="SUPER_ADMIN",
                    rating=1500,
                )
                session.merge(user_db)
                session.commit()

    def add_user(self, login, password):
        try:
            with Session(engine) as session:
                user_db = UsersDB(
                    id=str(uuid.uuid4()),
                    login=login,
                    password_hash=create_hash(password),
                    rating=1500
                )

                session.add(user_db)
                session.commit()
                return True
        except IntegrityError:
            return False

    def get_user(self, login, password):
        with Session(engine) as session:
            query = select(UsersDB).where(UsersDB.login == login, UsersDB.password_hash == create_hash(password))
            user_db = session.exec(query).first()
            if user_db:
                return user_db
            else:
                return None

    def get_user_by_id(self, user_id):
        with Session(engine) as session:
            query = select(UsersDB).where(UsersDB.id == user_id)
            user_db = session.exec(query).first()
            if user_db:
                return user_db
            else:
                return None

    def create_new_card(self, card_db):
        with Session(engine) as session:
            session.add(card_db)
            session.commit()

    def get_random_cards(self, cards):
        with Session(engine) as session:
            users_db = []
            for i in range(cards):
                query = select(CardsDB).order_by(func.random()).limit(1)
                user_db = session.exec(query).first()
                if user_db:
                    users_db.append(user_db)
            return users_db

    def get_card_by_id(self, card_id):
        with Session(engine) as session:
            query = select(CardsDB).where(CardsDB.id == card_id)
            card_db = session.exec(query).first()
            return card_db

    def set_raiting(self, user_id, R_new):
        with Session(engine) as session:
            query = select(UsersDB).where(UsersDB.id == user_id)
            user_db = session.exec(query).first()
            user_db.rating = R_new
            session.commit()
            session.refresh(user_db)

    def get_scoreboard(self, user_id, limit):
        with Session(engine) as session:
            query = select(UsersDB).order_by(UsersDB.rating.desc()).limit(limit)
            users_db = session.exec(query).all()
            curr_user_db = session.exec(select(UsersDB).where(UsersDB.id == user_id)).first()
            scoreboard = []
            flag = False
            for i in range(len(users_db)):
                if users_db[i].id == curr_user_db.id:
                    is_current = True
                else:
                    is_current = False
                if is_current:
                    flag = True
                scoreboard.append({'position' : i, 'login': users_db[i].login, 'rating': users_db[i].rating, 'is_current': is_current})

            if not flag:
                current_player = {'position': -1, 'login': curr_user_db.login, 'rating': curr_user_db.rating, 'is_current': True}
                scoreboard.append(current_player)

            return scoreboard
