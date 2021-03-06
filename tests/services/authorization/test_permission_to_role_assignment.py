"""
:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import pytest

from byceps.services.authorization import service


def test_assign_permission_to_role(admin_app_with_db, permission, role):
    role_permission_ids_before = get_permission_ids_for_role(role)
    assert permission.id not in role_permission_ids_before

    service.assign_permission_to_role(permission.id, role.id)

    role_permission_ids_after = get_permission_ids_for_role(role)
    assert permission.id in role_permission_ids_after


def test_deassign_permission_from_role(admin_app_with_db, permission, role):
    service.assign_permission_to_role(permission.id, role.id)

    role_permission_ids_before = get_permission_ids_for_role(role)
    assert permission.id in role_permission_ids_before

    service.deassign_permission_from_role(permission.id, role.id)

    role_permission_ids_after = get_permission_ids_for_role(role)
    assert permission.id not in role_permission_ids_after


@pytest.fixture
def permission():
    return service.create_permission('board_topic_hide', 'Hide board topics')


@pytest.fixture
def role():
    return service.create_role('board_moderator', 'Board Moderator')


def get_permission_ids_for_role(role):
    return {p.id for p in role.permissions}
