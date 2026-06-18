from flask import Flask, render_template, session

from data.answer_form import AnswerForm
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def func():
    return render_template('main.html')


with open('cities.txt', mode='r', encoding='utf-8') as f:
    cities = []
    for e in f.readlines():
        cities += e.strip().split()


@app.route('/cities', methods=['GET', 'POST'])
def cities_game():
    # Инициализация сессионных данных при первом заходе
    if 'cities_message_list' not in session:
        session['cities_message_list'] = []
    if 'last_word' not in session:
        session['last_word'] = ''

    form = AnswerForm()
    if form.validate_on_submit():
        word = form.answer.data
        # Добавляем сообщение в сессионный список
        session['cities_message_list'].append((word, 0))
        session.modified = True

        word = word.lower().strip()
        last_word = session['last_word']

        if last_word:
            if last_word[-1] in ['ь', 'ы']:
                letter0 = last_word[-2]
            else:
                letter0 = last_word[-1]
        else:
            letter0 = ''

        if letter0 != '' and letter0 != word[0]:
            session['cities_message_list'].append(
                (f'Твой город должен начинаться не на букву "{word[0]}", а на букву "{letter0}".', 1))
            session.modified = True
        else:
            if word[-1] in ['ь', 'ы']:
                letter = word[-2]
            else:
                letter = word[-1]
            words_to_choose = list(filter(lambda x: x[0].lower() == letter, cities))
            if len(words_to_choose) == 0:
                session['cities_message_list'].append((
                    f'Я не знаю городов, которые начинаются на букву "{letter}". Пожалуйста, введи название другого города.',
                    1))
                session.modified = True
            else:
                new_word = random.choice(words_to_choose)
                session['cities_message_list'].append((new_word, 1))
                session['last_word'] = new_word  # Сохраняем в сессию
                session.modified = True

        form.answer.data = ''
        session.modified = True
    return render_template('chat.html',
                           message_list=session['cities_message_list'],
                           form=form,
                           title='Игра в города')


end_game_message = ['покупаю', 'беру', 'покупаю слона', 'куплю', 'куплю слона', 'беру слона', 'возьму', 'возьму слона',
                    'я покупаю слона', 'я беру слона', 'я куплю слона', 'я возьму слона', 'ладно', 'хорошо']


@app.route('/elephant', methods=['GET', 'POST'])
def elephant():
    # Инициализация сессионных данных
    if 'elephant_message_list' not in session:
        session['elephant_message_list'] = [('Привет! Купи слона.', 1)]
    if 'last_elephant_message' not in session:
        session['last_elephant_message'] = ''
    if 'elephant_is_finished' not in session:
        session['elephant_is_finished'] = False

    form = AnswerForm()
    if form.validate_on_submit():
        session['last_elephant_message'] = form.answer.data
        session['elephant_message_list'].append((session['last_elephant_message'], 0))
        if session['last_elephant_message'].lower() in end_game_message:
            session['elephant_message_list'].append(('Молодец! 🐘', 1))
            session['elephant_is_finished'] = True
        else:
            session['elephant_message_list'].append(
                (f'Все говорят "{session["last_elephant_message"]}", а ты купи слона!', 1))
        form.answer.data = ''
    return render_template('chat.html',
                           message_list=session['elephant_message_list'],
                           form=form,
                           title='Купи слона',
                           is_finished=session['elephant_is_finished'])


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
