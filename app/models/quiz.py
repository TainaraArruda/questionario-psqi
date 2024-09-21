from app import db
from datetime import datetime

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Questões 1-4
    question_1 = db.Column(db.Time, nullable=False)
    question_2 = db.Column(db.Integer, nullable=False)
    question_3 = db.Column(db.Time, nullable=False)
    question_4 = db.Column(db.Float, nullable=False)

    # Questão 5 (a-j)
    question_5_a = db.Column(db.Integer, nullable=False)
    question_5_b = db.Column(db.Integer, nullable=False)
    question_5_c = db.Column(db.Integer, nullable=False)
    question_5_d = db.Column(db.Integer, nullable=False)
    question_5_e = db.Column(db.Integer, nullable=False)
    question_5_f = db.Column(db.Integer, nullable=False)
    question_5_g = db.Column(db.Integer, nullable=False)
    question_5_h = db.Column(db.Integer, nullable=False)
    question_5_i = db.Column(db.Integer, nullable=False)
    question_5_j = db.Column(db.Integer, nullable=False)
    question_5_j_other = db.Column(db.String(200))

    # Questões 6-10
    question_6 = db.Column(db.Integer, nullable=False)
    question_7 = db.Column(db.Integer, nullable=False)
    question_8 = db.Column(db.Integer, nullable=False)
    question_9 = db.Column(db.Integer, nullable=False)
    question_10 = db.Column(db.Integer, nullable=False)

    # Resultado do PSQI
    subjective_sleep_quality = db.Column(db.Integer, nullable=True)
    sleep_latency = db.Column(db.Integer, nullable=True)
    sleep_duration = db.Column(db.Integer, nullable=True)
    habitual_sleep_efficiency = db.Column(db.Integer, nullable=True)
    sleep_disorders = db.Column(db.Integer, nullable=True)
    use_of_sleeping_pills = db.Column(db.Integer, nullable=True)
    daytime_dysfunction = db.Column(db.Integer, nullable=True)
    overall_score = db.Column(db.Integer, nullable=True)


    # Relacionamento com o usuário
    user = db.relationship('User', back_populates='quizzes')

    def __repr__(self):
        return f'<Quiz {self.id} for User {self.user_id}>'