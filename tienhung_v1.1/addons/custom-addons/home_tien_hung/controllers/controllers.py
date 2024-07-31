# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class HomeTienHung(http.Controller):
   
    @http.route('/api/user_status_counts', auth='public', methods=['GET'], csrf=False)
    def get_user_status_counts(self, **kw):
        UserLoginStatus = request.env['res.users']
        result = UserLoginStatus.get_status_counts()
        return request.make_response(json.dumps(result), headers={'Content-Type': 'application/json'})
    

