# -*- coding: utf-8 -*-

from odoo import models, fields


class Department(models.Model):
    _inherit = 'hr.department'

    _sql_constraints = [
        ('hrms_external_id_unique', 'unique (hrms_external_id)',
         'The hrms_external_id already exists!'),
    ]

    hrms_external_id = fields.Char(string='HRMS External ID', unique=True)


class Employee(models.Model):
    _inherit = 'hr.employee'

    _sql_constraints = [
        ('hrms_external_id_unique', 'unique (hrms_external_id)',
         'The hrms_external_id already exists!'),
    ]

    hrms_external_id = fields.Char(string='HRMS External ID', unique=True)


class Leave(models.Model):
    _inherit = 'hr.leave'

    _sql_constraints = [
        ('hrms_external_id_unique', 'unique (hrms_external_id)',
         'The hrms_external_id already exists!'),
    ]
    hrms_external_id = fields.Char(string='HRMS External ID', unique=True)
