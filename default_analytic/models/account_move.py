# -*- coding: utf-8 -*-
from odoo import models, fields, api #type: ignore

class AccountMove(models.Model):
    _inherit = 'account.move'

    general_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='General Analytic Account',
        help='If you select an account here, it will be assigned to all lines. If you remove it, the default values (Company or User) will be restored.'
    )

    @api.onchange('general_analytic_account_id')
    def _onchange_general_analytic_account_id(self):
        """
        Si hay cuenta general -> Se aplica a todo.
        Si se borra -> Se busca el default (Empresa > Usuario > Nada) y se restaura.
        """
        for move in self:
            distribution_to_apply = False

            # 1. Determinar qué distribución aplicar
            if move.general_analytic_account_id:
                # CASO A: El usuario seleccionó una cuenta general
                distribution_to_apply = {
                    str(move.general_analytic_account_id.id): 100
                }
            else:
                # CASO B: El usuario borró la cuenta general -> Calcular Default (Fallback)
                analytic_account_fallback = False
                
                # Prioridad 1: Configuración de la Empresa (del documento actual)
                if move.company_id.analytic_account_default_id:
                    analytic_account_fallback = move.company_id.analytic_account_default_id
                
                # Prioridad 2: Configuración del Usuario (si falló la empresa)
                elif self.env.user.default_analytic_account_id:
                    analytic_account_fallback = self.env.user.default_analytic_account_id
                
                # Si encontramos algún default, preparamos el JSON
                if analytic_account_fallback:
                    distribution_to_apply = {
                        str(analytic_account_fallback.id): 100
                    }
                # Si no, distribution_to_apply se queda en False (limpia el campo)

            # 2. Aplicar masivamente a las líneas existentes
            # Usamos un bucle simple para actualizar la vista en tiempo real
            for line in move.invoice_line_ids:
                line.analytic_distribution = distribution_to_apply
            
            # Opcional: También actualizar apuntes contables si es necesario
            # for line in move.line_ids:
            #    line.analytic_distribution = distribution_to_apply