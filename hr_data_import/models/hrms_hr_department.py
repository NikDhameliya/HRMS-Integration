# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrmsHrDepartment(models.Model):
    _name = "hrms.hr.department"
    _description = 'HR Department HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one('hr.data.dashboard', string="HRMS Instance", required=True)
    created_at = fields.Datetime()
    updated_at = fields.Datetime()
    hrms_external_id = fields.Char(string="HRMS Department ID")
    department_id = fields.Many2one('hr.department', string="Department", ondelete="cascade")
    exported_in_hrms = fields.Boolean(default=False)
    type = fields.Integer(string="Type")
    number_of_members = fields.Integer(string="Number of Members")
    number_of_members_with_subteams = fields.Integer(string="Number of Members with Subteams")
    team_leader_id = fields.Many2one('hr.employee', string="Team Leader")
    hr_ids = fields.Many2many('hr.employee', 'hr_employee_hrs_dept_rel', 'employee_id', 'hr_id', string="HR IDs")
    managers = fields.Many2many('hr.employee', string="Managers")
    child_ids = fields.Many2many('hr.department', 'hr_department_subteams_dept_rel', 'department_id', 'subteam_id', string="Subteams")
    parent_id = fields.Many2one('hr.department', string="Parent Team", index=True)

