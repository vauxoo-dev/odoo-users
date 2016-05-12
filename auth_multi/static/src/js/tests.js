odoo.define('auth_multi.tour', function (require) {
'use strict';

    var Tour = require('web.Tour');

    Tour.register({
        id: 'test_instance_oauth_multi',
        name: 'Login Using Google Oauth',
        mode: 'test',
        steps: [
            {
                title: 'Wait for login and redirect',
                wait: 9000,
            },
            {
                title: 'Show the main window for the user',
                waitFor: 'span:contains("Test Oauth")',
            },
        ],
    });

});
