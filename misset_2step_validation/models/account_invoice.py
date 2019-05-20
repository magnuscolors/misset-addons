# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    account_analytic_id = fields.Many2one('account.analytic.account',
        string='Analytic Account')
    
#     @api.onchange('account_analytic_id')
#     def onchange_domain_analytic(self):
#         res = {}
#         team_lst = []
#         invoice_id = None
#         sales_team = self.env['sales.team']
#         if self.account_analytic_id:
#             saless_team_ids = sales_team.search([('analytic_account_id','=',self.account_analytic_id.id)])
#             for team in saless_team_ids:
#                 team_lst.append(team.sales_team_id.id)
#             if team_lst:
#                 res['domain'] = {'team_id': [('id', 'in', team_lst)]}
#         print ("res....",res)
#         return res
    
    
class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.onchange('account_analytic_id')
    def onchange_use_insurance(self):
        result = {}
#         self.invoice_id.account_analytic_id = self.account_analytic_id.id
#         print ("AAAA",self.invoice_id.account_analytic_id.name)
#         print ("BBB",self.account_analytic_id.name)
#         result['value']={'invoice_id.account_analytic_id':self.account_analytic_id.id}
        self.invoice_id.write({'account_analytic_id':self.account_analytic_id.id})
        return result
#         team_lst = []
#         invoice_id = None
#         sales_team = self.env['sales.team']
#         if self.account_analytic_id:
#             saless_team_ids = sales_team.search([('analytic_account_id','=',self.account_analytic_id.id)])
#             for team in saless_team_ids:
#                 team_lst.append(team.sales_team_id.id)
#             invoice_id = self.invoice_id
#             if team_lst:
#                 res['values'] = {'team_id': [('id', 'in', team_lst)]}
#         print ("res....",res)
#         return res
    