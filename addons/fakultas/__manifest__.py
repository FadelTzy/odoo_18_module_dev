{
    'name': 'Fakultas Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Module for managing fakultas (faculties) information',
    'description': "This module provides functionalities to manage fakultas (faculties) information including details and departments",
    'author': 'Fadel',
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'views/fakultas_data_views.xml',
        'views/fakultas_menus.xml',
        'security/ir.model.access.csv',
    ],
}