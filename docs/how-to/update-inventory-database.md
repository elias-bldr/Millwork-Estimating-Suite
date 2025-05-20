<!-- docs/how-to/update-inventory-database.md -->
# How-to: Update Inventory Costs

1. Open `inventory_costs.xlsx`.  
2. Edit **Cost_Each**; keep SKU unchanged.  
3. Save.

## Refresh assemblies

Re-run Assembly Builder **Build Batch**.  
Only assemblies with changed SKUs regenerate (hash diff).

!!! danger
    **Do not rename SKUs** in the sheet—assemblies reference SKU as key.

## Bump plugin version?

If > 25 % of SKUs change, create new plugin release (e.g. 2.1.0) and post on portal.

