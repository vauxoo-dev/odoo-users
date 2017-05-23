# -*- coding: utf-8 -*-
import urllib2
import logging
import simplejson
import urlparse
import werkzeug.utils

from odoo import SUPERUSER_ID, api
from odoo import http
from odoo import registry as registry_get
from odoo.addons.auth_oauth.controllers.main import (OAuthController,
                                                     fragment_to_query_string)


_logger = logging.getLogger(__name__)


class OAuthControllerInherit(OAuthController):

    @http.route('/auth_oauth/signin', type='http', auth='none')
    @fragment_to_query_string
    def signin(self, **kw):
        state = simplejson.loads(kw['state'])
        dbname = state['d']
        provider = state['p']
        registry = registry_get(dbname)
        context = state.get('c', {})
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, context)
            if not kw.get('access_token') and kw.get('code'):
                p_brw = env['auth.oauth.provider'].\
                    browse(provider)
                params = werkzeug.url_encode({
                    'code': kw.get('code'),
                    'client_id': p_brw.client_id,
                    'client_secret': p_brw.client_secret})
                endpoint = p_brw.url_get_token
                if endpoint:
                    if urlparse.urlparse(endpoint)[4]:
                        url = endpoint + '&' + params
                    else:
                        url = endpoint + '?' + params
                    furl = urllib2.urlopen(url)
                    response = furl.read()
                    response = werkzeug.url_decode(response)
                    kw.update({'access_token': response.get('access_token')})
        return super(OAuthControllerInherit, self).signin(**kw)
