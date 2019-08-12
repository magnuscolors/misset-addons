# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HrExpense(models.Model):
    _inherit = "hr.expense"

    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='WKR')

    def _get_recursive_departments(self):
        analytic_account = self.env['account.analytic.account']
        employee = self.env.user._get_related_employees()
        department_id = employee.department_id.id or False
        if not department_id:
            return analytic_account

        query = """
                    WITH RECURSIVE deptgroup AS (
                            SELECT id, parent_id FROM hr_department
                            WHERE hr_department.id = %s
                        UNION
                            SELECT  d.id, d.parent_id
                            FROM    hr_department d
                            INNER JOIN deptgroup dg
                            ON dg.id = d.parent_id
                    )
                    SELECT * FROM deptgroup
                    """
        self._cr.execute(query, (department_id,))
        result = self._cr.fetchall()

        department_ids = list(set([y for x in result for y in x]))

        analytic_account = analytic_account.search([('department_id', 'in', department_ids)])
        return analytic_account


    @api.onchange('analytic_account_id')
    def onchange_analytic_account_id(self):
        analytic_account = self._get_recursive_departments()
        if analytic_account:
            return {'domain': {
                'analytic_account_id': [
                    ('id', 'in', analytic_account.ids)]}}
        return {}
    
    def _prepare_move_line(self, line):
        move_line = super(HrExpense, self)._prepare_move_line(line)
        if self.analytic_tag_ids:
            move_line.update({'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})
        return move_line