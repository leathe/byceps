"""
:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from tests.base import AbstractAppTestCase
from tests.helpers import (
    create_email_config,
    create_site,
    create_user,
    http_client,
    login_user,
)


class PasswordUpdateFormTestCase(AbstractAppTestCase):

    def setUp(self):
        super().setUp()

        create_email_config()
        create_site()

    def test_when_logged_in_form_is_available(self):
        user = create_user()
        login_user(user.id)

        response = self.send_request(user_id=user.id)

        assert response.status_code == 200

    def test_when_not_logged_in_form_is_unavailable(self):
        response = self.send_request()

        assert response.status_code == 404

    # helpers

    def send_request(self, *, user_id=None):
        url = '/authentication/password/update'
        with http_client(self.app, user_id=user_id) as client:
            return client.get(url)
