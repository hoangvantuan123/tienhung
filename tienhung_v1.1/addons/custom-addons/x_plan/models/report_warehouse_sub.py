from odoo import models, fields

class ReportWarehouseSub(models.Model):
    _name = 'report.warehouse.sub'
    _description = 'Report Warehouse Sub'

    report_warehouse_id = fields.Many2one('report.warehouse', string='Warehouse', ondelete='cascade')
    warehouse_stock_id = fields.Many2one('warehouse.stock', string='Warehouse Stock')
    plan = fields.Many2one('x.plan', string="Plan")
    po = fields.Many2one('product', string='PO Number')
    product_color = fields.Char(string='Product Color')
    product_size = fields.Selection([
            ('xxs', 'XXS'),
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('x2l', '2XL'),
            ('x3l', '3XL'),
            ('t2', '2T'),
            ('t3', '3T'),
            ('t4', '4T'),
            ('t5', '5T'),
            ('m12', '12M'),
            ('m18', '18M')
    ], string='Product Size')
    quantity_received = fields.Integer(string='Quantity Received')
    subsidy = fields.Float(string='Subsidy')
    allowance_cd = fields.Float(string='Allowance CD')
    support_bonus_percent = fields.Float(string='Support Bonus %')
    unit_price = fields.Float(string='Unit Price')
    total_unit_price = fields.Float(string='Total Unit Price')
    accumulated_quantity = fields.Integer(string='Accumulated Quantity')
    total_price = fields.Float(string='Total Price')
    total_size_qty = fields.Integer(string='Total Size Quantity')
    x_plan_id = fields.Many2one('x.plan', string="Plan")
    total_quantity_received = fields.Integer(string='Total Quantity Received')
    target_status = fields.Selection([('achieved', 'Achieved'), ('not_achieved', 'Not Achieved')], string='Target Status')