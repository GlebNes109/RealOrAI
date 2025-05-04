import uuid
from select import select

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from src.config import settings
from src.models.db_models import UsersDB
from src.utility_services import create_hash

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
                    role="SUPER_ADMIN"
                )
                session.merge(user_db)
                session.commit()

    def add_user(self, login, password):
        with Session(engine) as session:
            user_db = UsersDB(
                id=str(uuid.uuid4()),
                login=login,
                password_hash=create_hash(password)
            )

            session.add(user_db)
            session.commit()