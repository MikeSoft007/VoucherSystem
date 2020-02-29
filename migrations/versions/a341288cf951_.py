"""empty message

Revision ID: a341288cf951
Revises: 
Create Date: 2020-02-29 11:42:24.267498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a341288cf951'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('register',
    sa.Column('s_n', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pin', sa.String(length=140), nullable=False),
    sa.Column('request_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('s_n'),
    sa.UniqueConstraint('pin')
    )
    op.create_index(op.f('ix_register_request_time'), 'register', ['request_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_register_request_time'), table_name='register')
    op.drop_table('register')
    # ### end Alembic commands ###