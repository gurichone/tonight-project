"""empty message

Revision ID: 144fd69d04cb
Revises: 766c753258ad
Create Date: 2024-10-29 00:32:01.327961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '144fd69d04cb'
down_revision = '766c753258ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('class_num', sa.String(length=4), nullable=False),
    sa.Column('course_name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('class_num')
    )
    op.create_table('score',
    sa.Column('score_id', sa.String(), nullable=False),
    sa.Column('class_num', sa.Integer(), nullable=True),
    sa.Column('student_num', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.String(), nullable=True),
    sa.Column('subject_name', sa.String(), nullable=True),
    sa.Column('attend_day', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('score_id')
    )
    op.create_table('student',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('student_name', sa.String(), nullable=True),
    sa.Column('student_email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('entrollment_year', sa.Integer(), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('school_name', sa.String(), nullable=True),
    sa.Column('course_name', sa.String(), nullable=True),
    sa.Column('class_num', sa.Integer(), nullable=True),
    sa.Column('icon_path', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_student_student_email'), ['student_email'], unique=True)
        batch_op.create_index(batch_op.f('ix_student_student_name'), ['student_name'], unique=False)

    op.create_table('subject',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('subject_id', sa.String(length=10), nullable=False),
    sa.Column('subject_name', sa.String(length=20), nullable=False),
    sa.Column('course_name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teacher',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('teacher_name', sa.String(), nullable=True),
    sa.Column('teacher_email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('class_num', sa.String(), nullable=True),
    sa.Column('icon_path', sa.String(), nullable=True),
    sa.Column('authority', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_teacher_teacher_email'), ['teacher_email'], unique=True)
        batch_op.create_index(batch_op.f('ix_teacher_teacher_name'), ['teacher_name'], unique=False)

    op.create_table('submission',
    sa.Column('submission_id', sa.String(), nullable=False),
    sa.Column('submission_name', sa.String(), nullable=False),
    sa.Column('subject_id', sa.String(), nullable=False),
    sa.Column('course_name', sa.String(), nullable=False),
    sa.Column('submission_type', sa.String(), nullable=False),
    sa.Column('submissin_rimit', sa.DateTime(), nullable=False),
    sa.Column('scoreing_type', sa.Integer(), nullable=False),
    sa.Column('question_file', sa.String(), nullable=True),
    sa.Column('testcase_file', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['course_name'], ['course.course_name'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.subject_id'], ),
    sa.PrimaryKeyConstraint('submission_id')
    )
    op.create_table('submission_situation',
    sa.Column('submission_id', sa.String(), nullable=False),
    sa.Column('student_id', sa.String(), nullable=False),
    sa.Column('point', sa.Integer(), nullable=True),
    sa.Column('submitted', sa.Boolean(), nullable=False),
    sa.Column('file', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.submission_id'], ),
    sa.PrimaryKeyConstraint('submission_id')
    )
    op.drop_table('events')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('ix_users_email')
        batch_op.drop_index('ix_users_username')

    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('ix_users_username', ['username'], unique=False)
        batch_op.create_index('ix_users_email', ['email'], unique=1)

    op.create_table('events',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('event', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('submission_situation')
    op.drop_table('submission')
    with op.batch_alter_table('teacher', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_teacher_teacher_name'))
        batch_op.drop_index(batch_op.f('ix_teacher_teacher_email'))

    op.drop_table('teacher')
    op.drop_table('subject')
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_student_student_name'))
        batch_op.drop_index(batch_op.f('ix_student_student_email'))

    op.drop_table('student')
    op.drop_table('score')
    op.drop_table('course')
    # ### end Alembic commands ###
