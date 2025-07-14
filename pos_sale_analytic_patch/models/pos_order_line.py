from odoo import api, fields, models # type: ignore[import]

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        store=True,
        compute='_compute_analytic_account_id',
    )

    @api.depends('order_id.session_id.config_id.account_analytic_id')
    def _compute_analytic_account_id(self):
        for line in self:
            analytic = (
                line.order_id.session_id.config_id.account_analytic_id
                if line.order_id and line.order_id.session_id and line.order_id.session_id.config_id
                else False
            )
            line.analytic_account_id = analytic.id if analytic else False
