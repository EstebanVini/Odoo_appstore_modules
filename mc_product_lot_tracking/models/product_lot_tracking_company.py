from odoo import models, fields, api # type: ignore

class ProductLotTrackingCompany(models.Model):
    _name = 'product.lot.tracking.company'
    _description = 'Product Lot Tracking by Company'
    _rec_name = 'display_name'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string="Product Template",
        required=True,
        ondelete='cascade'
    )
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True
    )
    tracking = fields.Selection(
        [
            ('none', 'No Tracking'),
            ('lot', 'By Lot'),
            ('serial', 'By Serial')
        ],
        string="Tracking",
        required=True,
        default='none'
    )
    display_name = fields.Char(
        compute="_compute_display_name",
        store=True
    )

    _sql_constraints = [
        (
            'product_company_uniq',
            'unique(product_tmpl_id,company_id)',
            'A configuration for this product and company already exists!'
        ),
    ]

    @api.depends('product_tmpl_id', 'company_id')
    def _compute_display_name(self):
        for rec in self:
            product = rec.product_tmpl_id.display_name or ''
            company = rec.company_id.display_name or ''
            rec.display_name = f"{product} - {company}"
