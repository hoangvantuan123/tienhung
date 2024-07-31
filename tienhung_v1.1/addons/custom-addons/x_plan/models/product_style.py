from odoo import models, fields, api


class ProductStyle(models.Model):
    _name = 'product'
    _description = 'Product Style'
    @api.depends('style_name', 'po', 'colors')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.style_name} - {record.po} - {record.colors}"

   
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    style_name = fields.Char(string='Style Name')
    po = fields.Char(string='PO')
    ngay_kiem_1 = fields.Date(string='Ngày kiểm 1')
    ngay_kiem_2 = fields.Date(string='Ngày kiểm 2')
    colors = fields.Char(string='Colors')
    port = fields.Char(string='PORT')
    """ xs = fields.Integer(string='XS')
    s = fields.Integer(string='S')
    m = fields.Integer(string='M')
    l = fields.Integer(string='L')
    xl = fields.Integer(string='XL')
    xxl = fields.Integer(string='XXL') """

    xxs = fields.Integer(string='XXS')
    xs = fields.Integer(string='XS')
    s = fields.Integer(string='S')
    m = fields.Integer(string='M')
    l = fields.Integer(string='L')
    xl = fields.Integer(string='XL')
    xxl = fields.Integer(string='XXL')
    x2l = fields.Integer(string='2XL')
    x3l = fields.Integer(string='3XL')
    t2 = fields.Integer(string='2T')
    t3 = fields.Integer(string='3T')
    t4 = fields.Integer(string='4T')
    t5 = fields.Integer(string='5T')
    m12 = fields.Integer(string='12M')
    m18 = fields.Integer(string='18M')

    total_sizes = fields.Integer( string='Total', compute='_compute_total_sizes')
    x_plan_csv_id = fields.Many2one( comodel_name='x.plan', string="Plan CSV")

    total_xs = fields.Integer(string='Total XS', compute='_compute_total_sizes')
    total_s = fields.Integer(string='Total S', compute='_compute_total_sizes')
    total_m = fields.Integer(string='Total M', compute='_compute_total_sizes')
    total_l = fields.Integer(string='Total L', compute='_compute_total_sizes')
    total_xl = fields.Integer(string='Total XL', compute='_compute_total_sizes')
    total_xxl = fields.Integer(string='Total XXL', compute='_compute_total_sizes')

    show_style_name = fields.Boolean(compute='_compute_show_field', store=False)
    show_po = fields.Boolean(compute='_compute_show_field', store=False)
    show_ngay_kiem_1 = fields.Boolean(compute='_compute_show_field', store=False)
    show_ngay_kiem_2 = fields.Boolean(compute='_compute_show_field', store=False)
    show_colors = fields.Boolean(compute='_compute_show_field', store=False)
    show_port = fields.Boolean(compute='_compute_show_field', store=False)
    show_xs = fields.Boolean(compute='_compute_show_field', store=False)
    show_s = fields.Boolean(compute='_compute_show_field', store=False)
    show_m = fields.Boolean(compute='_compute_show_field', store=False)
    show_l = fields.Boolean(compute='_compute_show_field', store=False)
    show_xl = fields.Boolean(compute='_compute_show_field', store=False)
    show_xxl = fields.Boolean(compute='_compute_show_field', store=False)
    show_total_sizes = fields.Boolean(compute='_compute_show_field', store=False)

    

    @api.depends('style_name', 'po', 'ngay_kiem_1', 'ngay_kiem_2', 'colors', 'port', 'xs', 's', 'm', 'l', 'xl', 'xxl', 'total_sizes')
    def _compute_show_field(self):
        for record in self:
            record.show_style_name = bool(record.style_name)
            record.show_po = bool(record.po)
            record.show_ngay_kiem_1 = bool(record.ngay_kiem_1)
            record.show_ngay_kiem_2 = bool(record.ngay_kiem_2)
            record.show_colors = bool(record.colors)
            record.show_port = bool(record.port)
            record.show_xs = bool(record.xs)
            record.show_s = bool(record.s)
            record.show_m = bool(record.m)
            record.show_l = bool(record.l)
            record.show_xl = bool(record.xl)
            record.show_xxl = bool(record.xxl)
            record.show_total_sizes = bool(record.total_sizes)

    @api.depends('xxs', 'xs', 's', 'm', 'l', 'xl', 'xxl', 'x2l', 'x3l', 't2', 't3', 't4', 't5', 'm12', 'm18')
    def _compute_total_sizes(self):
        for record in self:
            record.total_sizes = (
                record.xxs + record.xs + record.s + record.m + record.l + record.xl +
                record.xxl + record.x2l + record.x3l + record.t2 + record.t3 +
                record.t4 + record.t5 + record.m12 + record.m18
            )
            record.total_xs = record.xs
            record.total_s = record.s
            record.total_m = record.m
            record.total_l = record.l
            record.total_xl = record.xl
            record.total_xxl = record.xxl
    

    @api.model
    def default_get(self, fields_list):
        defaults = super(ProductStyle, self).default_get(fields_list)
        active_id = self._context.get('active_id')
        if active_id:
            active_record = self.env['x.plan'].browse(active_id)
            defaults['x_plan_csv_id'] = active_record.id
        return defaults

    @api.model
    def create(self, vals):
        product = super(ProductStyle, self).create(vals)
        # Cập nhật lại tổng số sản phẩm trong kế hoạch liên quan
        if product.x_plan_csv_id:
            product.x_plan_csv_id._update_total_products()
        return product

    def write(self, vals):
        result = super(ProductStyle, self).write(vals)
        # Cập nhật lại tổng số sản phẩm trong kế hoạch liên quan
        for product in self:
            if product.x_plan_csv_id:
                product.x_plan_csv_id._update_total_products()
        return result

    
