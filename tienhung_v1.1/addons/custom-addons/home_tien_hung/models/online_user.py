from odoo import models, fields, api
from odoo.http import request

class OnlineUser(models.Model):
    _name = 'online.user'
    _description = 'Online User'

    user_id = fields.Many2one('res.users', string='User')
    login_time = fields.Datetime(string='Login Time', default=fields.Datetime.now)
    session_id = fields.Char(string='Session ID')

    @api.model
    def track_user_login(self, session_id):
        user = request.env.user
        existing_record = self.search([('user_id', '=', user.id), ('session_id', '=', session_id)])
        if not existing_record:
            self.create({'user_id': user.id, 'session_id': session_id})

    @api.model
    def track_user_logout(self, session_id):
        self.search([('session_id', '=', session_id)]).unlink()
