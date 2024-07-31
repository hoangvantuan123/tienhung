# -*- coding: utf-8 -*-
{
    'name': "Plan Management",

    'summary': "Module to manage plans",

    'description': """
A module to manage plans with specific fields and statuses.
    """,

    'author': "tuanvhoang31@gmail.com",
    'website': "",
    'category': 'Management',
    'version': '0.1',
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        #'security/plan_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/plan_menu.xml',
        'views/plan_view.xml',
        'views/stage_views.xml',
        'views/pass_cutting.xml',
        'views/work_process.xml',
        'views/producing_warehouse_view.xml',
        'views/product_style.xml',
        'views/target_views.xml',
        'views/payroll_view.xml',
        'views/dashboard_performance_views.xml',
        'views/performance_data_template.xml',
        'views/time_keeping.xml',
        'views/employee_views.xml',
        'views/stage_team_view.xml',
        'views/assign_more_work_views.xml',
        'views/productivity_reports_views.xml',
        'views/home.xml',
        'views/report_warehouse.xml',
    ],
    'license': 'AGPL-3',

    'assets': {
        'web.assets_backend': [
            'x_plan/static/src/components/**/*.js',
            'x_plan/static/src/components/**/*.xml',
            'x_plan/static/src/components/**/*.scss',
            'x_plan/static/src/css/warehouse.css',
        ],
    },

}
