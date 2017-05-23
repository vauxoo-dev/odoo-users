# -*- coding: utf-8 -*-
import logging
import urlparse
import base64
import requests
from odoo import models, api
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def auth_oauth(self, provider, params):
        """Modified to set the id of the user returned by uber api"""
        # Advice by Google (to avoid Confused Deputy Problem)
        # if validation.audience != OUR_CLIENT_ID:
        #   abort()
        # else:
        #   continue with the process
        access_token = params.get('access_token')
        validation = self._auth_oauth_validate(provider, access_token)
        if validation.get('rider_id'):
            # Workaround: uber does not send 'user_id' in Open Graph Api
            if validation.get('uuid'):
                validation['user_id'] = validation['uuid']
            else:
                raise AccessDenied()
        else:
            return super(ResUsers, self).auth_oauth(provider, params)

        # retrieve and sign in user
        login = self._auth_oauth_signin(provider, validation, params)
        if not login:
            raise AccessDenied()
        # return user credentials
        return (self.env.cr.dbname, login, access_token)

    @api.model
    def _generate_signup_values(self, provider, validation, params):
        """Modified to add the values returned by uber api"""
        res = super(ResUsers, self)._generate_signup_values(provider,
                                                            validation, params)
        if validation.get('picture') and urlparse.urlparse(
                            validation.get('picture')).scheme:
            res.update(
                {'image': base64.b64encode(
                    requests.get(validation.get('picture')).content)})
        return res
