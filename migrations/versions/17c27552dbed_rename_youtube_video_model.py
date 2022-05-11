"""rename youtube video model

Revision ID: 17c27552dbed
Revises: dfcd2e67d259
Create Date: 2022-04-18 13:29:37.342247

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '17c27552dbed'
down_revision = 'dfcd2e67d259'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video_posted',
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('youtube_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('videos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('videos',
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='videos_pkey')
    )
    op.drop_table('video_posted')
    # ### end Alembic commands ###