# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrmsHrDepartment(models.Model):
    _name = "hrms.hr.department"
    _description = 'HR Department HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one('hr.data.dashboard', string="HRMS Instance", required=True)
    hrms_external_id = fields.Char(string="HRMS Department ID")
    department_id = fields.Many2one('hr.department', string="Department", ondelete="cascade")
    type = fields.Integer(string="Type")
    number_of_members = fields.Integer(string="Number of Members")
    number_of_members_with_subteams = fields.Integer(string="Number of Members with Subteams")
    team_leader_id = fields.Many2one('hr.employee', string="Team Leader")
    hr_ids = fields.Many2many('hr.employee', 'hr_employee_hrs_dept_rel', 'employee_id', 'hr_id', string="HR IDs")
    managers = fields.Many2many('hr.employee', string="Managers")
    child_ids = fields.Many2many('hr.department', 'hr_department_subteams_dept_rel', 'department_id', 'subteam_id', string="Subteams")
    parent_id = fields.Many2one('hr.department', string="Parent Team", index=True)

    def hrms_create_department(self, department_data, skip_existing_department=False):
        Department = self.env['hr.department']
        created_department_ids = []

        for dept in department_data:
            if skip_existing_department:
                existing_dept = Department.search([('hrms_external_id', '=', dept['id'])])
                if existing_dept:
                    continue
            
            vals = {
                'name': dept['name'],
                'hrms_external_id': dept['id'],
                'type': dept.get('type', 1),
                'number_of_members': dept.get('number_of_members', 0),
                'number_of_members_with_subteams': dept.get('number_of_members_with_subteams', 0),
                'team_leader_id': self.env['hr.employee'].search([('id', '=', dept['team_leader_id'])]).id if dept['team_leader_id'] else False,
                'hr_ids': [(6, 0, [self.env['hr.employee'].search([('id', '=', hr_id)]).id for hr_id in dept.get('hr_ids', [])])],
                'managers': [(6, 0, [self.env['hr.employee'].search([('id', '=', manager_id)]).id for manager_id in dept.get('managers', [])])],
                'child_ids': [(6, 0, [self.env['hr.department'].search([('hrms_external_id', '=', subteam_id)]).id for subteam_id in dept.get('subteams', [])])],
                'parent_id': self.env['hr.department'].search([('hrms_external_id', '=', dept['parent_id'])]).id if dept['parent_id'] else False
            }
            
            department = Department.create(vals)
            created_department_ids.append(department.id)
            
            self.create({
                'name': dept['name'],
                'company_id': self.env.company.id,
                'hrms_instance_id': self.env.context.get('hrms_instance_id'),
                'hrms_external_id': dept['id'],
                'department_id': department.id,
                'type': dept.get('type', 1),
                'number_of_members': dept.get('number_of_members', 0),
                'number_of_members_with_subteams': dept.get('number_of_members_with_subteams', 0),
                'team_leader_id': self.env['hr.employee'].search([('id', '=', dept['team_leader_id'])]).id if dept['team_leader_id'] else False,
                'hr_ids': [(6, 0, [self.env['hr.employee'].search([('id', '=', hr_id)]).id for hr_id in dept.get('hr_ids', [])])],
                'managers': [(6, 0, [self.env['hr.employee'].search([('id', '=', manager_id)]).id for manager_id in dept.get('managers', [])])],
                'child_ids': [(6, 0, [self.env['hr.department'].search([('hrms_external_id', '=', subteam_id)]).id for subteam_id in dept.get('subteams', [])])],
                'parent_id': self.env['hr.department'].search([('hrms_external_id', '=', dept['parent_id'])]).id if dept['parent_id'] else False
            })
        return created_department_ids