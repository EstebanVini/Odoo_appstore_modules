{
    "name": "Product Lot Tracking by Company",
    "version": "18.0.1.0.0",
    "author": "Esteban Viniegra Pérez Olagaray | Pridecta",
    "category": "Inventory",
    "license": "AGPL-3",
    "website": "https://pridecta.es",
    "summary": "Allows defining lot tracking at the company level.",
    "description": "Configure the tracking type (lot/serial/no tracking) per product and company.",
    "depends": [
        "stock", "product"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
    ],
    "icon": "/mc_product_lot_tracking/static/description/icon.png",
    "images": [
        "static/description/cover.png",
    ],
    "installable": True,
    "application": False,
}
