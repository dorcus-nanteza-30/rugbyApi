
from app.extensions import db

class TeamMember(db.Model):
    __tablename__ = "teammembers"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    position_of_player = db.Column(db.String(50), nullable=False)
    jersey_number_of_player = db.Column(db.String(30), unique=True, nullable=False)
    biography_of_player = db.Column(db.String(255), nullable=False)
    image_of_player = db.Column(db.Text, nullable=False)

    # relationships
    user = db.relationship("User", back_populates="team_members")
    event = db.relationship("Event", back_populates="participants")

    def __init__(self, user_id, event_id, position_of_player, jersey_number_of_player, biography_of_player, image_of_player):
        self.user_id = user_id
        self.event_id = event_id
        self.position_of_player = position_of_player
        self.jersey_number_of_player = jersey_number_of_player
        self.biography_of_player = biography_of_player
        self.image_of_player = image_of_player

    def get_full_name(self):
        return f'{self.position_of_player} {self.jersey_number_of_player}'
