# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from datetime import datetime
import logging

_logger = logging.getLogger("HRMS Leave Operations")


class HrmsHrLeave(models.Model):
    _name = "hrms.hr.leave"
    _description = 'HR Leave HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    employee_id = fields.Many2one(
        'hr.employee', string="Employee", required=True)
    email = fields.Char(string="Email")
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one(
        'hr.data.dashboard', string="HRMS Instance", required=True)
    updated_at = fields.Datetime()
    hrms_external_id = fields.Char(string="HRMS Leave ID")
    leave_id = fields.Many2one('hr.leave', string="Leave", ondelete="cascade")
    end_test = fields.Date(string="End Test")
    fired_date = fields.Date(string="Fired Date")
    leave_detail_ids = fields.One2many(
        'hr.leave.detail', 'hrms_leave_id', string="Business Trip")

    def hrms_create_leave(self, leave_data, skip_existing_leave=False):
        Leave = self.env['hr.leave']
        created_leave_ids = []

        def str_to_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else False

        def time_to_hour(time_str):
            if not time_str:
                return False
            hours, minutes = map(int, time_str.split(':'))
            return hours if minutes == 0 else hours + minutes / 60.0

        for leave in leave_data:
            try:
                if skip_existing_leave:
                    existing_leave = Leave.search([('hrms_external_id', '=', leave['id'])])
                    if existing_leave:
                        continue
                employee_id = self.env['hr.employee'].search(
                    [('hrms_external_id', '=', leave['id'])], limit=1)
                if not employee_id:
                    employee_id = self.env['hr.employee'].create({
                        'name': leave['name'], 
                        'hrms_external_id': leave['id'], 
                        'work_email': leave['email'],
                        'employee_type': 'employee',
                        'company_id': self.env.company.id
                    })

                for leave_type in ['business_trip', 'home_work', 'sick_leave', 'documented_sick_leave', 'vacation', 'unpaid_vacation', 'overtime', 'weekend_work', 'night_shift', 'day_transfer']:
                    for detail in leave.get(leave_type, []):
                        leave_vals = {
                            'name': leave['name'],
                            'end_test': str_to_date(leave.get('end_test')) if leave.get('end_test') else False,
                            'fired_date': str_to_date(leave.get('fired_date')) if leave.get('fired_date') else False,
                            'holiday_type': 'employee',
                            'employee_id': employee_id.id if employee_id else False,
                            'request_date_from': str_to_date(detail.get('date')) if detail.get('date') else False,
                            'leave_detail_ids': []
                        }
                        
                        # Initialize from_time and to_time
                        from_time = None
                        to_time = None
                        if detail.get('is_full_day') == True:
                            leave_vals['leave_type_request_unit'] = 'day'
                            leave_vals['request_date_to'] = str_to_date(detail.get('date')) if detail.get('date') else False
                        else:
                            from_time = time_to_hour(detail.get('from', False))
                            to_time = time_to_hour(detail.get('to', False))
                            print("CALLLLLLLLLLLLLLLL", from_time, to_time)
                            leave_vals['leave_type_request_unit'] = 'hour'
                            leave_vals['request_unit_hours'] = True
                            leave_vals['request_hour_from'] = str(from_time) if from_time else False
                            leave_vals['request_hour_to'] = str(to_time) if to_time else False
                            print("LEAVE VALSSSSSSS", leave_vals)

                        detail_vals = {
                            'date': str_to_date(detail.get('date')) if detail.get('date') else False,
                            'is_full_day': detail.get('is_full_day', False),
                            'from_time': str(from_time) if from_time else False,
                            'to_time': str(to_time) if to_time else False,
                            'used_minutes': detail.get('used_minutes', 0),
                            'type': leave_type
                        }
                        holiday_status_id = self.env['hr.leave.type'].search([('name', '=', leave_type)], limit=1)
                        if not holiday_status_id:
                            holiday_status_id = self.env['hr.leave.type'].create({
                                'name': leave_type, 'employee_requests': 'no', 'request_unit': 'day', 'requires_allocation': 'yes'
                            })
                        leave_vals.update({
                            'holiday_status_id': holiday_status_id.id
                        })
                        leave_vals['leave_detail_ids'].append((0, 0, detail_vals))
                        leave_record = Leave.create(leave_vals)
                        hrms_leave = self.create({
                            'name': leave['name'],
                            'employee_id': employee_id.id if employee_id else False,
                            'email': leave['email'],
                            'company_id': self.env.company.id,
                            'hrms_instance_id': self.env.context.get('hrms_instance_id'),
                            'hrms_external_id': leave['id'],
                            'end_test': str_to_date(leave.get('end_test')) if leave.get('end_test') else False,
                            'fired_date': str_to_date(leave.get('fired_date')) if leave.get('fired_date') else False,
                            'leave_detail_ids': [detail for detail in leave_vals['leave_detail_ids']]
                        })
                        created_leave_ids.append(hrms_leave.id)
            except Exception as e:
                _logger.error(f"Error processing leave for {leave['name']}: {e}")
                continue
        return created_leave_ids

