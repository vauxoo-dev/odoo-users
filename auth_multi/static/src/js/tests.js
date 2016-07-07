odoo.define('auth_multi.tour', function (require) {
'use strict';

    var Tour = require('web.Tour');

    Tour.register({
        id: 'test_instance_oauth_multi',
        name: 'Login Using Google Oauth',
        path: '/web/login',
        mode: 'test',
        steps: [
            {
                title: 'Wait for login and redirect',
                element: 'input',
                waitFor: 'input',
                onload: function(tour){
                    window.location.href = 'http://127.0.0.1:8069/auth_oauth/signin?state=%7B%22p%22:+3,+%22r%22:+%22http%253A%252F%252Flocalhost:' +
                    '8069%252Fweb%22,+%22d%22:+%22auth2%22%7D&access_token=ya29.CjXgA59Z3ezBdP_Bki4fth6FtrG9Nw&token_type=Bearer&expires_in=3600'
                },
            },
            {
                title: 'Show the main window for the user',
                waitFor: 'span:contains("Test Oauth")',
            },
        ],
    });

});
