import uuid
from sqlalchemy import create_engine, func
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session, select

from app.src.config import settings
from app.src.database.db_models import UsersDB, CardsDB
from app.src.utility_services import create_hash

DATABASE_URL = f"postgresql://{settings.postgres_username}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"
engine = create_engine(DATABASE_URL)


class Repository:
    def __init__(self):
        try:
            # SQLModel.metadata.drop_all(engine)
            SQLModel.metadata.create_all(engine)
            self.add_super_admin()

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
                    score=0,
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
                    score=0
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

    def get_random_card(self):
        with Session(engine) as session:
            query = select(CardsDB).order_by(func.random()).limit(1)
            user_db = session.exec(query).first()
            return user_db

    def get_card_by_id(self, card_id):
        with Session(engine) as session:
            query = select(CardsDB).where(CardsDB.id == card_id)
            card_db = session.exec(query).first()
            return card_db