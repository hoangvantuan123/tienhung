# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class home_tien_hung(models.Model):
#     _name = 'home_tien_hung.home_tien_hung'
#     _description = 'home_tien_hung.home_tien_hung'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

