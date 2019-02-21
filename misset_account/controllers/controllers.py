# -*- coding: utf-8 -*-
from odoo import http

# class MissetAccount(http.Controller):
#     @http.route('/misset_account/misset_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/misset_account/misset_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('misset_account.listing', {
#             'root': '/misset_account/misset_account',
#             'objects': http.request.env['misset_account.misset_account'].search([]),
#         })

#     @http.route('/misset_account/misset_account/objects/<model("misset_account.misset_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('misset_account.object', {
#             'object': obj
#         })