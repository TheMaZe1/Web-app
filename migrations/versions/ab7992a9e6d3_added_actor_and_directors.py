"""added_actor_and_directors

Revision ID: ab7992a9e6d3
Revises: 49949c124d10
Create Date: 2023-08-27 13:11:56.127470

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'ab7992a9e6d3'
down_revision = '49949c124d10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_actors_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_actors_photo'), ['photo'], unique=True)

    op.create_table('directors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('directors', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_directors_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_directors_photo'), ['photo'], unique=True)

    op.create_table('actor_films',
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('film_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], )
    )
    op.create_table('director_films',
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.Column('film_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['directors.id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('director_films')
    op.drop_table('actor_films')
    with op.batch_alter_table('directors', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_directors_photo'))
        batch_op.drop_index(batch_op.f('ix_directors_name'))

    op.drop_table('directors')
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_actors_photo'))
        batch_op.drop_index(batch_op.f('ix_actors_name'))

    op.drop_table('actors')
    # ### end Alembic commands ###
