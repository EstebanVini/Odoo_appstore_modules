# POS Analytic Account Auto

This Odoo 15 module guarantees that analytic accounts assigned to POS orders are stored and visible in the **standard sales report** (`sale.report`).  
It ensures the analytic account is filled on every POS order line and patches the sales report SQL view to persist this field even after upgrades or module reinstalls.

---

## Features

- Adds the `analytic_account_id` field to `pos.order.line` (POS order lines).
- Automatically computes and stores the analytic account on POS order lines, using the POS configuration of the session.
- **Patches the `sale.report` SQL view** so that analytic account data for POS orders is visible and usable in all native sales analysis.
- Maintains compatibility with [OCA pos_analytic_by_config](https://github.com/OCA/account-analytic).
- Automatically restores the patch after Odoo or POS/sale module upgrades.

---

## Installation

1. Clone this repository into your Odoo addons folder.
2. Update your app list in Odoo.
3. Install the “POS Analytic Account Auto” module from the Apps menu.

---

## Usage

- No configuration required.
- Every new POS sale will have its analytic account assigned according to the POS configuration.
- The analytic account field is now available in the `sale.report` (Sales Analysis), so you can group, filter, and analyze by analytic account natively.

---

## Technical Notes

- If you upgrade Odoo or any module that rewrites the `sale.report` view, simply update this module to restore the analytic field automatically.
- For historical POS lines created before installing this module, run a recompute on `pos.order.line` to fill missing analytic accounts.

---

## Dependencies

- `point_of_sale`
- `sale`
- `pos_analytic_by_config` (OCA)

---

## Credits

**Author:**  
Esteban Viniegra Pérez Olagaray
esteban@eviniegra.software

Pridecta
https://pridecta.com

---

## License

AGPL-3.0

---

