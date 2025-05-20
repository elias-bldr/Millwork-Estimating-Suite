# gui.py  – persistent & bulk‑SKU version
import os, json, pathlib
import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk       # pip install ttkbootstrap
from core.models import Assembly, Part
import core.db, core.script_writer
import re
import sys, shutil
from pathlib import Path
import os

# find the OS-appropriate per-user data dir
if os.name == 'nt':
    base = Path(os.getenv('APPDATA', Path.home() / 'AppData' / 'Roaming'))
else:
    # macOS: ~/Library/Application Support
    # Linux:  ~/.config
    base = Path(os.getenv('XDG_CONFIG_HOME', Path.home() / '.config'))

APP_DIR  = base / "Millwork BOM Builder"
APP_FILE = APP_DIR / "assemblies.json"

def resource_path(rel_path: str) -> Path:
    """
    Return the path to a bundled file (in _MEIPASS when frozen,
    or in src/resources when running normally).
    """
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent / "resources"
    return base_path / rel_path

# make sure the folder exists
APP_DIR.mkdir(parents=True, exist_ok=True)

# if no per-user file yet, seed it from our bundled default
if not APP_FILE.exists():
    default = resource_path("assemblies.json")
    if default.exists():
        shutil.copy(default, APP_FILE)

FOLDER_CHOICES = ["Exterior Doors", "Interior Doors", "Base", "Casing", "Closets", "Stairs", "Hardware", "Misc"]

# mapping from dataset → PlanSwift ItemType
TYPE_MAP = {
    "Inventory": "Material",
    "MW Labor":  "Labor",
    "Install":   "Subcontract"
    # anything else → "Other"
}

# ------------------------------------------------------------
# Helper functions to persist assemblies
# ------------------------------------------------------------
def save_assemblies(assemblies: list[Assembly]):
    data = [
        {
            "name": a.name,
            "folder": a.folder,
            "qty":    a.qty,
            "parts": [p.__dict__ for p in a.parts]
        } for a in assemblies
    ]
    APP_FILE.write_text(json.dumps(data, indent=2))

def load_assemblies() -> list[Assembly]:
    if not APP_FILE.exists():
        return []
    try:
        raw = json.loads(APP_FILE.read_text())
        return [
            Assembly(
                name   = o["name"],
                folder = o.get("folder","Misc"),
                qty    = float(o.get("qty", 1.0)),
                parts  = [Part(**p) for p in o["parts"]]
                )
                for o in raw]
    except (ValueError, KeyError):
        messagebox.showwarning("Corrupt file",
                               "Saved assemblies file is corrupt; starting fresh.")
        return []

# ------------------------------------------------------------
class BomBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(str(resource_path("assemblybuilder.ico")))
        self.title("Millwork Assembly Builder")
        self.geometry("1040x700")            # a little taller for bulk window

        # ---- Data source ----
        self.inv = core.db.load_inventory()
        self.lab = core.db.load_labor()
        self.ins = core.db.load_install()
        self.ext = core.db.load_external()

        # ---- State ----
        self.assemblies: list[Assembly] = load_assemblies()
        self._visible_assemblies: list[Assembly] = []
        self.folder_filter = tk.StringVar(value="All")
        self.cost_each = 0.0
        self.descr     = ""
        self.editing_idx = None
        # store a handle to the Add button so we can change its text:
        self.add_btn = None


        self._build_ui()
        self._populate_asm_list()
        self._update_ds_view()

    # ------------------------------------------------ UI build
    def _build_ui(self):
        left = ttk.Frame(self); left.pack(side="left", fill="y", padx=8, pady=8)
        right= ttk.Frame(self); right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        # just before the Listbox…
        ttk.Label(left, text="Filter by Folder:").pack(pady=(0,2))
        filter_cb = ttk.Combobox(
            left,
            textvariable=self.folder_filter,
            values=["All"] + FOLDER_CHOICES,
            state="readonly",
            width=28
        )
        filter_cb.pack()
        filter_cb.bind("<<ComboboxSelected>>", lambda e: self._populate_asm_list())

        # Assembly list
        ttk.Label(left, text="Assemblies").pack(pady=(0,4))
        self.asm_lb = tk.Listbox(left, width=30, height=28, selectmode="extended")
        self.asm_lb.pack(fill="y", expand=True)
        ttk.Button(left, text="+ New Assembly", command=self._add_assembly).pack(pady=4)
        ttk.Button(left, text="Delete Assembly", command=self._del_assembly).pack()
        ttk.Button(left, text="Bulk Add SKUs ▶", command=self._open_bulk_win)\
            .pack(pady=(20,0))                     # Bonus feature button

        # Part‑editor frame
        editor = ttk.Labelframe(right, text="Part Editor", padding=10)
        editor.pack(fill="x")

        self.item_type = tk.StringVar(value="Inventory")
        ttk.Label(editor, text="Dataset").grid(row=0, column=0, sticky="e")
        self.type_cb = ttk.Combobox(editor, textvariable=self.item_type,
                                    values=["Inventory","MW Labor","Install","External"],
                                    state="readonly", width=18)
        self.type_cb.grid(row=0, column=1, padx=5)
        self.type_cb.bind("<<ComboboxSelected>>", lambda e: self._update_ds_view())

        ttk.Label(editor, text="SKU").grid(row=1, column=0, sticky="e", pady=4)
        self.sku_entry = ttk.Entry(editor, width=25)
        self.sku_entry.grid(row=1, column=1, padx=5, pady=4)
        self.sku_entry.bind("<Return>", lambda e: self._lookup_sku())

        ttk.Button(editor, text="Lookup", command=self._lookup_sku).grid(row=1, column=2, padx=4)

        ttk.Label(editor, text="Qty").grid(row=2, column=0, sticky="e")
        self.qty_entry = ttk.Entry(editor, width=10)
        self.qty_entry.insert(0, "1")
        self.qty_entry.grid(row=2, column=1, sticky="w")

        # Dataset Treeview
        ds_frame = ttk.Labelframe(editor, text="Data Browser", padding=4)
        ds_frame.grid(row=0, column=3, rowspan=3, padx=(15,0))
        self.ds_tv = ttk.Treeview(ds_frame, columns=("sku","descr","cost"), show="headings", height=8)
        for c, w in [("sku",110),("descr",230),("cost",80)]:
            self.ds_tv.heading(c, text=c.upper())
            self.ds_tv.column(c, width=w, anchor="w")
        self.ds_tv.pack(side="left", fill="both", expand=True)
        self.ds_tv.bind("<<TreeviewSelect>>", self._on_dataset_select)
        ttk.Scrollbar(ds_frame, orient="vertical", command=self.ds_tv.yview)\
            .pack(side="right", fill="y")
        self.ds_tv.configure(yscrollcommand=lambda *a:None)

        self.add_btn = ttk.Button(editor, text="Add Part", command=self._add_part)
        self.add_btn.grid(row=3, column=1, pady=6)

        # Parts table
        self.parts_tv = ttk.Treeview(right,
                                     columns=("type","sku","qty","cost","descr"),
                                     show="headings", height=13)
        for c in ("type","sku","qty","cost","descr"):
            self.parts_tv.heading(c, text=c.capitalize())
            self.parts_tv.column(c, width=100 if c!="descr" else 240, anchor="w")
        self.parts_tv.pack(fill="both", expand=True, pady=6)
        
        self.parts_tv.bind("<<TreeviewSelect>>", self._on_part_select)

        ttk.Button(right, text="Generate PlanSwift Script", command=self._generate).pack(pady=4)
        ttk.Button(right, text="Delete Part", command=self._del_part).pack(pady=4)

        self.asm_lb.bind("<<ListboxSelect>>", lambda e: self._refresh_parts())

    # ------------------------------------------------ Assembly list helpers
    def _populate_asm_list(self):
        self.asm_lb.delete(0, tk.END)
        self._visible_assemblies.clear()
        filt = self.folder_filter.get()
        for a in self.assemblies:
            if filt == "All" or a.folder == filt:
                self._visible_assemblies.append(a)
                self.asm_lb.insert(tk.END, a.name)
        # clear details if nothing selected
        self._refresh_parts()

    def _selected_assemblies(self) -> list[Assembly]:
        idxs = self.asm_lb.curselection()
        return [self._visible_assemblies[i] for i in idxs]

    def _add_assembly(self):
        dlg = tk.Toplevel(self); dlg.title("New Assembly")
        dlg.grab_set()                         # modal

        ttk.Label(dlg, text="Assembly name:").grid(row=0, column=0, pady=(8,4), padx=6, sticky="e")
        name_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=name_var, width=28).grid(row=0, column=1, pady=(8,4), padx=6)

        ttk.Label(dlg, text="Qty:").grid(row=1, column=0, sticky="e", padx=6)
        qty_var = tk.StringVar(value="1")
        ttk.Entry(dlg, textvariable=qty_var, width=10).grid(row=1, column=1, padx=6, pady=4)

        ttk.Label(dlg, text="Folder:").grid(row=2, column=0, sticky="e", padx=6)
        self._last_folder = getattr(self, "_last_folder", "Misc")
        folder_var = tk.StringVar(value=self._last_folder)
        ttk.Combobox(dlg, textvariable=folder_var,
                     values=FOLDER_CHOICES, state="readonly", width=26).grid(row=2, column=1, padx=6, pady=4)

        def _ok():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Required", "Name cannot be blank.");
                return
            
            try:
                qty = float(qty_var.get())
            except ValueError:
                qty = 1.0

            asm = Assembly(name=name, folder=folder_var.get(), qty=qty)

            self.assemblies.append(asm)
            self._last_folder = folder_var.get()        # remember last choice
            save_assemblies(self.assemblies)
            self._populate_asm_list()
            dlg.destroy()

        ttk.Button(dlg, text="Create", command=_ok).grid(row=3, column=1, pady=8, sticky="e")

    def _del_assembly(self):
        sel = self.asm_lb.curselection()
        if not sel:
            return
        # grab the real object from visible list
        asm = self._visible_assemblies[sel[0]]
        asm_name = asm.name
        if not messagebox.askyesno("Confirm delete",
                                   f"Delete assembly '{asm_name}'?"):
            return
        self.assemblies.remove(asm)
        save_assemblies(self.assemblies)
        self._populate_asm_list()
        self.parts_tv.delete(*self.parts_tv.get_children())

    def _del_part(self):
        # Gather all selected assemblies
        selected_asms = self._selected_assemblies()
        if not selected_asms:
            messagebox.showerror("No assembly", "Select one or more assemblies first.")
            return

        # Which row in the parts table is selected?
        sel = self.parts_tv.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a part to delete.")
            return
        part_idx = self.parts_tv.index(sel[0])

        # Confirm delete
        part = selected_asms[0].parts[part_idx]  # use first for the message
        if not messagebox.askyesno(
            "Confirm delete",
            f"Delete part {part.sku} ({part.item_type}), qty {part.qty} from ALL selected assemblies?"
        ):
            return

        # Now delete that index from each selected assembly (if it exists)
        for asm in selected_asms:
            if part_idx < len(asm.parts):
                del asm.parts[part_idx]
                # re-consolidate in case you want to collapse duplicates
                self._consolidate_parts(asm)

        save_assemblies(self.assemblies)
        self._refresh_parts()

    def _selected_asm(self) -> Assembly | None:
        sel = self.asm_lb.curselection()
        if not sel:
            return None
        return self._visible_assemblies[sel[0]]

    # ------------------------------------------------ Dataset browser + lookup
    def _update_ds_view(self):
        df = {"Inventory": self.inv, "MW Labor": self.lab,
              "Install": self.ins,  "External": self.ext}[self.item_type.get()]
        self.ds_tv.delete(*self.ds_tv.get_children())
        for sku, row in df.iterrows():
            self.ds_tv.insert("", "end",
                              values=(sku, row["Description"], row["Cost Each"]))

    def _on_dataset_select(self, _):
        sel = self.ds_tv.selection()
        if not sel:
            return
        sku, descr, cost = self.ds_tv.item(sel[0], "values")
        self._fill_entry_fields(sku, descr, cost)

    # --- Manual SKU lookup (search ALL datasets) ------------
    def _lookup_sku(self):
        code = self.sku_entry.get().strip()
        if not code:
            return
        for df in (self.inv, self.lab, self.ins, self.ext):
            if code in df.index:
                row = df.loc[code]
                self._fill_entry_fields(code, row["Description"], row["Cost Each"])
                return
        messagebox.showwarning("Not found", f"{code} not found in any dataset.")

    def _fill_entry_fields(self, sku, descr, cost):
        self.sku_entry.delete(0, tk.END); self.sku_entry.insert(0, sku)
        self.cost_each = float(cost) if str(cost).strip() else 0.0
        self.descr     = descr
        self.qty_entry.focus_set()

    def _on_part_select(self, _event):
        asm = self._selected_asm()
        if not asm:
            return

        sel = self.parts_tv.selection()
        if not sel:
            return
        tree_iid = sel[0]
        idx = self.parts_tv.index(tree_iid)
        self.editing_idx = idx

        part = asm.parts[idx]
        # reverse-map item_type to your dataset names
        inv = {v:k for k,v in TYPE_MAP.items()}
        ds_name = inv.get(part.item_type, "External")  # fallback

        # populate the controls
        self.item_type.set(ds_name)
        self._update_ds_view()       # reload dataset browser to match combobox
        self.sku_entry.delete(0, tk.END)
        self.sku_entry.insert(0, part.sku)
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, str(part.qty))
        # store cost/descr so your next add will pick them up
        self.cost_each = part.cost_each
        self.descr     = part.descr

        # flip button into “Update”
        self.add_btn.config(text="Update Part")

    # ------------------------------------------------ Parts table actions
    def _add_part(self):
        asms = self._selected_assemblies()
        if not asms:
            messagebox.showerror("No assembly", "Select one or more assemblies first.")
            return

        try:
            qty = float(self.qty_entry.get())
        except ValueError:
            qty = 1.0

        sku = self.sku_entry.get().strip()
        # Look up cost & descr in whichever dataframe contains it:
        for df_name, df in [
            ("Inventory", self.inv),
            ("MW Labor",  self.lab),
            ("Install",   self.ins),
            ("External",  self.ext)
        ]:
            if sku in df.index:
                row = df.loc[sku]
                self.cost_each = float(row["Cost Each"])
                self.descr     = row["Description"]
                ps_type = TYPE_MAP.get(df_name, "Other")
                break
        else:
            # if no dataframe had the SKU, fall back to "Other"
            ps_type = "Other"

        new_part = Part(ps_type, sku, qty, self.cost_each, self.descr)

        for asm in asms:
            if self.editing_idx is not None and len(asms) == 1:
                asm.parts[self.editing_idx] = new_part
            else:
                for p in asm.parts:
                    if (p.sku, p.item_type) == (new_part.sku, new_part.item_type):
                        p.qty += new_part.qty
                        break
                else:
                    asm.parts.append(new_part)
            self._consolidate_parts(asm)

        self.editing_idx = None
        self.add_btn.config(text="Add Part")
        save_assemblies(self.assemblies)
        self._refresh_parts()

    def _consolidate_parts(self, asm):
        """
        Merge any parts with the same (item_type,sku,cost_each,descr) by summing qty.
        """
        merged = {}
        for p in asm.parts:
            key = (p.item_type, p.sku, p.cost_each, p.descr)
            if key in merged:
                merged[key].qty += p.qty
            else:
                # clone to avoid mutating the original
                merged[key] = Part(p.item_type, p.sku, p.qty, p.cost_each, p.descr)
        asm.parts[:] = merged.values()

    def _refresh_parts(self):
        # whenever you refresh the parts list:
        self.editing_idx = None
        self.add_btn.config(text="Add Part")
        self.parts_tv.delete(*self.parts_tv.get_children())
        asm = self._selected_asm()
        if not asm: return
        for p in asm.parts:
            self.parts_tv.insert("", "end", values=(
                p.item_type, p.sku, p.qty,
                f"{p.cost_each:.2f}", p.descr))

    # ------------------------------------------------ Bulk Add window
    def _open_bulk_win(self):
        asms = self._selected_assemblies()
        if not asms:
            messagebox.showerror("No assembly", "Select one or more assemblies first.")
            return

        win = tk.Toplevel(self); win.title("Bulk add SKUs with Qty")
        ttk.Label(
            win,
            text="Paste one SKU per line.  Separate qty with comma, tab or space.\n"
                 "Example:  1012LBRKTW , 12",
            justify="left"
        ).pack(padx=8, pady=6)

        txt = tk.Text(win, width=60, height=14)
        txt.pack(padx=8, pady=4)

        def parse_qty(token: str) -> float:
            try:
                return float(token)
            except ValueError:
                return 1.0

        def _bulk_add():
            raw_lines = txt.get("1.0", "end").strip().splitlines()
            added = 0
            for asm in asms:
                for line in raw_lines:
                    if not line.strip():
                        continue
                    parts = [tok for tok in re.split(r"[, \t]+", line.strip()) if tok]
                    sku = parts[0]
                    qty = float(parts[1]) if len(parts) > 1 else 1.0

                    for df_name, df in [
                        ("Inventory", self.inv),
                        ("MW Labor",  self.lab),
                        ("Install",   self.ins),
                        ("External",  self.ext)
                    ]:
                        if sku in df.index:
                            row     = df.loc[sku]
                            ps_type = TYPE_MAP.get(df_name, "Other")
                            asm.parts.append(
                                Part(ps_type, sku, qty,
                                    float(row["Cost Each"]), row["Description"])
                            )
                            added += 1
                            break
                self._consolidate_parts(asm)

            if added:
                save_assemblies(self.assemblies)
                self._refresh_parts()
            messagebox.showinfo("Bulk add", f"Added {added} parts.")
            win.destroy()

        ttk.Button(win, text="Add to Assembly", command=_bulk_add).pack(pady=6)

    # ------------------------------------------------ Output
    def _generate(self):
        if not self.assemblies:
            messagebox.showwarning("Nothing to write", "No assemblies.")
            return

        # figure out which folder the user has selected
        folder = self.folder_filter.get()

        # only grab those assemblies in that folder (or all, if “All”)
        to_export = [
            asm
            for asm in self.assemblies
            if folder == "All" or asm.folder == folder
        ]

        if not to_export:
            messagebox.showwarning(
                "Nothing to write",
                f"No assemblies in the “{folder}” folder."
            )
            return

        # build your filename & path exactly as you already do
        safe = "".join(c for c in folder if c.isalnum()) if folder != "All" else "All"
        base_dir = r"C:\Program Files (x86)\PlanSwift10\Data\Plugins\Create Tools"
        os.makedirs(base_dir, exist_ok=True)
        filename = f"Import{safe}Assemblies.psscript"
        out = os.path.join(base_dir, filename)

        # hand only the filtered list to your writer
        core.script_writer.write_psscript(to_export, out)
        messagebox.showinfo("Done", f"Script saved to:\n{out}")

def main():
    BomBuilder().mainloop()

if __name__ == "__main__":
    main()
