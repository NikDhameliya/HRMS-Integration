# -*- coding: utf-8 -*-

from odoo import models


class DataQueueMixinEpt(models.AbstractModel):
    """ Mixin class for delete unused data queue from database."""
    _inherit = "data.queue.mixin"

    def delete_data_queue_ept(self, queue_data=False, is_delete_queue=False):
        """
        This method will delete completed data queues from database.
        """
        if not queue_data:
            queue_data = []
        queue_data += ["hrms_employee_data_queue_ept", "hrms_department_data_queue_ept",
                       "hrms_leave_data_queue_ept"]
        return super(DataQueueMixinEpt, self).delete_data_queue_ept(queue_data, is_delete_queue)
