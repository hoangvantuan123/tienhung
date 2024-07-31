# -*- coding: utf-8 -*-

{
    'name': "User Log Details",
    'version': '17.0.1.0.0',
    'summary': """Login User Details & IP Address""",
    'description': """This module records login information of user""",
    'author': "tuanvhoang31@gmail.com",
    'company': "tuanvhoang31@gmail.com ",
    'maintainer': 'tuanvhoang31@gmail.com',
    'website': "tuanvhoang31@gmail.com",
    'category': 'Tools',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/login_user_views.xml'],
    'demo': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
