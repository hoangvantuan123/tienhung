# -*- coding: utf-8 -*-
from odoo import models, fields, api

class UserLoginStatus(models.Model):
    _inherit = 'res.users'

    status = fields.Selection(selection=[
        ('done', 'Online'),
        ('blocked', 'Offline'),
    ], string="Login Status", default='blocked',readonly = True)

    total_log_record = fields.Integer('Total Log Information',compute='_count_total_log')

    def _count_total_log(self):
        for record in self:
            rec = self.env['res.users.logger'].sudo().search([('username','=',record.id)])
            record.total_log_record = len(rec)


    def show_log_record(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.users.logger",
            "domain": [('username','=',self.id)],
            "name": "User Logging Record",
            'view_mode': 'list',
        }

    @api.model
    def get_online_users_count(self):
        # Đếm số người dùng có trạng thái 'Online'
        return self.search_count([('status', '=', 'done')])

    @api.model
    def log_user_login(self, user_id, latitude, longitude):
        # Ghi lại thông tin đăng nhập
        self.env['res.users.logger'].create({
            'username': user_id,
            'login_time': fields.Datetime.now(),
            'latitude': latitude,
            'longitude': longitude,
        })

    @api.model
    def log_user_logout(self, user_id):
        # Cập nhật thời gian đăng xuất cho phiên làm việc cuối cùng
        log_entry = self.env['res.users.logger'].search([
            ('username', '=', user_id),
            ('logout_time', '=', False)
        ], limit=1)
        if log_entry:
            log_entry.write({
                'logout_time': fields.Datetime.now()
            })
    @api.model
    def get_status_counts(self):
        """Trả về số lượng người dùng theo trạng thái"""
        online_count = self.search_count([('status', '=', 'done')])
        offline_count = self.search_count([('status', '=', 'blocked')])
        return {
            'online_count': online_count,
            'offline_count': offline_count
        }
class UserLog(models.Model):
    _name = 'res.users.logger'

    username = fields.Many2one('res.users', "User Name")
    login_time = fields.Datetime("Login Time")
    logout_time = fields.Datetime("Logout Time")
    system_use_time = fields.Char("System Use Time", compute='_compute_system_use_time')
    latitude = fields.Float("Latitude")  # Thêm trường để lưu trữ vĩ độ
    longitude = fields.Float("Longitude") 

    def _compute_system_use_time(self):
        for record in self:
            if record.logout_time:
                time_diff = str(record.logout_time - record.login_time)
            else:
                time_diff = str(fields.Datetime.now() - record.login_time)
            time_diff = time_diff[:time_diff.find('.')]
            record.system_use_time = time_diff

    