from odoo import models, fields, api

class StageResponse(models.Model):
    _name = 'stage.response'
    _description = 'Stage Response'

    stage_id = fields.Many2one(comodel_name='stage', string='Stage')
    plan_id = fields.Many2one(comodel_name='x.plan', compute='_compute_plan_id', store=True, string='Plan')
    cutting_id = fields.Many2one(comodel_name='cutting.line', string='Cutting', domain="[('stage_id', '=', stage_id)]")
    pass_cutting_id = fields.Many2one(comodel_name='pass.cutting', string='Pass Cutting', domain="[('stage_id', '=', stage_id)]")