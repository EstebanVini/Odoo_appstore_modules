# -*- coding: utf-8 -*-
from odoo import models, fields #type: ignore

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Campo many2one solicitado para la configuración
    default_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Default Analytic Account',
        help='This account will be automatically assigned to invoice lines created by this user.'
    )