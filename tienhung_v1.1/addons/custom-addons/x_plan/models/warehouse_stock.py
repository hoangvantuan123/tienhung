from odoo import models, fields, api

class WarehouseStock(models.Model):
    _name = 'warehouse.stock'
    _description = 'Warehouse Stock Information'

    name = fields.Many2one('x.plan', string="Plan")
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    po = fields.Many2one('product', string='PO Number')
    product_color = fields.Char(string='Product Color', related='po.colors', store=True)
    product_size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    ], string='Product Size')
    quantity_received = fields.Integer(string='Quantity Received', required=True)
    subsidy = fields.Float(string='Subsidy')
    allowance_cd = fields.Float(string='Allowance CD')
    support_bonus_percent = fields.Float(string='Support Bonus %')
    port = fields.Char(string='Port', compute='_compute_port', store=True)
    unit_price = fields.Float(string='Unit Price')
    total_unit_price = fields.Float(string='Total Unit Price', compute='_compute_total_unit_price', store=True)
    accumulated_quantity = fields.Integer(string='Accumulated Quantity', compute='_compute_accumulated_quantity', store=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    total_size_qty = fields.Integer(string='Total Size Quantity', compute='_compute_total_size_qty', store=True, readonly=True)
    x_plan_id = fields.Many2one(comodel_name='x.plan', related='po.x_plan_csv_id', string="Plan", store=True)
    total_quantity_received = fields.Integer(string='Total Quantity Received', compute='_compute_quantity_received')
    target_status = fields.Selection([
        ('achieved', 'Achieved'),
        ('not_achieved', 'Not Achieved'),
        ('error', 'Error'),
    ], string='Target Status', compute='_compute_status', store=True)

    @api.depends('po')
    def _compute_port(self):
        for record in self:
            record.port = record.po.port or ''

    @api.depends('po', 'product_size')
    def _compute_total_size_qty(self):
        for record in self:
            if record.po and record.product_size:
                size_field = f'total_{record.product_size}'
                record.total_size_qty = getattr(record.po, size_field, 0)

    @api.depends('quantity_received', 'x_plan_id', 'po', 'product_color', 'product_size')
    def _compute_accumulated_quantity(self):
        for record in self:
            if record.x_plan_id and record.po and record.product_color and record.product_size:
                total_quantity_received_history = sum(
                    self.search([
                        ('x_plan_id', '=', record.x_plan_id.id),
                        ('po', '=', record.po.id),
                        ('product_color', '=', record.product_color),
                        ('product_size', '=', record.product_size),
                    ]).mapped('quantity_received')
                )
                record.accumulated_quantity = total_quantity_received_history

    @api.depends('quantity_received', 'total_unit_price', 'allowance_cd', 'support_bonus_percent')
    def _compute_total_price(self):
        for record in self:
            bonus_ht = (record.total_unit_price * record.support_bonus_percent) / 100
            record.total_price = record.total_unit_price + record.allowance_cd + bonus_ht

    @api.depends('quantity_received')
    def _compute_quantity_received(self):
        for record in self:
            record.total_quantity_received = record.quantity_received

    @api.model
    def create(self, vals):
        product = super(WarehouseStock, self).create(vals)
        if product.name:
            product.name._update_total_entered_quantity()
        return product

    def write(self, vals):
        result = super(WarehouseStock, self).write(vals)
        for product in self:
            if product.name:
                product.name._update_total_entered_quantity()
        return result

    @api.depends('x_plan_id', 'po', 'product_color', 'product_size')
    def _compute_total_quantity_received(self):
        for rec in self:
            total_quantity_received_history = sum(
                rec.search([
                    ('x_plan_id', '=', rec.x_plan_id.id),
                    ('po', '=', rec.po.id),
                    ('product_color', '=', rec.product_color),
                    ('product_size', '=', rec.product_size),
                ]).mapped('quantity_received')
            )
            rec.accumulated_quantity = total_quantity_received_history

    @api.depends('unit_price', 'subsidy')
    def _compute_total_unit_price(self):
        for record in self:
            record.total_unit_price = record.unit_price + record.subsidy

    @api.depends('x_plan_id', 'po', 'product_color', 'product_size')
    def _compute_status(self):
        for record in self:
            if record.quantity_received == record.total_size_qty:
                    record.target_status = 'achieved'
            elif record.quantity_received< record.total_size_qty:
                record.target_status = 'not_achieved'
            elif record.quantity_received > record.total_size_qty:
                record.target_status = 'error'

    @api.onchange('product_size', 'po')
    def _onchange_product_size(self):
        if self.product_size and self.po:
            product = self.po
            if product:
                size_field = f'total_{self.product_size}'
                self.total_size_qty = getattr(product, size_field, 0)  # Lưu tổng số size vào trường mới
