from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Stage(models.Model):
    _name = 'stage'
    _description = 'Stage in Plan'

    @api.depends('stage_type', 'x_plan_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.x_plan_id.name} - stage  - {record.stage_type}"

    name = fields.Char(string='Stage Name', compute='_compute_name', store=True)
    department_id = fields.Many2one('hr.department', string='Department')
    teams = fields.Many2many('hr.department', string='Teams') #

    quantity_per_team = fields.Integer(string='Total Execution Quantity per Team', compute='_compute_quantity_per_team', readonly=True) #
    total_quantity_per_team = fields.Integer(string='Total Quantity', compute='_compute_quantity_per_team_x_plan', readonly=True) #
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    computed_total_duration = fields.Float( string='Computed Total Duration (hours)', compute='_compute_total_duration', store=True)
    stage_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Stage Type', required=True)
    description = fields.Text(string='Description')
    x_plan_id = fields.Many2one( comodel_name='x.plan', string="Plan", required=True)
    pass_cutting_ids = fields.One2many(
        'pass.cutting', 'stage_id', string='Pass Cutting')
    cutting_line_ids = fields.One2many(
        'cutting.line', 'stage_id', string='Cutting Line')
    work_process_id = fields.One2many('work.process', 'stage_id' ,string='Work Process')
    work_pass_cutting_id = fields.One2many('work.pass.cutting', 'stage_id' ,string='Work Process')
    stageteam_ids = fields.One2many(
        'stageteam.list', 'stage_id', string='Stage Team')
    target_ids = fields.One2many(
        'target', 'target_stage_id', string='Target')

    work_sub_filtered_cut_ids = fields.One2many(
        'work.pass.cutting', compute='_compute_work_sub_filtered_cut_ids', string='Filtered Work Cut'
    )
    work_sub_filtered_sew_ids = fields.One2many(
        'work.process', compute='_compute_work_sub_filtered_sew_ids', string='Filtered Work Sew'
    )

    @api.depends('work_pass_cutting_id')
    def _compute_work_sub_filtered_cut_ids(self):
        for record in self:
            record.work_sub_filtered_cut_ids = self.env['work.pass.cutting'].search([
                ('is_checked', '=', False)  ,
                ('stage_id', '=', record.id), 
            ])

    @api.depends('work_process_id')
    def _compute_work_sub_filtered_sew_ids(self):
        for record in self:
            record.work_sub_filtered_sew_ids = self.env['work.process'].search([
                ('is_checked', '=', False), 
                ('stage_id', '=', record.id), 
            ])



    def write(self, vals):
        res = super(Stage, self).write(vals)
        if 'stage_type' in vals:
            for record in self:
                if record.stage_type in ['cut', 'sew', 'prepare']:
                    record.x_plan_id.write({'name': record.x_plan_id.name})  # Cập nhật trường nào đó trong plan
        return res
    
    @api.depends('quantity_per_team')
    def _compute_quantity_per_team_x_plan(self):
        for record in self:
            record.total_quantity_per_team = record.x_plan_id.total_products or ''

    @api.depends('stageteam_ids.quantity_per_team')
    def _compute_quantity_per_team(self):
        for record in self:
            total_quantity = sum(record.stageteam_ids.mapped('quantity_per_team'))
            record.quantity_per_team = total_quantity

    @api.constrains('stageteam_ids', 'total_quantity_per_team')
    def _check_total_quantity(self):
        for record in self:
            total_quantity = sum(record.stageteam_ids.mapped('quantity_per_team'))
            if total_quantity > record.total_quantity_per_team:
                raise ValidationError("The total quantity per team cannot exceed the total products in the plan.")

    @api.depends('start_time', 'end_time')
    def _compute_total_duration(self):
        for stage in self:
            if stage.start_time and stage.end_time:
                start_dt = fields.Datetime.from_string(stage.start_time)
                end_dt = fields.Datetime.from_string(stage.end_time)
                duration_hours = (end_dt - start_dt).total_seconds() / 3600.0
                stage.computed_total_duration = duration_hours
            else:
                stage.computed_total_duration = 0.0
    
    @api.model
    def default_get(self, fields_list):
        defaults = super(Stage, self).default_get(fields_list)
        active_id = self._context.get('active_id')
        if active_id:
            active_record = self.env['x.plan'].browse(active_id)
            defaults['x_plan_id'] = active_record.id
        return defaults

    
