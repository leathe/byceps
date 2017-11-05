"""
byceps.blueprints.seating.views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2017 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from flask import abort, g

from ...config import get_seat_management_enabled, get_ticket_management_enabled
from ...services.seating import area_service as seating_area_service
from ...util.framework.blueprint import create_blueprint
from ...util.framework.templating import templated


blueprint = create_blueprint('seating', __name__)


@blueprint.route('/')
@templated
def index():
    """List areas."""
    areas = seating_area_service.get_areas_for_party(g.party_id)

    return {
        'areas': areas,
    }


@blueprint.route('/areas/<slug>')
@templated
def view_area(slug):
    """View area."""
    area = seating_area_service.find_area_for_party_by_slug(g.party_id, slug)
    if area is None:
        abort(404)

    seat_management_enabled = get_seat_management_enabled()
    ticket_management_enabled = get_ticket_management_enabled()

    return {
        'area': area,
        'seat_management_enabled': seat_management_enabled,
        'ticket_management_enabled': ticket_management_enabled,
    }
