# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class CommonLogBookEpt(models.Model):
    _name = "common.log.book"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = 'id desc'
    _description = "Common log book Ept"

    name = fields.Char(readonly=True)
    log_lines = fields.One2many('common.log.lines', 'log_book_id')
    message = fields.Text()
    model_id = fields.Many2one("ir.model", help="Model Id", string="Model")
    res_id = fields.Integer(string="Record ID", help="Process record id")

    @api.model_create_multi
    def create(self, vals_list):
        """ To generate a sequence for a common logbook.
            @param : vals : Dictionary of common log book create.
        """
        for vals in vals_list:
            seq = self.env['ir.sequence'].next_by_code('common.log.book') or '/'
            vals['name'] = seq
        return super(CommonLogBookEpt, self).create(vals_list)

    def create_common_log_book_ept(self, **kwargs):
        """
        This method is use to create a log book.
        @param : **kwargs, Pass the argument like,
        log_book = self.env['common.log.book'].create_common_log_book_ept (module='hr_data_import',
        model_name='hr.employee',type='import')
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
        model_id = self.env['ir.model']
        return model_id.sudo().search([('model', '=', model_name)])
