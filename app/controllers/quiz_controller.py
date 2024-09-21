from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from flask_login import login_required, current_user
from app.models.user import User
from app.models.quiz import Quiz as QuizModel
from datetime import datetime, time, timedelta
from wtforms import Form, StringField, IntegerField, DateField, TimeField, FloatField, RadioField, validators
from wtforms.validators import DataRequired, NumberRange, Optional, Length, InputRequired
from sqlalchemy import asc
from sqlalchemy import func

bp = Blueprint('quiz', __name__)

class Quiz(Form):
    question_1 = TimeField('Questão 1', [validators.DataRequired()])
    question_2 = IntegerField('Questão 2', [validators.DataRequired(), validators.NumberRange(min=0)])
    question_3 = TimeField('Questão 3', [validators.DataRequired()])
    question_4 = FloatField('Questão 4', [validators.DataRequired(), validators.NumberRange(min=0, max=24)])
    question_5_a = RadioField('Questão 5a', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_b = RadioField('Questão 5b', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_c = RadioField('Questão 5c', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_d = RadioField('Questão 5d', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_e = RadioField('Questão 5e', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_f = RadioField('Questão 5f', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_g = RadioField('Questão 5g', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_h = RadioField('Questão 5h', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_i = RadioField('Questão 5i', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_5_j_other = StringField('Questão 5j Outro', [Optional(), Length(max=200)])
    question_5_j = RadioField('Questão 5j', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_6 = RadioField('Questão 6', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_7 = RadioField('Questão 7', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_8 = RadioField('Questão 8', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_9 = RadioField('Questão 9', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    question_10 = RadioField('Questão 10', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])


@bp.route('/', methods=['GET'])
@login_required
def index():
    quizzes = QuizModel.query.filter_by(user_id=current_user.id).order_by(asc(QuizModel.created_at)).all()

    chart_data = {
        'labels': [],
        'scores': []
    }
    for quiz in quizzes:
        chart_data['labels'].append(quiz.created_at.strftime('%d/%m/%Y'))
        chart_data['scores'].append(quiz.overall_score)

    min_score = db.session.query(
            QuizModel.id,
            QuizModel.overall_score,
            QuizModel.created_at
        ).filter(
            QuizModel.user_id == current_user.id
        ).order_by(
            QuizModel.overall_score.asc(),
            QuizModel.created_at.asc()
        ).first()

    max_score = db.session.query(
        QuizModel.id,
            QuizModel.overall_score,
            QuizModel.created_at
        ).filter(
            QuizModel.user_id == current_user.id
        ).order_by(
            QuizModel.overall_score.desc(),
            QuizModel.created_at.desc()
        ).first()


    return render_template('quiz/index.html', quizzes=quizzes, title="Seus questionários", chart_data=chart_data, min_score=min_score, max_score=max_score)

@bp.route('/quiz', methods=['GET'])
@login_required
def quiz():
    title="ÍNDICE DA QUALIDADE DO SONO DE PITTSBURGH – (PSQI-BR)"
    return render_template('quiz/quiz.html', title=title)


@bp.route('/quiz', methods=['POST'])
@login_required
def create_quiz():
    form = Quiz(request.form)

    if form.validate():

        subjective_sleep_quality = int(form.question_6.data)
        sleep_latency = 0
        if int(form.question_2.data) <= 15:
            sleep_latency = 0
        elif int(form.question_2.data) > 15 and int(form.question_2.data) <= 30:
            sleep_latency = 1
        elif int(form.question_2.data) > 30 and int(form.question_2.data) <= 60:
            sleep_latency = 2
        else:
            sleep_latency = 3

        sleep_latency += int(form.question_5_a.data)

        if sleep_latency >= 1 and sleep_latency < 3:
            sleep_latency = 1
        elif sleep_latency >= 3 and sleep_latency < 5:
            sleep_latency = 2
        elif sleep_latency >= 5 and sleep_latency < 7:
            sleep_latency = 3
        else:
            sleep_latency = 0

        sleep_duration = 0
        if float(form.question_4.data) > 7:
            sleep_duration = 0
        elif float(form.question_4.data) >= 6 and float(form.question_4.data) <= 7:
            sleep_duration = 1
        elif float(form.question_4.data) >= 5 and float(form.question_4.data) < 6:
            sleep_duration = 2
        else:
            sleep_duration = 3

        dt1 = datetime.combine(datetime.min, form.question_1.data)
        dt2 = datetime.combine(datetime.min, form.question_3.data)
        time_diff = dt2 - dt1

        if time_diff.days < 0:
            time_diff = timedelta(days=1) + time_diff

        hours_in_bed = round(time_diff.total_seconds() / 3600, 2)
        habitual_sleep_efficiency = (float(form.question_4.data) / hours_in_bed) * 100

        if habitual_sleep_efficiency >= 85:
            habitual_sleep_efficiency = 0
        elif habitual_sleep_efficiency < 85 and habitual_sleep_efficiency >= 75:
            habitual_sleep_efficiency = 1
        elif habitual_sleep_efficiency < 75 and habitual_sleep_efficiency >= 65:
            habitual_sleep_efficiency = 2
        elif habitual_sleep_efficiency < 65:
            habitual_sleep_efficiency = 3

        sleep_disorders = int(form.question_5_b.data) + int(form.question_5_c.data) + int(form.question_5_d.data) + int(form.question_5_e.data) + int(form.question_5_f.data) + int(form.question_5_g.data) + int(form.question_5_h.data) + int(form.question_5_i.data) + int(form.question_5_j.data)

        if sleep_disorders >= 1 and sleep_disorders < 10:
            sleep_disorders = 1
        elif sleep_disorders >= 10 and sleep_disorders < 19:
            sleep_disorders = 2
        elif sleep_disorders >= 19 and sleep_disorders < 28:
            sleep_disorders = 3
        else:
            sleep_disorders = 0

        use_of_sleeping_pills = int(form.question_7.data)

        daytime_dysfunction = int(form.question_8.data) + int(form.question_9.data)

        if daytime_dysfunction >= 1 and daytime_dysfunction < 3:
            daytime_dysfunction = 1
        elif daytime_dysfunction >= 3 and daytime_dysfunction < 5:
            daytime_dysfunction = 2
        elif daytime_dysfunction >= 5 and daytime_dysfunction < 7:
            daytime_dysfunction = 3
        else:
            daytime_dysfunction = 0


        overall_score = subjective_sleep_quality + sleep_latency + sleep_duration + habitual_sleep_efficiency + sleep_disorders + use_of_sleeping_pills + daytime_dysfunction

        try:
            new_quiz = QuizModel(
                user_id=current_user.id,
                question_1=form.question_1.data,
                question_2=form.question_2.data,
                question_3=form.question_3.data,
                question_4=form.question_4.data,
                question_5_a=form.question_5_a.data,
                question_5_b=form.question_5_b.data,
                question_5_c=form.question_5_c.data,
                question_5_d=form.question_5_d.data,
                question_5_e=form.question_5_e.data,
                question_5_f=form.question_5_f.data,
                question_5_g=form.question_5_g.data,
                question_5_h=form.question_5_h.data,
                question_5_i=form.question_5_i.data,
                question_5_j=form.question_5_j.data,
                question_5_j_other=form.question_5_j_other.data,
                question_6=form.question_6.data,
                question_7=form.question_7.data,
                question_8=form.question_8.data,
                question_9=form.question_9.data,
                question_10=form.question_10.data,
                subjective_sleep_quality=subjective_sleep_quality,
                sleep_latency=sleep_latency,
                sleep_duration=sleep_duration,
                habitual_sleep_efficiency=habitual_sleep_efficiency,
                sleep_disorders=sleep_disorders,
                use_of_sleeping_pills=use_of_sleeping_pills,
                daytime_dysfunction=daytime_dysfunction,
                overall_score=overall_score
            )

            db.session.add(new_quiz)
            db.session.commit()

            flash('Quiz salvo com sucesso!', 'success')
            return redirect(url_for('quiz.get_quiz', id=new_quiz.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar o quiz: {str(e)}', 'error')
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro no campo {field}: {error}', 'error')

    return render_template('quiz/quiz.html', form=form)


@bp.route('/quiz/<int:id>', methods=['GET'])
@login_required
def get_quiz(id):
    quiz = QuizModel.query.filter_by(id=id, user_id=current_user.id).first()
    if quiz:
        title="Quizz ID: " + str(quiz.id)
        return render_template('quiz/result.html', quiz=quiz, title=title)
    else:
        flash('Quiz não encontrado', 'error')
        return redirect(url_for('quiz.index'))