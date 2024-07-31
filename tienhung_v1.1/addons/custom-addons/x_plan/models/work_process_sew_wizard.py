from odoo import models, fields, api

class WorkProcessSewWizard(models.TransientModel):
    _name = 'work.process.sew.wizard'
    _description = 'Work Process Sew Wizard'

    cutting_ids = fields.Many2many('cutting.line', string='Sews')

    def action_apply(self):
        active_id = self._context.get('active_id')
        if not active_id:
            return

        work_process = self.env['work.process'].browse(active_id)
        if not work_process.exists():
            return {'type': 'ir.actions.act_window_close'}

        sub_work_data = []

        for cutting_id in self.cutting_ids:
            sub_work_data.append((0, 0, {
                'work_sub_id': work_process.id,  
                'cutting_id': cutting_id.id,
            }))

        if sub_work_data: 
            work_process.write({
                'work_sub_ids': sub_work_data
            })
        return {'type': 'ir.actions.act_window_close'}
