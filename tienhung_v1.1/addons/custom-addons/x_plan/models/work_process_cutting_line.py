from odoo import models, fields, api
from datetime import datetime


class WorkProcessCuttingLine(models.Model):
    _name = 'work.process'
    _description = 'Work Process'

    name = fields.Many2one('hr.employee', string='Employee Name')
    employee_name = fields.Char(string='Employee Name')
    stage = fields.Char(string='Stage')
    completed = fields.Boolean(string='Completed')
    to_be_completed = fields.Boolean(string='To Be Completed')
    unit_price = fields.Float(string='Total Unit Price' , compute='_compute_unit_price_counts', store=True)
    product_code = fields.Char(string='Product Code')
    team = fields.Char(string='Team')
    employee_card_number = fields.Char(string='Employee Card Number', compute='_compute_new_employee_card_number', store=True, readonly=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    duration = fields.Integer(
        string='Duration', compute='_compute_duration', store=True)

    cutting_line_id = fields.Many2one(
        comodel_name='cutting.line', string='Cutting Line')
    work_step = fields.Char(
        string='Work Step', compute='_compute_work_step', store=True)
    stage_id = fields.Many2one(comodel_name='stage', string='Stage')
    department_id = fields.Many2one(related='stage_id.department_id', string='Department', store=True, readonly=True)
    work_sub_ids = fields.One2many('work.process.cutting.sub','work_sub_id', string='Work Sub')
    work_stage_cutting_line_id = fields.Many2one('stage.line', string='Stage Team Line')

    productivity_reports_ids = fields.One2many('productivity.reports','sewing_line_work_id', string='Productivity Reports')
 
    department_id = fields.Many2one('hr.department', string='Department', compute='_compute_department_id', store=True)
    plan_id = fields.Many2one('x.plan', string='Plan', compute='_compute_plan_id', store=True)
    pass_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Pass Type', compute='_compute_pass_type', store=True)
    is_checked = fields.Boolean(string='Checked', default=False)
    payroll_plan_work_sub_id = fields.Many2one('payroll.plan.work.sub',string='Payroll Plan Work Sub')
    assign_more_work_sub_filtered_ids = fields.One2many('assign.more.work.sub', compute='_compute_assign_more_work_sub_filtered_ids', string='Filtered More Work Sub')
    
    




    @api.depends('name')
    def _compute_new_employee_card_number(self):
        for record in self:
            record.employee_card_number = record.name.barcode or ''

    @api.depends('stage_id')
    def _compute_plan_id(self):
        for record in self:
            record.plan_id = record.stage_id.x_plan_id or ''

    @api.depends('stage_id')
    def _compute_pass_type(self):
        for record in self:
            record.pass_type = record.stage_id.stage_type or ''

    @api.depends('name')
    def _compute_department_id(self):
        for record in self:
            if record.name:
                record.department_id = record.name.department_id
            else:
                record.department_id = False
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration = (record.end_date - record.start_date).days
            elif record.start_date and not record.end_date:
                record.duration = (datetime.now().date() - record.start_date).days
            elif not record.start_date and record.end_date:
                record.duration = (record.end_date - datetime.now().date()).days
            else:
                record.duration = 0

    @api.depends('cutting_line_id')
    def _compute_work_step(self):
        for record in self:
            if record.cutting_line_id:
                record.work_step = record.cutting_line_id.name
            else:
                record.work_step = ''

    @api.onchange('cutting_line_id')
    def _onchange_cutting_line_id(self):
        if self.cutting_line_id:
            cutting_line = self.env['cutting.line'].browse(self.cutting_line_id.id)
            self.unit_price = cutting_line.unit_price_05

 

    @api.depends('work_sub_ids.unit_price')
    def _compute_unit_price_counts(self):
        for record in self:
            record.unit_price = sum(line.unit_price for line in record.work_sub_ids)

    @api.onchange('work_sub_ids')
    def _onchange_timekeeping_line_ids(self):
        self._compute_unit_price_counts()

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        return super(WorkProcessCuttingLine, self).search(args, offset, limit, order)


    @api.depends('name')
    def _compute_assign_more_work_sub_filtered_ids(self):
        for record in self:
            record.assign_more_work_sub_filtered_ids = self.env['assign.more.work.sub'].search([
                ('new_employee', '=', record.name.id),
                ('create_date', '>=', fields.Date.today()),
                ('is_checked', '=', False),
                ('plan_id' , '=', record.plan_id.id),
                ('stage_id' , '=', record.stage_id.id),
            ])