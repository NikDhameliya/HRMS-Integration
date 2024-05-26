# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime



class HrmsHrLeave(models.Model):
    _name = "hrms.hr.leave"
    _description = 'HR Leave HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    email = fields.Char(string="Email")
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one('hr.data.dashboard', string="HRMS Instance", required=True)
    updated_at = fields.Datetime()
    hrms_external_id = fields.Char(string="HRMS Leave ID")
    leave_id = fields.Many2one('hr.leave', string="Leave", ondelete="cascade")
    end_test = fields.Date(string="End Test")
    fired_date = fields.Date(string="Fired Date")
    leave_detail_ids = fields.One2many('hr.leave.detail', 'leave_id', string="Business Trip")

    def hrms_create_leave(self, leave_data, skip_existing_leave=False):
        Leave = self.env['hr.leave']
        created_leave_ids = []

        def str_to_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else False

        for leave in leave_data:
            if skip_existing_leave:
                existing_leave = Leave.search([('hrms_external_id', '=', leave['id'])])
                if existing_leave:
                    continue
            
            leave_vals = {
                'name': leave['name'],
                'hrms_external_id': leave['id'],
                'end_test': str_to_date(leave.get('end_test')) if leave.get('end_test') else False,
                'fired_date': str_to_date(leave.get('fired_date')) if leave.get('fired_date') else False,
                'leave_detail_ids': []
            }
            
            for leave_type in ['business_trip', 'home_work', 'sick_leave', 'documented_sick_leave', 'vacation', 'unpaid_vacation', 'overtime', 'weekend_work', 'night_shift', 'day_transfer']:
                for detail in leave.get(leave_type, []):
                    detail_vals = {
                        'date': str_to_date(detail.get('date')) if detail.get('date') else False,
                        'is_full_day': detail.get('is_full_day', False),
                        'from_time': detail.get('from', False),
                        'to_time': detail.get('to', False),
                        'used_minutes': detail.get('used_minutes', 0),
                        'type': leave_type
                    }
                    leave_vals['leave_detail_ids'].append((0, 0, detail_vals))
            
            leave_record = Leave.create(leave_vals)
            
            hrms_leave = self.create({
                'name': leave['name'],
                'email': leave['email'],
                'company_id': self.env.company.id,
                'hrms_instance_id': self.env.context.get('hrms_instance_id'),
                'hrms_external_id': leave['id'],
                'leave_id': leave_record.id,
                'end_test': str_to_date(leave.get('end_test')) if leave.get('end_test') else False,
                'fired_date': str_to_date(leave.get('fired_date')) if leave.get('fired_date') else False,
                'leave_detail_ids': [(0, 0, detail) for detail in leave_vals['leave_detail_ids']]
            })
            created_leave_ids.append(hrms_leave.id)
        return created_leave_ids
