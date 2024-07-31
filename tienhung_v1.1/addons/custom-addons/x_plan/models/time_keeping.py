from odoo import models, fields, api

class Timekeeping(models.Model):
    _name = 'timekeeping.list'
    _description = 'Timekeeping List'

    @api.depends('create_date')
    def _compute_name(self):
        for record in self:
            record.name = f"Timekeeping  - {record.create_date}"

    name = fields.Char(string='Timekeeping Name', compute='_compute_name' , required=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    timekeeping_line_ids = fields.One2many('timekeeping.line', 'timekeeping_id', string='Timekeeping Lines')
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    create_month_year = fields.Char(string='Creation Month/Year', compute='_compute_create_month_year', store=True)
    
    # New fields to count employees by vacation status
    present_count = fields.Integer(string='Present Count', compute='_compute_status_counts', store=True)
    absent_count = fields.Integer(string='Absent Count', compute='_compute_status_counts', store=True)
    half_day_count = fields.Integer(string='Half Dayt', compute='_compute_status_counts', store=True)
    vacation_status_p_count = fields.Integer(string='P Count', compute='_compute_status_counts', store=True)
    vacation_status_ro_count = fields.Integer(string='RO Count', compute='_compute_status_counts', store=True)
    vacation_status_r_count = fields.Integer(string='R Count', compute='_compute_status_counts', store=True)
    vacation_status_o_count = fields.Integer(string='OO Count', compute='_compute_status_counts', store=True)
    vacation_status_oo_count = fields.Integer(string='O Count', compute='_compute_status_counts', store=True)
    vacation_status_co_count = fields.Integer(string='CO Count', compute='_compute_status_counts', store=True)
    vacation_status_bo_count = fields.Integer(string='BO Count', compute='_compute_status_counts', store=True)
    vacation_status_d_count = fields.Integer(string='Đ Count', compute='_compute_status_counts', store=True)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', self.department_id.id)])
            existing_employees = self.timekeeping_line_ids.mapped('employee_id')
            to_add = [(0, 0, {'employee_id': emp.id}) for emp in employees if emp not in existing_employees]
            to_remove_ids = self.timekeeping_line_ids.filtered(lambda line: line.employee_id not in employees).ids
            if to_remove_ids:
                self.timekeeping_line_ids = [(2, line_id) for line_id in to_remove_ids]
            if to_add:
                self.update({
                    'timekeeping_line_ids': to_add,
                })
        else:
            self.timekeeping_line_ids = [(5, 0, 0)]  # Clear existing lines

    @api.model
    def create(self, vals):
        if 'create_date' in vals:
            vals['create_month_year'] = fields.Datetime.from_string(vals['create_date']).strftime('%m/%Y')
        payroll = super(Timekeeping, self).create(vals)
        payroll._onchange_department_id()
        return payroll

    @api.depends('create_date')
    def _compute_create_month_year(self):
        for record in self:
            if record.create_date:
                record.create_month_year = record.create_date.strftime('%m/%Y')

 
    @api.depends('timekeeping_line_ids.present', 'timekeeping_line_ids.vacation_status')
    def _compute_status_counts(self):
        for record in self:
            record.present_count = sum(line.present for line in record.timekeeping_line_ids)
            record.absent_count = sum(line.absent for line in record.timekeeping_line_ids)
            record.half_day_count = sum(line.half_day for line in record.timekeeping_line_ids)
            record.vacation_status_p_count = sum(line.vacation_status == 'p' for line in record.timekeeping_line_ids)
            record.vacation_status_ro_count = sum(line.vacation_status == 'ro' for line in record.timekeeping_line_ids)
            record.vacation_status_r_count = sum(line.vacation_status == 'r' for line in record.timekeeping_line_ids)
            record.vacation_status_oo_count = sum(line.vacation_status == 'oo' for line in record.timekeeping_line_ids)
            record.vacation_status_o_count = sum(line.vacation_status == 'o' for line in record.timekeeping_line_ids)
            record.vacation_status_co_count = sum(line.vacation_status == 'co' for line in record.timekeeping_line_ids)
            record.vacation_status_bo_count = sum(line.vacation_status == 'bo' for line in record.timekeeping_line_ids)
            record.vacation_status_d_count = sum(line.vacation_status == 'đ' for line in record.timekeeping_line_ids)

    @api.onchange('timekeeping_line_ids')
    def _onchange_timekeeping_line_ids(self):
        self._compute_status_counts()
