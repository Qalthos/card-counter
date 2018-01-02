from flask import url_for
from sqlalchemy import Column, ForeignKey, BLOB, Date, Integer, String, func, select, and_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from card_counter.database import Base


class Proof(Base):
    __tablename__ = 'proof'

    id = Column(Integer, primary_key=True)
    image = Column(BLOB)

    games = relationship('Game', back_populates='proof')


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
    player = relationship('Player', back_populates='scores')

    @hybrid_property
    def score(self):
        return sum((self.six, self.seven, self.eight, self.nine, self.ten))

    def __str__(self):
        return "{1} scored {0.score} points: {0.six} {0.seven} {0.eight} {0.nine} {0.ten}".format(self, self.player)


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    date = Column(Date)

    proof_id = Column(Integer, ForeignKey('proof.id'))

    proof = relationship('Proof', back_populates='games')
    scores = relationship('Score', back_populates='game')

    @hybrid_property
    def players(self):
        return [hand.player for hand in self.scores]

    @hybrid_property
    def winning_hand(self):
        lowest_score = min(score.score for score in self.scores)
        return [score for score in self.scores if score.score == lowest_score]

    @winning_hand.expression
    def winning_hand(cls):
        return select([Score]).where(and_(
            Score.game_id == cls.id,
            Score.score == select([func.min(Score.score)]).where(Score.game_id == cls.id).correlate(cls)
        ))

    @hybrid_property
    def winning_player(self):
        return [hand.player for hand in self.winning_hand]

    @winning_player.expression
    def winning_player(cls):
        return select([Player.id]).where(
            Player.id.in_(
                select([Score.player_id]).where(and_(
                    Score.game_id == cls.id,
                    Score.score == select([func.min(Score.score)]).where(Score.game_id == cls.id).correlate(cls)
                ))
            )
        )

    def __str__(self):
        return "<a href='{1}'>{0.date} [{0.id}]</a>".format(self, url_for('show_game', game_id=self.id))


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    scores = relationship('Score', back_populates='player')

    @hybrid_property
    def games(self):
        return [game for game in Game.query.all() if self in game.players]

    @hybrid_property
    def won_games(self):
        return [game for game in Game.query.all() if self in game.winning_player]

    @won_games.expression
    def won_games(cls):
        return select([func.count(Game.id)]).where(
            cls.id.in_(Game.winning_player)
        )


    def __str__(self):
        return "<a href='{1}'>{0.name}</a>".format(self, url_for('show_player', player_id=self.id))