# -*- coding: utf-8 -*-

from odoo import _, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # hrm_api_key = fields.Char(string="HRM API Key")
    hrm_token = fields.Char(string="HRM API Token")
    hrm_base_url = fields.Char(string="HRM Base URL")
    import_job_status = fields.Selection([
        ('stopped', 'Stopped'),
        ('running', 'Running'),
    ], string="Import Job Status", default='stopped')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # hrm_api_key = fields.Char(string="HRM API Key", related="company_id.hrm_api_key", readonly=False,
    #                           help="Set API Key")
    hrm_token = fields.Char(string="HRM Token", related="company_id.hrm_token", readonly=False,
                            help="Set API Token")
    hrm_base_url = fields.Char(string="HRM Base URL", related="company_id.hrm_base_url", readonly=False,
                               help="Set Base URL")
    import_job_status = fields.Selection(related="company_id.import_job_status", readonly=False)
