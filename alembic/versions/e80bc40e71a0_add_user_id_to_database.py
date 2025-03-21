"""add user id to database

Revision ID: e80bc40e71a0
Revises: 214795b15e30
Create Date: 2024-09-10 15:24:17.535802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e80bc40e71a0'
down_revision = '214795b15e30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('database', sa.Column('user_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'database', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'database', type_='foreignkey')
    op.drop_column('database', 'user_id')
    # ### end Alembic commands ###
