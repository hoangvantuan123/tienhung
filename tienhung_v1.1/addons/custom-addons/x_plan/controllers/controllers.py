# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request



class DashboardPerformanceController(http.Controller):

    @http.route('/performance_dashboard/data/<int:active_id>', type='http', auth='public', website=True)
    def get_performance_data(self, active_id):
        performance_record = request.env['dashboard.performance'].sudo().browse(active_id)
        if performance_record.exists():
            return request.render('x_plan.performance_data_template', {
                'performance_record': performance_record,
            })
        else:
            # Trả về template thông báo khi không tìm thấy dữ liệu
            return request.render('x_plan.not_found_template', {})
    

    @http.route('/import_csv/import_csv', auth='public')
    def index(self, **kw):
        return "Hello, world"
    
   