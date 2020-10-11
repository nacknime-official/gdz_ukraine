from app.models.db import TimedBaseModel, db


class Solution(TimedBaseModel):
    __tablename__ = "solutions"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)


class Photo(TimedBaseModel):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    url = db.Column(db.String)
    photo_id = db.Column(db.String)
    solution_id = db.Column(db.Integer, db.ForeignKey("solutions.id"))
