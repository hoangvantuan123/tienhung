from odoo import models, fields, api

class EmployeeWorkHistory(models.Model):
    _name = 'employee.work.history'
    _description = 'Employee Work History'

    product_code = fields.Char(string='Product Code')
    work_step = fields.Char(string='Work Step')
    quantity = fields.Float(string='Quantity')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    payroll_line_id = fields.Many2one('payroll.line', string='Payroll Line', ondelete='cascade')

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price

    

