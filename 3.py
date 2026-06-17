from flask import Flask, render_template

from data.answer_form import AnswerForm
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def func():
    return render_template('main.html')


cities_message_list = []
with open('cities.txt', mode='r', encoding='utf-8') as f:
    cities = []
    for e in f.readlines():
        cities += e.strip().split()
last_word = ''


@app.route('/cities', methods=['GET', 'POST'])
def cities_game():
    global last_word
    form = AnswerForm()
    if form.validate_on_submit():
        word = form.answer.data
        cities_message_list.append((word, 0))
        word = word.lower().strip()
        if last_word:
            if last_word[-1] == 'ь' or last_word[-1] == 'ы':
                letter0 = last_word[-2]
            else:
                letter0 = last_word[-1]
        else:
            letter0 = ''
        if letter0 != '' and letter0 != word[0]:
            cities_message_list.append(
                (f'Твой город должен начинаться не на букву "{word[0]}", а на букву "{letter0}".', 1))
        else:
            if word[-1] == 'ь' or word[-1] == 'ы':
                letter = word[-2]
            else:
                letter = word[-1]
            words_to_choose = list(filter(lambda x: x[0].lower() == letter, cities))
            if len(words_to_choose) == 0:
                cities_message_list.append((
                    f'Я не знаю городов, которые начинаются на букву "{letter}". Пожалуйста, введи название другого города.',
                    1))
            else:
                new_word = random.choice(words_to_choose)
                cities_message_list.append((new_word, 1))
                last_word = new_word
        form.answer.data = ''
    return render_template('chat.html', message_list=cities_message_list, form=form, title='Игра в города')


elephant_message_list = [('Привет! Купи слона.', 1)]
last_elephant_message = ''
end_game_message = ['покупаю', 'беру', 'покупаю слона', 'куплю', 'куплю слона', 'беру слона', 'возьму', 'возьму слона',
                    'я покупаю слона', 'я беру слона', 'я куплю слона', 'я возьму слона', 'ладно', 'хорошо']
elephant_is_finished = False


@app.route('/elephant', methods=['GET', 'POST'])
def elephant():
    global last_elephant_message
    global elephant_is_finished
    form = AnswerForm()
    if form.validate_on_submit():
        last_elephant_message = form.answer.data
        elephant_message_list.append((last_elephant_message, 0))
        if last_elephant_message.lower() in end_game_message:
            elephant_message_list.append(('Молодец! 🐘', 1))
            elephant_is_finished = True
        else:
            elephant_message_list.append((f'Все говорят "{last_elephant_message}", а ты купи слона!', 1))
        form.answer.data = ''
    return render_template('chat.html', message_list=elephant_message_list, form=form, title='Купи слона',
                           is_finished=elephant_is_finished)


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
