# User & Company Default Analytic Account

This module extends the analytic accounting functionality in Odoo 18 to automate the assignment of analytic accounts on customer invoices and vendor bills.

It allows defining default accounts at the **User** and **Company** levels, establishing a priority hierarchy to determine which account is automatically applied to invoice lines. Additionally, it provides a tool within the invoice itself to apply massive changes to all lines.

## Features

* **User Default:** Define a default analytic account for specific users.
* **Company Default:** Define a default analytic account for each company (Multi-company support).
* **Priority Hierarchy:** The system intelligently decides which account to use based on a specific order.
* **Mass Editing on Invoice:** A new field in the invoice header allows you to force an analytic account onto all lines with a single click.
* **Odoo 18 Compatibility:** Correctly handles the new JSON format of the `analytic_distribution` field.

## Configuration

### 1. Configure User Default Account
If a user typically imputes expenses or revenue to a specific account (e.g., a salesperson to their department), configure it here:

1.  Go to **Settings** > **Users & Companies** > **Users**.
2.  Select a user.
3.  In the **"Access Rights"** tab, locate the **Multi Companies** section (below "Default Company").
4.  Set the value in the **"Default Analytic Account"** field.

### 2. Configure Company Default Account
This account acts as a fallback if no specific account is set for the user or on the invoice, and it has a higher priority than the user setting.

1.  Go to **Settings** > **Users & Companies** > **Companies**.
2.  Select the company.
3.  In the **"General Information"** tab, right below the Currency field, you will find the **"Default Analytic Account (Company)"** field.

---

## Usage & Workflow

The module operates automatically when creating invoices or credit notes. The assignment logic follows this priority order (from highest to lowest):

### A. Automatic Assignment (On line creation)
When adding a line to an invoice (manually or automatically), the system looks for the analytic account in this order:

1.  **Invoice Header (Highest Priority):** If the *"General Analytic Account"* field on the invoice has a value, this is forced onto the new line.
2.  **Company (High Priority):** If there is no account in the header, the system looks for the account configured on the current **Company**.
3.  **User (Medium Priority):** If the company has no configuration, the system looks for the account configured on the current **User**.
4.  **Empty:** If none of the above conditions are met, the field is left empty.

### B. Mass Change on Invoice (Master Switch)
Inside an Invoice (Customer or Vendor), you will see a new field on the right side of the header (above the lines) called **"General Analytic Account"**.

* **Select an Account:** When you choose an account in this field, the module **immediately** updates all existing invoice lines, assigning 100% of the distribution to the selected account.
* **Remove the Account:** If you clear the value of this field, the module **recalculates** all lines, reverting them to their original default value (based on Company or User configuration).

## Technical Information

* **Technical Name:** `user_default_analytic_by_pridecta`
* **Dependencies:** `base`, `account`, `analytic`
* **Affected Models:**
    * `res.users` (Added `default_analytic_account_id` field)
    * `res.company` (Added `analytic_account_default_id` field)
    * `account.move` (`onchange` logic and `general_analytic_account_id` field)
    * `account.move.line` (`default_get` logic and `analytic_distribution`)

## Author

Developed by **Pridecta** for Odoo 18.