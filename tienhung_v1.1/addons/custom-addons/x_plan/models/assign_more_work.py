from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class AssignMoreWork(models.Model):
    _name = 'assign.more.work'
    _description = 'Assign More Work'

    name = fields.Many2one('hr.employee', string='Employee Name')
    department_id = fields.Many2one('hr.department', compute='_compute_name_department_id',string='Department', store=True)

    new_employee_card_number = fields.Char(string='Employee Card Number', compute='_compute_new_employee_card_number', store=True, readonly=True)
    ex_employee = fields.Many2one('hr.employee', string='ex-Employee')
    ex_employee_card_number = fields.Char(string='ex-Employee Card Number', compute='_compute_ex_employee_card_number', store=True, readonly=True)
    total_unit_price = fields.Float(string='Total Unit Price')
    plan_id = fields.Many2one(comodel_name='x.plan', string="Plan")
    stage_id = fields.Many2one(comodel_name='stage', string='Stage')
    stage_type = fields.Selection([
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Stage Type',  compute='_compute_stage_type', store=True, )
    assign_more_work_sub_ids = fields.One2many('assign.more.work.sub', 'assign_more_work_id', string='Assign More Work sub Lines')
    is_checked = fields.Boolean(string='Checked', default=False)
    payroll_plan_work_sub_id = fields.Many2one('payroll.plan.work.sub',string='Payroll Plan Work Sub')
    

    @api.depends('name')
    def _compute_name_department_id(self):
        for record in self:
            if record.name:
                record.department_id = record.name.department_id
            else:
                record.department_id = False

    @api.depends('name')
    def _compute_new_employee_card_number(self):
        for record in self:
            record.new_employee_card_number = record.name.barcode or ''

    @api.depends('stage_id')
    def _compute_stage_type(self):
        for record in self:
            record.stage_type = record.stage_id.stage_type or ''

    @api.depends('ex_employee')
    def _compute_ex_employee_card_number(self):
        for record in self:
            record.ex_employee_card_number = record.ex_employee.barcode or ''

    @api.onchange('stage_type', 'ex_employee')
    def _onchange_stage_type_ex_employee(self):
        if self.stage_type == 'cut' and self.ex_employee:
            self._load_pass_cutting_data()
        elif self.stage_type == 'sew' and self.ex_employee:
            self._load_sew_data()
        else:
            self.assign_more_work_sub_ids = [(5, 0, 0)]  # Clear existing lines

    def _load_pass_cutting_data(self):
        if self.stage_id and self.ex_employee:
            pass_cutting_records = self.env['work.pass.cutting'].search([
                ('stage_id', '=', self.stage_id.id),
                ('name', '=', self.ex_employee.id),
                 ('is_checked', '=', False)
            ])
            sub_lines = []
            for pass_cutting in pass_cutting_records:
                for sub in pass_cutting.work_sub_ids:
                    sub_line = {
                        'work_sub_id' :pass_cutting.id,
                        'unit_price': sub.unit_price,
                        'stage_id': sub.stage_id.id,
                        'pass_cutting_id': sub.pass_cutting_id.id,
                        'stage_type': self.stage_type,
                        'assign_more_work_id': self.id,
                      
                    }
                    sub_lines.append((0, 0, sub_line))
            self.assign_more_work_sub_ids = sub_lines
        else:
            self.assign_more_work_sub_ids = [(5, 0, 0)]  # Clear existing lines

    def _load_sew_data(self):
        if self.stage_id and self.ex_employee:
            sew_records = self.env['work.process'].search([
                ('stage_id', '=', self.stage_id.id),
                ('name', '=', self.ex_employee.id),
                 ('is_checked', '=', False)
            ])
            sub_lines = []
            for sew in sew_records:
                for sub in sew.work_sub_ids:
                    sub_line = {
                        'unit_price': sub.unit_price,
                        'stage_id': sub.stage_id.id,
                        'cutting_id': sub.cutting_id.id,
                        'stage_type': self.stage_type,
                        'assign_more_work_id': self.id,
                        'work_sub_id' : sew.id,
                    }
                    sub_lines.append((0, 0, sub_line))
            self.assign_more_work_sub_ids = sub_lines
        else:
            self.assign_more_work_sub_ids = [(5, 0, 0)]  # Clear existing lines
