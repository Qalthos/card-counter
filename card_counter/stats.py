from flask import render_template_string

from card_counter.models import Game, Player, Score


def _render(title, data):
    template = '''
<h2>{{ title }}</h2>
{% for datum in data %}
<p>{{ datum|safe }}</p>
{% endfor %}
'''
    return render_template_string(template, title=title.format(len(data)), data=data)

def lowest_scores():
    scores = Score.query.order_by(Score.score).limit(5).all()
    return _render('{} lowest scores', scores)


def highest_scores():
    scores = Score.query.order_by(Score.score.desc()).limit(5).all()
    return _render('{} highest scores', scores)


def winningest_players():
    template = "{{ player|safe }} has won {{ player.won_games|length }} games"
    players = sorted(Player.query.all(), key=lambda p:len(p.won_games), reverse=True)[:5]
    player_strings = [render_template_string(template, player=player) for player in players]

    return _render('{} winningest players', player_strings)


def best_players():
    template = "{{ player|safe }} has won {{ (100 * player.won_games|length) // player.games|length }}% of games"
    players = sorted(Player.query.all(), key=lambda p:len(p.won_games)/len(p.games), reverse=True)[:5]
    player_strings = [render_template_string(template, player=player) for player in players]

    return _render('{} top players', player_strings)


def recent_games():
    games = Game.query.order_by(Game.date.desc()).limit(5).all()
    return _render('{} most recent games', games)