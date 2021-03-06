"""
:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from byceps.services.user_badge import (
    command_service as badge_command_service,
    service as badge_service,
)
from byceps.services.user_badge.transfer.models import QuantifiedBadgeAwarding


def test_award_badge(api_client, api_client_authz_header, user, admin):
    badge = badge_command_service.create_badge(
        'supporter', 'Supporter', 'supporter.svg'
    )

    before = badge_service.get_awardings_of_badge(badge.id)
    assert before == set()

    url = f'/api/user_badges/awardings'
    headers = [api_client_authz_header]
    json_data = {
        'badge_slug': 'supporter',
        'user_id': str(user.id),
        'initiator_id': str(admin.id),
    }

    response = api_client.post(url, headers=headers, json=json_data)
    assert response.status_code == 204

    actual = badge_service.get_awardings_of_badge(badge.id)
    assert actual == {QuantifiedBadgeAwarding(badge.id, user.id, 1)}
