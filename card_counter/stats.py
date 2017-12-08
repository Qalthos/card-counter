from flask import render_template_string

from card_counter.models import Game, Score

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
    rendered_hands = [render_template_string(HAND_TEMPLATE, hand=hand) for hand in query]
    return render_template_string(TEMPLATE, title=f'{len(query)} lowest scores', data=rendered_hands)


def highest_scores():
    query = Score.query.order_by(Score.score.desc()).limit(5).all()
    rendered_hands = [render_template_string(HAND_TEMPLATE, hand=hand) for hand in query]
    return render_template_string(TEMPLATE, title=f'{len(query)} highest scores', data=rendered_hands)