"""empty message

Revision ID: 4c763d9cffd4
Revises: 
Create Date: 2024-12-14 17:53:15.940632

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4c763d9cffd4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('user_event_type',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('event_type', sa.String(length=50), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_event_type_id'), 'user_event_type', ['id'], unique=False)
    op.create_index(op.f('ix_user_event_type_user_id'), 'user_event_type', ['user_id'], unique=False)
    op.create_table('user_recurring_slot',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('day', sa.String(length=50), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('recurring_start_date', sa.DateTime(), nullable=False),
    sa.Column('recurring_end_date', sa.DateTime(), nullable=False),
    sa.Column('slot_type', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_recurring_slot_id'), 'user_recurring_slot', ['id'], unique=False)
    op.create_index(op.f('ix_user_recurring_slot_user_id'), 'user_recurring_slot', ['user_id'], unique=False)
    op.create_table('user_slot',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('slot_type', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_slot_id'), 'user_slot', ['id'], unique=False)
    op.create_index(op.f('ix_user_slot_user_id'), 'user_slot', ['user_id'], unique=False)
    op.create_table('user_slot_guest',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('guest_user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('guest_user_role', sa.String(length=25), nullable=False),
    sa.Column('user_slot_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_slot_guest_guest_user_id'), 'user_slot_guest', ['guest_user_id'], unique=False)
    op.create_index(op.f('ix_user_slot_guest_id'), 'user_slot_guest', ['id'], unique=False)
    op.create_index(op.f('ix_user_slot_guest_user_slot_id'), 'user_slot_guest', ['user_slot_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_slot_guest_user_slot_id'), table_name='user_slot_guest')
    op.drop_index(op.f('ix_user_slot_guest_id'), table_name='user_slot_guest')
    op.drop_index(op.f('ix_user_slot_guest_guest_user_id'), table_name='user_slot_guest')
    op.drop_table('user_slot_guest')
    op.drop_index(op.f('ix_user_slot_user_id'), table_name='user_slot')
    op.drop_index(op.f('ix_user_slot_id'), table_name='user_slot')
    op.drop_table('user_slot')
    op.drop_index(op.f('ix_user_recurring_slot_user_id'), table_name='user_recurring_slot')
    op.drop_index(op.f('ix_user_recurring_slot_id'), table_name='user_recurring_slot')
    op.drop_table('user_recurring_slot')
    op.drop_index(op.f('ix_user_event_type_user_id'), table_name='user_event_type')
    op.drop_index(op.f('ix_user_event_type_id'), table_name='user_event_type')
    op.drop_table('user_event_type')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
