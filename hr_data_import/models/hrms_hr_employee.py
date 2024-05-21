# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrmsHrEmployee(models.Model):
    _name = "hrms.hr.employee"
    _description = 'HR Employee HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one(
        'hr.data.dashboard', string="HRMS Instance", required=True)
    created_at = fields.Datetime()
    updated_at = fields.Datetime()
    active = fields.Boolean(default=True)
    hrms_external_id = fields.Char(string="HRMS Employee ID")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    # exported_in_hrms

    
    # def update_employees_in_hrms