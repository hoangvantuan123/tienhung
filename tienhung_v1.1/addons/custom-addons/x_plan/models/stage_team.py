from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class StageTeam(models.Model):
    _name = 'stageteam.list'
    _description = 'Stage Team List'

    @api.depends('stage_type')
    def _compute_name(self):
        for record in self:
            record.name = f"Team  - {record.stage_type}"
    name = fields.Char(string='Stage Name', compute='_compute_name', store=True)
    """ department_id_root = fields.Many2one(
    'hr.department', string='Department Root', domain=lambda self: [('parent_id', '=', False)]  
    ) """

    department_id = fields.Many2one(
    'hr.department', string='Department', required=True  
    )
    stageteam_line_ids = fields.One2many('stage.line', 'stageteam_id', string='Stage Team Lines')
    create_date = fields.Datetime(string='Creation Date', default=fields.Datetime.now)
    
    stage_id = fields.Many2one( comodel_name='stage', string="Stage")
    quantity_per_team = fields.Integer(string='Execution Quantity per Team', required=True, default=0)
    stage_type = fields.Selection([
        ('prepare', 'Prepare'),
        ('cut', 'Cut'),
        ('sew', 'Sew')
    ], string='Stage Type',compute='_compute_stage_type', store=True)
    

   
    
    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', self.department_id.id)])
            existing_employees = self.stageteam_line_ids.mapped('employee_id')
            to_add = [(0, 0, {'employee_id': emp.id}) for emp in employees if emp not in existing_employees]
            to_remove_ids = self.stageteam_line_ids.filtered(lambda line: line.employee_id not in employees).ids
            if to_remove_ids:
                self.stageteam_line_ids = [(2, line_id) for line_id in to_remove_ids]
            if to_add:
                self.update({
                    'stageteam_line_ids': to_add,
                })
        else:
            self.stageteam_line_ids = [(5, 0, 0)]  

 
    @api.constrains('quantity_per_team', 'stage_id')
    def _check_quantity_per_team(self):
        for record in self:
            total_quantity = sum(record.stage_id.stageteam_ids.mapped('quantity_per_team'))
            if total_quantity > record.stage_id.x_plan_id.total_products:
                raise ValidationError("The total quantity per team cannot exceed the total products in the plan.")
            
   
   