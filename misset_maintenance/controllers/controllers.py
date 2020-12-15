# -*- coding: utf-8 -*-
from odoo import http

# class MissetMaintenance(http.Controller):
#     @http.route('/misset_maintenance/misset_maintenance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/misset_maintenance/misset_maintenance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('misset_maintenance.listing', {
#             'root': '/misset_maintenance/misset_maintenance',
#             'objects': http.request.env['misset_maintenance.misset_maintenance'].search([]),
#         })

#     @http.route('/misset_maintenance/misset_maintenance/objects/<model("misset_maintenance.misset_maintenance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('misset_maintenance.object', {
#             'object': obj
#         })