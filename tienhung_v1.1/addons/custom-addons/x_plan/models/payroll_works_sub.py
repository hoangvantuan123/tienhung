from odoo import models, fields, api

class PayrollPlanWorkSub(models.Model):
    _name = 'payroll.plan.work.sub'
    _description = 'Payroll Plan Work Sub'

    name = fields.Many2one('hr.employee', string='Employee')
    payroll_work_id = fields.Many2one('payroll.plan.work', string='Payroll Work', ondelete='cascade')
    cd = fields.Many2one(comodel_name='pass.cutting', string='CĐ')
    cd_sew = fields.Many2one(comodel_name='cutting.line', string='CĐ')
    sl = fields.Integer(string='SL')
    dg = fields.Integer(string='ĐG')
    type = fields.Selection([
        ('', ''),
        ('*', '*')
    ], string='Type')
    money = fields.Integer(string='Money')
    department_id = fields.Many2one('hr.department', string='Department', compute='_compute_department_id', store=True)
    stage_id = fields.Many2one(comodel_name='stage', string='Stage')
    stage_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Pass Type', compute='_compute_stage_type', store=True)
    
    is_checked = fields.Boolean(string='Checked', default=False)
    work_sub_id = fields.Many2one('work.pass.cutting.sub', string='Payroll Plan Work Sub')
    work_more_sub_id = fields.Many2one('assign.more.work.sub', string='Payroll Plan Work More Sub')
    work_sew_sub_id = fields.Many2one('work.process.cutting.sub', string='Payroll Plan Sew Sub')

    @api.depends('name')
    def _compute_department_id(self):
        for record in self:
            record.department_id = record.name.department_id if record.name else False

    @api.depends('stage_id')
    def _compute_stage_type(self):
        for record in self:
            record.stage_type = record.stage_id.stage_type if record.stage_id else ''
    @api.model
    def create(self, vals):
        record = super(PayrollPlanWorkSub, self).create(vals)
        if record.work_sub_id:
            record.work_sub_id.is_checked = True
        if record.work_more_sub_id:
            record.work_more_sub_id.is_checked = True
        if record.work_sew_sub_id:
            record.work_sew_sub_id.is_checked = True
        record._update_productivity_reports()
        return record

    def write(self, vals):
        res = super(PayrollPlanWorkSub, self).write(vals)
        for record in self:
            if record.work_sub_id:
                record.work_sub_id.is_checked = True
            if record.work_more_sub_id:
                record.work_more_sub_id.is_checked = True
            if record.work_sew_sub_id:
                record.work_sew_sub_id.is_checked = True
            if 'sl' in vals and record.work_sub_id:
                record.work_sub_id.ns = vals.get('sl', record.sl)
        return res

    def unlink(self):
        work_sub_ids = self.mapped('work_sub_id')
        work_more_sub_ids = self.mapped('work_more_sub_id')
        work_sew_ids = self.mapped('work_sew_sub_id')
        
        res = super(PayrollPlanWorkSub, self).unlink()
        
        for work_sub in work_sub_ids:
            if not self.search_count([('work_sub_id', '=', work_sub.id)]):
                work_sub.is_checked = False
        for work_more_sub in work_more_sub_ids:
            if not self.search_count([('work_more_sub_id', '=', work_more_sub.id)]):
                work_more_sub.is_checked = False
        for work_sew_sub in work_sew_ids:
            if not self.search_count([('work_sew_sub_id', '=', work_sew_sub.id)]):
                work_sew_sub.is_checked = False
        
        return res


    def _update_productivity_reports(self):
        for record in self:
            if record.work_sub_id:
                self.env['productivity.reports'].search([
                    ('cutting_line_work_sub_id', '=', record.work_sub_id.id)
                ]).write({'is_checked': True})

                self.env['work.pass.cutting'].search([
                    ('id', '=', record.work_sub_id.work_sub_id.id)
                ]).write({'is_checked': True})

            if record.work_more_sub_id:
                self.env['productivity.reports'].search([
                    ('cutting_line_work_sub_id', '=', record.work_more_sub_id.id)
                ]).write({'is_checked': True})

                self.env['assign.more.work'].search([
                    ('id', '=', record.work_more_sub_id.assign_more_work_id.id)
                ]).write({'is_checked': True})
            
            if record.work_sew_sub_id:
                self.env['productivity.reports'].search([
                    ('sewing_line_work_sub_id', '=', record.work_sew_sub_id.id)
                ]).write({'is_checked': True})

                self.env['work.process'].search([
                    ('id', '=', record.work_sew_sub_id.work_sub_id.id)
                ]).write({'is_checked': True})