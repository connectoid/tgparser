from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import db_settings
from .models import Base, User, BlockedUser

engine = create_engine(db_settings.URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_user(tg_id, username):
    session = Session()
    user = session.query(User).filter(User.tg_id == str(tg_id)).first()
    if user is None:
        new_user = User(tg_id=tg_id, username=username)
        session.add(new_user)
        session.commit()
        return 1
    else:
        return -1

def get_admins():
    session = Session()
    users = session.query(User).filter_by(admin=True).all()
    return users

def check_premium(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == str(tg_id)).first()
    if user.premium == True or user.admin == True:
        return 1
    else:
        return -1