from odoo import models, fields, api

class TimekeepingLine(models.Model):
    _name = 'timekeeping.line'
    _description = 'Timekeeping Line'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    timekeeping_id = fields.Many2one('timekeeping.list', string='Timekeeping', required=True, ondelete='cascade')
    employee_card = fields.Char(string='Employee Card Number', compute='_compute_employee_card_number', readonly=True)
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    create_month_year = fields.Char(string='Creation Month/Year', compute='_compute_create_month_year', store=True)
    present = fields.Boolean(string='Full Day', default=True)
    half_day = fields.Boolean(string='Half Day', default=False)
    absent = fields.Boolean(string='Absent', default=False)
    
    vacation_status = fields.Selection([
        ('p', 'P'),
        ('ro', 'RO'),
        ('r', 'R'),
        ('oo', 'OO'),
        ('co', 'CO'),
        ('o', 'O'),
        ('bo', 'BO'),
        ('đ', 'Đ')
    ], string='Vacation Status')
    note = fields.Text(string='Note')

    @api.depends('employee_id')
    def _compute_employee_card_number(self):
        for record in self:
            record.employee_card = record.employee_id.barcode or ''

    @api.model
    def create(self, vals):
        if 'create_date' in vals:
            vals['create_month_year'] = fields.Datetime.from_string(vals['create_date']).strftime('%m/%Y')
        payroll = super(TimekeepingLine, self).create(vals)
        return payroll

    @api.depends('create_date')
    def _compute_create_month_year(self):
        for record in self:
            if record.create_date:
                record.create_month_year = record.create_date.strftime('%m/%Y')

    @api.onchange('present', 'half_day', 'absent')
    def _onchange_attendance(self):
        if self.present:
            self.half_day = False
            self.absent = False
        elif self.half_day:
            self.present = False
            self.absent = False
        elif self.absent:
            self.present = False
            self.half_day = False