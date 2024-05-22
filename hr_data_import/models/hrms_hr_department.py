# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrmsHrDepartment(models.Model):
    _name = "hrms.hr.department"
    _description = 'HR Department HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one('hr.data.dashboard', string="HRMS Instance", required=True)
    created_at = fields.Datetime()
    updated_at = fields.Datetime()
    hrms_external_id = fields.Char(string="HRMS Department ID")
    department_id = fields.Many2one('hr.department', string="Department", ondelete="cascade")
    exported_in_hrms = fields.Boolean(default=False)
