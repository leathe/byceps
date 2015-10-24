# -*- coding: utf-8 -*-

"""
byceps.blueprints.ticket.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2015 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from ...database import db

from ..party.models import Party
from ..seating.models import Category

from .models import Ticket


def find_ticket_for_user(user, party):
    """Return the ticket used by the user for the party, or `None` if not
    found.
    """
    if user.is_anonymous:
        return None

    return Ticket.query \
        .filter(Ticket.used_by == user) \
        .options(
            db.joinedload('occupied_seat').joinedload('area'),
        ) \
        .for_party(party) \
        .first()


def get_attended_parties(user):
    """Return the parties the user has attended."""
    return Party.query \
        .join(Category).join(Ticket).filter(Ticket.used_by == user) \
        .all()
