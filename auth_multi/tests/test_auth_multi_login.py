# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: nhomar@vauxoo.com
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################

import openerp.tests
import mock


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestOauthMulti(openerp.tests.HttpCase):

    def setUp(self):
        super(TestOauthMulti, self).setUp()

    @mock.patch('openerp.addons.auth_oauth.res_users.'
                'res_users._auth_oauth_rpc')
    def test_01_login_with_users(self, mock_oauth_rpc):
        """Trying the login with google
        """
        response = {
            "id": "123456789987654321",
            "email": "test@vauxoo.com",
            "verified_email": True,
            "name": "Test Oauth",
            "given_name": "Test 1",
            "family_name": "Oauth",
            "gender": "male",
            "locale": "es",
            "hd": "vauxoo.com"}

        mock_oauth_rpc.return_value = response
        token = 'ya29.CjXgA59Z3ezBdP_Bki4fth6FtrG9Nw'
        domain = self.env['ir.config_parameter'].get_param('web.base.url')
        path = '/auth_oauth/signin?state=%7B%22p%22:+3,+%22r%22:+%22'\
            '{domain}%252Fweb%22,+%22d%22:+%22'\
            'auth2%22%7D&access_token={token}&token_type=Bearer'\
            '&expires_in=3600'.\
            format(domain=domain, token=token)
        self.phantom_js(
            path,
            "odoo.__DEBUG__.services['web.Tour'].run('test_instance_oauth_multi', 'test')",
            "odoo.__DEBUG__.services['web.Tour'].tours.test_instance_oauth_multi")
