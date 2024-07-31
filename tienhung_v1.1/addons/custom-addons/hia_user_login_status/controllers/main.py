# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.web.controllers.home import Home as WebHome
from odoo.addons.web.controllers.session import Session
from odoo.http import request
from datetime import datetime

class UserOnlineStatusController(http.Controller):
    
    
    @http.route('/home_tien_hung/home_tien_hung', auth='public')
    def index(self, **kw):
        return "Hello, world"