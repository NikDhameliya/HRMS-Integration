# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrmsHrLeave(models.Model):
    _name = "hrms.hr.leave"
    _description = 'HR Leave HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    email = fields.Char(string="Email")
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one('hr.data.dashboard', string="HRMS Instance", required=True)
    created_at = fields.Datetime()
    updated_at = fields.Datetime()
    hrms_external_id = fields.Char(string="HRMS Leave ID")
    leave_id = fields.Many2one('hr.leave', string="Leave", ondelete="cascade")
    exported_in_hrms = fields.Boolean(default=False)
    business_trip = fields.One2many('hr.leave.detail', 'leave_id', string="Business Trip")
    home_work = fields.One2many('hr.leave.detail', 'leave_id', string="Home Work")
    sick_leave = fields.One2many('hr.leave.detail', 'leave_id', string="Sick Leave")
    documented_sick_leave = fields.One2many('hr.leave.detail', 'leave_id', string="Documented Sick Leave")
    vacation = fields.One2many('hr.leave.detail', 'leave_id', string="Vacation")
    unpaid_vacation = fields.One2many('hr.leave.detail', 'leave_id', string="Unpaid Vacation")
    overtime = fields.One2many('hr.leave.detail', 'leave_id', string="Overtime")
    weekend_work = fields.One2many('hr.leave.detail', 'leave_id', string="Weekend Work")
    night_shift = fields.One2many('hr.leave.detail', 'leave_id', string="Night Shift")
    day_transfer = fields.One2many('hr.leave.detail', 'leave_id', string="Day Transfer")
    end_test = fields.Date(string="End Test")
    fired_date = fields.Date(string="Fired Date")
