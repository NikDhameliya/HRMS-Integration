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
        data_ids = False
        context = dict(self.env.context or {})
        context.update({'hrms_instance_id': self.hrms_instance_id.id})
        try:
            if self.hrms_operation == "sync_employee":
                employee_ids = self.with_context(context).hrms_create_employee(
                    self.skip_existing_employee)
                # Flatten the list of lists into a single list
                flat_employee_ids = [
                    item for sublist in employee_ids for item in sublist]
                if flat_employee_ids:
                    data_ids = flat_employee_ids
                    if data_ids:
                        return {
                            'type': 'ir.actions.act_window',
                            'name': _('HRMS Employees'),
                            'res_model': 'hrms.hr.employee',
                            'views': [[False, 'list'], [False, 'form']],
                            'domain': [('id', 'in', data_ids)],
                        }

            elif self.hrms_operation == "sync_department":
                department_ids = self.with_context(context).hrms_create_department(
                    self.skip_existing_department)
                # Flatten the list of lists into a single list
                flat_department_ids = [
                    item for sublist in department_ids for item in sublist]

                if flat_department_ids:
                    data_ids = flat_department_ids
                    if data_ids:
                        return {
                            'type': 'ir.actions.act_window',
                            'name': _('HRMS Departments'),
                            'res_model': 'hrms.hr.department',
                            'views': [[False, 'list'], [False, 'form']],
                            'domain': [('id', 'in', data_ids)],
                        }

            elif self.hrms_operation == "sync_leave":
                leave_ids = self.with_context(context).hrms_create_leave(self.skip_existing_leave)
                # Flatten the list of lists into a single list
                flat_leave_ids = [
                    item for sublist in leave_ids for item in sublist]
                if flat_leave_ids:
                    data_ids = flat_leave_ids
                    if flat_leave_ids:
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

        # response = requests.request("GET", api_url, headers=headers, data=payload)
        response = {'result': {'current_page': 1, 'data': [{'id': 'ND', 'name': 'John Doe', 'email': 'john.doe@example.com', 'position': 'CEO', 'grade': '', 'residence': 'Country, City', 'residence_comment': False, 'country': 'Молдова', 'city': False, 'phone': '1234567890', 'skype': False, 'linked_in': False, 'telegram': False, 'birth_date': '1982-08-11', 'end_test': '2016-04-01', 'fired_date': False, 'start_date': '2016-04-01', 'gender': 1, 'additional_email': 'alternate.email@example.com', 'additional_phone': False, 'relocate': False, 'duties': False, 'description': False, 'additional_info': False, 'team': [{'id': 2, 'name': 'Management'}], 'career': [{'start_date': '2021-04-08', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': '', 'department': False, 'position': 'CEO&СТО', 'grade': '', 'place': '', 'team': 'Management', 'comment': False}, {'start_date': '2021-03-29', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': '', 'department': False, 'position': 'CEO&СТО', 'grade': '', 'place': '', 'team': '', 'comment': ''}], 'contacts': [{'type_id': 2, 'type_name': 'email', 'value': 'alternate.email@example.com'}, {'type_id': 1, 'type_name': 'phone', 'value': '1234567890'}], 'languages': [], 'educations': [], 'skills': [], 'awards': []}, {'id': '7xl', 'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'position': 'HR Specialist', 'grade': '', 'residence': 'Country, City, Address', 'residence_comment': 'Address details', 'country': 'Україна', 'city': 'Суми', 'phone': '0987654321', 'skype': False, 'linked_in': False, 'telegram': False, 'birth_date': '1995-11-26', 'end_test': '2021-03-11', 'fired_date': False, 'start_date': '2021-02-11', 'gender': 2, 'additional_email': False, 'additional_phone': False, 'relocate': False, 'duties': False, 'description': False, 'additional_info': "Relative's contact phone number - 1231231234", 'team': [{'id': 8, 'name': 'HR/ Recruiting'}, {'id': 2, 'name': 'Management'}], 'career': [{'start_date': '2021-05-27', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': False, 'department': False, 'position': 'HR Specialist/Recruiter', 'grade': '', 'place': False, 'team': 'Management', 'comment': False}, {'start_date': '2021-04-08', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': False,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'department': False, 'position': 'HR Specialist/Recruiter', 'grade': '', 'place': False, 'team': 'HR/ Recruiting', 'comment': False}, {'start_date': '', 'end_date': False, 'test_period_start_date': False, 'test_period_end_date': False, 'company_name': False, 'department': False, 'position': 'HR Specialist/Recruiter', 'grade': '', 'place': False, 'team': 'HR/ Recruiting', 'comment': False}], 'contacts': [{'type_id': 2, 'type_name': 'email', 'value': 'jane.smith@fakemail.com'}, {'type_id': 1, 'type_name': 'phone', 'value': '9876543210'}], 'languages': [], 'educations': [], 'skills': [], 'awards': []}], 'first_page_url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=1', 'from': 1, 'last_page': 19, 'last_page_url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=19', 'links': [{'url': False, 'label': '&laquo; Поп.', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=1', 'label': '1', 'active': True}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=2', 'label': '2', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=3', 'label': '3', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=4', 'label': '4', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=5', 'label': '5', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=6', 'label': '6', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=7', 'label': '7', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=8', 'label': '8', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=9', 'label': '9', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=10', 'label': '10', 'active': False}, {'url': False, 'label': '...', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=18', 'label': '18', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=19', 'label': '19', 'active': False}, {'url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=2', 'label': 'Наст. &raquo;', 'active': False}], 'next_page_url': 'https://mycompany.hrmsystem.com/api/v1/employees?page=2', 'path': 'https://mycompany.hrmsystem.com/api/v1/employees', 'per_page': 5, 'prev_page_url': False, 'to': 5, 'total': 200}, 'error': False, 'code': 200, 'messages': []}

        if response['code'] == 200:
            # TODO Uncomment below line and remove static data assign
            # employee_data = response.json().get('data', [])
            employee_data = response['result']['data']

        if len(employee_data) > 0:
            for employee_id_chunk in split_every(25, employee_data):
                hrms_employees_ids = employee_obj.hrms_create_employee(
                    employee_id_chunk, skip_existing_employee)
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

        # response = requests.request("GET", api_url, headers=headers, data=payload)
        response = {
    "result": {
        "current_page": 1,
        "data": [
            {
                "id": 2,
                "type": 1,
                "name": "Management",
                "number_of_members": 4,
                "number_of_members_with_subteams": 4,
                "team_leader_id": False,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "ND"
                ],
                "subteams": [],
                "parent_id": False
            },
            {
                "id": 5,
                "type": 1,
                "name": "Sales Team",
                "number_of_members": 5,
                "number_of_members_with_subteams": 5,
                "team_leader_id": "lXEQ",
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "ND",
                    "lXEQ"
                ],
                "subteams": [],
                "parent_id": False
            },
            {
                "id": 26,
                "type": 1,
                "name": "DELIVERY",
                "number_of_members": 1,
                "number_of_members_with_subteams": 29,
                "team_leader_id": False,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [],
                "subteams": [
                    7,
                    12,
                    21,
                    22,
                    24,
                    27,
                    28,
                    35,
                    39,
                    40,
                    41,
                    42
                ],
                "parent_id": False
            },
            {
                "id": 6,
                "type": 1,
                "name": "Training Camp",
                "number_of_members": 0,
                "number_of_members_with_subteams": 0,
                "team_leader_id": False,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "d82"
                ],
                "subteams": [],
                "parent_id": False
            },
            {
                "id": 7,
                "type": 1,
                "name": "Project ABC",
                "number_of_members": 7,
                "number_of_members_with_subteams": 7,
                "team_leader_id": False,
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "Oox"
                ],
                "subteams": [],
                "parent_id": 26
            },
            {
                "id": 8,
                "type": 1,
                "name": "HR/ Recruiting",
                "number_of_members": 2,
                "number_of_members_with_subteams": 2,
                "team_leader_id": "7xl",
                "hr_ids": [
                    "7xl"
                ],
                "managers": [
                    "ND",
                    "7xl"
                ],
                "subteams": [],
                "parent_id": False
            }
        ],
        "first_page_url": "https://mycompany.hrmsystem.com/api/v1/departments?page=1",
        "from": 1,
        "last_page": 5,
        "last_page_url": "https://mycompany.hrmsystem.com/api/v1/departments?page=5",
        "links": [
            {
                "url": False,
                "label": "&laquo; Prev.",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=1",
                "label": "1",
                "active": True
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=2",
                "label": "2",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=3",
                "label": "3",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=4",
                "label": "4",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=5",
                "label": "5",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/departments?page=2",
                "label": "Next. &raquo;",
                "active": False
            }
        ],
        "next_page_url": "https://mycompany.hrmsystem.com/api/v1/departments?page=2",
        "path": "https://mycompany.hrmsystem.com/api/v1/departments",
        "per_page": 5,
        "prev_page_url": False,
        "to": 5,
        "total": 21
    },
    "error": False,
    "code": 200,
    "messages": []
}

        if response['code'] == 200:
            # TODO Uncomment below line and remove static data assign
            # department_data = response.json().get('data', [])
            department_data = response['result']['data']

        if len(department_data) > 0:
            for department_id_chunk in split_every(25, department_data):
                hrms_departments_ids = department_obj.hrms_create_department(
                    department_id_chunk, skip_existing_department)
                hrms_departments = department_obj.browse(hrms_departments_ids)
                

                message = "Department created %s" % ', '.join(
                    hrms_departments.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification", "message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)
                hrms_department_ids.append(hrms_departments_ids)

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
        api_url = "https://{my_company_domain}/api/v1/out-off-office?page=1&per_page=20&additional_info=True"
        payload = {}
        headers = {
            'token': '{api_token}'
        }

        # response = requests.request("GET", api_url, headers=headers, data=payload)
        response = {
    "result": {
        "current_page": 1,
        "data": [
            {
                "id": "ND",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "end_test": "2016-04-01",
                "fired_date": False,
                "business_trip": [],
                "home_work": [],
                "sick_leave": [],
                "documented_sick_leave": [],
                "vacation": [                 
                    {
                        "date": "2023-02-09",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-02-08",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-02-07",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-02-06",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    }
                ],
                "unpaid_vacation": [],
                "overtime": [],
                "weekend_work": [
                    {
                        "date": "2021-06-27",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2021-04-17",
                        "is_full_day": False,
                        "from": "10:00",
                        "to": "16:00",
                        "used_minutes": 360
                    }
                ],
                "night_shift": [],
                "day_transfer": []
            },
            {
                "id": "7xl",
                "name": "Helen Aoe",
                "email": "helen.aoe@example.com",
                "end_test": "2021-03-11",
                "fired_date": False,
                "business_trip": [],
                "home_work": [
                    {
                        "date": "2021-09-06",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2021-08-02",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    }
                ],
                "sick_leave": [
                    {
                        "date": "2022-03-30",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2022-02-21",
                        "is_full_day": False,
                        "from": "14:30",
                        "to": "15:30",
                        "used_minutes": 60
                    },
                    {
                        "date": "2022-02-18",
                        "is_full_day": False,
                        "from": "11:30",
                        "to": "18:00",
                        "used_minutes": 390
                    },
                    {
                        "date": "2022-02-17",
                        "is_full_day": False,
                        "from": "09:00",
                        "to": "11:30",
                        "used_minutes": 150
                    },
                    {
                        "date": "2022-02-16",
                        "is_full_day": False,
                        "from": "14:30",
                        "to": "15:30",
                        "used_minutes": 60
                    },
                    {
                        "date": "2021-11-05",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    }
                ],
                "documented_sick_leave": [],
                "vacation": [
                    {
                        "date": "2024-03-25",
                        "is_full_day": False,
                        "from": "14:00",
                        "to": "18:00",
                        "used_minutes": 240
                    },
                    {
                        "date": "2024-02-23",
                        "is_full_day": False,
                        "from": "14:00",
                        "to": "18:00",
                        "used_minutes": 240
                    },
                    {
                        "date": "2023-12-29",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-12-28",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-12-21",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                ],
                "unpaid_vacation": [],
                "overtime": [
                    {
                        "date": "2022-06-08",
                        "is_full_day": False,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    }
                ],
                "weekend_work": [],
                "night_shift": [],
                "day_transfer": [
                    {
                        "start": {
                            "date": "2021-07-28",
                            "is_full_day": False,
                            "from": "16:30",
                            "to": "18:00",
                            "used_minutes": 90
                        },
                        "end": {
                            "date": "2021-07-27",
                            "is_full_day": False,
                            "from": "18:00",
                            "to": "19:30",
                            "used_minutes": 90
                        }
                    }
                ]
            },
            {
                "id": "RLp",
                "name": "Dennis Smith",
                "email": "dennis.smith@example.com",
                "end_test": "2021-12-19",
                "fired_date": False,
                "business_trip": [],
                "home_work": [],
                "sick_leave": [],
                "documented_sick_leave": [],
                "vacation": [
                    {
                        "date": "2023-12-22",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-11-10",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-11-09",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-11-08",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-04-18",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-04-17",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 480
                    },
                    {
                        "date": "2023-04-16",
                        "is_full_day": True,
                        "from": False,
                        "to": False,
                        "used_minutes": 0
                    },
                ],
                "unpaid_vacation": [],
                "overtime": [],
                "weekend_work": [],
                "night_shift": [],
                "day_transfer": []
            },
        ],
        "first_page_url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=1",
        "from": 1,
        "last_page": 19,
        "last_page_url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=19",
        "links": [
            {
                "url": False,
                "label": "&laquo; Prev.",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=1",
                "label": "1",
                "active": True
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=2",
                "label": "2",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=3",
                "label": "3",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=4",
                "label": "4",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=5",
                "label": "5",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=6",
                "label": "6",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=7",
                "label": "7",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=8",
                "label": "8",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=9",
                "label": "9",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=10",
                "label": "10",
                "active": False
            },
            {
                "url": False,
                "label": "...",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=18",
                "label": "18",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=19",
                "label": "19",
                "active": False
            },
            {
                "url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=2",
                "label": "Next. &raquo;",
                "active": False
            }
        ],
        "next_page_url": "https://mycompany.hrmsystem.com/api/v1/out-off-office?page=2",
        "path": "https://mycompany.hrmsystem.com/api/v1/out-off-office",
        "per_page": 5,
        "prev_page_url": False,
        "to": 5,
        "total": 94
    },
    "error": False,
    "code": 200,
    "messages": []
}

        if response['code'] == 200:
            leave_data = response.json().get('data', [])

        if len(leave_data) > 0:
            for leave_id_chunk in split_every(50, leave_data):
                hrms_leaves_ids = leave_obj.hrms_create_leave(
                    leave_id_chunk, skip_existing_leave)
                hrms_leaves = leave_obj.browse(hrms_leaves_ids)

                message = "Leave created %s" % ', '.join(
                    hrms_leaves.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification", "message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)
                hrms_leave_ids.append(hrms_leaves_ids)

            self._cr.commit()
        return hrms_leave_ids

