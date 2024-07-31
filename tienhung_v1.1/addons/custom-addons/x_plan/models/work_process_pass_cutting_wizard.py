from odoo import models, fields, api

class WorkProcessPassCuttingWizard(models.TransientModel):
    _name = 'work.process.pass.cutting.wizard'
    _description = 'Work Process Pass Cutting Wizard'

    pass_cutting_ids = fields.Many2many('pass.cutting', string='Pass Cuttings')

    def action_apply(self):
        active_id = self._context.get('active_id')
        if not active_id:
            return

        work_process = self.env['work.pass.cutting'].browse(active_id)
        if not work_process.exists():
            return {'type': 'ir.actions.act_window_close'}

        sub_work_data = []

        for pass_cutting in self.pass_cutting_ids:
            sub_work_data.append((0, 0, {
                'work_sub_id': work_process.id,  
                'pass_cutting_id': pass_cutting.id,
            }))

        if sub_work_data: 
            work_process.write({
                'work_sub_ids': sub_work_data
            })
        return {'type': 'ir.actions.act_window_close'}
