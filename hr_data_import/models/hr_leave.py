# -*- coding: utf-8 -*-

from odoo import models, fields


class Leave(models.Model):
    _inherit = 'hr.leave'

    hrms_external_id = fields.Char(string='HRMS External ID')
    leave_detail_ids = fields.One2many('hr.leave.detail', 'leave_id', string="Business Trip")
    end_test = fields.Date(string="End Test")
    fired_date = fields.Date(string="Fired Date")

    _sql_constraints = [
        ('hrms_external_id_unique', 'unique(hrms_external_id)',
         'The hrms_external_id already exists!'),
    ]


class HRLeaveDetail(models.Model):
    _name = 'hr.leave.detail'
    _description = 'HR Leave Detail'

    leave_id = fields.Many2one('hr.leave', string="Leave")
    date = fields.Date(string="Date")
    is_full_day = fields.Boolean(string="Is Full Day")
    from_time = fields.Float(string="From")
    to_time = fields.Float(string="To")
    used_minutes = fields.Integer(string="Used Minutes")
    type = fields.Selection([
        ('business_trip', 'Business Trip'),
        ('home_work', 'Home Work'),
        ('sick_leave', 'Sick Leave'),
        ('documented_sick_leave', 'Documented Sick Leave'),
        ('vacation', 'Vacation'),
        ('unpaid_vacation', 'Unpaid Vacation'),
        ('overtime', 'Overtime'),
        ('weekend_work', 'Weekend Work'),
        ('night_shift', 'Night Shift'),
        ('day_transfer', 'Day Transfer')
    ], string="Type")
