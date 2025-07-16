from odoo import models, fields, api # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class ProductTemplate(models.Model):
    _inherit = "product.template"

    tracking_company_ids = fields.One2many(
        'product.lot.tracking.company', 'product_tmpl_id', string='Tracking by Company'
    )

    def get_tracking_for_company(self, company_id):
        """Get tracking type for the given company, or fallback to global tracking."""
        self.ensure_one()
        rec = self.tracking_company_ids.filtered(lambda x: x.company_id.id == company_id)
        return rec.tracking if rec else self.tracking

# Patch stock.move.line to validate lot/serial according to the company config
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.constrains('lot_id', 'qty_done', 'product_id')
    def _check_lots(self):
        for line in self:
            # Ensure product_id is set and related template exists
            product = line.product_id
            product_tmpl = product.product_tmpl_id
            picking_company = line.picking_id.company_id
            tracking = product_tmpl.get_tracking_for_company(picking_company.id)
            if tracking == 'none':
                continue  # No tracking required
            if tracking == 'serial':
                if line.qty_done > 1 and not line.lot_id:
                    raise ValidationError(
                        "You must enter the serial number for product '%s' in company '%s'." % (
                            product.display_name, picking_company.display_name
                        )
                    )
            if tracking == 'lot':
                if not line.lot_id and line.qty_done:
                    raise ValidationError(
                        "You must enter the lot number for product '%s' in company '%s'." % (
                            product.display_name, picking_company.display_name
                        )
                    )
