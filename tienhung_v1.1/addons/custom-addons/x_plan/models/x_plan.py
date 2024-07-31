from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import csv
from datetime import datetime


class Plan(models.Model):
    _name = 'x.plan'
    _description = 'Manage Plan X'

    name = fields.Char(string='Product Code', required=True)
    customer = fields.Char(string='Customer', required=True)
    season = fields.Char(string='Season')
    total_time = fields.Integer( string='Total Time', compute='_compute_total_time', store=True)
    contract_price = fields.Monetary( string='Contract Price ($)', currency_field='currency_id')
    manufacturing_price = fields.Monetary( string='Manufacturing Price (VND)', currency_field='currency_id')
    product_image = fields.Binary(string='Product Image')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    status = fields.Selection([
        ('received', 'Received Information'),
        ('planning', 'Planning'),
        ('analyzing', 'Analyzing'),
        ('producing', 'Producing'),
        ('warehouse', 'In Warehouse'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Plan Status', default='received')
    product_style_ids = fields.One2many(
        'product', 'x_plan_csv_id', string="Product Styles")
    total_products = fields.Integer(string='Total Products', compute='_compute_total_products', store=True)
    total_xs = fields.Integer(string='Total XS', compute='_compute_total_xs', store=True)
    total_s = fields.Integer(string='Total S', compute='_compute_total_s', store=True)
    total_m = fields.Integer(string='Total M', compute='_compute_total_m', store=True)
    total_l = fields.Integer(string='Total L', compute='_compute_total_l', store=True)
    total_xl = fields.Integer(string='Total XL', compute='_compute_total_xl', store=True)
    total_xxl = fields.Integer(string='Total XXL', compute='_compute_total_xxl', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    x_stage_ids = fields.One2many(
            'stage', 'x_plan_id', string='Planning Stages', )
    teams_cut_text = fields.Char(string='Teams Cut', compute='_compute_teams_cut_text', store=True)
    teams_sew_text = fields.Char(string='Teams Sew', compute='_compute_teams_sew_text', store=True)
    entered_quantity = fields.Integer(string='Total number of goods imported', compute='_compute_entered_quantity', store=True)
    target_status = fields.Selection([('achieved', 'Achieved'), ('not_achieved', 'Not Achieved')], string='Target Status', compute='_compute_status', store=True)
    image = fields.Binary(string='Image')
    warehouse_stock_ids = fields.One2many(
        'warehouse.stock', 'name', string="Warehouse Stock")
    
    target_ids = fields.One2many(
        'target', 'plan_id', string="Target")
    
    @api.depends('start_date', 'end_date')
    def _compute_total_time(self):
        for record in self:
            if record.start_date and record.end_date:
                start = fields.Datetime.from_string(record.start_date)
                end = fields.Datetime.from_string(record.end_date)
                duration = end - start
                # Chuyển đổi giây thành giờ và làm tròn
                record.total_time = int(duration.total_seconds() / 3600)
            else:
                record.total_time = 0

    @api.onchange('currency_id')
    def onchange_currency_id(self):
        if self.currency_id:
            self.contract_price_currency_id = self.currency_id.id
            self.manufacturing_price_currency_id = self.currency_id.id

    def _parse_date(self, date_str):
        if date_str:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        return None
    
    @api.depends('product_style_ids.total_sizes')
    def _compute_total_products(self):
        for plan in self:
            total = sum(product.total_sizes for product in plan.product_style_ids)
            plan.total_products = total

    

    @api.depends('product_style_ids.total_xs')
    def _compute_total_xs(self):
        for plan in self:
            total_xs = sum(product.xs for product in plan.product_style_ids)
            plan.total_xs = total_xs

    @api.depends('product_style_ids.total_s')
    def _compute_total_s(self):
        for plan in self:
            total_s = sum(product.s for product in plan.product_style_ids)
            plan.total_s = total_s

    @api.depends('product_style_ids.total_m')
    def _compute_total_m(self):
        for plan in self:
            total_m = sum(product.m for product in plan.product_style_ids)
            plan.total_m = total_m

    @api.depends('product_style_ids.total_l')
    def _compute_total_l(self):
        for plan in self:
            total_l = sum(product.l for product in plan.product_style_ids)
            plan.total_l = total_l

    @api.depends('product_style_ids.total_xl')
    def _compute_total_xl(self):
        for plan in self:
            total_xl = sum(product.xl for product in plan.product_style_ids)
            plan.total_xl = total_xl

    @api.depends('product_style_ids.total_xxl')
    def _compute_total_xxl(self):
        for plan in self:
            total_xxl = sum(product.xxl for product in plan.product_style_ids)
            plan.total_xxl = total_xxl

    @api.model
    def _update_total_products(self):
        for plan in self:
            total = sum(product.total_sizes for product in plan.product_style_ids)
            plan.total_products = total
            total_xs = sum(product.xs for product in plan.product_style_ids)
            plan.total_xs = total_xs
            total_s = sum(product.s for product in plan.product_style_ids)
            plan.total_s = total_s
            total_m = sum(product.m for product in plan.product_style_ids)
            plan.total_m = total_m
            total_l = sum(product.l for product in plan.product_style_ids)
            plan.total_l = total_l
            total_xl = sum(product.xl for product in plan.product_style_ids)
            plan.total_xl = total_xl
            total_xxl = sum(product.xxl for product in plan.product_style_ids)
            plan.total_xxl = total_xxl
   
    @api.depends('entered_quantity', 'total_products')
    def _compute_status(self):
        for record in self:
            if record.entered_quantity >= record.total_products:
                record.target_status = 'achieved'
            else:
                record.target_status = 'not_achieved'


    @api.depends('x_stage_ids.stage_type', 'x_stage_ids.teams')
    def _compute_teams_cut_text(self):
        for plan in self:
            teams_cut = []
            for stage in plan.x_stage_ids:
                if stage.stage_type == 'cut':
                    teams_cut.extend(stage.teams.mapped('name'))
            plan.teams_cut_text = ', '.join(teams_cut)

    @api.depends('x_stage_ids.stage_type', 'x_stage_ids.teams')
    def _compute_teams_sew_text(self):
        for plan in self:
            teams_sew = []
            for stage in plan.x_stage_ids:
                if stage.stage_type == 'sew':
                    teams_sew.extend(stage.teams.mapped('name'))
            plan.teams_sew_text = ', '.join(teams_sew)

   

    @api.depends('warehouse_stock_ids.quantity_received')
    def _compute_entered_quantity(self):
        for stock in self:
            total_qty = sum(stock.total_quantity_received for stock in stock.warehouse_stock_ids)
            stock.entered_quantity = total_qty


    @api.model
    def _update_total_entered_quantity(self):
        for stock in self:
            total = sum(stock.total_quantity_received for stock in stock.warehouse_stock_ids)
            stock.entered_quantity = total