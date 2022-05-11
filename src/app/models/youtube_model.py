from flask_sqlalchemy_extension.model import SerializeMixin

from app.models import db
from app.models.mixins import TimestampMixin


class VideoPosted(SerializeMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String, nullable=False)
