# -*- coding: utf-8 -*-
# Your code goes below this line

from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError


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

        #customer.parent.zip
        def _kix_code(customer):
            nonkix = customer.zip or customer.parent.zip or ''
            kix = nonkix.replace(" ", "")
            return kix

        def _prepare_data(customer, pLine):
            records = []
            parent = customer.parent_id
            records.append(u''+str(pLine.proof_country_code) or '')
            records.append(u''+str(_kix_code(customer)))
            account_name = ''
            initial = ''
            firstname = ''
            infix = ''
            account_details = ''
            tital = ''
            last_name = ''
            if parent:
                account_name = parent.name
                account_details = account_name
            else:
                if customer.title:
                    tital = customer.title.name + " "
                if customer.initials:
                    initial= customer.initials + " "
                else:
                    if customer.firstname:
                        firstname = customer.firstname + " "
                if customer.infix:
                    infix = customer.infix + " "
                if customer.lastname:
                    last_name = customer.lastname
                account_details = str(tital) + str(initial) + str(firstname) + str(infix) + str(last_name)
#                 account_name = customer.name or ''
                
            records.append(u''+account_details or '')
            
            initial = ''
            firstname = ''
            infix = ''
            blank_details = ''
            tital = ''
            last_name = ''
            if parent:
                if customer.title:
                    tital = customer.title.name + " "
                if customer.initials:
                    initial= customer.initials + " "
                else:
                    if customer.firstname:
                        firstname = customer.firstname + " "
                if customer.infix:
                    infix = customer.infix + " "
                if customer.lastname:
                    last_name = customer.lastname 
                blank_details = str(tital) + str(initial) + str(firstname) + str(infix) + str(last_name)
                
#             if pLine.proof_number_payer.initials:
#                 initial= pLine.proof_number_payer.initials + ' '
#             elif pLine.proof_number_payer.firstname:
#                 initial = pLine.proof_number_payer.firstname + ' '
#             infix = ''
#             if pLine.proof_number_payer.infix:
#                 infix = pLine.proof_number_payer.infix + ' '
                
            records.append(u''+ str(blank_details))
            
            street_name_space = ' '
            stret_name = ''
            stret_number = ''
            if customer.street_name or parent.street_name:
                street_name_space = ' '
            stret_name = customer.street_name or parent.street_name or ''
            
            stret_number = customer.street_number or parent.street_number or ''
            if not stret_number:
                stret_number = ''
            street = stret_name + street_name_space + stret_number
            records.append(u''+street)
            records.append(pLine.proof_zip)
            records.append(u''+customer.city or parent.city or '')
            records.append(u''+customer.country_id.name or parent.country_id.name or '')
            amount = 0
            if customer.id in pLine.line_id.proof_number_adv_customer.ids:
                amount += pLine.line_id.proof_number_amt_adv_customer
            if pLine.line_id.proof_number_payer_id and pLine.line_id.proof_number_payer_id.id == customer.id:
                amount += pLine.line_id.proof_number_amt_payer
            records.append(amount)
#             records.append(pLine.line_id.product_template_id.name or '')
            issue_date_cov = datetime.datetime.strptime(pLine.issue_date, '%Y-%m-%d')
            issue_date_c = datetime.datetime.strftime(issue_date_cov , '%d/%m/%Y')
            records.append(issue_date_c)
            records.append(u''+str(pLine.title.name))
            
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

        header = ['LANDCODE', 'KIXCODE', 'NAAM', 'TAV', 'ADRES', 'POSTCODE', 'PLAATS',
                  'LAND', 'AANTAL','TITEL']

        row_datas = _form_data(proofLines)

        if row_datas:
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

NSMDeliveryListReport('report.report_pndl_delivery_list1.xlsx', 'sale.order.line')