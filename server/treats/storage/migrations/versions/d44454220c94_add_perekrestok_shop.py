"""Add Perekrestok shop

Revision ID: d44454220c94
Revises: 91251af51314
Create Date: 2022-10-07 23:23:16.181409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd44454220c94'
down_revision = '1a2e31dc5241'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO shops (title, display_title, url_rule) 
        VALUES ('perekrestok', 'Перекресток', '^https://(w{3}\.)?perekrestok\.ru/cat/.+$')
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM shops where title = 'perekrestok'
        """
    )
