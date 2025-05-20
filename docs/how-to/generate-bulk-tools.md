<!-- docs/how-to/generate-bulk-tools.md -->
# How-to: Generate Bulk Tools with Assembly Builder

### Scenario
Inventory prices updated → you need 800+ assemblies refreshed.

---

## 1 Update inventory source

`Settings ▸ Inventory file` → browse new Excel/CSV.

## 2 Build batch

Batch Group: STD_HOUSE_PACKAGE
SKUs linked: 823
Out-of-date assemblies: 17


Click **Generate Script**.

## 3 Run script in PlanSwift

`Tools ▸ Execute Script` → pick generated `.psscript`.

PlanSwift logs each insert to *Output* window.

## 4 Verify

*Run Cut List* → spot-check high-impact SKUs.

