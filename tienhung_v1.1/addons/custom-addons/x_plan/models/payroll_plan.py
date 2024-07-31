from odoo import models, fields, api


class PayrollPlan(models.Model):
    _name = 'payroll.plan'
    _description = 'Payroll plan'

    name = fields.Many2one('x.plan', string='Plan Id')
    quantity = fields.Float(string='Quantity')
    pass_type = fields.Selection([
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Pass Type', compute='_compute_pass_type', store=True)
    payroll_plan_id = fields.Many2one(
        'payroll.list', string='Payroll', ondelete='cascade')
    payroll_plan_work_id = fields.One2many(
        'payroll.plan.work', 'payroll_plan_work_ids', string='Payroll Plans')

    department_id = fields.Many2one(
        'hr.department', string='Department', compute='_compute_department_id', store=True)

    @api.depends('payroll_plan_id')
    def _compute_department_id(self):
        for record in self:
            if record.payroll_plan_id:
                record.department_id = record.payroll_plan_id.department_id
            else:
                record.department_id = False

    @api.depends('payroll_plan_id')
    def _compute_pass_type(self):
        for record in self:
            record.pass_type = record.payroll_plan_id.pass_type or ''

    @api.model
    def create(self, vals):
        record = super(PayrollPlan, self).create(vals)
        if record.pass_type == 'cut':
            record.check_and_update_payroll_plan_work()
        elif record.pass_type == 'sew':
            record.check_and_update_payroll_plan_work_sew()
        return record



    def unlink(self):
        for record in self:
            self.env['payroll.plan.work'].search(
                [('payroll_plan_work_ids', '=', record.id)]).unlink()
        return super(PayrollPlan, self).unlink()

    def check_and_update_payroll_plan_work(self):
        for record in self:
            # Xóa các bản ghi payroll.plan.work hiện tại liên kết với bản ghi này
            existing_records = self.env['payroll.plan.work'].search([
                ('payroll_plan_work_ids', '=', record.id)
            ])
            existing_records.unlink()

            # Truy vấn các bản ghi work.pass.cutting dựa trên các điều kiện cơ bản
            matching_records = self.env['work.pass.cutting'].search([
                ('plan_id', '=', record.name.id),
                ('pass_type', '=', record.pass_type),
                ('department_id', '=', record.department_id.id),
            ])
            valid_work_pass_cuttings = matching_records.filtered(
                lambda wc: any(not sub.is_checked for sub in wc.work_sub_ids)
            )

            matching_records_assign_more = self.env['assign.more.work'].search([
                ('plan_id', '=', record.name.id),
                ('stage_type', '=', record.pass_type),
                ('department_id', '=', record.department_id.id)
            ])

            valid_matching_records_assign_more = matching_records_assign_more.filtered(
                lambda wc: any(not sub.is_checked for sub in wc.assign_more_work_sub_ids)
            )

            # Giới hạn số lượng bản ghi cần xử lý
            max_quantity = record.quantity

            # Xử lý bản ghi work.pass.cutting
            for match in valid_work_pass_cuttings:
                payroll_plan_work = self.env['payroll.plan.work'].search([
                    ('name', '=', match.name.id),
                    ('payroll_plan_work_ids', '=', record.id),
                    ('payroll_plan_list_id', '=', record.payroll_plan_id.id)
                ], limit=1)

                if not payroll_plan_work:
                    payroll_plan_work = self.env['payroll.plan.work'].create({
                        'name': match.name.id,
                        'payroll_plan_work_ids': record.id,
                        'payroll_plan_list_id': record.payroll_plan_id.id,
                    })

                total_sl = 0
                for work_sub in match.work_sub_ids.filtered(lambda s: not s.is_checked):
                    if total_sl + work_sub.ns >= max_quantity:
                        break
                    self.env['payroll.plan.work.sub'].create({
                        'name': work_sub.work_sub_id.name.id,
                        'payroll_work_id': payroll_plan_work.id,
                        'cd': work_sub.pass_cutting_id.id,
                        'sl': work_sub.ns,
                        'dg': work_sub.unit_price,
                        'money': work_sub.unit_price,
                        'stage_id': work_sub.stage_id.id,
                        'work_sub_id': work_sub.id,
                    })
                    total_sl += work_sub.ns

            # Xử lý bản ghi assign.more.work
            for match in valid_matching_records_assign_more:
                payroll_plan_work_more = self.env['payroll.plan.work'].search([
                    ('name', '=', match.name.id),
                    ('payroll_plan_work_ids', '=', record.id),
                    ('payroll_plan_list_id', '=', record.payroll_plan_id.id)
                ], limit=1)

                if not payroll_plan_work_more:
                    payroll_plan_work_more = self.env['payroll.plan.work'].create({
                        'name': match.name.id,
                        'payroll_plan_work_ids': record.id,
                        'payroll_plan_list_id': record.payroll_plan_id.id,
                    })

                total_sl = 0
                for work_sub in match.assign_more_work_sub_ids.filtered(lambda s: not s.is_checked):
                    if total_sl + work_sub.ns_cut >= max_quantity:
                        break
                    self.env['payroll.plan.work.sub'].create({
                        'name': match.name.id,
                        'payroll_work_id': payroll_plan_work_more.id,
                        'cd': work_sub.pass_cutting_id.id,
                        'sl': work_sub.ns_cut,
                        'dg': work_sub.unit_price,
                        'money': work_sub.unit_price,
                        'stage_id': work_sub.stage_id.id,
                        'work_more_sub_id': work_sub.id,
                        'type': '*'
                    })
                    total_sl += work_sub.ns_cut


    def check_and_update_payroll_plan_work_sew(self):
        for record in self:
            existing_records = self.env['payroll.plan.work'].search([
                ('payroll_plan_work_ids', '=', record.id)
            ])
            existing_records.unlink()

            matching_records = self.env['work.process'].search([
                ('plan_id', '=', record.name.id),
                ('pass_type', '=', record.pass_type),
                ('department_id', '=', record.department_id.id),
            ])
            valid_work_sew = matching_records.filtered(
                lambda wc: any(not sub.is_checked for sub in wc.work_sub_ids)
            )

            matching_records_assign_more = self.env['assign.more.work'].search([
                ('plan_id', '=', record.name.id),
                ('stage_type', '=', record.pass_type),
                ('department_id', '=', record.department_id.id)
            ])

            valid_matching_records_assign_more = matching_records_assign_more.filtered(
                lambda wc: any(not sub.is_checked for sub in wc.assign_more_work_sub_ids)
            )

            max_quantity = record.quantity

            for match in valid_work_sew:
                payroll_plan_work = self.env['payroll.plan.work'].search([
                    ('name', '=', match.name.id),
                    ('payroll_plan_work_ids', '=', record.id),
                    ('payroll_plan_list_id', '=', record.payroll_plan_id.id)
                ], limit=1)

                if not payroll_plan_work:
                    payroll_plan_work = self.env['payroll.plan.work'].create({
                        'name': match.name.id,
                        'payroll_plan_work_ids': record.id,
                        'payroll_plan_list_id': record.payroll_plan_id.id,
                    })

                total_sl = 0
                for work_sub in match.work_sub_ids.filtered(lambda s: not s.is_checked):
                    if total_sl + work_sub.ns >= max_quantity:
                        break
                    self.env['payroll.plan.work.sub'].create({
                        'name': work_sub.work_sub_id.name.id,
                        'payroll_work_id': payroll_plan_work.id,
                        'cd_sew': work_sub.cutting_id.id,
                        'sl': work_sub.ns,
                        'dg': work_sub.unit_price,
                        'money': work_sub.unit_price,
                        'stage_id': work_sub.stage_id.id,
                        'work_sew_sub_id' : work_sub.id
                    })
                    total_sl += work_sub.ns

            # Xử lý bản ghi assign.more.work
            for match in valid_matching_records_assign_more:
                payroll_plan_work_more = self.env['payroll.plan.work'].search([
                    ('name', '=', match.name.id),
                    ('payroll_plan_work_ids', '=', record.id),
                    ('payroll_plan_list_id', '=', record.payroll_plan_id.id)
                ], limit=1)

                if not payroll_plan_work_more:
                    payroll_plan_work_more = self.env['payroll.plan.work'].create({
                        'name': match.name.id,
                        'payroll_plan_work_ids': record.id,
                        'payroll_plan_list_id': record.payroll_plan_id.id,
                    })

                total_sl = 0
                for work_sub in match.assign_more_work_sub_ids.filtered(lambda s: not s.is_checked):
                    if total_sl + work_sub.ns_sew >= max_quantity:
                        break
                    self.env['payroll.plan.work.sub'].create({
                        'name': match.name.id,
                        'payroll_work_id': payroll_plan_work_more.id,
                        'cd_sew': work_sub.cutting_id.id,
                        'sl': work_sub.ns_sew,
                        'dg': work_sub.unit_price,
                        'money': work_sub.unit_price,
                        'stage_id': work_sub.stage_id.id,
                        'work_more_sub_id': work_sub.id,
                        'type': '*'
                    })
                    total_sl += work_sub.ns_sew
  