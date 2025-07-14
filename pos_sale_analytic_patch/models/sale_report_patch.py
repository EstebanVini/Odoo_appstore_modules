from odoo import models # type: ignore[import]

class SaleReport(models.Model):
    _inherit = 'sale.report'

    def init(self):
        self.env.cr.execute("""
DROP VIEW IF EXISTS sale_report CASCADE;

CREATE VIEW sale_report AS

SELECT min(l.id) AS id,
    l.product_id,
    t.uom_id AS product_uom,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum(((l.product_uom_qty / u.factor) * u2.factor))
        ELSE (0)::numeric
    END AS product_uom_qty,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum(((l.qty_delivered / u.factor) * u2.factor))
        ELSE (0)::numeric
    END AS qty_delivered,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum((((l.product_uom_qty - l.qty_delivered) / u.factor) * u2.factor))
        ELSE (0)::numeric
    END AS qty_to_deliver,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum(((l.qty_invoiced / u.factor) * u2.factor))
        ELSE (0)::numeric
    END AS qty_invoiced,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum(((l.qty_to_invoice / u.factor) * u2.factor))
        ELSE (0)::numeric
    END AS qty_to_invoice,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum((l.price_total /
        CASE COALESCE(s.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE s.currency_rate
        END))
        ELSE (0)::numeric
    END AS price_total,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum((l.price_subtotal /
        CASE COALESCE(s.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE s.currency_rate
        END))
        ELSE (0)::numeric
    END AS price_subtotal,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum((l.untaxed_amount_to_invoice /
        CASE COALESCE(s.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE s.currency_rate
        END))
        ELSE (0)::numeric
    END AS untaxed_amount_to_invoice,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum((l.untaxed_amount_invoiced /
        CASE COALESCE(s.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE s.currency_rate
        END))
        ELSE (0)::numeric
    END AS untaxed_amount_invoiced,
    count(*) AS nbr,
    s.name,
    s.date_order AS date,
    s.state,
    s.partner_id,
    s.user_id,
    s.company_id,
    s.campaign_id,
    s.medium_id,
    s.source_id,
    (EXTRACT(epoch FROM avg((date_trunc('day'::text, s.date_order) - date_trunc('day'::text, s.create_date)))) / (((24 * 60) * 60))::numeric(16,2)) AS delay,
    t.categ_id,
    s.pricelist_id,
    s.analytic_account_id,
    s.team_id,
    p.product_tmpl_id,
    partner.country_id,
    partner.industry_id,
    partner.commercial_partner_id,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum((((p.weight * l.product_uom_qty) / u.factor) * u2.factor))
        ELSE (0)::numeric
    END AS weight,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum((((p.volume * l.product_uom_qty) / u.factor) * u2.factor))
        ELSE (0)::numeric
    END AS volume,
    l.discount,
    CASE
        WHEN (l.product_id IS NOT NULL) THEN sum(((((l.price_unit * l.product_uom_qty) * l.discount) / 100.0) /
        CASE COALESCE(s.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE s.currency_rate
        END))
        ELSE (0)::numeric
    END AS discount_amount,
    s.id AS order_id,
    s.shopify_instance_id,
    sum((l.margin /
        CASE COALESCE(s.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE s.currency_rate
        END)) AS margin,
    s.website_id,
    s.warehouse_id
   FROM (((((((sale_order_line l
     LEFT JOIN sale_order s ON ((s.id = l.order_id)))
     JOIN res_partner partner ON ((s.partner_id = partner.id)))
     LEFT JOIN product_product p ON ((l.product_id = p.id)))
     LEFT JOIN product_template t ON ((p.product_tmpl_id = t.id)))
     LEFT JOIN uom_uom u ON ((u.id = l.product_uom)))
     LEFT JOIN uom_uom u2 ON ((u2.id = t.uom_id)))
     LEFT JOIN product_pricelist pp ON ((s.pricelist_id = pp.id)))
  WHERE (l.display_type IS NULL)
  GROUP BY l.product_id, l.order_id, t.uom_id, t.categ_id, s.name, s.date_order, s.partner_id, s.user_id, s.state, s.company_id, s.campaign_id, s.medium_id, s.source_id, s.pricelist_id, s.analytic_account_id, s.team_id, p.product_tmpl_id, partner.country_id, partner.industry_id, partner.commercial_partner_id, l.discount, s.id, s.shopify_instance_id, s.warehouse_id, s.website_id

UNION ALL

SELECT (- min(l.id)) AS id,
    l.product_id,
    t.uom_id AS product_uom,
    sum(l.qty) AS product_uom_qty,
    sum(l.qty) AS qty_delivered,
    0 AS qty_to_deliver,
    CASE
        WHEN ((pos.state)::text = 'invoiced'::text) THEN sum(l.qty)
        ELSE (0)::numeric
    END AS qty_invoiced,
    CASE
        WHEN ((pos.state)::text <> 'invoiced'::text) THEN sum(l.qty)
        ELSE (0)::numeric
    END AS qty_to_invoice,
    (sum(l.price_subtotal_incl) / min(
        CASE COALESCE(pos.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE pos.currency_rate
        END)) AS price_total,
    (sum(l.price_subtotal) / min(
        CASE COALESCE(pos.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE pos.currency_rate
        END)) AS price_subtotal,
    (
        CASE
            WHEN ((pos.state)::text <> 'invoiced'::text) THEN sum(l.price_subtotal)
            ELSE (0)::numeric
        END / min(
        CASE COALESCE(pos.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE pos.currency_rate
        END)) AS untaxed_amount_to_invoice,
    (
        CASE
            WHEN ((pos.state)::text = 'invoiced'::text) THEN sum(l.price_subtotal)
            ELSE (0)::numeric
        END / min(
        CASE COALESCE(pos.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE pos.currency_rate
        END)) AS untaxed_amount_invoiced,
    count(*) AS nbr,
    pos.name,
    pos.date_order AS date,
    CASE
        WHEN ((pos.state)::text = 'draft'::text) THEN 'pos_draft'::character varying
        WHEN ((pos.state)::text = 'done'::text) THEN 'pos_done'::character varying
        ELSE pos.state
    END AS state,
    pos.partner_id,
    pos.user_id,
    pos.company_id,
    NULL::integer AS campaign_id,
    NULL::integer AS medium_id,
    NULL::integer AS source_id,
    (EXTRACT(epoch FROM avg((date_trunc('day'::text, pos.date_order) - date_trunc('day'::text, pos.create_date)))) / (((24 * 60) * 60))::numeric(16,2)) AS delay,
    t.categ_id,
    pos.pricelist_id,
    l.analytic_account_id AS analytic_account_id,
    pos.crm_team_id AS team_id,
    p.product_tmpl_id,
    partner.country_id,
    partner.industry_id,
    partner.commercial_partner_id,
    ((sum(p.weight) * l.qty) / u.factor) AS weight,
    ((sum(p.volume) * l.qty) / u.factor) AS volume,
    l.discount,
    sum(((((l.price_unit * l.discount) * l.qty) / 100.0) /
        CASE COALESCE(pos.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE pos.currency_rate
        END)) AS discount_amount,
    NULL::integer AS order_id,
    NULL::integer AS shopify_instance_id,
    sum((l.price_subtotal - (l.total_cost /
        CASE COALESCE(pos.currency_rate, (0)::numeric)
            WHEN 0 THEN 1.0
            ELSE pos.currency_rate
        END))) AS margin,
    NULL::integer AS website_id,
    NULL::integer AS warehouse_id
   FROM ((((((((pos_order_line l
     JOIN pos_order pos ON ((l.order_id = pos.id)))
     LEFT JOIN res_partner partner ON (((pos.partner_id = partner.id) OR (pos.partner_id = NULL::integer))))
     LEFT JOIN product_product p ON ((l.product_id = p.id)))
     LEFT JOIN product_template t ON ((p.product_tmpl_id = t.id)))
     LEFT JOIN uom_uom u ON ((u.id = t.uom_id)))
     LEFT JOIN pos_session session ON ((session.id = pos.session_id)))
     LEFT JOIN pos_config config ON ((config.id = session.config_id)))
     LEFT JOIN product_pricelist pp ON ((pos.pricelist_id = pp.id)))
  WHERE (l.sale_order_line_id IS NULL)
  GROUP BY l.order_id, l.product_id, l.price_unit, l.discount, l.qty, t.uom_id, t.categ_id, pos.name, pos.date_order, pos.partner_id, pos.user_id, pos.state, pos.company_id, pos.pricelist_id, p.product_tmpl_id, partner.country_id, partner.industry_id, partner.commercial_partner_id, u.factor, pos.crm_team_id, l.analytic_account_id;
        """)
