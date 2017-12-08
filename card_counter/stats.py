from flask import render_template_string

from card_counter.models import Player, Score

TEMPLATE = '''
<div style="width:50%; float:left;">
  <h2>{{ title }}</h2>
  {% for datum in data %}
  <p>{{ datum|safe }}</p>
  {% endfor %}
</div>
'''

HAND_TEMPLATE = "<a href='{{ url_for('show_player', player_id=hand.player.id) }}'>{{ hand.player.name }}</a> scored " \
    "{{ hand.score }} points: {{ hand.six }} {{ hand.seven }} {{ hand.eight }} {{ hand.nine }} {{ hand.ten }}"

def lowest_scores():
    query = Score.query.order_by(Score.score).limit(5).all()
    rendered_hands = (render_template_string(HAND_TEMPLATE, hand=hand) for hand in query)

    return _render('{} lowest scores'.format(len(query)), rendered_hands)


def highest_scores():
    query = Score.query.order_by(Score.score.desc()).limit(5).all()
    rendered_hands = (render_template_string(HAND_TEMPLATE, hand=hand) for hand in query)

    return _render('{} highest scores'.format(len(query)), rendered_hands)


def winningest_players():
    template = "<a href='{{ url_for('show_player', player_id=player.id) }}'>{{ player.name }}</a> has won " \
        "{{ player.won_games|length }} games"
    players = sorted(Player.query.all(), key=lambda p:len(p.won_games), reverse=True)[:5]
    player_strings = (render_template_string(template, player=player) for player in players)

    return _render('{} winningest players'.format(len(players)), player_strings)


def best_players():
    template = "<a href='{{ url_for('show_player', player_id=player.id) }}'>{{ player.name }}</a> has won " \
            "{{ (100 * player.won_games|length) // player.games|length }}% of games"
    players = sorted(Player.query.all(), key=lambda p:len(p.won_games)/len(p.games), reverse=True)[:5]
    player_strings = (render_template_string(template, player=player) for player in players)

    return _render('{} top players'.format(len(players)), player_strings)


def _render(title, data):
    return render_template_string(TEMPLATE, title=title, data=data)