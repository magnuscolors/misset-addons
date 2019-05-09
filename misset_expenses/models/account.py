# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    department_id = fields.Many2many('hr.department', string='Department')
