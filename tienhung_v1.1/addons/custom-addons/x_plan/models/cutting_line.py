from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class CuttingLine(models.Model):
    _name = 'cutting.line'
    _description = 'Cutting Line'

   

    name = fields.Text(string='Work Steps')
    stt = fields.Integer(string='STT')
    equipment = fields.Char(string='Equipment')
    worker_type = fields.Char(string='Worker Type')
    current_s = fields.Float(string='T/Current (S)')
    assistant_percent = fields.Float(string='Assistant %')
    total_time = fields.Float(string='Total Time')
    total_direct_cost = fields.Float(string='Total Direct Cost (May+Pick)')
    unit_price_05 = fields.Float(string='P/C Unit Price 0.5')
    stage_id = fields.Many2one( comodel_name='stage', string="Stage", required=True)
    total_cost_history_ids = fields.One2many(
        'cutting.line.history', 'cutting_line_id', string='Total Cost History')
    work_process_id = fields.One2many('work.process','cutting_line_id', string='Work Process')
    

    employee_count = fields.Integer(string='Employee Count', compute='_compute_employee_count', store=True)
    employee_details = fields.Html(string='Employee Details', compute='_compute_employee_details')

    @api.model
    def create(self, vals):
        record = super(CuttingLine, self).create(vals)
        if 'unit_price_05' in vals:
            self.env['cutting.line.history'].create({
                'cutting_line_id': record.id,
                'unit_price_05': vals['unit_price_05'],
            })
        return record

    def write(self, vals):
        result = super(CuttingLine, self).write(vals)
        if 'unit_price_05' in vals:
            for record in self:
                self.env['cutting.line.history'].create({
                    'cutting_line_id': record.id,
                    'unit_price_05': vals['unit_price_05'],
                })
        return result
    
    @api.model
    def default_get(self, fields_list):
        defaults = super(CuttingLine, self).default_get(fields_list)
        active_id = self._context.get('active_id')
        if active_id:
            active_record = self.env['stage'].browse(active_id)
            defaults['stage_id'] = active_record.id
        return defaults

    
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

