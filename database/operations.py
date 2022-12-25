from database import get_db
from database.models import User, AdditionalInfo, SubSubject, Records
from database.models import Subject
import pandas as pd

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


def create_add_info(user_id, value, type_=None):
    additional_info = AdditionalInfo(user_id=user_id, value=value, type=type_)
    db.add(additional_info)
    db.commit()
    return additional_info


def get_add_info(user_id):
    return db.query(AdditionalInfo).filter(AdditionalInfo.user_id == user_id).first()


def delete_add_info(info):
    db.delete(info)
    db.commit()


def add_subsubject(user_id, subject, value):
    subsubject = SubSubject(user_id=user_id, subject_id=db.query(Subject).filter(Subject.name == subject).first().id,
                            name=value)
    db.add(subsubject)
    db.commit()
    return subsubject


def add_stat(user_id, subject, subsubject, hours, date, description=None):
    subject_id = db.query(Subject).filter(Subject.name == subject).first().id
    subsubject_id = db.query(SubSubject).filter(SubSubject.name == subsubject).first().id
    record = Records(user_id=user_id, subject_id=subject_id, sub_subject_id=subsubject_id, timedelta=hours, date=date,
                     description=description)
    db.add(record)
    db.commit()


def get_records(user_id, start_date, end_date):
    df = pd.read_sql(db.query(Records, Subject).filter((Records.user_id == user_id) & (Records.subject_id == Subject.id)
                                                       & (Records.date >= start_date) & (
                                                               Records.date <= end_date)).statement, db.bind)

    df = df.drop_duplicates().reset_index()
    df["hours"] = pd.to_timedelta(df["timedelta"].astype(str)).dt.total_seconds() / 3600
    return df


def delete_subject(user_id, subject_name):
    subject = db.query(Subject).filter((Subject.name == subject_name) & (Subject.user_id == user_id)).first()
    db.delete(subject)
    db.commit()
