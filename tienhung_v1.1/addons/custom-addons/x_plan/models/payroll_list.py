from odoo import models, fields, api

class Payroll(models.Model):
    _name = 'payroll.list'
    _description = 'Payroll List'

    name = fields.Char(string='Payroll Name', required=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    payroll_line_ids = fields.One2many('payroll.line', 'payroll_id', string='Payroll Lines')
    payroll_plan_ids = fields.One2many('payroll.plan', 'payroll_plan_id', string='Payroll Plans')  # Đặt tên trường đúng là payroll_plan_ids

    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    create_month_year = fields.Char(string='Creation Month/Year', compute='_compute_create_month_year', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    total_quantity = fields.Float(string='Total Quantity', compute='_compute_total_quantity', store=True)
    start_time = fields.Datetime(string='Start Date', default=fields.Datetime.now)
    end_time = fields.Datetime(string='End Date', default=fields.Datetime.now)
    pass_type = fields.Selection([
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Pass Type')
    payroll_plan_work_ids = fields.One2many('payroll.plan.work', 'payroll_plan_list_id', string='Payroll Plans')

    @api.depends('create_date')
    def _compute_create_month_year(self):
        for record in self:
            if record.create_date:
                record.create_month_year = record.create_date.strftime('%m/%Y')

    @api.depends('payroll_line_ids.total_amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.total_amount for line in record.payroll_line_ids)

    @api.depends('payroll_line_ids.total_quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.total_quantity for line in record.payroll_line_ids)


    @api.onchange('payroll_line_ids')
    def _onchange_payroll_line_ids(self):
        self._compute_total_amount()
        self._compute_total_quantity()