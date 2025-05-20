<!-- docs/reference/cli-options.md -->
# Assembly Builder CLI

```bash
assembly_builder.exe build ^
  --inventory C:\data\inventory_costs.xlsx ^
  --group STD_HOUSE_PACKAGE ^
  --out C:\export\assemblies.psscript ^
  --skip-unchanged
Flag	Default	Description
--inventory	inventory_costs.xlsx	Source price sheet
--group	ALL	Batch group
--out	assemblies.psscript	Output path
--skip-unchanged	false	Hash diff optimization