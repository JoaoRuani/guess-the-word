from flask import Flask, render_template, redirect, url_for, session, request
import spacy
import random

app = Flask(__name__)
app.secret_key = b'9a5c68f5d1bea8b001aa1ec4c54fd91635dc4da54dfb169eca8b2c43c4628711'

nlp = spacy.load("pt_core_news_lg")
import pt_core_news_lg
nlp = pt_core_news_lg.load()
print('Model loaded!')

words = []
with open('game_words.txt', 'r', encoding='utf-8') as file:
    words = [l.replace('\n', '') for l in file.readlines()]

print(f'Words read: {len(words)}!')

@app.route("/")
def index():
    if not session.get('word_to_be_guessed'):
        word = random.choice(words)
        print(f'The keyword is {word}')
        session['word_to_be_guessed'] = word
    return render_template('app.html')

@app.route('/guess',)
def guess():
    if not session.get('word_to_be_guessed'):
        return redirect(url_for('index'))
   
    word_to_be_guessed = session['word_to_be_guessed']
    word_guessed = request.args.get('word')
    if(not word_guessed or word_guessed not in words):
        return 'I don\'t know this word)', 400
    else:
        nlp_word_guessed = nlp(word_guessed)
        nlp_word_to_be_guessed = nlp(word_to_be_guessed)
        similarity = nlp_word_guessed.similarity(nlp_word_to_be_guessed)
        if(similarity == 1):
            session.pop('word_to_be_guessed')
        return str(similarity)

@app.route('/giveup')
def giveup():
    return session.pop('word_to_be_guessed')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404