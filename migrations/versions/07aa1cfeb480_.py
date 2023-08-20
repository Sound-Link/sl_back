"""empty message

Revision ID: 07aa1cfeb480
Revises: 
Create Date: 2023-08-20 15:10:56.597517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07aa1cfeb480'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_room_id'), 'room', ['id'], unique=False)
    op.create_index(op.f('ix_room_name'), 'room', ['name'], unique=False)
    op.create_table('chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('user_type', sa.String(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_id'), 'chat', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_chat_id'), table_name='chat')
    op.drop_table('chat')
    op.drop_index(op.f('ix_room_name'), table_name='room')
    op.drop_index(op.f('ix_room_id'), table_name='room')
    op.drop_table('room')
    op.drop_table('user')
    # ### end Alembic commands ###