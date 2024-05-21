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
    color = fields.Integer(string='Color Index')
    employee_ids = fields.One2many('hrms.hr.employee', 'hrms_instance_id',string="Employees")
    department_ids = fields.One2many('hrms.hr.department', 'hrms_instance_id', string="Departments")
    leave_ids = fields.One2many('hrms.hr.leave', 'hrms_instance_id', string="Leaves")
    active = fields.Boolean(default=True)
    
    def _compute_kanban_shopify_order_data(self):
        for record in self:
            # Employee count query
            employee_data = record.get_total_employees()
            
            # Department count query
            department_data = record.get_total_departments()
            
            # Leaves count query
            leave_data = record.get_total_leaves()

            record.shopify_order_data = json.dumps({
                "title": "",
                "area": True,
                "color": "#875A7B",
                "is_sample_data": False,
                "employee_data": employee_data,
                "department_data": department_data,
                "leave_data": leave_data,
                "sort_on": self._context.get('sort'),
                "currency_symbol": record.company_id.currency_id.symbol or '',
            })

    def get_total_employees(self):
        """
        :return: total number of shopify employee ids and action for employee
        """
        employee_data = {}
        self._cr.execute("""select count(id) as total_count from hrms_hr_employee where
                        hrms_external_id != False and hrms_instance_id = %s""" % self.id)
        result = self._cr.dictfetchall()
        if result:
            total_count = result[0].get('total_count')
        view = self.env.ref('hr_data_import.action_employee_dashboard_view').sudo().read()[0]
        action = self.prepare_action(view, [('hrms_external_id', '!=', False), ('hrms_instance_id', '=', self.id)])
        employee_data.update({'employee_count': total_count, 'employee_action': action})
        return employee_data
    
    def get_total_departments(self):
        """
        :return: total number of shopify department ids and action for department
        """
        department_data = {}
        self._cr.execute("""select count(id) as total_count from hrms_hr_department where
                        hrms_external_id != False and hrms_instance_id = %s""" % self.id)
        result = self._cr.dictfetchall()
        if result:
            total_count = result[0].get('total_count')
        view = self.env.ref('hr_data_import.action_department_dashboard_view').sudo().read()[0]
        action = self.prepare_action(view, [('hrms_external_id', '!=', False), ('hrms_instance_id', '=', self.id)])
        department_data.update({'department_count': total_count, 'department_action': action})
        return department_data

    def get_total_leaves(self):
        """
        :return: total number of shopify leave ids and action for leave
        """
        leave_data = {}
        self._cr.execute("""select count(id) as total_count from hrms_hr_leave where
                        hrms_external_id != False and hrms_instance_id = %s""" % self.id)
        result = self._cr.dictfetchall()
        if result:
            total_count = result[0].get('total_count')
        view = self.env.ref('hr_data_import.action_leave_dashboard_view').sudo().read()[0]
        action = self.prepare_action(view, [('hrms_external_id', '!=', False), ('hrms_instance_id', '=', self.id)])
        leave_data.update({'leave_count': total_count, 'leave_action': action})
        return leave_data

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
        Use: To prepare shopify operation action
        :return: operation action details
        """
        view = self.env.ref('hr_data_import.action_wizard_hrms_instance_import_export_operations').sudo().read()[0]
        action = self.prepare_action(view, [])
        action.update({'context': {'default_hrms_instance_id': record_id}})
        return action