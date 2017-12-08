from inspect import getmembers, isfunction
import random

from flask import Flask, render_template

from card_counter import stats
from card_counter.models import Game, Player

app = Flask(__name__)

@app.route('/')
def overview():
    count = Game.query.count()
    rendered_stats = random.sample((
        stats.lowest_scores(),
        stats.highest_scores(),
        stats.winningest_players(),
        stats.best_players(),
        stats.recent_games(),
    ), 2)
    return render_template('index.html', total=count, stats=rendered_stats)

@app.route('/player/<player_id>')
def show_player(player_id):
    player = Player.query.filter_by(id=player_id).one()
    return render_template('player.html', player=player)

@app.route('/game/<game_id>')
def show_game(game_id):
    game = Game.query.filter_by(id=game_id).one()
    return render_template('game.html', game=game)
