from odoo import models, fields, api

class StageLine(models.Model):
    _name = 'stage.line'
    _description = 'Stage Line'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    stageteam_id = fields.Many2one('stageteam.list', string='Stage Team', ondelete='cascade')
    employee_card = fields.Char(string='Employee Card Number', compute='_compute_employee_card_number')
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    
    target_ids = fields.One2many('target', 'target_stage_line_id', string='Target')    
    stage_id = fields.Many2one('stage', string='Stage', compute='_compute_stage_id')

    stage_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Stage Type', compute='_compute_stage_type', store=True)
    work_pass_cutting_ids = fields.One2many('work.pass.cutting', 'work_stage_passcutting_line_id', string='Work Pass Cutting') 
    work_cutting_ids = fields.One2many('work.process', 'work_stage_cutting_line_id', string='Work Cutting') 

    @api.depends('employee_id')
    def _compute_employee_card_number(self):
        for record in self:
            record.employee_card = record.employee_id.barcode or ''

    @api.depends('stageteam_id')
    def _compute_stage_id(self):
        for record in self:
            record.stage_id = record.stageteam_id.stage_id or ''

    
    @api.depends('stage_id')
    def _compute_stage_type(self):
        for record in self:
            record.stage_type = record.stage_id.stage_type or ''
