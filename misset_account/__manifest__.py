# -*- coding: utf-8 -*-
{
    'name': "misset_account",

    'summary': """
       Enchances the Accounting Module according to Misset""",

    'description': """
        Enchances the Accounting Module according to Misset
    """,

    'author'  : 'Magnus - Willem Hulshof',
    'website' : 'http://www.magnus.nl',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['nsm_account','nsm_sale_advertising_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_invoice.xml',
        'report/report_saleorder_document_nsm.xml',
        'report/report_saleorderlines_document_nsm.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}