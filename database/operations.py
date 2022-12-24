from database import get_db
from database.models import User
from database.models import Subject

db = get_db()


def get_user_by_id(user_id):
    return db.query(User).filter(User.id == user_id).first()


def get_user_state(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return None
    return user.state


def set_user_state(user_id, state):
    user = get_user_by_id(user_id)
    if not user:
        user = User(id=user_id, state=state)
        db.add(user)

    user.state = state
    db.commit()

    return user


def add_new_subject(user_id, new_subject):
    subject = Subject(user_id=user_id, name=new_subject)
    db.add(subject)
    db.commit()
    return subject


def get_user_subjects(user_id):
    return db.query(Subject).filter(Subject.user_id == user_id).all()
