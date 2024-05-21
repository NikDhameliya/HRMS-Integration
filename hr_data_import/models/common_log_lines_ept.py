# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class CommonLogLineEpt(models.Model):
    _name = "common.log.lines"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Common log line"
    

    employee_id = fields.Many2one('hr.employee', ondelete="cascade")
    department_id = fields.Many2one('hr.department', ondelete="cascade")
    leave_id = fields.Many2one('hr.leave', ondelete="cascade")
    log_book_id = fields.Many2one('common.log.book.ept', ondelete="cascade")
    message = fields.Text()
    model_id = fields.Many2one("ir.model", string="Model")
    res_id = fields.Integer("Record ID")
    mismatch_details = fields.Boolean(string='Mismatch Detail', help="Mismatch Detail of process order")
    file_name = fields.Char()
    log_line_type = fields.Selection(selection=[('success', 'Success'), ('fail', 'Fail')], default='fail')
    operation_type = fields.Selection([('import', 'Import')], string="Operation")
    module = fields.Selection([('hrms', 'HRMS Connector')])

    def create_common_log_line_ept(self, **kwargs):
        """
        It is use to create log lines.
        @param : **kwargs, Pass the argument like, self.env['common.log.lines'].create_common_log_line_ept(
        log_book_id=1, message=message, mismatch=True, log_line_type='fail', model_name = 'hr.employee')
        """
        values = {}
        for key, value in kwargs.items():
            if hasattr(self, key):
                values.update({key: value})
        if kwargs.get('model_name'):
            model = self._get_model_id(kwargs.get('model_name'))
            values.update({'model_id': model.id})
        return self.create(values)

    def _get_model_id(self, model_name):
        """
        It is use to get the model id
        @param :  model_name : Name of the model
        """
        ir_model_obj = self.env['ir.model']
        return ir_model_obj.sudo().search([('model', '=', model_name)])
