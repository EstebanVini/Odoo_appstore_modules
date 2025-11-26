# -*- coding: utf-8 -*-
from odoo import models, api #type: ignore

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def default_get(self, fields_list):
        res = super(AccountMoveLine, self).default_get(fields_list)

        if 'analytic_distribution' in fields_list:
            # Verificar si ya viene algo (poco probable en creación, pero por seguridad)
            if not res.get('analytic_distribution'):
                
                analytic_account_id = False
                
                # --- NUEVA LÓGICA: Prioridad 0 (Contexto de la Factura) ---
                # Si el contexto trae una cuenta general definida en la cabecera
                if self.env.context.get('default_general_analytic_account_id'):
                    analytic_account_id = self.env.context.get('default_general_analytic_account_id')
                    # Asegurarnos de que sea un entero (el contexto a veces trae objetos o strings)
                    if isinstance(analytic_account_id, int):
                         analytic_account_id = self.env['account.analytic.account'].browse(analytic_account_id)
                
                # --- LÓGICA PREVIA (Si no hay cuenta forzada en cabecera) ---
                elif self.env.company.analytic_account_default_id:
                    analytic_account_id = self.env.company.analytic_account_default_id
                
                elif self.env.user.default_analytic_account_id:
                    analytic_account_id = self.env.user.default_analytic_account_id
                
                # --- ASIGNACIÓN FINAL ---
                if analytic_account_id:
                    res['analytic_distribution'] = {
                        str(analytic_account_id.id): 100
                    }

        return res