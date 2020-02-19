
from odoo import models, fields, api, tools, _
from datetime import datetime, timedelta
import time


class ActivityLogDeDuplicate(models.Model):
    _name = "crm.activity.de.duplicate"

    activity = fields.Selection([('Email', 'Email'), ('Call', 'Call'), ('Task', 'Task'), ('Afspraak', 'Afspraak')], string='Activity', required=True)
    total_ids = fields.Char(string='Total IDs')
    total_ids_count = fields.Char(string='Total IDs Count')
    duplicated_ids = fields.Char(string='Duplicated IDs')
    duplicated_ids_count = fields.Integer   (string='Duplicated IDs Count')
    deleted_ids = fields.Char(string='Deleted IDs')
    deleted_ids_count = fields.Char(string='Deleted IDs Count')
    likely_duplicated_ids = fields.Char(string='Likely Duplicated IDs')
    likely_duplicated_ids_count = fields.Char(string='Likely Duplicated IDs Count')
    likely_duplicated_deleted_ids = fields.Char(string='Likely Duplicated Deleted IDs')
    likely_duplicated_deleted_ids_count = fields.Char(string='Likely Duplicated Deleted IDs Count')

    @api.onchange('activity')
    def onchange_activity(self):
        domain = [('model', '=', 'crm.lead'), ('subtype_id','not in', ('Lead Created','Stage Changed','Opportunity Won','Discussions','Note','Lead aangemaakt','Fase gewijzigd','Prospect gewonnen','Discussies','Notitie')), ('subtype_id','!=',False)]
        mm_obj = self.env['mail.message']
        if self.activity:
            mail_messages = mm_obj.search(domain+[('subtype_id', '=', self.activity)])
            self.total_ids = mail_messages.ids
            self.total_ids_count = len(mail_messages.ids)

    @api.multi
    def action_show_duplicated_records(self):
        start = time.time()
        if self.activity:
            domain = [('subtype_id', '=', self.activity), ('model', '=', 'crm.lead'), ('subtype_id','not in', ('Lead Created','Stage Changed','Opportunity Won','Discussions','Note','Lead aangemaakt','Fase gewijzigd','Prospect gewonnen','Discussies','Notitie')), ('subtype_id','!=',False)]
            mm_obj = self.env['mail.message']
            mail_messages = mm_obj.search(domain)

            duplicated_recs = []
            for mm in mail_messages:
                if mm.id not in duplicated_recs:
                    duplicate_mm = mail_messages.search([('id', '!=', mm.id), ('model', '=', 'crm.lead'), ('res_id', '=', mm.res_id), ('author_id', '=', mm.author_id.id), ('message_type', '=', mm.message_type), ('subtype_id', '=', mm.subtype_id.id), ('date', '=', mm.date)])
                    if duplicate_mm and len(duplicate_mm) == 1:
                        mm_subject_len = len(mm.subject) if mm.subject else 0
                        dup_mm_subject_len = len(duplicate_mm.subject) if duplicate_mm.subject else 0

                        duplicated_rec = mm if mm_subject_len < dup_mm_subject_len else duplicate_mm

                        duplicated_recs.append(duplicated_rec.id)

            if not self.duplicated_ids:
                self.duplicated_ids = duplicated_recs
            if not self.duplicated_ids_count:
                self.duplicated_ids_count = len(duplicated_recs)
            print"\n\n\nprocess time taken>>>",(time.time() - start)

    @api.multi
    def action_delete_duplicated_records(self):
        start = time.time()
        duplicated_ids = self.duplicated_ids
        duplicated_ids_count = self.duplicated_ids_count
        if self.duplicated_ids_count > 0:
            encoded = self.duplicated_ids.encode("utf-8")
            import ast
            ids = ast.literal_eval(encoded)
            self._cr.execute('delete from mail_message where id in %s', (tuple(ids),))
            self.deleted_ids = duplicated_ids
            self.deleted_ids_count = duplicated_ids_count
        print"\n\n\nprocess time taken>>>",(time.time() - start)

    @api.multi
    def action_mark_likely_to_be_duplicated_records(self):
        start = time.time()
        if self.activity:
            domain = [('subtype_id', '=', self.activity), ('model', '=', 'crm.lead'), ('subtype_id','not in', ('Lead Created','Stage Changed','Opportunity Won','Discussions','Note','Lead aangemaakt','Fase gewijzigd','Prospect gewonnen','Discussies','Notitie')), ('subtype_id','!=',False)]
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

                        marked_recs.append(mm.id)
                        marked_recs.append(likely_duplicate_mm.id)

            if not self.likely_duplicated_ids:
                self.likely_duplicated_ids = marked_recs
            if not self.likely_duplicated_ids_count:
                self.likely_duplicated_ids_count = len(marked_recs)
            print"\n\n\nprocess time taken>>>",(time.time() - start)

    @api.multi
    def action_delete_likely_to_be_duplicated_records(self):
        start = time.time()
        if self.activity:
            domain = [('likely_to_be_duplicated', '=', True), ('subtype_id', '=', self.activity), ('model', '=', 'crm.lead'), ('subtype_id','not in', ('Lead Created','Stage Changed','Opportunity Won','Discussions','Note','Lead aangemaakt','Fase gewijzigd','Prospect gewonnen','Discussies','Notitie')), ('subtype_id','!=',False)]
            mm_obj = self.env['mail.message']
            mail_messages = mm_obj.search(domain)

            duplicated_recs = []
            for mm in mail_messages:
                if mm.id not in duplicated_recs:
                    cdatetime = datetime.strptime(mm.date, "%Y-%m-%d %H:%M:%S")
                    decreased_cdatetime = (cdatetime - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
                    duplicate_mm = mail_messages.search([('id', '!=', mm.id), ('model', '=', 'crm.lead'), ('res_id', '=', mm.res_id), ('author_id', '=', mm.author_id.id), ('message_type', '=', mm.message_type), ('subtype_id', '=', mm.subtype_id.id), ('date', '=', decreased_cdatetime)])

                    if duplicate_mm and len(duplicate_mm) == 1:
                        mm_subject_len = len(mm.subject) if mm.subject else 0
                        dup_mm_subject_len = len(duplicate_mm.subject) if duplicate_mm.subject else 0

                        duplicated_rec = mm if mm_subject_len < dup_mm_subject_len else duplicate_mm

                        duplicated_recs.append(duplicated_rec.id)

            if not self.likely_duplicated_deleted_ids:
                self.likely_duplicated_deleted_ids = duplicated_recs
            if not self.likely_duplicated_deleted_ids_count:
                self.likely_duplicated_deleted_ids_count = len(duplicated_recs)

            if duplicated_recs:
                self._cr.execute('delete from mail_message where id in %s', (tuple(duplicated_recs),))
            print"\n\n\nprocess time taken>>>",(time.time() - start)