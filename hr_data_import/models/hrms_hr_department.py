# -*- coding: utf-8 -*-

from odoo import models, fields, _

import logging

_logger = logging.getLogger("HRMS Department Operations")

class HrmsHrDepartment(models.Model):
    _name = "hrms.hr.department"
    _description = 'HR Department HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one('hr.data.dashboard', string="HRMS Instance", required=True)
    hrms_external_id = fields.Char(string="HRMS Department ID")
    hrms_process_id = fields.Many2one('process.import.export', string="Process ID")
    department_id = fields.Many2one('hr.department', string="Department")
    type = fields.Integer(string="Type")
    number_of_members = fields.Integer(string="Number of Members")
    number_of_members_with_subteams = fields.Integer(string="Number of Members with Subteams")
    team_leader_id = fields.Many2one('hr.employee', string="Team Leader")
    hr_ids = fields.Many2many('hr.employee', 'hr_employee_hrs_dept_rel', 'employee_id', 'hr_id', string="HR IDs")
    managers = fields.Many2many('hr.employee', string="Managers")
    child_ids = fields.Many2many('hr.department', 'hr_department_subteams_dept_rel', 'department_id', 'subteam_id', string="Subteams")
    parent_id = fields.Many2one('hr.department', string="Parent Team", index=True)

    def hrms_create_department(self, department_data, skip_existing_department, log_book):
        Department = self.env['hr.department']
        Employee = self.env['hr.employee']
        created_department_ids = []

        self.env['common.log.lines'].create_common_log_line_ept(
            log_book_id=log_book.id,
            message=f"Processing Department Data",
            log_line_type='success',
            model_name='hr.department'
        )

        for dept in department_data:
            try:
                import_job_status = self.env.company.import_job_status
                if import_job_status == 'stopped':
                    self.env['common.log.lines'].create_common_log_line_ept(
                        log_book_id=log_book.id,
                        message="Import job stopped by user",
                        log_line_type='warning',
                        model_name='hr.department'
                    )
                    break
                existing_dept = Department.search(
                    [('hrms_external_id', '=', dept.get('id'))], limit=1)
                if skip_existing_department and existing_dept:
                    self.env['common.log.lines'].create_common_log_line_ept(
                            log_book_id=log_book.id,
                            message=f"Skipping existing department with HRMS ID {dept.get('id')}",
                            log_line_type='info',
                            model_name='hr.department'
                        )
                    continue

                team_leader_id = Employee.search([('hrms_external_id', '=', dept.get('team_leader_id'))], limit=1).id if dept.get('team_leader_id') else False
                hr_ids = [emp.id for emp in Employee.search([('hrms_external_id', 'in', dept.get('hr_ids', []))]) if emp.id]
                manager_ids = [emp.id for emp in Employee.search([('hrms_external_id', 'in', dept.get('managers', []))]) if emp.id]
                subteam_ids = [dep.id for dep in Department.search([('hrms_external_id', 'in', dept.get('subteams', []))]) if dep.id]
                parent_id = Department.search([('hrms_external_id', '=', dept.get('parent_id'))], limit=1).id if dept.get('parent_id') else False

                vals = {
                    'name': dept['name'],
                    'hrms_external_id': dept['id'],
                    'type': dept.get('type', 1),
                    'number_of_members': dept.get('number_of_members', 0),
                    'number_of_members_with_subteams': dept.get('number_of_members_with_subteams', 0),
                    'team_leader_id': team_leader_id,
                    'hr_ids': [(6, 0, hr_ids)],
                    'managers': [(6, 0, manager_ids)],
                    'child_ids': [(6, 0, subteam_ids)],
                    'parent_id': parent_id
                }

                if existing_dept:
                    # Update the existing department
                    existing_dept.write(vals)
                    self.env['common.log.lines'].create_common_log_line_ept(
                            log_book_id=log_book.id,
                            message=f"Updated existing department {dept['name']} with HRMS ID {dept['id']}",
                            log_line_type='success',
                            model_name='hr.department'
                        )
                    department = existing_dept
                else:
                    department = Department.create(vals)
                    self.env['common.log.lines'].create_common_log_line_ept(
                        log_book_id=log_book.id,
                        message=f"Created new department {dept['name']} with HRMS ID {dept['id']}",
                        log_line_type='success',
                        model_name='hr.department'
                    )
                    created_department_ids.append(department.id)
                if existing_dept:
                    self.write({
                        'name': dept['name'],
                        'company_id': self.env.company.id,
                        'hrms_instance_id': self.env.context.get('hrms_instance_id'),
                        'hrms_process_id': self.env.context.get('hrms_process_id'),
                        'hrms_external_id': dept['id'],
                        'department_id': department.id,
                        'type': dept.get('type', 1),
                        'number_of_members': dept.get('number_of_members', 0),
                        'number_of_members_with_subteams': dept.get('number_of_members_with_subteams', 0),
                        'team_leader_id': team_leader_id,
                        'hr_ids': [(6, 0, hr_ids)],
                        'managers': [(6, 0, manager_ids)],
                        'child_ids': [(6, 0, subteam_ids)],
                        'parent_id': parent_id
                    })
                else:
                    self.create({
                        'name': dept['name'],
                        'company_id': self.env.company.id,
                        'hrms_instance_id': self.env.context.get('hrms_instance_id'),
                        'hrms_process_id': self.env.context.get('hrms_process_id'),
                        'hrms_external_id': dept['id'],
                        'department_id': department.id,
                        'type': dept.get('type', 1),
                        'number_of_members': dept.get('number_of_members', 0),
                        'number_of_members_with_subteams': dept.get('number_of_members_with_subteams', 0),
                        'team_leader_id': team_leader_id,
                        'hr_ids': [(6, 0, hr_ids)],
                        'managers': [(6, 0, manager_ids)],
                        'child_ids': [(6, 0, subteam_ids)],
                        'parent_id': parent_id
                    })
                    self.env['common.log.lines'].create_common_log_line_ept(
                        log_book_id=log_book.id,
                        message=f"Created new HRMS department {dept['name']} with HRMS ID {dept['id']}",
                        log_line_type='success',
                        model_name='hr.department'
                    )
            except Exception as e:
                _logger.error(f"Error processing department for {dept.get['name']}: {e}")
                self.env['common.log.lines'].create_common_log_line_ept(
                    log_book_id=log_book.id,
                    message=f"Error processing department for {dept.get['name']} with HRMS ID {dept.get('id')}: {e}",
                    log_line_type='error',
                    model_name='hr.department'
                )
                continue
        self.env['common.log.lines'].create_common_log_line_ept(
            log_book_id=log_book.id,
            message="Completed Department Data Processing",
            log_line_type='info',
            model_name='hr.department'
        )
        return created_department_ids