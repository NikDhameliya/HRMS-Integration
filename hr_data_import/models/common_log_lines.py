# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class CommonLogLineEpt(models.Model):
    _inherit = "common.log.lines"

    hrms_employee_data_queue_line_id = fields.Many2one("employee.data.queue.line",
                                                         "HRMS Employee Queue Line")
    hrms_department_data_queue_line_id = fields.Many2one("department.data.queue.line",
                                                       "HRMS Department Queue Line")
    hrms_leave_data_queue_line_id = fields.Many2one("leave.data.queue.line",
                                                          "HRMS Customer Queue Line")
    hrms_instance_id = fields.Many2one("hr.data.dashboard", "HRMS Instance")

    def create_crash_queue_schedule_activity(self, queue_id, model, note):
        """
        This method is used to create a schedule activity for the queue crash.
        Base on the HRMS configuration when any queue crash will create a schedule activity.
        :param queue_id: Record of the queue(employee,department and leave)
        :param model_id: Record of model(employee,department and leave)
        :param note: Message
        """
        mail_activity_obj = self.env['mail.activity']
        activity_type_id = queue_id and queue_id.hrms_instance_id.hrms_activity_type_id.id
        date_deadline = datetime.strftime(
            datetime.now() + timedelta(days=int(queue_id.hrms_instance_id.hrms_date_deadline)), "%Y-%m-%d")

        if queue_id:
            for user_id in queue_id.hrms_instance_id.hrms_user_ids:
                model_id = self._get_model_id(model).id
                mail_activity = mail_activity_obj.search(
                    [('res_model_id', '=', model_id), ('user_id', '=', user_id.id), ('res_id', '=', queue_id.id),
                     ('activity_type_id', '=', activity_type_id)])
                if not mail_activity:
                    vals = self.prepare_vals_for_schedule_activity(activity_type_id, note, queue_id, user_id, model_id,
                                                                   date_deadline)
                    try:
                        mail_activity_obj.create(vals)
                    except Exception as error:
                        _logger.info("Unable to create schedule activity, Please give proper "
                                     "access right of this user :%s  ", user_id.name)
                        _logger.info(error)
        return True

    def prepare_vals_for_schedule_activity(self, activity_type_id, note, queue_id, user_id, model_id, date_deadline):
        """ This method used to prepare a vals for the schedule activity.
            :param activity_type_id: Record of the activity type(email,call,meeting, to do)
            :param user_id: Record of user(whom to assign schedule activity)
            :param date_deadline: date of schedule activity dead line.
            @return: values
        """
        values = {'activity_type_id': activity_type_id,
                  'note': note,
                  'res_id': queue_id.id,
                  'user_id': user_id.id or self._uid,
                  'res_model_id': model_id,
                  'date_deadline': date_deadline
                  }
        return values

    def create_common_log_line_ept(self, **kwargs):
        """
        Inherit This method for search any existing same log line placed or not
        """
        record_id = self.search_existing_record(**kwargs)
        if record_id:
            record_id.unlink()
        return super(CommonLogLineEpt, self).create_common_log_line_ept(**kwargs)

    def search_existing_record(self, **kwargs):
        model = self._get_model_id(kwargs.get('model_name')).id
        record_id = self.search([('hrms_instance_id', '=', kwargs.get('hrms_instance_id')),
                                 ('model_id', '=', model),
                                 ('message', '=', kwargs.get('message')),
                                 ('hrms_employee_data_queue_line_id', '=',
                                  kwargs.get('hrms_employee_data_queue_line_id')),
                                 ('hrms_department_data_queue_line_id', '=',
                                  kwargs.get('hrms_department_data_queue_line_id')),
                                 ('hrms_leave_data_queue_line_id', '=',
                                  kwargs.get('hrms_leave_data_queue_line_id'))
                                 ])
        return record_id
