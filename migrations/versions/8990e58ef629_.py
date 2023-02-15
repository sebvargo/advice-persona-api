"""empty message

Revision ID: 8990e58ef629
Revises: 
Create Date: 2023-01-13 13:21:31.590537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8990e58ef629'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entity',
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('entity_id')
    )
    op.create_table('persona',
    sa.Column('persona_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('persona_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('role_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tag',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('advice',
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('persona_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('adviceslip_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['persona_id'], ['persona.persona_id'], ),
    sa.PrimaryKeyConstraint('entity_id')
    )
    op.create_table('entity_comment',
    sa.Column('comment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id', 'entity_id')
    )
    with op.batch_alter_table('entity_comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_entity_comment_content'), ['content'], unique=False)

    op.create_table('entity_like',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'entity_id')
    )
    op.create_table('entity_tag',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.tag_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'entity_id')
    )
    op.create_table('entity_view',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['entity.entity_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'entity_id')
    )
    op.create_table('user_role',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.create_table('entity_comment_like',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['comment_id', 'entity_id'], ['entity_comment.comment_id', 'entity_comment.entity_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'comment_id', 'entity_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entity_comment_like')
    op.drop_table('user_role')
    op.drop_table('entity_view')
    op.drop_table('entity_tag')
    op.drop_table('entity_like')
    with op.batch_alter_table('entity_comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_entity_comment_content'))

    op.drop_table('entity_comment')
    op.drop_table('advice')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('tag')
    op.drop_table('role')
    op.drop_table('persona')
    op.drop_table('entity')
    # ### end Alembic commands ###
