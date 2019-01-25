import argparse
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from .db_session import engine

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--add_table", help="Table name needed")
    args = parser.parse_args()
    if args.add_table:
        Base.metadata.tables[args.add_table].create(bind=engine)
    else:
        Base.metadata.create_all(engine)

