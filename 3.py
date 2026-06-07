from flask import Flask, render_template

from data.answer_form import AnswerForm
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
message_list = []
with open('cities.txt', mode='r', encoding='utf-8') as f:
    cities = []
    for e in f.readlines():
        cities += e.strip().split()

last_word = ''


@app.route('/', methods=['GET', 'POST'])
def func():
    global last_word
    form = AnswerForm()
    if form.validate_on_submit():
        word = form.answer.data
        message_list.append((word, 0))
        word = word.lower().strip()
        if last_word:
            if last_word[-1] == 'ь' or last_word[-1] == 'ы':
                letter0 = last_word[-2]
            else:
                letter0 = last_word[-1]
        else:
            letter0 = ''
        if letter0 != '' and letter0 != word[0]:
            message_list.append((f'Твой город должен начинаться не на букву "{word[0]}", а на букву "{letter0}".', 1))
        else:
            if word[-1] == 'ь' or word[-1] == 'ы':
                letter = word[-2]
            else:
                letter = word[-1]
            words_to_choose = list(filter(lambda x: x[0].lower() == letter, cities))
            if len(words_to_choose) == 0:
                message_list.append((
                                    f'Я не знаю городов, которые начинаются на букву "{letter}". Пожалуйста, введи название другого города.',
                                    1))
            else:
                new_word = random.choice(words_to_choose)
                message_list.append((new_word, 1))
                last_word = new_word
        form.answer.data = ''
    return render_template('words_game.html', message_list=message_list, form=form)


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
