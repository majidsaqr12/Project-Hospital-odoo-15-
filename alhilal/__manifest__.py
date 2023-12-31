# -*- coding: utf-8 -*-
{
    'name': "AL HILAL",
    'version': '1.0.0',
    'author': 'Majid Saqr',
    'category': 'Alhilal hospital Management',
    'summary': 'Alhilal Hospital Management',
    'description': 'Alhilal Hospital Management',
    'sequence': '-200',
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/doctor_view.xml',
        'views/nurse_view.xml',
        'views/patient_view.xml',
        'views/salary_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'
}