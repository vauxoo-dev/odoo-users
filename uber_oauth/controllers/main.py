# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from odoo.addons.auth_oauth.controllers.main import (OAuthController,
                                                     set_cookie_and_redirect,
                                                     fragment_to_query_string)


_logger = logging.getLogger(__name__)


class OAuthControllerInherit(OAuthController):

    @http.route('/auth_oauth/signin', type='http', auth='none')
    @fragment_to_query_string
    def signin(self, **kw):
        res = super(OAuthControllerInherit, self).signin(**kw)
        if (not request.params.get('access_token') and
                'uber' in request.params.get('state')):
            url = "/auth_oauth/signin"
            return set_cookie_and_redirect(url)
        return res
