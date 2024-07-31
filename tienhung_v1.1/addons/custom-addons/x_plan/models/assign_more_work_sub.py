from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
import pytz

class AssignMoreWorkSub(models.Model):
    _name = 'assign.more.work.sub'
    _description = 'Assign More Work Sub'

    work_sub_id = fields.Many2one(comodel_name='work.pass.cutting', string='Work Subs')
    unit_price = fields.Float(string='Unit Price')
    stage_id = fields.Many2one(comodel_name='stage', string='Stage')
    plan_id = fields.Many2one(comodel_name='x.plan', compute='_compute_plan_id', store=True, string='Plan')
    cutting_id = fields.Many2one(comodel_name='cutting.line', string='Cutting', domain="[('stage_id', '=', stage_id)]")
    pass_cutting_id = fields.Many2one(comodel_name='pass.cutting', string='Pass Cutting', domain="[('stage_id', '=', stage_id)]")
    stage_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Stage Type')
    assign_more_work_id = fields.Many2one('assign.more.work', string='Assign More Work', required=True, ondelete='cascade')
    new_employee = fields.Many2one('hr.employee', string='Employee', compute='_compute_new_employee', store=True)
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    quantity_per_team = fields.Integer(string='Total Execution Quantity', compute='_compute_quantity_per_team', store=True)
    kh = fields.Integer(string='KH')

    ns_cut = fields.Integer(string='NS', compute='_compute_ns_cut', store=True)
    ns_sew = fields.Integer(string='NS', compute='_compute_ns_sew', store=True)

    total_ns_cut = fields.Integer(string='Total NS Cut', compute='_compute_total_ns_cut', store=True)
    total_ns_sew = fields.Integer(string='Total NS Cut', compute='_compute_total_ns_sew', store=True)
   
    is_checked = fields.Boolean(string='Checked', default=False)
    payroll_plan_work_sub_id = fields.Many2one('payroll.plan.work.sub',string='Payroll Plan Work Sub')

    @api.depends('assign_more_work_id')
    def _compute_new_employee(self):
        for record in self:
            record.new_employee = record.assign_more_work_id.name.id or ''


    @api.depends('stage_id')
    def _compute_plan_id(self):
        for record in self:
            record.plan_id = record.stage_id.x_plan_id.id or ''

    @api.depends('stage_id')
    def _compute_quantity_per_team(self):
        for record in self:
            record.quantity_per_team = record.stage_id.quantity_per_team or ''


    @api.depends('stage_id', 'pass_cutting_id')
    def _compute_total_ns_cut(self):
        for record in self:
            reports = self.env['productivity.reports'].search([
                ('stage_id', '=', record.stage_id.id),
                ('pass_cutting_id', '=', record.pass_cutting_id.id),
                ('is_checked', '=', False),
            ])
            total_quantity = sum(reports.mapped('quantity'))
            record.total_ns_cut = total_quantity
    

    @api.depends('stage_id', 'pass_cutting_id', 'assign_more_work_id')
    def _compute_ns_cut(self):
        for record in self:
            employee_id = record.assign_more_work_id.name.id or ''
            if not employee_id:
                record.ns_cut = 0
                continue
            reports = self.env['productivity.reports'].search([
                ('name', '=', employee_id),
                ('stage_id', '=', record.stage_id.id),
                ('pass_cutting_id', '=', record.pass_cutting_id.id),
                ('is_checked', '=', False),
            ])

            total_quantity = sum(reports.mapped('quantity'))
            record.ns_cut = total_quantity


    @api.depends('stage_id', 'cutting_id', 'assign_more_work_id')
    def _compute_ns_sew(self):
        for record in self:
            employee_id = record.assign_more_work_id.name.id or ''
            if not employee_id:
                record.ns_sew = 0
                continue
            reports = self.env['productivity.reports'].search([
                ('name', '=', employee_id),
                ('stage_id', '=', record.stage_id.id),
                ('cutting_id', '=', record.cutting_id.id),
                ('is_checked', '=', False),
            ])
            total_quantity = sum(reports.mapped('quantity'))
            record.ns_sew = total_quantity
    
    


    @api.depends('stage_id', 'pass_cutting_id')
    def _compute_total_ns_sew(self):
        for record in self:
            reports = self.env['productivity.reports'].search([
                ('stage_id', '=', record.stage_id.id),
                ('cutting_id', '=', record.cutting_id.id),
                ('is_checked', '=', False),
            ])
            total_quantity = sum(reports.mapped('quantity'))
            record.total_ns_sew = total_quantity

    
    @api.model
    def create(self, vals):
        res = super(AssignMoreWorkSub, self).create(vals)
        res._compute_target_value_today_more_work()
        return res
    
    def _compute_target_value_today_more_work(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(vietnam_tz).date() 
        for record in self:
            if record.assign_more_work_id and record.plan_id:
                employee_id = record.assign_more_work_id.name.id
                targets = self.env['target'].search([
                    ('user_id', '=', employee_id),
                    ('target_stage_id', '=', record.stage_id.id),
                    ('start_date', '=', today) 
                ])
                record.kh = sum(target.target_value for target in targets)
            else:
                record.kh = 0.0