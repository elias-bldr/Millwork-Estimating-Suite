<!-- docs/getting-started/quick-start-assembly-builder.md -->
# Quick-start · Assembly Builder

Goal: regenerate assemblies when inventory costs change and import them in bulk.

## 1 Launch & connect database

1. Start **Assembly Builder**.  
2. *Settings ▸ Inventory source* → point to `\\shared\inventory_costs.xlsx` (or local).

## 2 Generate scripts

* Click **Build Batch** ▸ choose *STD HOUSE PACKAGE*.  
* App outputs `export\MillworkAssemblies_2025-05-16.psscript`.

## 3 Import into PlanSwift

1. PlanSwift ► *Tools* ▸ **Execute Script** → select the `.psscript`.
2. Check *Takeoff* panel: existing items update, new ones appear.

!!! info
    Assembly Builder skips identical rows (hash match) for speed.

## 4 Verify pricing

Run *Segment Cost* report; totals should match updated inventory.

Next: learn [Generate bulk tools](../how-to/generate-bulk-tools.md).
