from inspect import getmembers, isfunction
import random

from flask import Flask, render_template

from card_counter import stats
from card_counter.models import Game, Player

app = Flask(__name__)

@app.route('/')
def overview():
    count = Game.query.count()
    stat_funcs = dict(getmembers(stats, isfunction))
    rendered_stats = {name.replace('_', ' '): function() for name, function in random.sample(stat_funcs.items(), 2)}
    return render_template('index.html', total=count, stats=rendered_stats)

@app.route('/player/<player_id>')
def show_player(player_id):
    player = Player.query.filter_by(id=player_id).one()
    return render_template('player.html', player=player)
