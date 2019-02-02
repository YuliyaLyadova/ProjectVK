import argparse
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import sys

sys.path.append("../")

from utils.db_session import engine

Base = declarative_base()


class VKGroupBase(Base):
    __tablename__ = 'vkgroupbase'

    id = sa.Column(sa.Integer(), primary_key=True)
    group_id = sa.Column(sa.Integer())
    group_name = sa.Column(sa.String(100), nullable=True)
    is_closed = sa.Column(sa.Boolean(), default=False)
    is_deactivated = sa.Column(sa.Boolean(), default=False)
    group_type = sa.Column(sa.String(50), nullable=True)
    description = sa.Column(sa.String(1000), nullable=True)
    members_count = sa.Column(sa.Integer(), nullable=True)
    trending = sa.Column(sa.Integer(), nullable=True)
    wall = sa.Column(sa.Integer(), nullable=True)

    def __repr__(self):
        return f"{self.group_name} ({self.group_id}, {self.members_count})"


class GroupMembersBase(Base):
    __tablename__ = 'groupmembersbase'

    id = sa.Column(sa.Integer(), primary_key=True)
    group_id = sa.Column(sa.Integer())
    member_id = sa.Column(sa.Integer())
    first_name = sa.Column(sa.String(100), nullable=True)
    last_name = sa.Column(sa.String(100), nullable=True)
    is_closed = sa.Column(sa.Integer())
    is_deactivated = sa.Column(sa.Integer())
    sex = sa.Column(sa.Integer(), nullable=True)
    bdate = sa.Column(sa.Date(), nullable=True)
    city_id = sa.Column(sa.Integer(), nullable=True)
    city_title = sa.Column(sa.String(100), nullable=True)
    country_id = sa.Column(sa.Integer(), nullable=True)
    country_title = sa.Column(sa.String(100), nullable=True)

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

