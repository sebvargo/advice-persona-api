"""empty message

Revision ID: 981937ac9a9e
Revises: a6dde027d21b
Create Date: 2023-01-12 15:13:17.838904

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '981937ac9a9e'
down_revision = 'a6dde027d21b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('user_role',
    sa.Column('user_role_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_role_id', 'user_id')
    )
    op.drop_table('user_roles')
    op.drop_table('roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('role_id', sa.INTEGER(), server_default=sa.text("nextval('roles_role_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('role_id', name='roles_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('user_roles',
    sa.Column('user_role_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], name='user_roles_role_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='user_roles_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_role_id', name='user_roles_pkey')
    )
    op.drop_table('user_role')
    op.drop_table('role')
    # ### end Alembic commands ###