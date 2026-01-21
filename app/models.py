from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    elo_score = db.Column(db.Integer, nullable=False, default=1000)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    game_records = db.relationship('GameRecord', backref='player', lazy=True)
    practice_records = db.relationship('PracticeRecord', backref='player', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.elo_score}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class GameRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_type = db.Column(db.String(20), nullable=False)  # 'pvp' or 'ai'
    opponent_id = db.Column(db.Integer, nullable=True)
    opponent_username = db.Column(db.String(20), nullable=True)
    result = db.Column(db.String(10), nullable=False)  # 'win', 'lose', 'draw'
    final_score = db.Column(db.Integer, nullable=False)
    opponent_final_score = db.Column(db.Integer, nullable=False)
    elo_change = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rounds = db.relationship('RoundRecord', backref='game_record', lazy=True)
    
    def __repr__(self):
        return f"GameRecord('{self.game_type}', '{self.result}', '{self.created_at}')"

class RoundRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer, nullable=False)
    problem = db.Column(db.String(100), nullable=False)
    user_guess = db.Column(db.String(100), nullable=False)
    user_correct = db.Column(db.Boolean, nullable=False)
    opponent_guess = db.Column(db.String(100), nullable=False)
    opponent_correct = db.Column(db.Boolean, nullable=False)
    user_damage_dealt = db.Column(db.Float, nullable=False)
    opponent_damage_dealt = db.Column(db.Float, nullable=False)
    game_record_id = db.Column(db.Integer, db.ForeignKey('game_record.id'), nullable=False)
    
    def __repr__(self):
        return f"RoundRecord('{self.round_number}', '{self.problem}')"

class PracticeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    guess_count = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def __repr__(self):
        return f"PracticeRecord('{self.problem}', '{self.difficulty}', '{self.correct}')"
