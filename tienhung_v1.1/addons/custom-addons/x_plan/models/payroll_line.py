from odoo import models, fields, api

class PayrollLine(models.Model):
    _name = 'payroll.line'
    _description = 'Payroll Line'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    payroll_id = fields.Many2one('payroll.list', string='Payroll', required=True, ondelete='cascade')
    total_quantity = fields.Float(string='Total Quantity')
    total_amount = fields.Float(string='Amount')
    work_history_ids = fields.One2many('employee.work.history', 'payroll_line_id', string='Work History')
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    create_month_year = fields.Char(string='Creation Month/Year', compute='_compute_create_month_year', store=True)
    


    @api.model
    def create(self, vals):
        if 'create_date' in vals:
            vals['create_month_year'] = fields.Datetime.from_string(vals['create_date']).strftime('%m/%Y')
        payroll = super(PayrollLine, self).create(vals)
        return payroll

    @api.depends('create_date')
    def _compute_create_month_year(self):
        for record in self:
            if record.create_date:
                record.create_month_year = record.create_date.strftime('%m/%Y')
