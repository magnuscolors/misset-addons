# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Partner(models.Model):
    _description = 'Partner'
    _inherit = "res.partner"

    check_group = fields.Boolean(string="Check Group", compute='_check_user_group_users')

    @api.one
    def _check_user_group_users(self):
        is_update = True
        current_uid = self.env.uid
        res_users = self.env['res.users'].browse(current_uid)
        is_checked = res_users.has_group('misset_supplier_bank_access.supplier_full_access')
        if self.supplier is True and is_checked is False:
            is_update = False
        self.check_group = is_update
        
