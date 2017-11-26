#!/usr/bin/env python
from datetime import datetime

from card_counter.database import session, init_db
from card_counter.models import Game, Score, Player

HANDS = ['six', 'seven', 'eight', 'nine', 'ten']

def input_loop():
    try:
        while True:
            date_str = input("Date: ")
            if not date_str:
                break
            try:
                game_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print('Date must be in YYYY-MM-DD format')
                continue

            game = Game(date=game_date)
            session.add(game)
            while True:
                player_name = input("Player name: ")
                if not player_name:
                    break

                player = session.query(Player).filter(Player.name.like(player_name)).one_or_none()
                if player is None:
                    player = Player(name=player_name)
                    session.add(player)
                while True:
                    scores = [int(x) for x in input("Player scores: ").split()]
                    if len(scores) == 5:
                        print("Total was {}".format(sum(scores)))
                        break
                    print("Need five scores (ex. '30 45 0 120 180')")

                session.add(Score(game=game, player=player, **dict(zip(HANDS, scores))))

            session.commit()

    except KeyboardInterrupt:
        pass


def main():
    init_db()
    input_loop()


if __name__ == '__main__':
    main()
