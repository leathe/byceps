"""
byceps.services.ticketing.models.category
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ....database import BaseQuery, db, generate_uuid
from ....typing import PartyID
from ....util.instances import ReprBuilder


class CategoryQuery(BaseQuery):

    def for_party(self, party_id: PartyID) -> BaseQuery:
        return self.filter_by(party_id=party_id)


class Category(db.Model):
    """A ticket category."""

    __tablename__ = 'ticket_categories'
    __table_args__ = (
        db.UniqueConstraint('party_id', 'title'),
    )
    query_class = CategoryQuery

    id = db.Column(db.Uuid, default=generate_uuid, primary_key=True)
    party_id = db.Column(db.UnicodeText, db.ForeignKey('parties.id'), index=True, nullable=False)
    title = db.Column(db.UnicodeText, nullable=False)

    def __init__(self, party_id: PartyID, title: str) -> None:
        self.party_id = party_id
        self.title = title

    def __repr__(self) -> str:
        return ReprBuilder(self) \
            .add('id', str(self.id)) \
            .add('party', self.party_id) \
            .add_with_lookup('title') \
            .build()
