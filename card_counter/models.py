from sqlalchemy import Column, ForeignKey, BLOB, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from card_counter.database import Base


class Proof(Base):
    __tablename__ = 'proof'

    id = Column(Integer, primary_key=True)
    image = Column(BLOB)

    games = relationship('Game', back_populates='proof')


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    date = Column(Date)

    proof_id = Column(Integer, ForeignKey('proof.id'))

    proof = relationship('Proof', back_populates='games')
    scores = relationship('Score', back_populates='game')

    @hybrid_property
    def winning_hand(self):
        lowest_score = min(score.score for score in self.scores)
        return [score for score in self.scores if score.score == lowest_score]

    @hybrid_property
    def winning_player(self):
        return [hand.player for hand in self.winning_hand]

    def __str__(self):
        return '\n'.join((str(score) for score in self.scores))


class Score(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True)
    six = Column(Integer)
    seven = Column(Integer)
    eight = Column(Integer)
    nine = Column(Integer)
    ten = Column(Integer)

    game_id = Column(Integer, ForeignKey('game.id'))
    player_id = Column(Integer, ForeignKey('player.id'))

    game = relationship('Game', back_populates='scores')
    player = relationship('Player')

    @hybrid_property
    def score(self):
        return sum((self.six, self.seven, self.eight, self.nine, self.ten))

    def __str__(self):
        return "{0.player.name} scored {0.score} points: {0.six} {0.seven} {0.eight} {0.nine} {0.ten}".format(self)


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    @hybrid_property
    def won_games(self):
        return [game for game in Game.query.all() if self in game.winning_player]