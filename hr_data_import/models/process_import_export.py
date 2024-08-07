# -*- coding: utf-8 -*-

import logging
import json
from datetime import datetime
import requests

from odoo.tools.misc import split_every

from odoo import models, fields, api, _

_logger = logging.getLogger("hrms Operations")


class ProcessImportExport(models.Model):
    _name = 'process.import.export'
    _description = 'Process Import Export'

    hrms_instance_id = fields.Many2one("hr.data.dashboard", string="Instance",
                                       default=lambda self: self.env.ref('hr_data_import.hr_data_dashboard'))
    hrms_operation = fields.Selection(
        [
            ("sync_employee", "Import Employees"),
            ("sync_department", "Import Departments"),
            ("sync_leave", "Import Leaves"),
        ],
        default="sync_employee", string="Operation")
    skip_existing_employee = fields.Boolean(string="Do Not Update Existing Employees",
                                            help="Check if you want to skip existing Employees.")

    skip_existing_department = fields.Boolean(string="Do Not Update Existing Departments",
                                              help="Check if you want to skip existing Departments.")
    skip_existing_leave = fields.Boolean(string="Do Not Update Existing Leaves",
                                         help="Check if you want to skip existing Leaves.")
    log_book_id = fields.Many2one('common.log.book', string="Log Book")
    log_lines = fields.One2many(related='log_book_id.log_lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('started', 'Started'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    hrms_employee_ids = fields.Many2many(
        'hrms.hr.employee',
        string="Employee Ids",
        help="Based on employee ids get employee from api and import in odoo",
        compute='_compute_hrms_employee_ids'
    )
    hrms_department_ids = fields.Many2many(
        'hrms.hr.department',
        string="Department Ids",
        compute='_compute_hrms_department_ids'
    )
    hrms_leave_ids = fields.Many2many(
        'hrms.hr.leave',
        string="Leave Ids",
        compute='_compute_hrms_leave_ids'
    )

    page = fields.Integer(String="Page", default=1)
    per_page = fields.Integer(String="Per Page", default=5)

    employee_count = fields.Integer(string="Employees", compute='_compute_employee_count')
    department_count = fields.Integer(string="Departments", compute='_compute_department_count')
    leave_count = fields.Integer(string="Leaves", compute='_compute_leave_count')
    log_count = fields.Integer(string="Log Book", compute='_compute_log_count')
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)

    def _compute_hrms_employee_ids(self):
        for record in self:
            if record.id:
                employee_ids = self.env['hrms.hr.employee'].search([('hrms_process_id', '=', record.id)]).ids
                record.hrms_employee_ids = [(6, 0, employee_ids)]
            else:
                record.hrms_employee_ids = [(6, 0, [])]

    def _compute_hrms_department_ids(self):
        for record in self:
            if record.id:
                department_ids = self.env['hrms.hr.department'].search([('hrms_process_id', '=', record.id)]).ids
                record.hrms_department_ids = [(6, 0, department_ids)]
            else:
                record.hrms_department_ids = [(6, 0, [])]

    def _compute_hrms_leave_ids(self):
        for record in self:
            if record.id:
                leave_ids = self.env['hrms.hr.leave'].search([('hrms_process_id', '=', record.id)]).ids
                record.hrms_leave_ids = [(6, 0, leave_ids)]
            else:
                record.hrms_leave_ids = [(6, 0, [])]

    @api.depends('hrms_employee_ids')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = len(record.hrms_employee_ids.ids)

    @api.depends('hrms_department_ids')
    def _compute_department_count(self):
        for record in self:
            record.department_count = len(record.hrms_department_ids.ids)

    @api.depends('hrms_leave_ids')
    def _compute_leave_count(self):
        for record in self:
            record.leave_count = len(record.hrms_leave_ids.ids)

    @api.depends('log_book_id')
    def _compute_log_count(self):
        for record in self:
            record.log_count = len(record.log_book_id.log_lines) if record.log_book_id else 0

    def action_start(self):
        self.env.company.import_job_status = 'running'
        self.state = 'started'
        self.hrms_execute()
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def action_stop(self):
        self.env.company.import_job_status = 'stopped'
        self.state = 'cancelled'

    def action_done(self):
        self.env.company.import_job_status = 'stopped'
        self.state = 'done'

    def action_view_logbook(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Log Book',
            'res_model': 'common.log.book',
            'view_mode': 'form',
            'res_id': self.log_book_id.id,
        }

    def action_view_employees(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employees',
            'res_model': 'hr.employee',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.hrms_employee_ids.ids)],
        }

    def action_view_departments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Departments',
            'res_model': 'hr.department',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.hrms_department_ids.ids)],
        }

    def action_view_leaves(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Leaves',
            'res_model': 'hr.leave',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.hrms_leave_ids.ids)],
        }

    def hrms_execute(self):
        """This method used to execute the operation as per given in wizard.
        """
        data_ids = False
        context = dict(self.env.context or {})
        context.update({'hrms_instance_id': self.hrms_instance_id.id, 'hrms_process_id': self.id})
        self.env.company.import_job_status = 'running'
        self.state = 'started'
        try:
            if self.hrms_operation == "sync_employee":
                log_book = self.env['common.log.book'].create_common_log_book_ept(model_name='hr.employee',
                                                                                  type='import',
                                                                                  message="Starting employee import")
                self.log_book_id = log_book.id
                employee_ids = self.with_context(context).hrms_create_employee(
                    self.skip_existing_employee, log_book)
                # Flatten the list of lists into a single list
                flat_employee_ids = [
                    item for sublist in employee_ids for item in sublist]
                if flat_employee_ids:
                    data_ids = flat_employee_ids
                    if data_ids:
                        self.action_done()
                        return {
                            'type': 'ir.actions.act_window',
                            'name': _('HRMS Employees'),
                            'res_model': 'hrms.hr.employee',
                            'views': [[False, 'list'], [False, 'form']],
                            'domain': [('id', 'in', data_ids)],
                        }

            elif self.hrms_operation == "sync_department":
                log_book = self.env['common.log.book'].create_common_log_book_ept(model_name='hr.department',
                                                                                  type='import',
                                                                                  message="Starting Department import")
                self.log_book_id = log_book.id
                department_ids = self.with_context(context).hrms_create_department(
                    self.skip_existing_department, log_book)
                # Flatten the list of lists into a single list
                flat_department_ids = [
                    item for sublist in department_ids for item in sublist]

                if flat_department_ids:
                    data_ids = flat_department_ids
                    if data_ids:
                        self.action_done()
                        return {
                            'type': 'ir.actions.act_window',
                            'name': _('HRMS Departments'),
                            'res_model': 'hrms.hr.department',
                            'views': [[False, 'list'], [False, 'form']],
                            'domain': [('id', 'in', data_ids)],
                        }

            elif self.hrms_operation == "sync_leave":
                log_book = self.env['common.log.book'].create_common_log_book_ept(model_name='hr.leave', type='import',
                                                                                  message="Starting Leaves import")
                self.log_book_id = log_book.id
                leave_ids = self.with_context(
                    context).hrms_create_leave(self.skip_existing_leave, log_book)
                # Flatten the list of lists into a single list
                flat_leave_ids = [
                    item for sublist in leave_ids for item in sublist]
                if flat_leave_ids:
                    data_ids = flat_leave_ids
                    if flat_leave_ids:
                        self.action_done()
                        return {
                            'type': 'ir.actions.act_window',
                            'name': _('HRMS Leaves'),
                            'res_model': 'hrms.hr.leave',
                            'views': [[False, 'list'], [False, 'form']],
                            'domain': [('id', 'in', data_ids)],
                        }
        except KeyError as e:
            _logger.error(
                "Error in hrms_execute: Missing reference %s", str(e))
        except Exception as e:
            _logger.error("Unexpected error in hrms_execute: %s", str(e))

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def hrms_create_employee(self, skip_existing_employee, log_book):
        """
        It creates employee data queue from data of Employee.
        """
        employee_data = []
        hrms_employee_ids = []
        employee_obj = self.env["hrms.hr.employee"]
        bus_bus_obj = self.env["bus.bus"]

        # Replace this with your actual API endpoint and API key
        api_url = "{domain}/api/v1/employees?page={page}&per_page={per_page}".format(
            page=self.page or 1,
            per_page=self.per_page or 10,
            domain=self.company_id.hrm_base_url
        )

        headers = {
            # 'token': self.company_id.hrm_token
        }

        while True:
            try:
                response = requests.request("GET", api_url, headers=headers)
            except Exception as e:
                _logger.error("Unexpected error in API request: %s", str(e))
                break

            if response.status_code != 200:
                break

            result = json.loads(response.text).get('result', False)
            if not result:
                break
            if result.get('data', False):
                employee_data += result['data']

            if result.get('links', False) and result.get('next_page_url', False):
                api_url = result['next_page_url'] + '&per_page={per_page}'.format(per_page=self.per_page)
            else:
                break

        if len(employee_data) > 0:
            for employee_id_chunk in split_every(25, employee_data):
                hrms_employees_ids = employee_obj.hrms_create_employee(
                    employee_id_chunk, skip_existing_employee, log_book)
                hrms_employees = employee_obj.browse(hrms_employees_ids)
                message = "Employee created %s" % ', '.join(
                    hrms_employees.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification", "message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)
                hrms_employee_ids.append(hrms_employees_ids)

            self._cr.commit()

        return hrms_employee_ids

    def hrms_create_department(self, skip_existing_department, log_book):
        """
        It creates department data queue from data of department.
        """
        department_data = []
        hrms_department_ids = []
        department_obj = self.env["hrms.hr.department"]

        api_url = "{domain}/api/v1/employees?page={page}&per_page={per_page}".format(
            page=self.page or 1,
            per_page=self.per_page or 10,
            domain=self.company_id.hrm_base_url
        )

        headers = {
            # 'token': self.company_id.hrm_token
        }

        while True:
            try:
                response = requests.request("GET", api_url, headers=headers)
            except Exception as e:
                _logger.error("Unexpected error in API request: %s", str(e))
                break

            result = json.loads(response.text).get('result', False)
            if not result:
                break

            if result.get('data', False):
                department_data += result['data']

            if result.get('links', False) and result.get('next_page_url', False):
                api_url = result['next_page_url'] + '&per_page={per_page}'.format(per_page=self.per_page)
            else:
                break

        if len(department_data) > 0:
            for department_id_chunk in split_every(25, department_data):
                hrms_departments_ids = department_obj.hrms_create_department(
                    department_id_chunk, skip_existing_department, log_book)
                hrms_department_ids.append(hrms_departments_ids)
        return hrms_department_ids

    def hrms_create_leave(self, skip_existing_leave, log_book):
        """
        It creates leave data queue from data of leave.
        """
        leave_data = []
        hrms_leave_ids = []
        leave_obj = self.env["hrms.hr.leave"]

        # Replace this with your actual API endpoint and API key
        api_url = "{domain}/api/v1/out-off-office?page={page}&per_page={per_page}".format(
            page=self.page or 1,
            per_page=self.per_page or 10,
            domain=self.company_id.hrm_base_url
        )

        headers = {
            # 'token': self.company_id.hrm_token
        }

        while True:
            try:
                    response = requests.request("GET", api_url, headers=headers)
            except Exception as e:
                _logger.error("Unexpected error in API request: %s", str(e))
                break

            if response.status_code != 200:
                break

            result = json.loads(response.text).get('result', False)
            if not result:
                break
            if result.get('data', False):
                leave_data += result['data']

            if result.get('links', False) and result.get('next_page_url', False):
                api_url = result['next_page_url'] + '&per_page={per_page}'.format(per_page=self.per_page)
            else:
                break

        if len(leave_data) > 0:
            for leave_id_chunk in split_every(50, leave_data):
                hrms_leaves_ids = leave_obj.hrms_create_leave(
                    leave_id_chunk, skip_existing_leave, log_book)
                hrms_leave_ids.append(hrms_leaves_ids)

            self._cr.commit()
        return hrms_leave_ids
