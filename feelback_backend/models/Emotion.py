from .. import db
from .Person import Person
import enum


class EmotionType(enum.Enum):
    Happy = 0
    Sad = 1
    Angry = 2
    Surprised = 3
    Disgusted = 4
    Afraid = 5
    Neutral = 6


class Emotion(db.Model):
    """
    Emotion Model
    """

    __tablename__ = 'emotions'

    frame_number = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(64), primary_key=True)
    emotion = db.Column(db.Enum(EmotionType), nullable=False)

    __table_args__ = (db.ForeignKeyConstraint((person_id, video_id), (Person.id, Person.video_id)), {})

    def __init__(self, frame_number: int, person_id: int, video_id: str, emotion: EmotionType):
        self.frame_number = frame_number
        self.person_id = person_id
        self.video_id = video_id
        self.emotion = emotion

    def __repr__(self):
        return f"<Emotion {self.emotion}>"
