{
    'name': 'HRM Data Migration',
    'version': '17.0.0.1',
    'category': 'Human Resources',
    'summary': 'Module to import HR data from an external HRM system via API',
    'description': 'Custom module to import HR data from an external HRM system.',
    'author': 'Nikunj Dhameliya',
    'depends': ['base', 'hr', 'hr_holidays'],
    'data': [
        'data/data.xml',
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'views/hrms_hr_employee_view.xml',
        'views/hrms_hr_department_view.xml',
        'views/hrms_hr_leave_view.xml',
        'views/hr_data_dashboard_views.xml',
        'views/menu_items.xml',
        'views/res_config_settings_views.xml',
        'wizard/process_import_export_view.xml',
        'wizard/queue_process_wizard_view.xml',
        'views/employee_data_queue_view.xml',
        'views/department_data_queue_view.xml',
        'views/leave_data_queue_view.xml',
        'views/common_log_book_view.xml'
    ],
    'cloc_exclude': ['**/*.xml', ],
    'assets': {
        'web.assets_backend': [
            '/hr_data_import/static/src/scss/graph_widget_ept.scss',
            '/hr_data_import/static/src/scss/on_boarding_wizards.css',
            '/hr_data_import/static/src/scss/queue_line_dashboard.scss',
            '/hr_data_import/static/src/js/graph_widget_ept.js',
            '/hr_data_import/static/src/js/queue_line_dashboard.js',
            '/hr_data_import/static/src/xml/dashboard_widget.xml',
            '/hr_data_import/static/src/xml/queue_line_dashboard.xml'
        ],
        'web.assets_backend': [
            'hr_data_import/static/src/css/hrms_base.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3'
}
