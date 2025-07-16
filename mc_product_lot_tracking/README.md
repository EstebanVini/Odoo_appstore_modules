# Product Lot Tracking per Company

**Odoo 18.0 – Community & Enterprise**

---

## Overview

Product Lot Tracking per Company allows you to configure and enforce lot/serial tracking rules on a per-product, per-company basis in multi-company Odoo environments.

By default, Odoo enforces the lot/serial tracking setting globally on each product, making it impossible to have different rules for different companies. This module solves that limitation with a simple, robust, and user-friendly approach.

---

## Key Features

- **Per-company tracking rules:** Set specific lot/serial/no tracking requirements for each product and company.
- **Dynamic enforcement:** Odoo will only require lot/serial numbers when a company-specific rule is present; otherwise, it uses the global product setting.
- **Flexible for intercompany operations:** Useful for manufacturers selling to internal companies that do not need to track lots on their side.
- **Fully integrated with Odoo inventory flows:** Works with stock transfers, receipts, deliveries, and all standard processes.
- **Easy configuration:** "Tracking by Company" table available on the product form, in the "General Information" tab.
- **Compatible with Odoo 18 Community and Enterprise.**

---

## Use Cases

- **Manufacturing company** that needs lot/serial tracking for production, but sells to a distribution company (in the same Odoo database) where no tracking is needed for internal logistics.
- **Intercompany sales/purchase synchronization** where the supplier company enforces lot tracking and the buyer company does not want to require it.
- **Compliance with region-specific or customer-specific traceability requirements** by company.

---

## Installation

1. Copy the `mc_product_lot_tracking` folder into your Odoo addons path.
2. Update the apps list in Odoo.
3. Install the module from the Apps menu.

---

## Usage

1. Go to **Inventory > Products** and open any product template.
2. On the **General Information** tab, you will find the new **Tracking by Company** section.
3. Add rules for each company where you want to override the global tracking behavior.
4. When receiving or delivering this product, Odoo will enforce the correct tracking requirements according to the company processing the operation.

---

## Compatibility

- Odoo 18.0 Community and Enterprise.
- Works with standard Inventory, Purchase, and Sales modules.
- Fully supports multi-company environments.

---

## Screenshots

![Tracking by Company table](static/description/image.png)

---

## Support and Customization

For support, customization, or consultancy services:

**Esteban Viniegra Pérez Olagaray**  
Email: [esteban@eviniegra.software](mailto:esteban@eviniegra.software)  
Company: [Pridecta](https://pridecta.es)

---

## License

Odoo Enterprise Edition License (OEEL-1).

---

**Developed and maintained by Pridecta**  
https://pridecta.es
