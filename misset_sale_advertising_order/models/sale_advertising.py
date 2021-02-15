# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2016 Magnus (<http://www.magnus.nl>). All Rights Reserved
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
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class sale_advertising_issue(models.Model):
    _inherit = "sale.advertising.issue"
    _description="Sale Advertising Issue"


    dtp_deadline = fields.Datetime("Closing time for DTP")

    # same code available in nsm_sale_advertising_order
    # @api.multi
    # def write(self, vals):
    #     result = super(sale_advertising_issue, self).write(vals)
    #     issue_date = vals.get('issue_date', False)
    #     if issue_date:
    #         issue_date = str(issue_date)
    #         op, ids = ('IN', tuple(self.ids)) if len(self.ids) > 1 else ('=', self.id)
    #         query = ("""
    #                 UPDATE sale_order_line
    #                 SET from_date = {0},
    #                     to_date = {0}
    #                 WHERE adv_issue {1} {2}
    #                 """.format(
    #                 "'%s'" % issue_date,
    #                 op,
    #                 ids
    #             ))
    #         self.env.cr.execute(query)
    #     return result

class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    #Every sale needs approval, if ver_tr_exc = True, verifcation done by manager first else only Traffic user needs to approve.
    @api.multi
    def action_submit(self):
        res = super(SaleOrder, self).action_submit()
        orders = self.filtered(lambda s: s.advertising and s.state in ['submitted'] and not s.ver_tr_exc)
        for o in orders:
            o.message_post(body=_("This quotation has been directly submitted for Traffic Approval, as Manager Approval is not required."))
            o.action_approve1()
        return res

    @api.multi
    def write(self, vals):
        for rec in self:
            if rec.advertising and rec.state not in ('draft', 'submitted') and  not rec.user_has_groups(
                    'sale_advertising_order.group_senior_sales,sale_advertising_order.group_traffic_user,sales_team.group_sale_manager')\
                    and not rec.order_line.filtered(lambda ol: ol.multi_line):
                raise UserError(_("You can't modify an order after approval!"))
        return super(SaleOrder, self).write(vals)

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        customer_contact = self.customer_contact
        partner = self.partner_id
        if partner and customer_contact:
            self.customer_contact = False
        return super(SaleOrder, self).onchange_partner_id()

    @api.onchange('published_customer')
    def onchange_published_customer(self):
        if self.published_customer:
            self.partner_id = self.published_customer

