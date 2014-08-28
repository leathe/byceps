# -*- coding: utf-8 -*-

from byceps.blueprints.brand.models import Brand
from byceps.blueprints.orga.models import OrgaFlag, OrgaTeam, \
    Membership as OrgaTeamMembership
from byceps.blueprints.party.models import Party
from byceps.blueprints.seating.models import Area as SeatingArea, \
    Category as SeatingCategory, Point, Seat
from byceps.blueprints.terms.models import Version as TermsVersion
from byceps.blueprints.user.models import User
from byceps.blueprints.user_group.models import UserGroup

from .util import add_to_database


# -------------------------------------------------------------------- #
# brands


@add_to_database
def create_brand(id, title):
    return Brand(id=id, title=title)


def get_brand(id):
    return Brand.query.get(id)


# -------------------------------------------------------------------- #
# parties


@add_to_database
def create_party(**kwargs):
    return Party(**kwargs)


def get_party(id):
    return Party.query.get(id)


# -------------------------------------------------------------------- #
# users


@add_to_database
def create_user(screen_name, email_address, password, *, enabled=False):
    user = User.create(screen_name, email_address, password)
    user.enabled = enabled
    return user


def get_user(screen_name):
    return User.query.filter_by(screen_name=screen_name).one()


# -------------------------------------------------------------------- #
# orga teams


@add_to_database
def promote_orga(brand, user):
    return OrgaFlag(brand=brand, user=user)


@add_to_database
def create_orga_team(id, title):
    return OrgaTeam(id=id, title=title)


@add_to_database
def assign_user_to_orga_team(user, orga_team, party):
    return OrgaTeamMembership(orga_team=orga_team, party=party, user=user)


# -------------------------------------------------------------------- #
# user groups


@add_to_database
def create_user_group(creator, title, description=None):
    return UserGroup(creator, title, description)


# -------------------------------------------------------------------- #
# terms


@add_to_database
def create_terms_version(brand, creator, body):
    return TermsVersion(brand=brand, creator=creator, body=body)


# -------------------------------------------------------------------- #
# seating


@add_to_database
def create_seating_area(party, title):
    return SeatingArea(party=party, title=title)


@add_to_database
def create_seat_category(party, title):
    return SeatingCategory(party=party, title=title)


@add_to_database
def create_seat(area, coord_x, coord_y, category):
    seat = Seat(area=area, category=category)
    seat.coords = Point(x=coord_x, y=coord_y)
    return seat
