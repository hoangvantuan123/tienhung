from odoo import models, fields, api

class CuttingLineHistory(models.Model):
    _name = 'cutting.line.history'
    _description = 'Cutting Line History'

    cutting_line_id = fields.Many2one('cutting.line', string='Cutting Line')
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)
    unit_price_05 = fields.Float(string='Total Cost')
