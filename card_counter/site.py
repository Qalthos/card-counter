from inspect import getmembers, isfunction
import random

from flask import Flask, render_template
import pygal

from card_counter.stats import stat_functions
from card_counter.models import Game, Player

app = Flask(__name__)

@app.route('/')
def overview():
    player_count = Player.query.count()
    game_count = Game.query.count()
    rendered_stats = [function() for function in random.sample(stat_functions, 2)]
    return render_template('index.html', player_count=player_count, game_count=game_count, stats=rendered_stats)


@app.route('/players')
def players():
    return render_template('list.html', items=Player.query.all())


@app.route('/player/<player_id>')
def show_player(player_id):
    player = Player.query.filter_by(id=player_id).one()

    plot = pygal.Box()
    for deal in ['six', 'seven', 'eight', 'nine', 'ten', 'score']:
        plot.add(deal, [getattr(game, deal) for game in player.scores])

    return render_template('player.html', player=player, plot=plot.render(disable_xml_declaration=True))


@app.route('/games')
def games():
    return render_template('list.html', items=Game.query.all())


@app.route('/game/<game_id>')
def show_game(game_id):
    game = Game.query.filter_by(id=game_id).one()
    return render_template('game.html', game=game)
