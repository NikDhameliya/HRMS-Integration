# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime

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
    # cron_process_notification = fields.Text(string="hrms Note: ", store=False,
    #                                         help="Used to display that cron will be run after some time")


    def hrms_execute(self):
        """This method used to execute the operation as per given in wizard.
        """
        employee_data_queue_obj = self.env["employee.data.queue"]
        department_data_queue_obj = self.env["department.data.queue"]
        leave_data_queue_obj = self.env["leave.data.queue"]
        queue_ids = False

        instance = self.hrms_instance_id
        if self.hrms_operation == "sync_employee":
            employee_queue_ids = employee_data_queue_obj.hrms_create_employee_data_queue(
                instance, self.import_employees,
                self.skip_existing_employee)
            if employee_queue_ids:
                queue_ids = employee_queue_ids
                action_name = "hr_data_import.action_hrms_employee_data_queue"
                form_view_name = "hr_data_import.employee_synced_data_form_view"

        if self.hrms_operation == "sync_department":
            department_queue_ids = department_data_queue_obj.hrms_create_department_data_queue(
                instance, self.import_departments,
                self.skip_existing_department)
            if department_queue_ids:
                queue_ids = department_queue_ids
                action_name = "hr_data_import.action_hrms_department_data_queue"
                form_view_name = "hr_data_import.department_synced_data_form_view"

            
        if self.hrms_operation == "sync_leave":
            leave_queue_ids = leave_data_queue_obj.hrms_create_leave_data_queue(
                instance, self.import_leaves,
                self.skip_existing_leave)
            if leave_queue_ids:
                queue_ids = leave_queue_ids
                action_name = "hr_data_import.action_hrms_leave_data_queue"
                form_view_name = "hr_data_import.leave_synced_data_form_view"


        if queue_ids and action_name and form_view_name:
            action = self.env.ref(action_name).sudo().read()[0]
            form_view = self.sudo().env.ref(form_view_name)

            if len(queue_ids) == 1:
                action.update({"view_id": (form_view.id, form_view.name), "res_id": queue_ids[0],
                               "views": [(form_view.id, "form")]})
            else:
                action["domain"] = [("id", "in", queue_ids)]
            return action

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def manual_update_employee_to_hrms(self):
        hrms_employee_obj = self.env['hrms.hr.employee']
        instance_obj = self.env['hr.data.dashboard']

        start = time.time()
        hrms_employees = self._context.get('active_ids', [])

        employee = hrms_employee_obj.browse(hrms_employees)
        employees = employee.filtered(lambda x: x.exported_in_hrms)
        if employees and len(employees) > 80:
            raise UserError(_("Error:\n- System will not update more then 80 Employees at a "
                              "time.\n- Please select only 80 employee for export."))
        hrms_instance = instance_obj.search([])
        for instance in hrms_instance:
            hrms_employees = employees.filtered(lambda employee: employee.hrms_instance_id == instance)
            if hrms_employees:
                hrms_employee_obj.update_employees_in_hrms(instance, hrms_employees)
        end = time.time()
        _logger.info("Update Processed %s Employees in %s seconds.", str(len(employee)), str(end - start))
        return True

    def manual_update_department_to_hrms(self):
        hrms_department_obj = self.env['hrms.hr.department']
        instance_obj = self.env['hr.data.dashboard']

        start = time.time()
        hrms_departments = self._context.get('active_ids', [])

        department = hrms_department_obj.browse(hrms_departments)
        departments = department.filtered(lambda x: x.exported_in_hrms)
        if departments and len(departments) > 80:
            raise UserError(_("Error:\n- System will not update more then 80 Departments at a "
                              "time.\n- Please select only 80 Department for export."))
        hrms_instance = instance_obj.search([])
        for instance in hrms_instance:
            hrms_departments = departments.filtered(lambda department: department.hrms_instance_id == instance)
            if hrms_departments:
                hrms_department_obj.update_departments_in_hrms(instance, hrms_departments)
        end = time.time()
        _logger.info("Update Processed %s Departments in %s seconds.", str(len(department)), str(end - start))
        return True
    
    def manual_update_leave_to_hrms(self):
        hrms_employee_obj = self.env['hrms.hr.employee']
        instance_obj = self.env['hr.data.dashboard']

        start = time.time()
        hrms_employees = self._context.get('active_ids', [])

        employee = hrms_employee_obj.browse(hrms_employees)
        employees = employee.filtered(lambda x: x.exported_in_hrms)
        if employees and len(employees) > 80:
            raise UserError(_("Error:\n- System will not update more then 80 Employees at a "
                              "time.\n- Please select only 80 employee for export."))
        hrms_instance = instance_obj.search([])
        for instance in hrms_instance:
            hrms_employees = employees.filtered(lambda employee: employee.hrms_instance_id == instance)
            if hrms_employees:
                hrms_employee_obj.update_employees_in_hrms(instance, hrms_employees)
        end = time.time()
        _logger.info("Update Processed %s Employees in %s seconds.", str(len(employee)), str(end - start))
        return True

    def create_employee_data_queues(self, employee_data):
        """
        It creates employee data queue from data of Employee.
        """
        employee_queue_list = []
        employee_data_queue_obj = self.env["employee.data.queue"]
        employee_data_queue_line_obj = self.env["employee.data.queue.line"]
        bus_bus_obj = self.env["bus.bus"]

        if len(employee_data) > 0:
            for employee_id_chunk in split_every(125, employee_data):
                employee_queue = employee_data_queue_obj.create_employee_queue(self.hrms_instance_id,
                                                                                 "import_process")
                employee_data_queue_line_obj.hrms_create_multi_queue(employee_queue, employee_id_chunk)

                message = "Employee Queue created %s" % ', '.join(employee_queue.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification","message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)

                employee_queue_list.append(employee_queue.id)
            self._cr.commit()
        return employee_queue_list
    
    def create_department_data_queues(self, department_data):
        """
        It creates department data queue from data of department.
        """
        department_queue_list = []
        department_data_queue_obj = self.env["department.data.queue"]
        department_data_queue_line_obj = self.env["department.data.queue.line"]
        bus_bus_obj = self.env["bus.bus"]

        if len(department_data) > 0:
            for department_id_chunk in split_every(125, department_data):
                department_queue = department_data_queue_obj.create_department_queue(self.hrms_instance_id,
                                                                                 "import_process")
                department_data_queue_line_obj.hrms_create_multi_queue(department_queue, department_id_chunk)

                message = "Department Queue created %s" % ', '.join(department_queue.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification","message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)

                department_queue_list.append(department_queue.id)
            self._cr.commit()
        return department_queue_list

    def create_leave_data_queues(self, leave_data):
        """
        It creates leave data queue from data of leave.
        """
        leave_queue_list = []
        leave_data_queue_obj = self.env["leave.data.queue"]
        leave_data_queue_line_obj = self.env["leave.data.queue.line"]
        bus_bus_obj = self.env["bus.bus"]

        if len(leave_data) > 0:
            for leave_id_chunk in split_every(125, leave_data):
                leave_queue = leave_data_queue_obj.create_leave_queue(self.hrms_instance_id,
                                                                                 "import_process")
                leave_data_queue_line_obj.hrms_create_multi_queue(leave_queue, leave_id_chunk)

                message = "Leave Queue created %s" % ', '.join(leave_queue.mapped('name'))
                bus_bus_obj._sendone(self.env.user.partner_id, "simple_notification",
                                     {"title": "HRMS Notification","message": message, "sticky": False,
                                      "warning": True})
                _logger.info(message)

                leave_queue_list.append(leave_queue.id)
            self._cr.commit()
        return leave_queue_list


    # @api.onchange("hrms_instance_id", "hrms_operation")
    # def onchange_hrms_instance_id(self):
    #     """
    #     This method sets field values, when the Instance will be changed.
    #     """
    #     instance = self.hrms_instance_id
    #     current_time = datetime.now()
    #     if instance:
    #         if self.hrms_operation == "sync_employee":
    #             self.orders_from_date = instance.hrms_last_date_employee_import or False
    #         elif self.hrms_operation == "sync_department":
    #             self.orders_from_date = instance.hrms_last_date_department_import or False
    #         elif self.hrms_operation == 'sync_leave':
    #             self.orders_from_date = instance.hrms_last_date_leave_import or False
    #         self.orders_to_date = current_time