# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Message(models.Model):
    _inherit = 'mail.message'

    likely_to_be_duplicated = fields.Boolean(string='Likely to be duplicated')