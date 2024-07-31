from odoo import models, fields, api
from datetime import datetime
import io
import csv
from odoo.exceptions import ValidationError


class PassCutting(models.Model):
    _name = 'pass.cutting'
    _description = 'Pass Cutting'


    name = fields.Text(string='Work Steps', required=True)
    stt = fields.Integer(string='STT')
    step = fields.Char(string='Step')
    worker_type = fields.Char(string='Worker Type')
    assistant = fields.Char(string='Assistant')
    start_time = fields.Float(string='Time')
    end_time = fields.Float(string='Time')
    total_time = fields.Float( string='Total Time (s)')
    total_cost = fields.Float(string='Total Cost', track_visibility='onchange')
    stage_id = fields.Many2one( comodel_name='stage', string="Stage")
    total_cost_history_ids = fields.One2many(
        'pass.cutting.history', 'pass_cutting_id', string='Total Cost History')
    work_process_id = fields.One2many('work.pass.cutting','pass_cutting_id', string='Work Process Pass Cutting')
    
    work_sub_ids = fields.One2many('work.pass.cutting.sub', 'pass_cutting_id', string='Work Subs')
    employee_count = fields.Integer(string='Employee Count', compute='_compute_employee_count', store=True)
    employee_details = fields.Html(string='Employee Details', compute='_compute_employee_details')

    @api.depends('work_process_id')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = len(record.work_process_id)

    @api.depends('work_process_id')
    def _compute_employee_details(self):
        for record in self:
            employee_info = "<div style='text-align: center;'>"
            count = 0
            more_count = 0
            for work_process in record.work_process_id:
                if work_process.name:
                    if count < 1:  
                        employee_info += f"<div style='display: inline-block; margin-right: 10px;'><img src='/web/image/hr.employee/{work_process.name.id}/image_1024' width='30' height='30' style='border-radius: 12%;' /><br/>{work_process.name.name}</div>"
                        count += 1
                    else:
                        more_count += 1
            if more_count > 0:
                employee_info += f"<div style='display: inline-block;'>+ {more_count} more</div>"
            employee_info += "</div>"
            record.employee_details = employee_info


   
    @api.model
    def create(self, vals):
        record = super(PassCutting, self).create(vals)
        if 'total_cost' in vals:
            self.env['pass.cutting.history'].create({
                'pass_cutting_id': record.id,
                'total_cost': vals['total_cost'],
            })
        return record

    def write(self, vals):
        result = super(PassCutting, self).write(vals)
        if 'total_cost' in vals:
            for record in self:
                self.env['pass.cutting.history'].create({
                    'pass_cutting_id': record.id,
                    'total_cost': vals['total_cost'],
                })
        return result

    @api.model
    def default_get(self, fields_list):
        defaults = super(PassCutting, self).default_get(fields_list)
        active_id = self._context.get('active_id')
        if active_id:
            active_record = self.env['stage'].browse(active_id)
            defaults['stage_id'] = active_record.id
        return defaults
    
    """  @api.onchange('work_process_id')
    def _onchange_work_process_id(self):
        for record in self.work_process_id:
            if record.pass_cutting_id:
                record.unit_price = record.pass_cutting_id.total_cost """