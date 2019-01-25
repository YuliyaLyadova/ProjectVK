import sqlalchemy as sa
import sys
sys.path.append("../")

from sqlalchemy.orm import sessionmaker
from service.base import DATABASE

# an Engine, which the Session will use for connection
# resources
engine = sa.create_engine(sa.engine.url.URL(**DATABASE['default']))

# create a Session
session = sessionmaker(engine)
