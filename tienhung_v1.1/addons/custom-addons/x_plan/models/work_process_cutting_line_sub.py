from odoo import models, fields, api
from datetime import datetime
import pytz
from odoo.exceptions import ValidationError
class WorkProcessCuttingLineSub(models.Model):
    _name = 'work.process.cutting.sub'
    _description = 'Work Process Cutting Sub'

    employee = fields.Many2one('hr.employee', string='Employee Name')
    unit_price = fields.Float(string='Unit Price', compute='_compute_unit_price', store=True)
    start_date = fields.Datetime(string='Start Date',default=fields.Datetime.now)
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now)
    duration = fields.Integer(string='Duration', compute='_compute_duration_pass_cutting', store=True)
    stage_id = fields.Many2one(comodel_name='stage', string='Stage',compute='_compute_stage_id', store=True)
    cutting_id = fields.Many2one(comodel_name='cutting.line', string='Cutting', domain="[('stage_id', '=', stage_id)]")
    work_sub_id = fields.Many2one(comodel_name='work.process', string='Work Subs', ondelete='cascade')
    
    plan_id = fields.Many2one('x.plan', string='Plan', compute='_compute_plan_id', store=True)
    productivity_reports_ids = fields.One2many('productivity.reports','sewing_line_work_id', string='Productivity Reports')
 

    kh = fields.Integer(string='KH')
    ns = fields.Integer(string='NS', compute='_compute_ns_sew', store=True)
    
    quantity_per_team = fields.Integer(string='Total Execution Quantity', compute='_compute_quantity_per_team', store=True)
    ns_history = fields.Integer(string='NS History', compute='_compute_ns', store=True)
    pass_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Pass Type', compute='_compute_pass_type', store=True)
    total_ns = fields.Integer(string='Total NS', compute='_compute_total_ns_sew', store=True)
    is_checked = fields.Boolean(string='Checked', default=False)
    payroll_plan_work_sub_id = fields.Many2one('payroll.plan.work.sub',string='Payroll Plan Work Sub')



    @api.depends('start_date', 'end_date')
    def _compute_duration_pass_cutting(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration = (record.end_date - record.start_date).days
            elif record.start_date and not record.end_date:
                record.duration = (datetime.now().date() - record.start_date).days
            elif not record.start_date and record.end_date:
                record.duration = (record.end_date - datetime.now().date()).days
            else:
                record.duration = 0

    @api.depends('stage_id')
    def _compute_plan_id(self):
        for record in self:
            record.plan_id = record.stage_id.x_plan_id or ''

    @api.depends('stage_id')
    def _compute_pass_type(self):
        for record in self:
            record.pass_type = record.stage_id.stage_type or ''

    @api.depends('cutting_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.cutting_id.unit_price_05 or ''


    @api.depends('work_sub_id')
    def _compute_stage_id(self):
        for record in self:
            record.stage_id = record.work_sub_id.stage_id or ''

    
    @api.depends('stage_id')
    def _compute_quantity_per_team(self):
        for record in self:
            record.quantity_per_team = record.stage_id.quantity_per_team or ''

    @api.model
    def create(self, vals):
        res = super(WorkProcessCuttingLineSub, self).create(vals)
        res._compute_target_value_today_method_sew()
        return res
    
    def _compute_target_value_today_method_sew(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(vietnam_tz).date() 
        for record in self:
            if record.work_sub_id and record.plan_id:
                employee_id = record.work_sub_id.name.id
                targets = self.env['target'].search([
                    ('user_id', '=', employee_id),
                    ('target_stage_id', '=', record.stage_id.id),
                    ('start_date', '=', today) 
                ])
                record.kh = sum(target.target_value for target in targets)
            else:
                record.kh = 0.0


    @api.depends('stage_id', 'cutting_id', 'work_sub_id')
    def _compute_ns_sew(self):
        for record in self:
            if record.work_sub_id:
                employee_id = record.work_sub_id.name.id if record.work_sub_id.name else False
                if not employee_id:
                    record.ns = 0
                    continue
                reports = self.env['productivity.reports'].search([
                    ('name', '=', employee_id),
                    ('stage_id', '=', record.stage_id.id),
                    ('cutting_id', '=', record.cutting_id.id),
                    ('is_checked', '=', False),
                ])

                total_quantity = sum(reports.mapped('quantity'))
                record.ns = total_quantity
            else:
                record.ns = 0

    @api.depends('stage_id', 'cutting_id', 'work_sub_id')
    def _compute_total_ns_sew(self):
        for record in self:
            if record.work_sub_id:
                reports = self.env['productivity.reports'].search([
                    ('stage_id', '=', record.stage_id.id),
                    ('cutting_id', '=', record.cutting_id.id),
                    ('is_checked', '=', False),
                ])
                total_quantity = sum(reports.mapped('quantity'))
                record.total_ns = total_quantity
            else:
                record.ns = 0

    @api.constrains('total_ns', 'quantity_per_team')
    def _check_total_quantity(self):
        for record in self:
            total_quantity = record.total_ns
            if total_quantity > record.quantity_per_team:
                raise ValidationError("The number of Total NS must not exceed the allowed number")
    