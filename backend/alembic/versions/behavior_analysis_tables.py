"""add behavior analysis tables

Revision ID: behavior_001
Revises: a1b2c3d4e5f6
Create Date: 2025-12-02

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'behavior_001'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Create datasets table
    op.create_table(
        'datasets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dataset_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('dataset_type', sa.Enum('criteo', 'hillstrom', 'financial', 'b2b', 'custom', name='datasettype'), nullable=False),
        sa.Column('status', sa.Enum('uploading', 'processing', 'normalizing', 'completed', 'failed', name='datasetstatus'), nullable=True),
        sa.Column('original_filename', sa.String(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('total_records', sa.Integer(), nullable=True),
        sa.Column('treatment_count', sa.Integer(), nullable=True),
        sa.Column('control_count', sa.Integer(), nullable=True),
        sa.Column('churn_rate_treatment', sa.Float(), nullable=True),
        sa.Column('churn_rate_control', sa.Float(), nullable=True),
        sa.Column('schema_mapping', sa.JSON(), nullable=True),
        sa.Column('processing_log', sa.JSON(), nullable=True),
        sa.Column('uploaded_by_user_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['uploaded_by_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datasets_dataset_id'), 'datasets', ['dataset_id'], unique=True)

    # Create behavior_customers table
    op.create_table(
        'behavior_customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('dataset_id', sa.Integer(), nullable=False),
        sa.Column('treatment', sa.Integer(), nullable=False),
        sa.Column('treatment_type', sa.String(), nullable=True),
        sa.Column('outcome', sa.Integer(), nullable=False),
        sa.Column('days_since_last_activity', sa.Float(), nullable=True),
        sa.Column('activity_count_30d', sa.Integer(), nullable=True),
        sa.Column('activity_count_90d', sa.Integer(), nullable=True),
        sa.Column('total_value_30d', sa.Float(), nullable=True),
        sa.Column('total_value_90d', sa.Float(), nullable=True),
        sa.Column('avg_value_per_activity', sa.Float(), nullable=True),
        sa.Column('recency_score', sa.Integer(), nullable=True),
        sa.Column('frequency_score', sa.Integer(), nullable=True),
        sa.Column('monetary_score', sa.Integer(), nullable=True),
        sa.Column('rfm_score', sa.Integer(), nullable=True),
        sa.Column('tenure_days', sa.Integer(), nullable=True),
        sa.Column('engagement_score', sa.Float(), nullable=True),
        sa.Column('activity_trend', sa.Float(), nullable=True),
        sa.Column('feature_usage_count', sa.Integer(), nullable=True),
        sa.Column('session_count_30d', sa.Integer(), nullable=True),
        sa.Column('support_tickets_30d', sa.Integer(), nullable=True),
        sa.Column('satisfaction_score', sa.Float(), nullable=True),
        sa.Column('payment_failures', sa.Integer(), nullable=True),
        sa.Column('account_balance', sa.Float(), nullable=True),
        sa.Column('churn_risk_score', sa.Float(), nullable=True),
        sa.Column('uplift_score', sa.Float(), nullable=True),
        sa.Column('customer_segment', sa.String(), nullable=True),
        sa.Column('clv_estimate', sa.Float(), nullable=True),
        sa.Column('original_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_behavior_customers_customer_id'), 'behavior_customers', ['customer_id'], unique=False)

    # Create customer_behavior_summaries table
    op.create_table(
        'customer_behavior_summaries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('lifecycle_stage', sa.String(), nullable=True),
        sa.Column('customer_type', sa.String(), nullable=True),
        sa.Column('activity_level', sa.String(), nullable=True),
        sa.Column('value_segment', sa.String(), nullable=True),
        sa.Column('engagement_trend', sa.String(), nullable=True),
        sa.Column('preferred_channels', sa.JSON(), nullable=True),
        sa.Column('last_active_days_ago', sa.Integer(), nullable=True),
        sa.Column('avg_frequency_per_month', sa.Float(), nullable=True),
        sa.Column('risk_level', sa.String(), nullable=True),
        sa.Column('risk_indicators', sa.JSON(), nullable=True),
        sa.Column('behavioral_trends', sa.JSON(), nullable=True),
        sa.Column('recommended_interventions', sa.JSON(), nullable=True),
        sa.Column('expected_retention_lift', sa.Float(), nullable=True),
        sa.Column('intervention_roi', sa.Float(), nullable=True),
        sa.Column('summary_text', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['behavior_customers.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('customer_id')
    )

    # Create interventions table
    op.create_table(
        'interventions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('treatment_id', sa.String(), nullable=False),
        sa.Column('intervention_type', sa.String(), nullable=True),
        sa.Column('channel', sa.String(), nullable=True),
        sa.Column('uplift_score', sa.Float(), nullable=True),
        sa.Column('expected_value', sa.Float(), nullable=True),
        sa.Column('roi', sa.Float(), nullable=True),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('message_title', sa.String(), nullable=True),
        sa.Column('message_body', sa.String(), nullable=True),
        sa.Column('message_cta', sa.String(), nullable=True),
        sa.Column('recommended_timing', sa.String(), nullable=True),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('executed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('customer_responded', sa.Integer(), nullable=True),
        sa.Column('customer_retained', sa.Integer(), nullable=True),
        sa.Column('actual_value', sa.Float(), nullable=True),
        sa.Column('widget_config', sa.JSON(), nullable=True),
        sa.Column('ab_test_variant', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['behavior_customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('interventions')
    op.drop_table('customer_behavior_summaries')
    op.drop_index(op.f('ix_behavior_customers_customer_id'), table_name='behavior_customers')
    op.drop_table('behavior_customers')
    op.drop_index(op.f('ix_datasets_dataset_id'), table_name='datasets')
    op.drop_table('datasets')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS datasettype')
    op.execute('DROP TYPE IF EXISTS datasetstatus')
