"""empty message

Revision ID: 3c455d7523d5
Revises: ba5c74ad9345
Create Date: 2024-12-15 07:17:12.588463

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3c455d7523d5'
down_revision = 'ba5c74ad9345'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_slot', 'user_event_type_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_slot', 'user_event_type_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###
