# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Partner(models.Model):
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
    def create(self, vals):
        """Add inverted names at creation if unavailable."""
        context = dict(self.env.context)
        name = vals.get("name", context.get("default_name"))

        if name is not None:
            # Calculate the splitted fields
            inverted = self._get_inverse_name(
                self._get_whitespace_cleaned_name(name),
                vals.get("is_company",
                         self.default_get(["is_company"])["is_company"]))
            print ("inverted",inverted)
#             for key, value in inverted.iteritems():
#                 if not vals.get(key) or context.get("copy"):
#                     vals[key] = value
            # Remove the combined fields
            if "name" in vals:
                del vals["name"]
            if "default_name" in context:
                del context["default_name"]
                
        if vals.get('parent_id'):
            vals.update({'is_company':False,'company_type':'person'})
        return super(Partner, self.with_context(context)).create(vals)