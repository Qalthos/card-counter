import itertools

from flask import render_template_string

from card_counter.models import Game, Player, Score


WIN_TEMPLATE = '{{{{ item|safe }}}} has won {0} games'

def _render(title, data):
    template = '''
<h2>{{ title }}</h2>
{% for datum in data %}
<p>{{ datum|safe }}</p>
{% endfor %}
'''
    return render_template_string(template, title=title.format(len(data)), data=data)


def _custom_render(title, item_template, iterable):
    data = [render_template_string(item_template, item=item) for item in iterable][:5]
    return _render(title, data)


stat_functions = [
    lambda : _render('{} lowest scores', Score.query.order_by(Score.score).limit(5).all()),
    lambda : _render('{} highest scores', Score.query.order_by(Score.score.desc()).limit(5).all()),
    lambda : _custom_render('{} winningest players', WIN_TEMPLATE.format("{{ item.won_games|length }}"),
                            sorted(Player.query.all(), key=lambda p:len(p.won_games), reverse=True)),
    lambda : _custom_render('{} top players', WIN_TEMPLATE.format("{{ 100 * item.won_games|length // item.games|length }}% of"),
                            sorted(Player.query.all(), key=lambda p:len(p.won_games)/len(p.games), reverse=True)),
    lambda : _render('{} most recent games', Game.query.order_by(Game.date.desc()).limit(5).all()),
    lambda : _render('{} lowest losing scores', list(itertools.islice(lowest_losing_hands(), 5))),
]

def lowest_losing_hands():
    winners = Game.query.values(Game.winning_hand)
    winners = [score for scores in winners for score in scores]
    scores = Score.query.order_by(Score.score.asc())
    for score in scores.all():
        if score.id not in winners:
            yield score
