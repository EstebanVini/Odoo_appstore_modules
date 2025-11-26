# -*- coding: utf-8 -*-
from odoo import models, fields #type: ignore

class ResCompany(models.Model):
    _inherit = 'res.company'

    analytic_account_default_id = fields.Many2one(
        'account.analytic.account',
        string='Default Analytic Account',
        help="This account takes precedence over the user's configuration."
    )