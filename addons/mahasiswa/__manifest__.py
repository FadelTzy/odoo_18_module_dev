{
    'name':'Mahasiswa Management',
    'version':'1.0',
    'category':'Education',
    'summary':'Module for managing mahasiswa (students) information',
    'description':"This module provides functionalities to manage mahasiswa (students) information including personal details, courses, and grades",
    'author':'Fadel',
    'depends':['base'],
    'application':True,
    'installable':True,
    'data':[
        'views/mahasiswa_data_views.xml',
        'views/mahasiswa_menus.xml',
        'security/ir.model.access.csv',
    ],
}