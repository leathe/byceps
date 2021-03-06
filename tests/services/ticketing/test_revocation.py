"""

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.services.seating import (
    area_service as seating_area_service,
    seat_service,
)
from byceps.services.ticketing import (
    category_service,
    event_service,
    ticket_creation_service,
    ticket_revocation_service,
    ticket_seat_management_service,
    ticket_service,
)

# Import models to ensure the corresponding tables are created so
# `Seat.assignment` is available.
import byceps.services.seating.models.seat_group

from tests.base import AbstractAppTestCase
from tests.helpers import create_brand, create_party, create_user


class TicketRevocationTestCase(AbstractAppTestCase):

    def setUp(self):
        super().setUp()

        brand = create_brand()
        self.party = create_party(brand_id=brand.id)

        self.category_id = self.create_category('Premium').id
        self.owner_id = create_user('Ticket_Owner').id
        self.admin_id = create_user('Orga').id

    def test_revoke_ticket(self):
        ticket_before = ticket_creation_service.create_ticket(
            self.category_id, self.owner_id
        )
        assert not ticket_before.revoked

        events_before = event_service.get_events_for_ticket(ticket_before.id)
        assert len(events_before) == 0

        # -------------------------------- #

        ticket_id = ticket_before.id

        ticket_revocation_service.revoke_ticket(ticket_id, self.admin_id)

        # -------------------------------- #

        ticket_after = ticket_service.find_ticket(ticket_id)
        assert ticket_after.revoked

        events_after = event_service.get_events_for_ticket(ticket_after.id)
        assert len(events_after) == 1

        ticket_revoked_event = events_after[0]
        assert ticket_revoked_event.event_type == 'ticket-revoked'
        assert ticket_revoked_event.data == {
                'initiator_id': str(self.admin_id),
            }

    def test_revoke_tickets(self):
        tickets_before = ticket_creation_service.create_tickets(
            self.category_id, self.owner_id, 3
        )

        for ticket_before in tickets_before:
            assert not ticket_before.revoked

            events_before = event_service.get_events_for_ticket(
                ticket_before.id
            )
            assert len(events_before) == 0

        # -------------------------------- #

        ticket_ids = {ticket.id for ticket in tickets_before}

        ticket_revocation_service.revoke_tickets(ticket_ids, self.admin_id)

        # -------------------------------- #

        tickets_after = ticket_service.find_tickets(ticket_ids)
        for ticket_after in tickets_after:
            assert ticket_after.revoked

            events_after = event_service.get_events_for_ticket(ticket_after.id)
            assert len(events_after) == 1

            ticket_revoked_event = events_after[0]
            assert ticket_revoked_event.event_type == 'ticket-revoked'
            assert ticket_revoked_event.data == {
                'initiator_id': str(self.admin_id),
            }

    def test_revoke_ticket_with_seat(self):
        area = seating_area_service.create_area(self.party.id, 'main', 'Main')
        seat = seat_service.create_seat(area, 0, 0, self.category_id)

        ticket = ticket_creation_service.create_ticket(
            self.category_id, self.owner_id
        )

        ticket_seat_management_service.occupy_seat(
            ticket.id, seat.id, self.owner_id
        )

        assert ticket.occupied_seat_id == seat.id

        events_before = event_service.get_events_for_ticket(ticket.id)
        event_types_before = {event.event_type for event in events_before}
        assert 'seat-released' not in event_types_before

        # -------------------------------- #

        ticket_revocation_service.revoke_ticket(ticket.id, self.admin_id)

        # -------------------------------- #

        assert ticket.occupied_seat_id is None

        events_after = event_service.get_events_for_ticket(ticket.id)
        event_types_after = {event.event_type for event in events_after}
        assert 'seat-released' in event_types_after

    def test_revoke_tickets_with_seats(self):
        area = seating_area_service.create_area(self.party.id, 'main', 'Main')

        tickets = ticket_creation_service.create_tickets(
            self.category_id, self.owner_id, 2
        )

        ticket_ids = {ticket.id for ticket in tickets}

        for ticket in tickets:
            seat = seat_service.create_seat(area, 0, 0, self.category_id)

            ticket_seat_management_service.occupy_seat(
                ticket.id, seat.id, self.owner_id
            )

            assert ticket.occupied_seat_id == seat.id

        # -------------------------------- #

        ticket_revocation_service.revoke_tickets(ticket_ids, self.admin_id)

        # -------------------------------- #

        for ticket in tickets:
            assert ticket.occupied_seat_id is None

            events_after = event_service.get_events_for_ticket(ticket.id)
            event_types_after = {event.event_type for event in events_after}
            assert 'seat-released' in event_types_after

    # -------------------------------------------------------------------- #
    # helpers

    def create_category(self, title):
        return category_service.create_category(self.party.id, title)
