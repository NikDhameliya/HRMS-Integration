# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime
import requests

from odoo.exceptions import UserError
from odoo.tools.misc import split_every

from odoo import models, fields, api, _

_logger = logging.getLogger("hrms Operations")


class ProcessImportExport(models.TransientModel):
    _name = 'process.import.export'
    _description = 'Process Import Export'

    hrms_instance_id = fields.Many2one("hr.data.dashboard", string="Instance")
    hrms_operation = fields.Selection(
        [
            ("sync_employee", "Import Employees"),
            ("sync_department", "Import Departments"),
            ("sync_leave", "Import Leaves"),
        ],
        default="sync_employee", string="Operation")
    hrms_employee_ids = fields.Text(string="Employee Ids",
                                       help="Based on employee ids get employee from api and import in odoo")
    skip_existing_employee = fields.Boolean(string="Do Not Update Existing Employees",
                                           help="Check if you want to skip existing Employees.")
    hrms_department_ids = fields.Text(string="Department Ids",
                                       help="Based on department ids get department from api and import in odoo")
    skip_existing_department = fields.Boolean(string="Do Not Update Existing Departments",
                                           help="Check if you want to skip existing Departments.")
    hrms_leave_ids = fields.Text(string="Leave Ids",
                                       help="Based on Leave ids get Leave from api and import in odoo")
    skip_existing_leave = fields.Boolean(string="Do Not Update Existing Leaves",
                                           help="Check if you want to skip existing Leaves.")



    def hrms_execute(self):
        """This method used to execute the operation as per given in wizard.
        """
        employee_obj = self.env["hrms.hr.employee"]
        department_obj = self.env["hrms.hr.department"]
        leave_obj = self.env["hrms.hr.leave"]
        data_ids = False

        instance = self.hrms_instance_id
        if self.hrms_operation == "sync_employee":
            employee_ids = self.hrms_create_employee(
                self.skip_existing_employee)
            if employee_ids:
                data_ids = employee_ids
                action_name = "hr_data_import.view_hrms_employee_form"
                form_view_name = "hr_data_import.action_hrms_employee"

        if self.hrms_operation == "sync_department":
            department_ids = self.hrms_create_department(
                self.skip_existing_department)
            if department_ids:
                data_ids = department_ids
                action_name = "hr_data_import.view_hrms_hr_department_form"
                form_view_name = "hr_data_import.action_hrms_department"

            
        if self.hrms_operation == "sync_leave":
            leave_ids = self.hrms_create_leave(
                self.skip_existing_leave)
            if leave_ids:
                data_ids = leave_ids
                action_name = "hr_data_import.view_hrms_hr_leave_form"
                form_view_name = "hr_data_import.action_hrms_leave"


        if data_ids and action_name and form_view_name:
            action = self.env.ref(action_name).sudo().read()[0]
            form_view = self.sudo().env.ref(form_view_name)

            if len(data_ids) == 1:
                action.update({"view_id": (form_view.id, form_view.name), "res_id": data_ids[0],
                               "views": [(form_view.id, "form")]})
            else:
                action["domain"] = [("id", "in", data_ids)]
            return action

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def hrms_create_employee(self, skip_existing_employee):
        """
        It creates employee data queue from data of Employee.
        """
        employee_data = []
        hrms_employee_ids = []
        employee_obj = self.env["hrms.hr.employee"]
        bus_bus_obj = self.env["bus.bus"]
        # Replace this with your actual API endpoint and API key
        api_url = "https://{my_company_domain}/api/v1/employees?page=1&per_page=5"
        payload = {}
        headers = {
          'token': '{api_token}'
        }

        response = requests.request("GET", api_url, headers=headers, data=payload)

        if response.status_code == 200:
            #TODO Uncomment below line and remove static data assign
            # employee_data = response.json().get('data', [])
            response = {'result': {'current_page': 1, 'data': [{'id': 'ND', 'name': 'John Doe', 'email': 'john.doe@example.com', 'position': 'CEO', 'grade': '', 'residence': 'Country, City', 'residence_comment': False, 'country': 'Молдова', 'city': False, 'phone': '1234567890', 'skype': False, 'linked_in': False, 'telegram': False, 'birth_date': '1982-08-11', 'end_test': '2016-04-01', 'fired_date': False, 'start_date': '2016-04-01', 'gender': 1, 'additional_email': 'alternate.email@example.com', 'additional_phone': False, 'relocate': False, 'duties': False, 'description': False, 'additional_info': False, 'team': [{'id': 2, 'name': 'Management'}], 'career': [{'start_date': '2021-04-08', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': '', 'department': False, 'position': 'CEO&СТО', 'grade': '', 'place': '', 'team': 'Management', 'comment': False}, {'start_date': '2021-03-29', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': '', 'department': False, 'position': 'CEO&СТО', 'grade': '', 'place': '', 'team': '', 'comment': ''}], 'contacts': [{'type_id': 2, 'type_name': 'email', 'value': 'alternate.email@example.com'}, {'type_id': 1, 'type_name': 'phone', 'value': '1234567890'}], 'languages': [], 'educations': [], 'skills': [], 'awards': []}, {'id': '7xl', 'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'position': 'HR Specialist', 'grade': '', 'residence': 'Country, City, Address', 'residence_comment': 'Address details', 'country': 'Україна', 'city': 'Суми', 'phone': '0987654321', 'skype': False, 'linked_in': False, 'telegram': False, 'birth_date': '1995-11-26', 'end_test': '2021-03-11', 'fired_date': False, 'start_date': '2021-02-11', 'gender': 2, 'additional_email': False, 'additional_phone': False, 'relocate': False, 'duties': False, 'description': False, 'additional_info': "Relative's contact phone number - 1231231234", 'team': [{'id': 8, 'name': 'HR/ Recruiting'}, {'id': 2, 'name': 'Management'}], 'career': [{'start_date': '2021-05-27', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': False, 'department': False, 'position': 'HR Specialist/Recruiter', 'grade': '', 'place': False, 'team': 'Management', 'comment': False}, {'start_date': '2021-04-08', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': False, 'department': False, 'position': 'HR Specialist/Recruiter', 'grade': '', 'place': False, 'team': 'HR/ Recruiting', 'comment': False}, {'start_date': '', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': False, 'department': False, 'position': 'HR Specialist/Recruiter', 'grade': '', 'place': False, 'team': 'HR/ Recruiting', 'comment': False}], 'contacts': [{'type_id': 2, 'type_name': 'email', 'value': 'jane.smith@fakemail.com'}, {'type_id': 1, 'type_name': 'phone', 'value': '9876543210'}], 'languages': [], 'educations': [], 'skills': [], 'awards': []}], 'first_page_url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=1', 'from': 1, 'last_page': 19, 'last_page_url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=19', 'links': [{'url': False, 'label': '&laquo; Поп.', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=1', 'label': '1', 'active': True}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=2', 'label': '2', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=3', 'label': '3', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=4', 'label': '4', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=5', 'label': '5', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=6', 'label': '6', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=7', 'label': '7', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=8', 'label': '8', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=9', 'label': '9', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=10', 'label': '10', 'active': False}, {'url': False, 'label': '...', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=18', 'label': '18', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=19', 'label': '19', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=2', 'label': 'Наст. &raquo;', 'active': False}], 'next_page_url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=2', 'path': 'https://mycompany.hrmsystem.com/api/v1/employees', 'per_page': 5, 'prev_page_url': False, 'to': 5, 'total': 200}, 'error': False, 'code': 200, 'messages': []}
            employee_data = response['result']['data']

        if len(employee_data) > 0:
            for employee_id_chunk in split_every(25, employee_data):
                hrms_employees = employee_obj.hrms_create_employee(employee_id_chunk, skip_existing_employee)

                message = "Employee created %s" % ', '.join(hrms_employees.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification","message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)
                hrms_employee_ids.append(hrms_employees.ids)

            self._cr.commit()
        return hrms_employee_ids
    
    def hrms_create_department(self, skip_existing_department):
        """
        It creates department data queue from data of department.
        """
        department_data = []
        hrms_department_ids = []
        department_obj = self.env["hrms.hr.department"]
        bus_bus_obj = self.env["bus.bus"]
        # Replace this with your actual API endpoint and API key
        api_url = "https://{my_company_domain}/api/v1/departments?page=1&per_page=5"
        payload = {}
        headers = {
          'token': '{api_token}'
        }

        response = requests.request("GET", api_url, headers=headers, data=payload)

        if response.status_code == 200:
            department_data = response.json().get('data', [])

        if len(department_data) > 0:
            for department_id_chunk in split_every(25, department_data):
                hrms_departments = department_obj.hrms_create_department(department_id_chunk, skip_existing_department)

                message = "Department created %s" % ', '.join(hrms_departments.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification","message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)
                hrms_department_ids.append(hrms_departments.ids)

            self._cr.commit()
        return hrms_department_ids
    
    def hrms_create_leave(self, skip_existing_leave):
        """
        It creates leave data queue from data of leave.
        """
        leave_data = []
        hrms_leave_ids = []
        leave_obj = self.env["hrms.hr.leave"]
        bus_bus_obj = self.env["bus.bus"]
        # Replace this with your actual API endpoint and API key
        api_url = "https://{my_company_domain}/api/v1/out-off-office?page=1&per_page=20&additional_info=true"
        payload = {}
        headers = {
          'token': '{api_token}'
        }

        response = requests.request("GET", api_url, headers=headers, data=payload)

        if response.status_code == 200:
            leave_data = response.json().get('data', [])

        if len(leave_data) > 0:
            for leave_id_chunk in split_every(50, leave_data):
                hrms_leaves = leave_obj.hrms_create_leave(leave_id_chunk, skip_existing_leave)

                message = "Leave created %s" % ', '.join(hrms_leaves.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification","message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)
                hrms_leave_ids.append(hrms_leaves.ids)

            self._cr.commit()
        return hrms_leave_ids

    # def manual_update_employee_to_hrms(self):
    #     hrms_employee_obj = self.env['hrms.hr.employee']
    #     instance_obj = self.env['hr.data.dashboard']

    #     start = time.time()
    #     hrms_employees = self._context.get('active_ids', [])

    #     employee = hrms_employee_obj.browse(hrms_employees)
    #     employees = employee.filtered(lambda x: x.exported_in_hrms)
    #     if employees and len(employees) > 80:
    #         raise UserError(_("Error:\n- System will not update more then 80 Employees at a "
    #                           "time.\n- Please select only 80 employee for export."))
    #     hrms_instance = instance_obj.search([])
    #     for instance in hrms_instance:
    #         hrms_employees = employees.filtered(lambda employee: employee.hrms_instance_id == instance)
    #         if hrms_employees:
    #             hrms_employee_obj.update_employees_in_hrms(instance, hrms_employees)
    #     end = time.time()
    #     _logger.info("Update Processed %s Employees in %s seconds.", str(len(employee)), str(end - start))
    #     return True

    # def manual_update_department_to_hrms(self):
    #     hrms_department_obj = self.env['hrms.hr.department']
    #     instance_obj = self.env['hr.data.dashboard']

    #     start = time.time()
    #     hrms_departments = self._context.get('active_ids', [])

    #     department = hrms_department_obj.browse(hrms_departments)
    #     departments = department.filtered(lambda x: x.exported_in_hrms)
    #     if departments and len(departments) > 80:
    #         raise UserError(_("Error:\n- System will not update more then 80 Departments at a "
    #                           "time.\n- Please select only 80 Department for export."))
    #     hrms_instance = instance_obj.search([])
    #     for instance in hrms_instance:
    #         hrms_departments = departments.filtered(lambda department: department.hrms_instance_id == instance)
    #         if hrms_departments:
    #             hrms_department_obj.update_departments_in_hrms(instance, hrms_departments)
    #     end = time.time()
    #     _logger.info("Update Processed %s Departments in %s seconds.", str(len(department)), str(end - start))
    #     return True
    
    # def manual_update_leave_to_hrms(self):
    #     hrms_employee_obj = self.env['hrms.hr.employee']
    #     instance_obj = self.env['hr.data.dashboard']

    #     start = time.time()
    #     hrms_employees = self._context.get('active_ids', [])

    #     employee = hrms_employee_obj.browse(hrms_employees)
    #     employees = employee.filtered(lambda x: x.exported_in_hrms)
    #     if employees and len(employees) > 80:
    #         raise UserError(_("Error:\n- System will not update more then 80 Employees at a "
    #                           "time.\n- Please select only 80 employee for export."))
    #     hrms_instance = instance_obj.search([])
    #     for instance in hrms_instance:
    #         hrms_employees = employees.filtered(lambda employee: employee.hrms_instance_id == instance)
    #         if hrms_employees:
    #             hrms_employee_obj.update_employees_in_hrms(instance, hrms_employees)
    #     end = time.time()
    #     _logger.info("Update Processed %s Employees in %s seconds.", str(len(employee)), str(end - start))
    #     return True
