"""empty message

Revision ID: d8c391ef0714
Revises: 23d4fe10b58d
Create Date: 2020-03-05 06:54:04.330889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8c391ef0714'
down_revision = '23d4fe10b58d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_register_request_time', table_name='register')
    op.drop_table('register')
    op.drop_index('ix_users_username', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.create_table('register',
    sa.Column('s_n', sa.INTEGER(), nullable=False),
    sa.Column('pin', sa.VARCHAR(length=140), nullable=False),
    sa.Column('request_time', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('s_n'),
    sa.UniqueConstraint('pin')
    )
    op.create_index('ix_register_request_time', 'register', ['request_time'], unique=False)
    # ### end Alembic commands ###
