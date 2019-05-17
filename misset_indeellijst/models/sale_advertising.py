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
import json
from datetime import datetime

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    material_status = fields.Selection([('Pending','Pending'),('Received','Received'),('Recurring','Recurring')],"Material status",default='Pending')
    date_material_received = fields.Datetime("Date material received")

    def _update_material_status(self, status):
        material_status = status
        date_material_received = datetime.now()
        if self.recurring and self.recurring_id:
            material_status = self.recurring_id.material_status
            date_material_received = self.recurring_id.date_material_received
        else:
            self += self.search([('recurring_id', '=', self.id), ('recurring', '=', True)])

        #Fix: sale_advertising_order has conflict for updating fully invoiced lines for non account user
        if self.filtered(lambda l: l.invoice_status == 'invoiced'):
            if not isinstance(date_material_received, str):
                date_material_received = str(date_material_received)
            op, ids = ('IN', tuple(self.ids)) if  len(self.ids) > 1 else ('=', self.id)

            query = ("""
                    UPDATE sale_order_line 
                    SET material_status = {0},
                        date_material_received = {1}
                    WHERE id {2} {3}
                    """.format(
                "'%s'" % material_status,
                "'%s'" % date_material_received,
                op,
                ids
            ))
            self.env.cr.execute(query)
        else:
            self.write({'material_status': material_status, 'date_material_received': date_material_received})


    @api.multi
    def material_received(self):
        for rec in self:
            material_status = 'Received'
            rec._update_material_status(material_status)
    
    @api.multi
    def material_pending(self):
        for rec in self:
            material_status = 'Pending'
            rec._update_material_status(material_status)

    @api.multi
    def material_recurring(self):
        for rec in self:
            material_status = 'Recurring'
            rec._update_material_status(material_status)


    #reset material_id as original ID
    @api.onchange('recurring')
    def _onchange_recurring(self):
        if not self.recurring and self.recurring_id:
            self.recurring_id = False


        
