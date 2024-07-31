from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
class WorkProcessPassCutting(models.Model):
    _name = 'work.pass.cutting'
    _description = 'Work Process Pass Cutting'

    
    name = fields.Many2one('hr.employee', string='Employee Name')
    completed = fields.Boolean(string='Completed')
    to_be_completed = fields.Boolean(string='To Be Completed')
    unit_price = fields.Float(string='Total Unit Price', compute='_compute_unit_price_counts', store=True)
    product_code = fields.Char(string='Product Code')
    team = fields.Char(string='Team')
    employee_card_number = fields.Char(string='Employee Card Number', compute='_compute_new_employee_card_number', store=True, readonly=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    duration = fields.Integer(string='Duration', compute='_compute_duration_pass_cutting', store=True)
   
    pass_cutting_id = fields.Many2one(comodel_name='pass.cutting', string='Pass Cutting')
    work_step = fields.Char(string='Work Step', compute='_compute_work_step', store=True)
    stage_id = fields.Many2one(comodel_name='stage', string='Stage')
    work_sub_ids = fields.One2many('work.pass.cutting.sub','work_sub_id', string='Work Sub')
    assign_more_work_sub_ids = fields.One2many('assign.more.work.sub','work_sub_id', string='More Work Sub')
    work_stage_passcutting_line_id = fields.Many2one('stage.line', string='Stage Team Line')

    productivity_reports_ids = fields.One2many('productivity.reports','cutting_line_work_id', string='Productivity Reports')
    
    assign_more_work_sub_filtered_ids = fields.One2many('assign.more.work.sub', compute='_compute_assign_more_work_sub_filtered_ids', string='Filtered More Work Sub')

    department_id = fields.Many2one('hr.department', string='Department', compute='_compute_department_id', store=True)
    plan_id = fields.Many2one('x.plan', string='Plan', compute='_compute_plan_id', store=True)
    pass_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Pass Type', compute='_compute_pass_type', store=True)
    image = fields.Binary(string='Image', compute='_compute_plan_id', store=True)
    work_sub_filtered_ids = fields.One2many(
        'work.pass.cutting.sub', compute='_compute_work_sub_filtered_ids', string='Filtered Work Sub'
    )

    is_checked = fields.Boolean(string='Checked', default=False)
    payroll_plan_work_sub_id = fields.Many2one('payroll.plan.work.sub',string='Payroll Plan Work Sub')

    @api.depends('stage_id')
    def _compute_plan_id(self):
        for record in self:
            record.plan_id = record.stage_id.x_plan_id or ''
    @api.depends('plan_id')
    def _compute_image(self):
        for record in self:
            record.image = record.plan_id.image or ''

    @api.depends('stage_id')
    def _compute_pass_type(self):
        for record in self:
            record.pass_type = record.stage_id.stage_type or ''

    @api.depends('name')
    def _compute_new_employee_card_number(self):
        for record in self:
            record.employee_card_number = record.name.barcode or ''

    @api.depends('name')
    def _compute_department_id(self):
        for record in self:
            if record.name:
                record.department_id = record.name.department_id
            else:
                record.department_id = False
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
    @api.depends('work_sub_ids')
    def _compute_work_sub_filtered_ids(self):
        for record in self:
            record.work_sub_filtered_ids = self.env['work.pass.cutting.sub'].search([
                ('work_sub_id', '=', record.id),
                ('is_checked', '=', False)  
            ])
            
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

    @api.depends('pass_cutting_id')
    def _compute_work_step(self):
        for record in self:
            if record.pass_cutting_id:
                record.work_step = record.pass_cutting_id.name
            else:
                record.work_step = ''

    @api.onchange('pass_cutting_id')
    def _onchange_pass_cutting_id(self):
        if self.pass_cutting_id:
            cutting_line = self.env['pass.cutting'].browse(self.pass_cutting_id.id)
            self.unit_price = cutting_line.total_cost

    @api.model
    def create(self, vals):
        record = super(WorkProcessPassCutting, self).create(vals)
        if record.pass_cutting_id:
            record.unit_price = record.pass_cutting_id.total_cost
        return record

    def write(self, vals):
        res = super(WorkProcessPassCutting, self).write(vals)
        if 'pass_cutting_id' in vals:
            for record in self:
                if record.pass_cutting_id:
                    record.unit_price = record.pass_cutting_id.total_cost
        return res

    @api.model
    def default_get(self, fields):
        res = super(WorkProcessPassCutting, self).default_get(fields)
        if 'pass_cutting_id' in fields and res.get('pass_cutting_id'):
            pass_cutting = self.env['pass.cutting'].browse(res['pass_cutting_id'])
            res['unit_price'] = pass_cutting.total_cost
        return res


    
    @api.depends('work_sub_ids.unit_price')
    def _compute_unit_price_counts(self):
        for record in self:
            record.unit_price = sum(line.unit_price for line in record.work_sub_ids)

    @api.onchange('work_sub_ids')
    def _onchange_timekeeping_line_ids(self):
        self._compute_unit_price_counts()

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        return super(WorkProcessPassCutting, self).search(args, offset, limit, order)
