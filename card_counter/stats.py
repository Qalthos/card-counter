from card_counter.models import Score


def lowest_scores():
    return Score.query.order_by(Score.score).limit(5).all()

def highest_scores():
    return Score.query.order_by(Score.score.desc()).limit(5).all()
