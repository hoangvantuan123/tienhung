{
    'name': "User Activity Tracker",

    'summary': """Check Login/Logout""",

    'description': """
      check login/logout status and total login time.
    """,

    'author': "tuanvhoang31@gmail.com",
    
    'company': 'tuanvhoang31@gmail.com',
    
    'maintainer': 'tuanvhoang31@gmail.com',
    
    'website': "https://github.com/hoangvantuan123",
    'category': 'Administration',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/setting.xml',
    ],
    'license': 'LGPL-3',

    'installable': True,

    'auto_install': False,

    'application': False
}