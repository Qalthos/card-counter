from flask import Flask, render_template

from card_counter.models import Game, Score

app = Flask(__name__)

@app.route('/')
def overview():
    count = Game.query.count()
    lowest_games = Score.query.order_by(Score.score).limit(5).all()
    highest_games = Score.query.order_by(Score.score.desc()).limit(5).all()
    return render_template('index.html', total=count, low=lowest_games, high=highest_games)


if __name__ == '___main__':
    app.debug = True
    app.run(host='0')
