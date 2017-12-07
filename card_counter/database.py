from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///cards.db', convert_unicode=True)
DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
class _Base(object):
    query = DBSession.query_property()

Base = declarative_base(cls=_Base)

def init_db():
    import card_counter.models
    Base.metadata.create_all(engine)
