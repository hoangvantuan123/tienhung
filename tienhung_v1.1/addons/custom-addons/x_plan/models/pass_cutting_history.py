from odoo import models, fields, api

class PassCuttingHistory(models.Model):
    _name = 'pass.cutting.history'
    _description = 'Pass Cutting History'

    pass_cutting_id = fields.Many2one('pass.cutting', string='Pass Cutting')
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now)
    total_cost = fields.Float(string='Total Cost')
