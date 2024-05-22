# -*- coding: utf-8 -*-

from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    api_id = fields.Char(string="API ID")
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
    career_ids = fields.One2many('hr.employee.career', 'employee_id', string='Career')
    contact_ids = fields.One2many('hr.employee.contact', 'employee_id', string='Contacts')
    awards = fields.Char(string="Awards")
    educations = fields.Char(string="Educations")
