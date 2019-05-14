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

    @api.multi
    def material_received(self):
        for rec in self:
            material_status = 'Received'
            date_material_received = datetime.now()
            if rec.recurring and rec.recurring_id:
                material_status = rec.recurring_id.material_status
                date_material_received = rec.date_material_received
            if rec.invoice_status == 'invoiced':
                if not isinstance(date_material_received, str):
                    date_material_received = str(date_material_received)
                self.env.cr.execute(
                    """UPDATE sale_order_line SET material_status = %s, date_material_received = %s
                    WHERE id = %s""",
                    (material_status, date_material_received, rec.id),
                )
            else:
                rec.write({'material_status':material_status, 'date_material_received':date_material_received})
    
    @api.multi
    def material_pending(self):
        for rec in self:
            material_status = 'Pending'
            date_material_received = datetime.now()
            if rec.recurring and rec.recurring_id:
                material_status = rec.recurring_id.material_status
                date_material_received = rec.date_material_received
            if rec.invoice_status == 'invoiced':
                if not isinstance(date_material_received, str):
                    date_material_received = str(date_material_received)
                self.env.cr.execute(
                    """UPDATE sale_order_line SET material_status = %s, date_material_received = %s
                    WHERE id = %s""",
                    (material_status, date_material_received, rec.id),
                )
            else:
                rec.write({'material_status':material_status,'date_material_received':date_material_received})
            
    @api.multi
    def material_recurring(self):
        for rec in self:
            material_status = 'Recurring'
            date_material_received = datetime.now()
            if rec.recurring and rec.recurring_id:
                material_status = rec.recurring_id.material_status
                date_material_received = rec.date_material_received
            if rec.invoice_status == 'invoiced':
                if not isinstance(date_material_received, str):
                    date_material_received = str(date_material_received)
                self.env.cr.execute(
                    """UPDATE sale_order_line SET material_status = %s, date_material_received = %s
                    WHERE id = %s""",
                    (material_status, date_material_received, rec.id),
                )
            else:
                rec.write({'material_status':material_status, 'date_material_received':date_material_received})
        
