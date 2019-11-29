# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import json


class HrExpense(models.Model):
    _inherit = "hr.expense"

    @api.depends('analytic_account_id')
    @api.multi
    def _compute_analytic_account_domain(self):
        """
        Compute the domain for the analytic_account_domain.
        """
        for rec in self:
            analytic_account = rec._get_recursive_departments()
            if analytic_account:
                rec.analytic_account_domain = json.dumps(
                    [('id', 'in', analytic_account.ids)]
                )
            else:
                rec.analytic_account_domain = []


    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='WKR')
    analytic_account_domain = fields.Char(compute='_compute_analytic_account_domain', readonly=True, store=False, )

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


    def _prepare_move_line(self, line):
        move_line = super(HrExpense, self)._prepare_move_line(line)
        if self.analytic_tag_ids:
            move_line.update({'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)]})
        return move_line
