# -*- coding: utf-8 -*-
from odoo import http

class HRDataImportController(http.Controller):

    @http.route('/hr_data_import/start', type='json', auth='user')
    def start_import(self):
        env = http.request.env
        env['hr.data.import'].import_data()
        return {'status': 'success'}
