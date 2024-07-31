from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class ProductivityReports(models.Model):
    _name = 'productivity.reports'
    _description = 'Productivity Reports'

    name = fields.Many2one('hr.employee', string='Employee')
    plan_id = fields.Many2one(comodel_name='x.plan', string="Plan")
    stage_id = fields.Many2one(comodel_name='stage', string='Stage')
    new_date = fields.Datetime(string='Date Added', default=fields.Datetime.now)
    quantity = fields.Integer(string='Quantity')
    cutting_line_work_id = fields.Many2one(comodel_name='work.pass.cutting', string='Cutting Line Work')
    cutting_line_work_sub_id = fields.Many2one(comodel_name='work.pass.cutting.sub', string='Cutting Line Work Sub')
    sewing_line_work_id = fields.Many2one(comodel_name='work.process', string='Sewing Line Works')
    sewing_line_work_sub_id = fields.Many2one(comodel_name='work.process.cutting.sub', string='Sewing Line Works Sub')
    pass_cutting_id = fields.Many2one(comodel_name='pass.cutting', string='Pass Cutting', domain="[('stage_id', '=', stage_id)]")
    cutting_id = fields.Many2one(comodel_name='cutting.line', string='Cutting', domain="[('stage_id', '=', stage_id)]")
    is_checked = fields.Boolean(string='Checked', default=False)
    payroll_plan_work_sub_id = fields.Many2one('payroll.plan.work.sub',string='Payroll Plan Work Sub')

    @api.model
    def create(self, vals):
        record = super(ProductivityReports, self).create(vals)
        record._update_related_ns()
        record._update_related_ns_sew()
        record._update_related_total_ns()
        record._update_related_total_ns_sew()
        record._update_related_ns_cut()
        return record

    def write(self, vals):
        result = super(ProductivityReports, self).write(vals)
        self._update_related_ns()
        self._update_related_ns_sew()
        self._update_related_total_ns()
        self._update_related_total_ns_sew()
        self._update_related_ns_cut()
        return result

    def _update_related_ns(self):
        related_records = self.env['work.pass.cutting.sub'].search([
            ('work_sub_id.name.id', '=', self.name.id),
            ('stage_id', '=', self.stage_id.id),
            ('pass_cutting_id', '=', self.pass_cutting_id.id),
            ('is_checked' , '=',  False)
        ])
        for record in related_records:
            record._compute_ns()

    def _update_related_ns_cut(self):
        related_records = self.env['assign.more.work.sub'].search([
            ('assign_more_work_id.name.id', '=', self.name.id),
            ('stage_id', '=', self.stage_id.id),
            ('pass_cutting_id', '=', self.pass_cutting_id.id), 
            ('is_checked' , '=',  False)
        ])
        for record in related_records:
            record._compute_ns_cut()


    def _update_related_total_ns(self):
        related_records = self.env['work.pass.cutting.sub'].search([
            ('stage_id', '=', self.stage_id.id),
            ('pass_cutting_id', '=', self.pass_cutting_id.id),
            ('is_checked' , '=',  False)
        ])
        for record in related_records:
            record._compute_total_ns()

    def _update_related_total_ns_cut(self):
        related_records = self.env['assign.more.work.sub'].search([
            ('stage_id', '=', self.stage_id.id),
            ('pass_cutting_id', '=', self.pass_cutting_id.id),
            ('is_checked' , '=',  False)
        ])
        for record in related_records:
            record._compute_total_ns_cut()

    def _update_related_ns_sew(self):
        # Update related records in WorkProcessCuttingSub
        related_records = self.env['work.process.cutting.sub'].search([
            ('work_sub_id.name.id', '=', self.name.id),
            ('stage_id', '=', self.stage_id.id),
            ('cutting_id', '=', self.cutting_id.id),
            ('is_checked' , '=',  False)
        ])
        for record in related_records:
            record._compute_ns_sew()
            
    def _update_related_total_ns_sew(self):
        related_records = self.env['work.process.cutting.sub'].search([
            ('stage_id', '=', self.stage_id.id),
            ('cutting_id', '=', self.cutting_id.id),
            ('is_checked' , '=',  False)
        ])
        for record in related_records:
            record._compute_total_ns_sew()

    
    @api.model
    def action_save(self):
        # Logic cho hành động lưu
        # Nếu bạn cần xử lý nhiều bản ghi, sử dụng self
        # Ví dụ: self.env['productivity.reports'].browse([1, 2, 3]).action_save()
        return {'type': 'ir.actions.act_window_close'}  # Đóng cửa sổ sau khi lưu

    @api.model
    def action_cancel(self):
        # Logic cho hành động hủy
        # Nếu bạn cần xử lý nhiều bản ghi, sử dụng self
        return {'type': 'ir.actions.act_window_close'} 