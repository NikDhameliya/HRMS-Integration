# -*- coding: utf-8 -*-

from odoo import models, _


class ShopifyQueueProcessEpt(models.TransientModel):
    _name = 'queue.process'
    _description = 'HRMS Queue Process'

    def manual_queue_process(self):
        """
        This method is used to call child methods while manually queue(employee, department and leave) process.
        """
        queue_process = self._context.get('queue_process')
        if queue_process == "process_employee_queue_manually":
            self.sudo().process_employee_queue_manually()
        if queue_process == "process_department_queue_manually":
            self.sudo().process_department_queue_manually()
        if queue_process == "process_leave_queue_manually":
            self.sudo().process_leave_queue_manually()

    def process_employee_queue_manually(self):
        """This method used to process the product queue manually. You can call the method from here :
            HRMS => Processes => Queues Logs => Employees => Action => Process Queue Manually.
        """
        model = self._context.get('active_model')
        employee_queue_line_obj = self.env["employee.data.queue.line"]
        employee_queue_ids = self._context.get('active_ids')
        if model == 'employee.data.queue.line':
            employee_queue_ids = employee_queue_line_obj.search(
                [('id', 'in', employee_queue_ids)]).mapped("employee_data_queue_id").ids
        for employee_queue_id in employee_queue_ids:
            employee_queue_line_batch = employee_queue_line_obj.search(
                [("employee_data_queue_id", "=", employee_queue_id),
                 ("state", "in", ('draft', 'failed'))])
            employee_queue_line_batch.process_employee_queue_line_data()
        return True

    def process_leave_queue_manually(self):
        """This method used to process the product queue manually. You can call the method from here :
            HRMS => Processes => Queues Logs => Leaves => Action => Process Queue Manually.
        """
        model = self._context.get('active_model')
        leave_queue_line_obj = self.env["leave.data.queue.line"]
        leave_queue_ids = self._context.get('active_ids')
        if model == 'leave.data.queue.line':
            leave_queue_ids = leave_queue_line_obj.search(
                [('id', 'in', leave_queue_ids)]).mapped("leave_data_queue_id").ids
        for leave_queue_id in leave_queue_ids:
            leave_queue_line_batch = leave_queue_line_obj.search(
                [("leave_data_queue_id", "=", leave_queue_id),
                 ("state", "in", ('draft', 'failed'))])
            leave_queue_line_batch.process_product_queue_line_data()
        return True
    
    def process_department_queue_manually(self):
        """This method used to process the product queue manually. You can call the method from here :
            HRMS => Processes => Queues Logs => Departments => Action => Process Queue Manually.
        """
        model = self._context.get('active_model')
        department_queue_line_obj = self.env["department.data.queue.line"]
        department_queue_ids = self._context.get('active_ids')
        if model == 'department.data.queue.line':
            department_queue_ids = department_queue_line_obj.search(
                [('id', 'in', department_queue_ids)]).mapped("product_data_queue_id").ids
        for department_queue_id in department_queue_ids:
            department_queue_line_batch = department_queue_line_obj.search(
                [("product_data_queue_id", "=", department_queue_id),
                 ("state", "in", ('draft', 'failed'))])
            department_queue_line_batch.process_product_queue_line_data()
        return True

    def set_to_completed_queue(self):
        """
        This method used to change the queue(order, product and customer) state as completed.
        """
        queue_process = self._context.get('queue_process')
        if queue_process == "set_to_completed_employee_queue":
            self.set_to_completed_employee_queue_manually()
        if queue_process == "set_to_completed_department_queue":
            self.set_to_completed_department_queue_manually()
        if queue_process == "set_to_completed_leave_queue":
            self.set_to_completed_leave_queue_manually()

    def set_to_completed_employee_queue_manually(self):
        """This method used to set product queue as completed. You can call the method from here :
            HRMS => Processes => Queues Logs => Employee => SET TO COMPLETED.
        """
        employee_queue_ids = self._context.get('active_ids')
        employee_queue_ids = self.env['employee.data.queue'].browse(employee_queue_ids)
        for employee_queue_id in employee_queue_ids:
            queue_lines = employee_queue_id.employee_data_queue_lines.filtered(
                lambda line: line.state in ['draft', 'failed'])
            queue_lines.write({'state': 'cancel', "synced_employee_data": False})
            employee_queue_id.message_post(
                body=_("Manually set to cancel queue lines %s - ") % (queue_lines.mapped('employee_data_id')))
        return True
    
    def set_to_completed_department_queue_manually(self):
        """This method used to set product queue as completed. You can call the method from here :
            HRMS => Processes => Queues Logs => Department => SET TO COMPLETED.
        """
        department_queue_ids = self._context.get('active_ids')
        department_queue_ids = self.env['department.data.queue'].browse(department_queue_ids)
        for department_queue_id in department_queue_ids:
            queue_lines = department_queue_id.department_data_queue_lines.filtered(
                lambda line: line.state in ['draft', 'failed'])
            queue_lines.write({'state': 'cancel', "synced_department_data": False})
            department_queue_id.message_post(
                body=_("Manually set to cancel queue lines %s - ") % (queue_lines.mapped('department_data_id')))
        return True
        
    
    def set_to_completed_leave_queue_manually(self):
        """This method used to set product queue as completed. You can call the method from here :
            HRMS => Processes => Queues Logs => Leave => SET TO COMPLETED.
        """
        leave_queue_ids = self._context.get('active_ids')
        leave_queue_ids = self.env['leave.data.queue'].browse(leave_queue_ids)
        for leave_queue_id in leave_queue_ids:
            queue_lines = leave_queue_id.leave_data_queue_lines.filtered(
                lambda line: line.state in ['draft', 'failed'])
            queue_lines.write({'state': 'cancel', "synced_leave_data": False})
            leave_queue_id.message_post(
                body=_("Manually set to cancel queue lines %s - ") % (queue_lines.mapped('leave_data_id')))
        return True
