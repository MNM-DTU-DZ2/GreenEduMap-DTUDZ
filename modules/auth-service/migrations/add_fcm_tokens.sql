"""Add FCM tokens table

Revision ID: add_fcm_tokens
Revises: 
Create Date: 2025-12-09 10:35:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_fcm_tokens'
down_revision = None  # Update this to previous migration if exists
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create fcm_tokens table."""
    op.create_table(
        'fcm_tokens',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('token', sa.String(length=512), nullable=False),
        sa.Column('device_type', sa.String(length=20), nullable=False, server_default='ios'),
        sa.Column('device_name', sa.String(length=100), nullable=True),
        sa.Column('device_id', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('notification_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('last_used', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token', name='uq_fcm_tokens_token'),
        comment='FCM tokens for push notifications'
    )
    
    # Create indexes
    op.create_index('ix_fcm_tokens_user_id', 'fcm_tokens', ['user_id'])
    op.create_index('ix_fcm_tokens_is_active', 'fcm_tokens', ['is_active'])
    
    # Add foreign key constraint (if users table exists)
    # op.create_foreign_key(
    #     'fk_fcm_tokens_user_id',
    #     'fcm_tokens', 'users',
    #     ['user_id'], ['id'],
    #     ondelete='CASCADE'
    # )


def downgrade() -> None:
    """Drop fcm_tokens table."""
    op.drop_index('ix_fcm_tokens_is_active', table_name='fcm_tokens')
    op.drop_index('ix_fcm_tokens_user_id', table_name='fcm_tokens')
    op.drop_table('fcm_tokens')
