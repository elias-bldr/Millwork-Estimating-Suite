# script_writer.py  – drop this in verbatim
from typing import Dict, List
from models import Assembly, Part

ADD_PART_PROC = '''
procedure AddPart(AsmPath: String; ItemType: String; SKU: String; Descr: String; Qty: Double; CostEach: Double);
begin
  P := Planswift.NewItem(AsmPath, ItemType, 'Mat');

  Planswift.SetPropertyFormula(P.FullPath, 'Selected Item', SKU);
  Planswift.SetPropertyFormula(P.FullPath, 'SKU #', SKU);
  Planswift.SetPropertyFormula(P.FullPath, 'Cost Each', CostEach);
  Planswift.SetPropertyFormula(P.FullPath, 'Qty Per Count', Qty);
  Planswift.SetPropertyFormula(P.FullPath, 'Description', Descr);
  Planswift.SetPropertyFormula(P.FullPath, 'Name', '[..] - [Description]');
end;

'''

def write_psscript(assemblies: List[Assembly], out_path: str):
    with open(out_path, "w", newline="\n") as f:
        # 1. header
        f.write(ADD_PART_PROC)
        f.write("procedure Main;\n")
        f.write("var\n")
        f.write("  Asm: IItem;\n")
        f.write("  ToolCount: Integer;\n")
        f.write("begin\n")
        f.write("  ToolCount := 0;\n\n")

        # 1a. build each unique folder only once
        f.write("  // create top-level folders\n")
        folder_vars: Dict[str,str] = {}
        for asm in assemblies:
            fld = asm.folder.replace("'", "''")
            if fld not in folder_vars:
                # sanitize for a valid Pascal variable
                var = "fld_" + "".join(c if c.isalnum() else "_" for c in fld)
                folder_vars[fld] = var
                f.write(f"  {var} := Planswift.NewItem('\\Storages\\Local\\Templates\\Millwork Tool Template','Folder','{fld}');\n")
        f.write("\n")

        # 2. each assembly, reusing the pre-created folder
        for asm in assemblies:
            asm_name   = asm.name.replace("'", "''")
            asm_folder = asm.folder.replace("'", "''")
            var        = folder_vars[asm_folder]

            f.write(f"  // --- {asm_folder}\\{asm_name}\n")
            f.write(f"  Asm := Planswift.NewItem({var}.FullPath, 'Assembly', '{asm_name}');\n")
            f.write(f"  Planswift.SetPropertyFormula(Asm.FullPath, 'Qty Per Count', {asm.qty});\n")
            f.write(f"  ToolCount := ToolCount + 1;\n\n")
            f.write(f"  // {asm_name} parts:\n")

            for part in asm.parts:
                descr = part.descr.strip().replace("'", "''")
                f.write(
                    f"  AddPart(Asm.FullPath, '{part.item_type}', '{part.sku}', "
                    f"'{descr}', {part.qty}, {part.cost_each});\n"
                )
            f.write("\n")

        # 3. footer
        f.write("  ShowMessage(IntToStr(ToolCount) + ' assemblies created successfully.');\n")
        f.write("end;\n\nMain;\n")
