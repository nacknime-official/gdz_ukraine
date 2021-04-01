from app.models.db import TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    grade = db.Column(db.Integer)
    subject = db.Column(db.String)
    author = db.Column(db.String)
    specification = db.Column(db.String)
    year = db.Column(db.Integer)
    main_topic = db.Column(db.String)
    sub_topic = db.Column(db.String)
    sub_sub_topic = db.Column(db.String)
    exercise = db.Column(db.String)

    is_blocked = db.Column(db.Boolean)
    is_subscribed_to_notifications = db.Column(db.Boolean, default=True)
