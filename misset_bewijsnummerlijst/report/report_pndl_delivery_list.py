# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


class NSMDeliveryListReport(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, proofLines):

        def _get_title(orderLine):
            title = []
            for advtitle in orderLine.title_ids:
                if advtitle.product_attribute_value_id:
                    title.append(advtitle.product_attribute_value_id.name)
            if orderLine.title.product_attribute_value_id:
                title.append(orderLine.title.product_attribute_value_id.name)
            title = ",".join(list(set(title))) if title else ' '
            return title

        def _kix_code(customer):
            nonkix = customer.zip or customer.parent.zip or ''
            kix = nonkix.replace(" ", "")
            return kix

        def _prepare_data(customer, pLine):
            records = []
            parent = customer.parent_id
            records.append(pLine.proof_country_code)
            records.append(_kix_code(customer))
            records.append(customer.name)
            initial = ''
            if pLine.proof_number_payer.initials:
                initial= pLine.proof_number_payer.initials
            elif pLine.proof_number_payer.firstname:
                initial = pLine.proof_number_payer.firstname
            infix = ''
            if pLine.proof_number_payer.infix:
                infix = pLine.proof_number_payer.infix
            blank_details =  str(pLine.proof_number_payer.title.name or '') +' ' + str(initial) +' ' + infix + pLine.proof_number_payer.lastname
            records.append(blank_details)
            street = str(customer.street_name or parent.street_name or '') + str(customer.street_number or parent.street_number or '')
            records.append(street)
            records.append(pLine.proof_zip)
            records.append(customer.city or parent.city or '')
            records.append(customer.country_id.name or parent.country_id.name or '')
            amount = 0
            if customer.id in pLine.line_id.proof_number_adv_customer.ids:
                amount += pLine.line_id.proof_number_amt_adv_customer
            if pLine.line_id.proof_number_payer_id and pLine.line_id.proof_number_payer_id.id == customer.id:
                amount += pLine.line_id.proof_number_amt_payer
            records.append(amount)
            records.append(pLine.line_id.name)
            records.append(pLine.issue_date)
            
            
            
#             parent = customer.parent_id
#             records.append(customer.country_id.code or parent.country_id.code or '')
#             records.append("Account")
# 
#             records.append(customer.zip or parent.zip or '')
#             records.append(parent.name if parent else customer.name)
# 
#             if parent and not parent.is_company:
#                 records.append(parent.initials or '')
#                 records.append(parent.infix or '')
#                 records.append(parent.lastname or '')
#             elif not parent and not customer.is_company:
#                 records.append(customer.initials or '')
#                 records.append(customer.infix or '')
#                 records.append(customer.lastname or '')
#             else:
#                 records.append('')
#                 records.append('')
#                 records.append('')
#             records.append(_get_title(orderLine))
# 
#             records.append(customer.street_number or parent.street_number or '')
#             records.append('')
#             records.append(customer.street_name or parent.street_name or '')
#             records.append(customer.city or parent.city or '')
# 
#             amount = 0
#             if customer.id in orderLine.proof_number_adv_customer.ids:
#                 amount += orderLine.proof_number_amt_adv_customer
#             if orderLine.proof_number_payer_id and orderLine.proof_number_payer_id.id == customer.id:
#                 amount += orderLine.proof_number_amt_payer
#             records.append(amount)
#             records.append(customer.name if parent else '')
            return records

        def _form_data(proofLines):
            row_datas = []
            # for orderLine in orderLines:
            for pLine in proofLines:
                # partners = orderLine.proof_number_adv_customer | orderLine.proof_number_payer
                #pLine.line_id
                row_datas.append(_prepare_data(pLine.proof_number_payer, pLine))
                # for part in partners:
                #     row_datas.append(_prepare_data(part, orderLine))

            return row_datas

        header = ['Country Code', 'KIX Postal Code', 'Account', '', 'Street', 'Postal Code', 'City',
                  'Country', 'Voucher Copy', 'Product Name', 'Issue Date']

        row_datas = _form_data(proofLines)

        if row_datas:
            print ("row_datasrow_datas",row_datas)
            bold_format = workbook.add_format({'bold': True})
            report_name = 'PNDL_{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
            sheet = workbook.add_worksheet(report_name[:31])
            for i, title in enumerate(header):
                sheet.write(0, i, title, bold_format)
            for row_index, row in enumerate(row_datas):
                for cell_index, cell_value in enumerate(row):
                    sheet.write(row_index + 1, cell_index, cell_value)
            workbook.close()
        else:
            raise UserError(_('No record found to print!'))
#         report_name = "Bewijsnummers"
#         report_id = self.env.ref('nsm_sale_advertising_order.report_nsm_proof_delivery_list_report_xlsx')
#         print ("report_id",report_id.print_report_name)
#         report_id.write({'print_report_name':'DK.xls'})


NSMDeliveryListReport('report.report_pndl_delivery_list1.xlsx', 'proof.number.delivery.list')