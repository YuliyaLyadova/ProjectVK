import sys
import argparse
import sqlalchemy as sa

sys.path.append("..")
from sqlalchemy.ext.declarative import declarative_base

from utils.db_session import engine

Base = declarative_base()


class GroupMembersBase(Base):
    __tablename__ = 'groupmembersbase'

    id = sa.Column(sa.Integer(), primary_key=True)
    group_id= sa.Column(sa.Integer())
    member_id = sa.Column(sa.Integer())
    first_name = sa.Column(sa.String(100), nullable=True)
    last_name = sa.Column(sa.String(100), nullable=True)
    is_closed = sa.Column(sa.Integer())
    is_deactivated = sa.Column(sa.Integer())
    sex = sa.Column(sa.Integer())
    bdate=sa.Column(sa.Date())
    city_id=sa.Column(sa.Integer())
    city_title=sa.Column(sa.String(100), nullable=True)
    country_id=sa.Column(sa.Integer())
    country_title=sa.Column(sa.String(100), nullable=True)
    
    def __repr__(self):
        return f"{self.group_id} ({self.member_id})"



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--add_table", help="Table name needed")
    args = parser.parse_args()
    if args.add_table:
        Base.metadata.tables[args.add_table].create(bind=engine)
    else:
        Base.metadata.create_all(engine)

