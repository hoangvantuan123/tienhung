from odoo import models, fields, api
from datetime import datetime, timedelta
import pytz
class ReportWarehouse(models.Model):
    _name = 'report.warehouse'
    _description = 'Report Warehouse'

    name = fields.Many2one('hr.employee', string='Employee', default=lambda self: self.env.user.employee_id.id)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    plan = fields.Many2one('x.plan', string="Plan")
    po = fields.Many2one('product', string='PO')
    port = fields.Char(string='Port', compute='_compute_port', store=True)
    create_date = fields.Datetime(string='Create Date', default=fields.Datetime.now)
    subsidy = fields.Float(string='Subsidy')
    allowance_cd = fields.Float(string='Allowance CD')
    support_bonus_percent = fields.Float(string='Support Bonus %')
    unit_price = fields.Float(string='Unit Price')
    total_unit_price = fields.Float(string='Total Unit Price', compute='_compute_total_unit_price', store=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    report_warehouse_sub_ids = fields.One2many('report.warehouse.sub', 'report_warehouse_id', string='Work Subs')

    @api.depends('unit_price', 'subsidy')
    def _compute_total_unit_price(self):
        for record in self:
            record.total_unit_price = record.unit_price + record.subsidy

    @api.depends('total_unit_price', 'allowance_cd', 'support_bonus_percent')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.total_unit_price + record.allowance_cd + record.support_bonus_percent


    @api.model
    def create(self, vals):
        record = super(ReportWarehouse, self).create(vals)
        return record

    def write(self, vals):
        res = super(ReportWarehouse, self).write(vals)
        return res

    @api.onchange('plan', 'po')
    def onchange_plan_po(self):
        if not self.plan or not self.po:
            return

        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(vietnam_tz)
        previous_day = today - timedelta(days=1)

        warehouse_stock_model = self.env['warehouse.stock']
        sub_model = self.env['report.warehouse.sub']

        matching_stocks = warehouse_stock_model.search([
            ('name', '=', self.plan.id),
            ('po', '=', self.po.id),
            ('create_date', '>=', previous_day.strftime('%Y-%m-%d 00:00:00')), 
            ('create_date', '<', today.strftime('%Y-%m-%d 00:00:00')),
        ])

        self.report_warehouse_sub_ids.unlink()

        sub_records = []
        for stock in matching_stocks:
            sub_records.append((0, 0, {
                'report_warehouse_id': self.id,
                'warehouse_stock_id': stock.id,
                'plan': stock.name.id,
                'po': stock.po.id,
                'product_color': stock.product_color,
                'product_size': stock.product_size,
                'quantity_received': stock.quantity_received,
                'subsidy': stock.subsidy,
                'allowance_cd': stock.allowance_cd,
                'support_bonus_percent': stock.support_bonus_percent,
                'unit_price': stock.unit_price,
                'total_unit_price': stock.total_unit_price,
                'accumulated_quantity': stock.accumulated_quantity,
                'total_price': stock.total_price,
                'total_size_qty': stock.total_size_qty,
                'x_plan_id': stock.x_plan_id.id,
                'total_quantity_received': stock.total_quantity_received,
                'target_status': stock.target_status,
            }))

        self.report_warehouse_sub_ids = sub_records
    @api.depends('po')
    def _compute_port(self):
        for record in self:
            record.port = record.po.port or ''