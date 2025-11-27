{
    'name': 'default_analytic',
    'version': '18.0.1.0.1',
    'summary': 'Set default analytic accounts for users and companies',
    'author': 'Esteban Viniegra | Pridecta',
    'website': 'https://pridecta.es',
    'license': 'LGPL-3',
    'category': 'Custom',
    'depends': ['base','account'],
    'data': [
            'views/res_users_views.xml',
            'views/res_company_views.xml',
            'views/account_move_views.xml',
        ],
    "images": [
        "static/description/cover.png",
    ],
    'application': True,
    'installable': True,
    'icon': '/default_analytic/static/description/icon.png',
}
