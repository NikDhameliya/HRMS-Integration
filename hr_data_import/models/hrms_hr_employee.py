# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger("HRMS Operations")


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
    languages = fields.Char(string="Languages")
    language_ids = fields.Many2many('res.lang', string='Languages')
    team_ids = fields.Many2many('hr.department', string='Teams')
    career_ids = fields.One2many(
        'hrms.hr.career', 'hrms_employee_id', string='Career')
    contact_ids = fields.One2many(
        'hrms.hr.contact', 'hrms_employee_id', string='Contacts')
    awards = fields.Char(string="Awards")
    educations = fields.Char(string="Educations")

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

            employee_vals = {
                'name': employee.get('name'),
                'email': employee.get('email'),
                'phone': employee.get('phone'),
                'skype': employee.get('skype'),
                'linked_in': employee.get('linked_in'),
                'telegram': employee.get('telegram'),
                'birth_date': employee.get('birth_date'),
                'end_test': employee.get('end_test'),
                'fired_date': employee.get('fired_date'),
                'start_date': employee.get('start_date'),
                'gender': 'male' if employee.get('gender') == 1 else 'female',
                'additional_email': employee.get('additional_email'),
                'additional_phone': employee.get('additional_phone'),
                'relocate': employee.get('relocate'),
                'duties': employee.get('duties'),
                'description': employee.get('description'),
                'additional_info': employee.get('additional_info'),
                'residence': employee.get('residence'),
                'residence_comment': employee.get('residence_comment'),
                'country': country_id.id if country_id else False,
                'city': employee.get('city'),
                'hrms_external_id': employee.get('id'),
                'company_id': self.env.company.id,
                'team_ids': [(6, 0, team_ids)],
                'job_id': job_id.id if job_id else False,
                'skill_ids': [(6, 0, skill_ids)],
                'language_ids': [(6, 0, language_ids)],
                'awards': awards,
                'educations': educations,
            }

            if employee_rec:
                employee_rec.write(employee_vals)
                hr_employee = employee_rec.employee_id
            else:
                hr_employee = hr_employee_obj.create({
                    'name': employee.get('name'),
                    'work_email': employee.get('email'),
                    'work_phone': employee.get('phone'),
                    'job_id': job_id.id if job_id else False,
                    'department_id': team_ids[0] if team_ids else False,
                    'country_id': country_id.id if country_id else False,
                    'address_home_id': employee.get('residence'),
                    'city': employee.get('city'),
                    'birthday': employee.get('birth_date'),
                    'start_date': employee.get('start_date'),
                    'gender': 'male' if employee.get('gender') == 1 else 'female',
                    'hrms_external_id': employee.get('id'),
                    'grade': employee.get('grade', ""),
                    'residence_comment': employee.get('residence_comment'),
                    'skype': employee.get('skype'),
                    'linked_in': employee.get('linked_in'),
                    'telegram': employee.get('telegram'),
                    'additional_email': employee.get('additional_email'),
                    'additional_phone': employee.get('additional_phone'),
                    'end_test': employee.get('end_test'),
                    'fired_date': employee.get('fired_date'),
                    'relocate': employee.get('relocate'),
                    'duties': employee.get('duties'),
                    'description': employee.get('description'),
                    'additional_info': employee.get('additional_info'),
                    'awards': awards,
                    'educations': educations
                })

                employee_vals['employee_id'] = hr_employee.id
                employee_rec = employee_obj.create(employee_vals)

            employee_ids.append(employee_rec.id)

            for contact in employee.get('contacts', []):
                contact_vals = {
                    'type_id': contact.get('type_id'),
                    'type_name': contact.get('type_name'),
                    'value': contact.get('value'),
                    'hrms_employee_id': employee_rec.id
                }
                contact_rec = employee_rec.contact_ids.search([('type_id', '=', contact.get(
                    'type_id')), ('hrms_employee_id', '=', employee_rec.id)], limit=1)
                if contact_rec:
                    contact_rec.write(contact_vals)
                else:
                    employee_rec.contact_ids.create(contact_vals)

            for career in employee.get('career', []):
                career_vals = {
                    'start_date': career.get('start_date'),
                    'end_date': career.get('end_date'),
                    'position': career.get('position'),
                    'team': career.get('team'),
                    'comment': career.get('comment'),
                    'hrms_employee_id': employee_rec.id
                }
                career_rec = employee_rec.career_ids.search([('start_date', '=', career.get('start_date')), (
                    'end_date', '=', career.get('end_date')), ('hrms_employee_id', '=', employee_rec.id)], limit=1)
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
