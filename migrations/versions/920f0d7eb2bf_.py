"""empty message

Revision ID: 920f0d7eb2bf
Revises: 9700280fdd33
Create Date: 2023-10-02 13:39:32.397222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '920f0d7eb2bf'
down_revision = '9700280fdd33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat', 'user_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('user_type', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###
