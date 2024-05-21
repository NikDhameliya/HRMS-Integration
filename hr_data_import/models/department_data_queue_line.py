# -*- coding: utf-8 -*-

import json
import logging
import time
from datetime import datetime

from odoo import models, fields, api, _

_logger = logging.getLogger("HRMS Department Queue Line")


class DepartmentDataQueueLine(models.Model):
    """This model is used to handel the department data queue line"""
    _name = "department.data.queue.line"
    _description = "Synced Department Data Line"

    state = fields.Selection([("draft", "Draft"), ("failed", "Failed"), ("done", "Done"),
                              ("cancel", "Cancelled")], default="draft")
    hrms_synced_department_data = fields.Char(string="HRMS Synced Data")
    hrms_department_data_id = fields.Text(string="Department ID")
    synced_department_queue_id = fields.Many2one("department.data.queue",
                                               string="HRMS Department",
                                               ondelete="cascade")
    last_process_date = fields.Datetime()
    hrms_instance_id = fields.Many2one("hr.data.dashboard", string="Instance")
    common_log_lines_ids = fields.One2many("common.log.lines",
                                           "hrms_department_data_queue_line_id",
                                           help="Log lines created against which line.")
    name = fields.Char(string="Department", help="HRMS Department Name")

    def hrms_create_multi_queue(self, department_queue_id, department_ids):
        """
        This method used to call child method for create a department queue line.
        :param department_queue_id: Record of the department queue.
        :param department_ids: 125 records of department response.
        """
        if department_queue_id:
            for result in department_ids:
                result = result.to_dict()
                self.hrms_department_data_queue_line_create(result, department_queue_id)
        return True

    def hrms_department_data_queue_line_create(self, result, department_queue_id):
        """
        This method used to create a department queue line.
        :param result:Response of 1 department.
        """
        synced_hrms_departments_line_obj = self.env["department.data.queue.line"]
        name = "%s %s" % (result.get("first_name") or "", result.get("last_name") or "")
        department_id = result.get("id")
        data = json.dumps(result)
        instance_id = department_queue_id.hrms_instance_id.id
        existing_department_data = synced_hrms_departments_line_obj.search(
            [('hrms_department_data_id', '=', department_id), ('hrms_instance_id', '=', instance_id),
             ('state', 'in', ['draft', 'failed'])])
        line_vals = {
            "synced_department_queue_id": department_queue_id.id,
            "hrms_department_data_id": department_id or "",
            "name": name.strip(),
            "hrms_synced_department_data": data,
            "hrms_instance_id": instance_id,
            "last_process_date": datetime.now(),
        }
        if not existing_department_data:
            return synced_hrms_departments_line_obj.create(line_vals)
        return existing_department_data.write({'hrms_synced_department_data': data})

    @api.model
    def sync_hrms_department_into_odoo(self):
        """
        This method is used to find department queue which queue lines have state in draft and is_action_require is False.
        If cronjob has tried more than 3 times to process any queue then it marks that queue has need process to
        manually. It will be called from auto queue process cron.
        """
        hrms_department_queue_obj = self.env["department.data.queue"]
        department_queue_ids = []

        query = """select queue.id
            from department_data_queue_line as queue_line
            inner join department_data_queue as queue on queue_line.synced_department_queue_id = queue.id
            where queue_line.state='draft' and queue.is_action_require = 'False'
            ORDER BY queue_line.create_date ASC"""
        self._cr.execute(query)
        department_data_queue_list = self._cr.fetchall()
        if department_data_queue_list:
            for department_data_queue_id in department_data_queue_list:
                if department_data_queue_id[0] not in department_queue_ids:
                    department_queue_ids.append(department_data_queue_id[0])
            queues = hrms_department_queue_obj.browse(department_queue_ids)
            self.filter_department_queue_lines_and_post_message(queues)
        return True

    def filter_department_queue_lines_and_post_message(self, queues):
        """
        This method is used to post a message if the queue is process more than 3 times otherwise
        it calls the child method to process the department queue line.
        :param queues: Record of the department queues.
        """
        common_log_line_obj = self.env["common.log.lines"]
        start = time.time()
        department_queue_process_cron_time = queues.hrms_instance_id.get_hrms_cron_execution_time(
            "hr_data_import.process_hrms_department_queue")

        for queue in queues:
            results = queue.synced_department_queue_line_ids.filtered(lambda x: x.state == "draft")

            queue.queue_process_count += 1
            # queue.queue_process_count = 4
            if queue.queue_process_count > 3:
                queue.is_action_require = True
                note = _("<p>Need to process this department queue manually.There are 3 attempts been made by " \
                         "automated action to process this queue,"
                         "<br/>- Ignore, if this queue is already processed.</p>")
                queue.message_post(body=note)
                if queue.hrms_instance_id.is_hrms_create_schedule:
                    common_log_line_obj.create_crash_queue_schedule_activity(queue, "department.data.queue",
                                                                             note)
                continue
            self._cr.commit()
            results.process_department_queue_lines()
            if time.time() - start > department_queue_process_cron_time - 60:
                return True

    def process_department_queue_lines(self):
        """
        This method process the queue lines.
        """
        queues = self.synced_department_queue_id

        for queue in queues:
            instance = queue.hrms_instance_id
            if instance.active:
                self.env.cr.execute("""update department_data_queue set is_process_queue = False where
                is_process_queue = True""")
                self._cr.commit()

                self.department_queue_commit_and_process(queue, instance)

                _logger.info("Department Queue %s is processed.", queue.name)

        return True

    def department_queue_commit_and_process(self, queue, instance):
        """ This method is used to commit the department queue line after 10 department queue line process
            and call the child method to process the department queue line.
            :param queue: Record of department queue.
        """
        hrms_department_obj = self.env["hrms.hr.department"]
        commit_count = 0
        for line in self:
            commit_count += 1
            if commit_count == 10:
                queue.is_process_queue = True
                self._cr.commit()
                commit_count = 0

            department_data = json.loads(line.hrms_synced_department_data)
            department = hrms_department_obj.hrms_create_department(department_data, instance, line)
            if department:
                line.update(
                    {"state": "done", "last_process_date": datetime.now(), 'hrms_synced_department_data': False})
            else:
                line.update({"state": "failed", "last_process_date": datetime.now()})
            queue.is_process_queue = False
