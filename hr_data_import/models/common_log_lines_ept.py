# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class CommonLogLineEpt(models.Model):
    _name = "common.log.lines"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Common log line"

    log_book_id = fields.Many2one('common.log.book', ondelete="cascade")
    message = fields.Text()
    model_id = fields.Many2one("ir.model", string="Model")
    res_id = fields.Integer("Record ID")
    mismatch_details = fields.Boolean(string='Mismatch Detail', help="Mismatch Detail of process record")
    log_line_type = fields.Selection(selection=[('success', 'Success'), ('error', 'Error'), ('info', 'Info'), ('warning', 'Warning')], default='info')

    def create_common_log_line_ept(self, **kwargs):
        """
        It is use to create log lines.
        @param : **kwargs, Pass the argument like, self.env['common.log.lines'].create_common_log_line_ept(
        log_book_id=1, message=message, mismatch=True, log_line_type='info', model_name = 'hr.employee')
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
    