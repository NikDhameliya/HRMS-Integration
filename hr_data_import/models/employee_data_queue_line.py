# -*- coding: utf-8 -*-

import json
import logging
import time
from datetime import datetime

from odoo import models, fields, api, _

_logger = logging.getLogger("HRMS Employee Queue Line")


class EmployeeDataQueueLine(models.Model):
    """This model is used to handel the employee data queue line"""
    _name = "employee.data.queue.line"
    _description = "Synced Employee Data Line"

    state = fields.Selection([("draft", "Draft"), ("failed", "Failed"), ("done", "Done"),
                              ("cancel", "Cancelled")], default="draft")
    hrms_synced_employee_data = fields.Char(string="HRMS Synced Data")
    hrms_employee_data_id = fields.Text(string="Employee ID")
    synced_employee_queue_id = fields.Many2one("employee.data.queue",
                                               string="HRMS Employee",
                                               ondelete="cascade")
    last_process_date = fields.Datetime()
    hrms_instance_id = fields.Many2one("hr.data.dashboard", string="Instance")
    common_log_lines_ids = fields.One2many("common.log.lines",
                                           "hrms_employee_data_queue_line_id",
                                           help="Log lines created against which line.")
    name = fields.Char(string="Employee", help="HRMS Employee Name")

    def hrms_create_multi_queue(self, employee_queue_id, employee_ids):
        """
        This method used to call child method for create a employee queue line.
        :param employee_queue_id: Record of the employee queue.
        :param employee_ids: 125 records of employee response.
        """
        if employee_queue_id:
            for result in employee_ids:
                result = result.to_dict()
                self.hrms_employee_data_queue_line_create(result, employee_queue_id)
        return True

    def hrms_employee_data_queue_line_create(self, result, employee_queue_id):
        """
        This method used to create a employee queue line.
        :param result:Response of 1 employee.
        """
        synced_hrms_employees_line_obj = self.env["employee.data.queue.line"]
        name = "%s %s" % (result.get("first_name") or "", result.get("last_name") or "")
        employee_id = result.get("id")
        data = json.dumps(result)
        instance_id = employee_queue_id.hrms_instance_id.id
        existing_employee_data = synced_hrms_employees_line_obj.search(
            [('hrms_employee_data_id', '=', employee_id), ('hrms_instance_id', '=', instance_id),
             ('state', 'in', ['draft', 'failed'])])
        line_vals = {
            "synced_employee_queue_id": employee_queue_id.id,
            "hrms_employee_data_id": employee_id or "",
            "name": name.strip(),
            "hrms_synced_employee_data": data,
            "hrms_instance_id": instance_id,
            "last_process_date": datetime.now(),
        }
        if not existing_employee_data:
            return synced_hrms_employees_line_obj.create(line_vals)
        return existing_employee_data.write({'hrms_synced_employee_data': data})

    @api.model
    def sync_hrms_employee_into_odoo(self):
        """
        This method is used to find employee queue which queue lines have state in draft and is_action_require is False.
        If cronjob has tried more than 3 times to process any queue then it marks that queue has need process to
        manually. It will be called from auto queue process cron.
        """
        hrms_employee_queue_obj = self.env["employee.data.queue"]
        employee_queue_ids = []

        query = """select queue.id
            from employee_data_queue_line as queue_line
            inner join employee_data_queue as queue on queue_line.synced_employee_queue_id = queue.id
            where queue_line.state='draft' and queue.is_action_require = 'False'
            ORDER BY queue_line.create_date ASC"""
        self._cr.execute(query)
        employee_data_queue_list = self._cr.fetchall()
        if employee_data_queue_list:
            for employee_data_queue_id in employee_data_queue_list:
                if employee_data_queue_id[0] not in employee_queue_ids:
                    employee_queue_ids.append(employee_data_queue_id[0])
            queues = hrms_employee_queue_obj.browse(employee_queue_ids)
            self.filter_employee_queue_lines_and_post_message(queues)
        return True

    def filter_employee_queue_lines_and_post_message(self, queues):
        """
        This method is used to post a message if the queue is process more than 3 times otherwise
        it calls the child method to process the employee queue line.
        :param queues: Record of the employee queues.
        """
        common_log_line_obj = self.env["common.log.lines"]
        start = time.time()
        employee_queue_process_cron_time = queues.hrms_instance_id.get_hrms_cron_execution_time(
            "hr_data_import.process_hrms_employee_queue")

        for queue in queues:
            results = queue.synced_employee_queue_line_ids.filtered(lambda x: x.state == "draft")

            queue.queue_process_count += 1
            # queue.queue_process_count = 4
            if queue.queue_process_count > 3:
                queue.is_action_require = True
                note = _("<p>Need to process this employee queue manually.There are 3 attempts been made by " \
                         "automated action to process this queue,"
                         "<br/>- Ignore, if this queue is already processed.</p>")
                queue.message_post(body=note)
                if queue.hrms_instance_id.is_hrms_create_schedule:
                    common_log_line_obj.create_crash_queue_schedule_activity(queue, "employee.data.queue",
                                                                             note)
                continue
            self._cr.commit()
            results.process_employee_queue_lines()
            if time.time() - start > employee_queue_process_cron_time - 60:
                return True

    def process_employee_queue_lines(self):
        """
        This method process the queue lines.
        """
        queues = self.synced_employee_queue_id

        for queue in queues:
            instance = queue.hrms_instance_id
            if instance.active:
                self.env.cr.execute("""update employee_data_queue set is_process_queue = False where
                is_process_queue = True""")
                self._cr.commit()

                self.employee_queue_commit_and_process(queue, instance)

                _logger.info("Employee Queue %s is processed.", queue.name)

        return True

    def employee_queue_commit_and_process(self, queue, instance):
        """ This method is used to commit the employee queue line after 10 employee queue line process
            and call the child method to process the employee queue line.
            :param queue: Record of employee queue.
        """
        hrms_employee_obj = self.env["hrms.hr.employee"]
        commit_count = 0
        for line in self:
            commit_count += 1
            if commit_count == 10:
                queue.is_process_queue = True
                self._cr.commit()
                commit_count = 0

            employee_data = json.loads(line.hrms_synced_employee_data)
            employee = hrms_employee_obj.hrms_create_employee(employee_data, instance, line)
            if employee:
                line.update(
                    {"state": "done", "last_process_date": datetime.now(), 'hrms_synced_employee_data': False})
            else:
                line.update({"state": "failed", "last_process_date": datetime.now()})
            queue.is_process_queue = False
