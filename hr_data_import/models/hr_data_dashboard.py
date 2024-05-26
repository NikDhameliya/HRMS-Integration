# -*- coding: utf-8 -*-

import json
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger("HRMS Instance")


class HrDataDashboard(models.Model):
    _name = "hr.data.dashboard"
    _description = 'HR Data Dashboard'

    name = fields.Char(size=120, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    auto_import_employees = fields.Boolean(
        string="Auto Create Employees if not found?")
    auto_import_departments = fields.Boolean(
        string="Auto Create Departments if not found?")
    auto_import_leaves = fields.Boolean(
        string="Auto Create Leaves if not found?")
    color = fields.Integer(string='Color Index')
    employee_ids = fields.One2many('hrms.hr.employee', 'hrms_instance_id',string="Employees")
    department_ids = fields.One2many('hrms.hr.department', 'hrms_instance_id', string="Departments")
    leave_ids = fields.One2many('hrms.hr.leave', 'hrms_instance_id', string="Leaves")
    total_employee = fields.Integer(string='Total Employee', compute='get_kanban_counts', store=True)
    total_department = fields.Integer(string='Total Department', compute='get_kanban_counts', store=True)
    total_leave = fields.Integer(string='Total Leave', compute='get_kanban_counts', store=True)
    active = fields.Boolean(default=True)
    
    @api.depends('employee_ids', 'department_ids', 'leave_ids')
    def get_kanban_counts(self):
        for data in self:
            data.total_employee = len(self.employee_ids.ids)
            data.total_department = len(self.department_ids.ids)
            data.total_leave = len(self.leave_ids.ids)

    def prepare_action(self, view, domain):
        """
        Use: To prepare action dictionary
        :return: action details
        """
        action = {
            'name': view.get('name'),
            'type': view.get('type'),
            'domain': domain,
            'view_mode': view.get('view_mode'),
            'view_id': view.get('view_id')[0] if view.get('view_id') else False,
            'views': view.get('views'),
            'res_model': view.get('res_model'),
            'target': view.get('target'),
        }

        if 'tree' in action['views'][0]:
            action['views'][0] = (action['view_id'], 'list')
        return action

    @api.model
    def perform_operation(self, record_id):
        """
        Use: To prepare hrms operation action
        :return: operation action details
        """
        view = self.env.ref('hr_data_import.action_wizard_hrms_instance_import_export_operations').sudo().read()[0]
        action = self.prepare_action(view, [])
        action.update({'context': {'default_hrms_instance_id': record_id}})
        return action