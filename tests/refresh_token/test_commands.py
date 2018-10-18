import io
import sys

from django.core.management import call_command

from graphql_jwt.shortcuts import create_refresh_token

from ..testcases import UserTestCase


class ClearTokensTests(UserTestCase):

    def setUp(self):
        super(ClearTokensTests, self).setUp()
        self.refresh_token = create_refresh_token(self.user)

        if sys.version_info[0] < 3:
            self.out = io.BytesIO()
        else:
            self.out = io.StringIO()

    def test_clear_revoked_tokens(self):
        self.refresh_token.revoke()
        call_command('cleartokens', stdout=self.out)

        self.assertIn('deleted 1 token', self.out.getvalue())

    def test_clear_expired_tokens(self):
        call_command('cleartokens', expired=True, stdout=self.out)

        self.assertIn('deleted 0 tokens', self.out.getvalue())
