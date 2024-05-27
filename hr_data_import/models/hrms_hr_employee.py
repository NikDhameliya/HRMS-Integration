# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
from datetime import datetime


_logger = logging.getLogger("HRMS Employee Operations")


class HrmsHrEmployee(models.Model):
    _name = "hrms.hr.employee"
    _description = 'HR Employee HRMS'

    name = fields.Char(string="Name", index=True, required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.company)
    hrms_instance_id = fields.Many2one(
        'hr.data.dashboard', string="HRMS Instance")
    active = fields.Boolean(default=True)
    hrms_external_id = fields.Char(string="HRMS Employee ID")
    employee_id = fields.Many2one(
        'hr.employee', string="Employee", ondelete="cascade")
    email = fields.Char(string='Email')
    job_id = fields.Many2one('hr.job', string='Position')
    residence = fields.Char(string='Residence')
    residence_comment = fields.Text(string='Residence Comment')
    country = fields.Many2one('res.country', string='Country')
    city = fields.Char(string='City')
    birth_date = fields.Date(string='Birth Date')
    linked_in = fields.Char(string='LinkedIn')
    skype = fields.Char(string='Skype')
    phone = fields.Char(string='Phone')
    telegram = fields.Char(string='Telegram')
    additional_email = fields.Char(string='Additional Email')
    additional_phone = fields.Char(string='Additional Phone')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    end_test = fields.Date(string="End Test")
    fired_date = fields.Date(string="Fired Date")
    start_date = fields.Date(string="Start Date")
    relocate = fields.Boolean(string="Relocate")
    duties = fields.Text(string="Duties")
    description = fields.Text(string="Description")
    additional_info = fields.Text(string="Additional Info.")
    skills = fields.Char(string="Skills")
    skill_ids = fields.Many2many('hr.skill', string='Skills')
    languages = fields.Char(string="Received Languages")
    language_ids = fields.Many2many('res.lang', string='Languages')
    team_ids = fields.Many2many('hr.department', string='Teams')
    career_ids = fields.One2many(
        'hrms.hr.career', 'hrms_employee_id', string='Career')
    contact_ids = fields.One2many(
        'hrms.hr.contact', 'hrms_employee_id', string='Contacts')
    awards = fields.Char(string="Awards")
    educations = fields.Char(string="Educations")
    grade = fields.Char(string="Grade")

    def hrms_create_employee(self, employee_data, skip_existing_employee):
        employee_obj = self.env["hrms.hr.employee"]
        hr_employee_obj = self.env['hr.employee']
        res_country_obj = self.env['res.country']
        hr_department_obj = self.env['hr.department']
        hr_job_obj = self.env['hr.job']

        employee_ids = []

        for employee in employee_data:
            employee_rec = employee_obj.search(
                [('hrms_external_id', '=', employee.get('id'))], limit=1)
            if skip_existing_employee and employee_rec:
                continue
            country_id = res_country_obj.search(
                [('name', '=', employee.get('country'))], limit=1)
            team_ids = []
            for team in employee.get('team', []):
                team_rec = hr_department_obj.search(
                    [('name', '=', team.get('name'))], limit=1)
                if not team_rec:
                    team_rec = hr_department_obj.create(
                        {'name': team.get('name')})
                team_ids.append(team_rec.id)
            job_id = hr_job_obj.search(
                [('name', '=', employee.get('position'))], limit=1)
            if not job_id:
                job_id = hr_job_obj.create({'name': employee.get('position')})
                
            # Handling skills, languages, awards, educations
            skill_ids = []
            for skill in employee.get('skills', []):
                skill_rec = self.env['hr.skill'].search([('name', '=', skill)], limit=1)
                if not skill_rec:
                    skill_rec = self.env['hr.skill'].create({'name': skill})
                skill_ids.append(skill_rec.id)

            language_ids = []
            #TODO check language search
            for language in employee.get('languages', []):
                language_rec = self.env['res.lang'].search([('name', 'like', language)], limit=1)
                if language_rec:
                    language_ids.append(language_rec.id)
                else:
                     _logger.info("Language %s Not found" % (language))

            awards = employee.get('awards', "")
            educations = employee.get('educations', "")

            #TODO Verify date format in Odoo DB
            def str_to_date(date_str):
                return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else False

            employee_vals = {
                'name': employee.get('name'),
                'employee_type': 'employee',
                'email': employee.get('email') or False,
                'phone': employee.get('phone') or False,
                'skype': employee.get('skype') or False,
                'grade': employee.get('grade', "") or False,
                'linked_in': employee.get('linked_in') or False,
                'telegram': employee.get('telegram') or False,
                'birth_date': str_to_date(employee.get('birth_date')) if employee.get('birth_date') else False,
                'end_test': employee.get('end_test') or False,
                'fired_date': str_to_date(employee.get('fired_date')) if employee.get('fired_date') else False,
                'start_date': str_to_date(employee.get('start_date')) if employee.get('start_date') else False,
                'gender': 'male' if employee.get('gender') == 1 else 'female',
                'additional_email': employee.get('additional_email') or False,
                'additional_phone': employee.get('additional_phone') or False,
                'relocate': employee.get('relocate') or False,
                'duties': employee.get('duties') or False,
                'description': employee.get('description') or False,
                'additional_info': employee.get('additional_info') or False,
                'residence': employee.get('residence') or False,
                'residence_comment': employee.get('residence_comment') or False,
                'country': country_id.id if country_id else False,
                'city': employee.get('city') or False,
                'hrms_external_id': employee.get('id') or False,
                'company_id': self.env.company.id,
                'team_ids': [(6, 0, team_ids)],
                'job_id': job_id.id if job_id else False,
                'skill_ids': [(6, 0, skill_ids)],
                'language_ids': [(6, 0, language_ids)],
                'awards': awards or False,
                'educations': educations or False,
                'hrms_instance_id': self.env.context.get('hrms_instance_id'),
            }

            if employee_rec:
                employee_rec.write(employee_vals)
                hr_employee = employee_rec.employee_id
            else:
                hr_employee = hr_employee_obj.create({
                    'name': employee.get('name'),
                    'work_email': employee.get('email') or False,
                    'work_phone': employee.get('phone') or False,
                    'job_id': job_id.id if job_id else False,
                    'department_id': team_ids[0] if team_ids else False,
                    'private_country_id': country_id.id if country_id else False,
                    'private_street': employee.get('residence') or False,
                    'private_city': employee.get('city') or False,
                    'birthday': str_to_date(employee.get('birthday')) if employee.get('birthday') else False,
                    'start_date': str_to_date(employee.get('start_date')) if employee.get('start_date') else False,
                    'gender': 'male' if employee.get('gender') == 1 else 'female',
                    'hrms_external_id': employee.get('id') or False,
                    'grade': employee.get('grade', "") or False,
                    'residence_comment': employee.get('residence_comment') or False,
                    'skype': employee.get('skype') or False,
                    'linked_in': employee.get('linked_in') or False,
                    'telegram': employee.get('telegram') or False,
                    'additional_email': employee.get('additional_email') or False,
                    'additional_phone': employee.get('additional_phone') or False,
                    'end_test': employee.get('end_test') or False,
                    'fired_date': str_to_date(employee.get('fired_date')) if employee.get('fired_date') else False,
                    'relocate': employee.get('relocate') or False,
                    'duties': employee.get('duties') or False,
                    'description': employee.get('description') or False,
                    'additional_info': employee.get('additional_info') or False,
                    'awards': awards or False,
                    'educations': educations or False
                })

                employee_vals['employee_id'] = hr_employee.id
                employee_rec = employee_obj.create(employee_vals)

            employee_ids.append(employee_rec.id)

            for contact in employee.get('contacts', []):
                contact_vals = {
                    'type_id': contact.get('type_id') or False,
                    'type_name': contact.get('type_name') or False,
                    'value': contact.get('value') or False,
                    'hrms_employee_id': employee_rec.id
                }
                search_domain = [('hrms_employee_id', '=', employee_rec.id)]
                if contact.get('type_id'):
                    search_domain.append(('type_id', '=', contact.get('type_id')))
                if contact.get('type_name'):
                    search_domain.append(('type_name', '=', contact.get('type_name')))

                contact_rec = employee_rec.contact_ids.search(search_domain, limit=1)
                if contact_rec:
                    contact_rec.write(contact_vals)
                else:
                    employee_rec.contact_ids.create(contact_vals)

            for career in employee.get('career', []):
                start_date = str_to_date(career.get('start_date'))
                end_date = str_to_date(career.get('end_date'))
                career_vals = {
                    'start_date': str_to_date(career.get('start_date')) if career.get('start_date') else False,
                    'end_date': str_to_date(career.get('end_date')) if career.get('end_date') else False,
                    'position': career.get('position') or False,
                    'team': career.get('team') or False,
                    'comment': career.get('comment') or False,
                    'hrms_employee_id': employee_rec.id
                }
                search_domain = [('hrms_employee_id', '=', employee_rec.id)]
                if start_date:
                    search_domain.append(('start_date', '=', start_date))
                if end_date:
                    search_domain.append(('end_date', '=', end_date))

                career_rec = employee_rec.career_ids.search(search_domain, limit=1)
                if career_rec:
                    career_rec.write(career_vals)
                else:
                    employee_rec.career_ids.create(career_vals)
        return employee_ids


class HRCareer(models.Model):
    _name = 'hrms.hr.career'
    _description = 'HR Career'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    test_period_start_date = fields.Date(string="Test Period Start Date")
    test_period_end_date = fields.Date(string="Test Period End Date")
    company_name = fields.Char(string="Company Name")
    department = fields.Char(string="Department")
    position = fields.Char(string="Position")
    grade = fields.Char(string="Grade")
    place = fields.Char(string="Place")
    team = fields.Char(string="Team")
    comment = fields.Text(string="Comment")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    hrms_employee_id = fields.Many2one(
        'hrms.hr.employee', string="HRMS Employee")


class HRContact(models.Model):
    _name = 'hrms.hr.contact'
    _description = 'HR Contact'

    type_id = fields.Integer(string="Type ID")
    type_name = fields.Char(string="Type Name")
    value = fields.Char(string="Value")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    hrms_employee_id = fields.Many2one(
        'hrms.hr.employee', string="HRMS Employee")
