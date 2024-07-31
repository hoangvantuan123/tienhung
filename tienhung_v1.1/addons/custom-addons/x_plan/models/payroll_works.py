from odoo import models, fields, api

class PayrollPlanWork(models.Model):
    _name = 'payroll.plan.work'
    _description = 'Payroll Plan Work'

    name = fields.Many2one('hr.employee', string='Employee')
    payroll_plan_work_ids = fields.Many2one('payroll.plan', string='Payroll Plan', ondelete='cascade')
    payroll_plan_list_id = fields.Many2one('payroll.list', string='Payroll List')
    total_sl = fields.Integer(string='Total SL')
    total_money = fields.Integer(string='Total Money')
    department_id = fields.Many2one('hr.department', string='Department', compute='_compute_department_id', store=True)
    payroll_plan_work_sub_id = fields.One2many(
        'payroll.plan.work.sub', 'payroll_work_id', string='Payroll Plans Sub')

    @api.depends('name')
    def _compute_department_id(self):
        for record in self:
            if record.name:
                record.department_id = record.name.department_id
            else:
                record.department_id = False
    def unlink(self):
        payroll_plan_work_sub_ids = self.mapped('payroll_plan_work_sub_id')
        work_sub_ids = payroll_plan_work_sub_ids.mapped('work_sub_id')
        work_more_sub_ids = payroll_plan_work_sub_ids.mapped('work_more_sub_id')
        work_sew_ids = payroll_plan_work_sub_ids.mapped('work_sew_sub_id')
        
        res = super(PayrollPlanWork, self).unlink()
        
        if work_sub_ids:
            for work_sub in work_sub_ids:
                if not self.env['payroll.plan.work.sub'].search_count([('work_sub_id', '=', work_sub.id)]):
                    work_sub.is_checked = False
        
        if work_more_sub_ids:
            for work_more_sub in work_more_sub_ids:
                if not self.env['payroll.plan.work.sub'].search_count([('work_more_sub_id', '=', work_more_sub.id)]):
                    work_more_sub.is_checked = False

        if work_sew_ids:
            for work_sew in work_sew_ids:
                if not self.env['payroll.plan.work.sub'].search_count([('work_sew_sub_id', '=', work_sew.id)]):
                    work_sew.is_checked = False
        
        return res