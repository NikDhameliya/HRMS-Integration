# -*- coding: utf-8 -*-

from odoo import models, fields

class Department(models.Model):
    _inherit = 'hr.department'
    
    hrms_external_id = fields.Char(string='HRMS External ID')
    type = fields.Integer(string="Type")
    number_of_members = fields.Integer(string="Number of Members")
    number_of_members_with_subteams = fields.Integer(string="Number of Members with Subteams")
    team_leader_id = fields.Many2one('hr.employee', string="Team Leader")
    hr_ids = fields.Many2many('hr.employee', 'hr_employee_hrs_rel', 'employee_id', 'hr_id', string="HR IDs")
    managers = fields.Many2many('hr.employee', 'hr_employee_managers_rel', 'department_id', 'manager_id',  string="Managers")

    _sql_constraints = [
        ('hrms_external_id_unique', 'unique(hrms_external_id)',
         'The hrms_external_id already exists!'),
    ]