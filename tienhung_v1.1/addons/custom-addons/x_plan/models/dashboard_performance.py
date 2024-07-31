from odoo import models, fields, api
from urllib.parse import urlencode
class DashboardPerformance(models.Model):
    _name = 'dashboard.performance'
    _description = 'Dashboard Performance'

    name = fields.Char(string='Name', required=True)
    plan = fields.Char(string='Plan')
    stage = fields.Char(string='Stage')
    operation = fields.Char(string='Operation')
    team = fields.Char(string='Team')
    performance_value = fields.Float(string='Performance Value')

    @api.model
    def action_open_performance_form(self, active_id=False):
        # Định nghĩa đường dẫn bạn đã định nghĩa trong route
        base_url = 'http://34.87.108.232:8069/'
        
        # Kiểm tra và xử lý active_id để tránh dấu []
        if active_id:
            url = base_url + '/performance_dashboard/data/%s' % str(active_id).replace('[', '').replace(']', '')
        else:
            url = base_url + '/performance_dashboard/data'
        
        # Redirect tới đường dẫn
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',  # Mở đường dẫn trong tab mới
        }

