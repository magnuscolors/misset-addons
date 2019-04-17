# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Partner(models.Model):
    _description = 'Partner'
    _inherit = "res.partner"

    company_type = fields.Selection(string='Company Type',
        selection=[('person', 'Individual'), ('company', 'Company')],
        compute='_compute_company_type', inverse='_write_company_type',default='company' )
    @api.model
    def default_get(self, fields):
        rec = super(Partner, self).default_get(fields)
        rec.update({'is_company':True,'company_type':'company'})
        return rec
        
    @api.model
    def create(self,vals):
        if vals.get('parent_id'):
            vals.update({'is_company':False,'company_type':'person'})
        res = super(Partner,self).create(vals)
        return res