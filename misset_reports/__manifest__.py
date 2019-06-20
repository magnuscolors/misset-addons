# -*- coding: utf-8 -*-
{
    'name': "misset_reports",

    'summary': """
        Enchances the Misset repots""",

    'description': """
        Enchances the Misset repots
    """,

    'author': "Magnus - Willem Hulshof",
    'website': "http://www.magnus.nl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Reports/Qweb',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['nsm_account', 'account_credit_control', 'nsm_sale_advertising_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_invoice.xml',
        'report/report_credit_control_summary.xml',
        'views/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}