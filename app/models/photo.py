from app.models.db import TimedBaseModel, db


class Photo(TimedBaseModel):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    photo_id = db.Column(db.String)
