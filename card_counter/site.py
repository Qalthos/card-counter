from flask import Flask, render_template
from sqlalchemy import desc

from card_counter.database import session
from card_counter.models import Game, Score

app = Flask(__name__)

@app.route('/')
def overview():
    count = session.query(Game).count()
    lowest_games = session.query(Score).order_by(Score.score).limit(5).all()
    highest_games = session.query(Score).order_by(desc(Score.score)).limit(5).all()
    return render_template('index.html', total=count, low=lowest_games, high=highest_games)


if __name__ == '___main__':
    app.debug = True
    app.run(host='0')
