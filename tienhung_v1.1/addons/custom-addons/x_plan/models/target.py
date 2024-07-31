from odoo import models, fields, api
from datetime import datetime
import pytz

class Target(models.Model):
    _name = 'target'
    _description = 'Target'

    user_id = fields.Many2one('hr.employee', string='Employee Name')
    employee_card_number = fields.Char(string='Employee Card Number', compute='_compute_new_employee_card_number', store=True)
    plan_id = fields.Many2one('x.plan', string="Plan")
    start_date = fields.Date(string='Start Date', default=fields.Date.today)  # Sử dụng fields.Date thay vì fields.Datetime
    end_date = fields.Date(string='End Date', default=fields.Date.today)  
    target_value = fields.Float(string='Target Value')
    achieved_value = fields.Float(string='Achieved Value')
    description = fields.Text(string='Description')
    target_stage_line_id = fields.Many2one('stage.line', string='Stage Team Line')
    target_stage_id = fields.Many2one('stage', string='Stage')

    @api.model
    def create(self, vals):
        res = super(Target, self).create(vals)
        res._update_work_pass_cutting_sub()
        res._update_work_sew_sub()
        res._update_more_work()
        return res

    def write(self, vals):
        res = super(Target, self).write(vals)
        self._update_work_pass_cutting_sub()
        self._update_work_sew_sub()
        self._update_more_work()
        return res

    @api.depends('user_id')
    def _compute_new_employee_card_number(self):
        for record in self:
            record.employee_card_number = record.user_id.barcode or ''

    def _update_work_pass_cutting_sub(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(vietnam_tz).date()  # Lấy ngày hiện tại theo múi giờ Việt Nam
        for target in self:
            if target.start_date:
                target_start_datetime = datetime.combine(target.start_date, datetime.min.time()).replace(tzinfo=vietnam_tz)
                if target_start_datetime.date() == today:
                    subs = self.env['work.pass.cutting.sub'].search([
                        ('work_sub_id.name.id', '=', target.user_id.id),
                        ('stage_id', '=', target.target_stage_id.id),
                    ])
                    for sub in subs:
                        sub._compute_target_value_today_method()

    def _update_work_sew_sub(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(vietnam_tz).date() 
        for target in self:
            if target.start_date:
                target_start_date_vietnam = datetime.combine(target.start_date, datetime.min.time()).replace(tzinfo=vietnam_tz)
                if target_start_date_vietnam.date() == today:
                    subs = self.env['work.process.cutting.sub'].search([
                        ('work_sub_id.name.id', '=', target.user_id.id),
                        ('stage_id', '=', target.target_stage_id.id),
                    ])
                    for sub in subs:
                        sub._compute_target_value_today_method_sew()
        
    def _update_more_work(self):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(vietnam_tz).date() 
        for target in self:
            if target.start_date:
                target_start_date_vietnam = datetime.combine(target.start_date, datetime.min.time()).replace(tzinfo=vietnam_tz)
                if target_start_date_vietnam.date() == today:
                    subs = self.env['assign.more.work.sub'].search([
                        ('assign_more_work_id.name.id', '=', target.user_id.id),
                        ('stage_id', '=', target.target_stage_id.id),
                    ])
                    for sub in subs:
                        sub._compute_target_value_today_more_work()