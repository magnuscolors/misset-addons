
from odoo import models, fields, api, tools, _
from datetime import datetime, timedelta


class ActivityLogDeDuplicate(models.Model):
    _name = "crm.activity.de.duplicate"

    activity = fields.Selection([('Email', 'Email'), ('Call', 'Call'), ('Task', 'Task'), ('Afspraak', 'Afspraak')], string='Activity', required=True)
    total_ids = fields.Char(string='Total IDs')
    total_ids_count = fields.Char(string='Total IDs Count')
    deleted_ids = fields.Char(string='Deleted IDs')
    deleted_ids_count = fields.Char(string='Deleted IDs Count')
    marked_ids = fields.Char(string='Likely Duplicated IDs')
    marked_ids_count = fields.Char(string='Likely Duplicated IDs Count')

    @api.onchange('activity')
    def onchange_activity(self):
        domain = [('model', '=', 'crm.lead'), ('subtype_id','not in', ('Lead Created','Stage Changed','Opportunity Won','Discussions','Note','Lead aangemaakt','Fase gewijzigd','Prospect gewonnen','Discussies','Notitie')), ('subtype_id','!=',False)]
        mm_obj = self.env['mail.message']
        if self.activity:
            mail_messages = mm_obj.search(domain+[('subtype_id', '=', self.activity)])
            self.total_ids = mail_messages.ids
            self.total_ids_count = len(mail_messages.ids)

    @api.multi
    def action_remove_duplicate_records(self):
        if self.activity:
            domain = [('subtype_id', '=', self.activity), ('model', '=', 'crm.lead'), ('subtype_id','not in', ('Lead Created','Stage Changed','Opportunity Won','Discussions','Note','Lead aangemaakt','Fase gewijzigd','Prospect gewonnen','Discussies','Notitie')), ('subtype_id','!=',False)]
            mm_obj = self.env['mail.message']
            mail_messages = mm_obj.search(domain)

            deleted_recs = []
            for mm in mail_messages:
                if mm.exists():
                    duplicate_mm = mail_messages.search([('id', '!=', mm.id), ('model', '=', 'crm.lead'), ('res_id', '=', mm.res_id), ('author_id', '=', mm.author_id.id), ('message_type', '=', mm.message_type), ('subtype_id', '=', mm.subtype_id.id), ('date', '=', mm.date)])
                    # duplicate_mm2 = mm_obj.search([('id', '!=', mm.id), ('date', '=', mm.date), ('email_from', '=', mm.email_from), ('author_id', '=', mm.author_id.id), ('record_name', '=', mm.record_name), ('parent_id', '=', mm.parent_id.id), ('model', '=', 'crm.lead'), ('res_id', '=', mm.res_id), ('message_type', '=', mm.message_type), ('subtype_id', '=', mm.subtype_id.id)])
                    if duplicate_mm and len(duplicate_mm) == 1:
                        mm_subject_len = len(mm.subject) if mm.subject else 0
                        dup_mm_subject_len = len(duplicate_mm.subject) if duplicate_mm.subject else 0
                        if mm_subject_len == 0 and dup_mm_subject_len == 0:
                            deleted_rec = duplicate_mm
                        elif mm_subject_len > dup_mm_subject_len:
                            deleted_rec = duplicate_mm
                        elif mm_subject_len < dup_mm_subject_len:
                            deleted_rec = mm
                        else:
                            deleted_rec = duplicate_mm

                        deleted_recs.append(deleted_rec.id)
                        deleted_rec.unlink()
            if not self.deleted_ids:
                self.deleted_ids = deleted_recs
            if not self.deleted_ids_count:
                self.deleted_ids_count = len(deleted_recs)

    @api.multi
    def action_mark_likely_to_be_duplicated_records(self):
        if self.activity:
            domain = [('likely_to_be_duplicated', '=', False), ('subtype_id', '=', self.activity), ('model', '=', 'crm.lead'), ('subtype_id','not in', ('Lead Created','Stage Changed','Opportunity Won','Discussions','Note','Lead aangemaakt','Fase gewijzigd','Prospect gewonnen','Discussies','Notitie')), ('subtype_id','!=',False)]
            mm_obj = self.env['mail.message']
            mail_messages = mm_obj.search(domain)

            marked_recs = []
            for mm in mail_messages:
                if mm.exists():
                    cdatetime = datetime.strptime(mm.date, "%Y-%m-%d %H:%M:%S")
                    decreased_cdatetime = (cdatetime - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
                    likely_duplicate_mm = mail_messages.search([('id', '!=', mm.id), ('model', '=', 'crm.lead'), ('res_id', '=', mm.res_id), ('author_id', '=', mm.author_id.id), ('message_type', '=', mm.message_type), ('subtype_id', '=', mm.subtype_id.id), ('date', '=', decreased_cdatetime)])
                    if likely_duplicate_mm and len(likely_duplicate_mm) == 1:
                        likely_duplicate_mm.likely_to_be_duplicated = True
                        mm.likely_to_be_duplicated = True

                        marked_recs.append(likely_duplicate_mm.id)
                        marked_recs.append(mm.id)

            if not self.marked_ids:
                self.marked_ids = marked_recs
            if not self.marked_ids_count:
                self.marked_ids_count = len(marked_recs)