# -*- coding: utf-8 -*-

from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    hrms_external_id = fields.Char(string='HRMS External ID')
    grade = fields.Char(string="Grade")
    residence_comment = fields.Text(string="Residence Comment")
    skype = fields.Char(string="Skype")
    linked_in = fields.Char(string="LinkedIn")
    telegram = fields.Char(string="Telegram")
    additional_email = fields.Char(string='Additional Email')
    additional_phone = fields.Char(string='Additional Phone')
    end_test = fields.Date(string="End Test")
    fired_date = fields.Date(string="Fired Date")
    start_date = fields.Date(string="Start Date")
    relocate = fields.Boolean(string="Relocate")
    duties = fields.Text(string="Duties")
    description = fields.Text(string="Description")
    additional_info = fields.Text(string="Additional Info.")
    skill_ids = fields.Many2many('hr.skill', string='Skills')
    language_ids = fields.Many2many('res.lang', string='Languages')
    team_ids = fields.Many2many('hr.department', string='Teams')
    career_ids = fields.One2many('hrms.hr.career', 'employee_id', string='Career')
    contact_ids = fields.One2many('hrms.hr.contact', 'employee_id', string='Contacts')
    awards = fields.Char(string="Awards")
    educations = fields.Char(string="Educations")

    _sql_constraints = [
        ('hrms_external_id_unique', 'unique(hrms_external_id)',
         'The hrms_external_id already exists!'),
    ]