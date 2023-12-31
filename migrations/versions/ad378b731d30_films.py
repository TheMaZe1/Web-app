"""films

Revision ID: ad378b731d30
Revises: 110a6d56e8ce
Create Date: 2023-08-16 16:11:42.020618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad378b731d30'
down_revision = '110a6d56e8ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('films',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('films', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_films_name'), ['name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('films', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_films_name'))

    op.drop_table('films')
    # ### end Alembic commands ###
