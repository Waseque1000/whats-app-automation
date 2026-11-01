"""Reusable styled dark table view built on ttk.Treeview with scrollbars."""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import List, Tuple, Dict, Any, Optional, Callable
from app.ui import theme


class TableView(ctk.CTkFrame):
    """Premium dark-themed data table widget with custom TTK styling."""

    def __init__(
        self,
        master,
        columns: List[Tuple[str, str, int]],  # (col_id, heading_text, width)
        on_select: Optional[Callable[[Dict[str, Any]], None]] = None,
        multi_select: bool = False,
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color=theme.COLOR_CARD,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=12,
            **kwargs,
        )
        self.columns_def = columns
        self.on_select_callback = on_select
        self.multi_select = multi_select
        self.rows_data: List[Dict[str, Any]] = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._init_treeview()

    def _init_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")

        # ── Treeview Body ─────────────────────────────────────────────────────
        style.configure(
            "Premium.Treeview",
            background=theme.COLOR_TABLE_BG,
            foreground=theme.COLOR_TEXT,
            fieldbackground=theme.COLOR_TABLE_BG,
            borderwidth=0,
            rowheight=38,
            font=(theme.FONT_FAMILY, 12),
        )
        style.map(
            "Premium.Treeview",
            background=[("selected", theme.COLOR_TABLE_SEL_BG)],
            foreground=[("selected", theme.COLOR_TABLE_SEL_FG)],
        )
        # Remove the focus dotted border
        style.layout("Premium.Treeview", [
            ("Premium.Treeview.treearea", {"sticky": "nswe"})
        ])

        # ── Column Headings ───────────────────────────────────────────────────
        style.configure(
            "Premium.Treeview.Heading",
            background=theme.COLOR_TABLE_HEADER,
            foreground=theme.COLOR_TEXT_MUTED,
            borderwidth=0,
            relief="flat",
            font=(theme.FONT_FAMILY, 11, "bold"),
            padding=(8, 10),
        )
        style.map(
            "Premium.Treeview.Heading",
            background=[("active", theme.COLOR_CARD_HOVER)],
            foreground=[("active", theme.COLOR_TEXT)],
        )

        # ── Scrollbar Styling ─────────────────────────────────────────────────
        style.configure(
            "Premium.Vertical.TScrollbar",
            background=theme.COLOR_CARD,
            troughcolor=theme.COLOR_TABLE_BG,
            borderwidth=0,
            arrowsize=12,
        )
        style.configure(
            "Premium.Horizontal.TScrollbar",
            background=theme.COLOR_CARD,
            troughcolor=theme.COLOR_TABLE_BG,
            borderwidth=0,
            arrowsize=12,
        )

        col_ids = [col[0] for col in self.columns_def]
        select_mode = "extended" if self.multi_select else "browse"

        self.tree = ttk.Treeview(
            self,
            columns=col_ids,
            show="headings",
            selectmode=select_mode,
            style="Premium.Treeview",
        )

        for col_id, heading, width in self.columns_def:
            self.tree.heading(col_id, text=f"  {heading}", anchor="w")
            self.tree.column(col_id, width=width, anchor="w", stretch=True, minwidth=40)

        # Scrollbars
        vsb = ttk.Scrollbar(
            self, orient="vertical", command=self.tree.yview,
            style="Premium.Vertical.TScrollbar",
        )
        hsb = ttk.Scrollbar(
            self, orient="horizontal", command=self.tree.xview,
            style="Premium.Horizontal.TScrollbar",
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(1, 0), pady=(1, 0))
        vsb.grid(row=0, column=1, sticky="ns", pady=(1, 0), padx=(0, 1))
        hsb.grid(row=1, column=0, sticky="ew", padx=(1, 0), pady=(0, 1))

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _on_tree_select(self, event):
        if not self.on_select_callback:
            return
        selected_items = self.tree.selection()
        if not selected_items:
            return
        item_id = selected_items[0]
        idx = int(self.tree.item(item_id, "text") or 0)
        if 0 <= idx < len(self.rows_data):
            self.on_select_callback(self.rows_data[idx])

    def set_data(self, records: List[Dict[str, Any]]):
        """Populates the table with data records."""
        self.clear()
        self.rows_data = records

        col_ids = [col[0] for col in self.columns_def]
        for idx, rec in enumerate(records):
            values = [rec.get(col_id, "") for col_id in col_ids]
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", "end", text=str(idx), values=values, tags=(tag,))

        self.tree.tag_configure("even", background=theme.COLOR_TABLE_BG)
        self.tree.tag_configure("odd",  background=theme.COLOR_TABLE_STRIPE)

    def get_selected_records(self) -> List[Dict[str, Any]]:
        """Returns all currently selected row records."""
        selected_ids = self.tree.selection()
        results = []
        for item_id in selected_ids:
            try:
                idx = int(self.tree.item(item_id, "text"))
                if 0 <= idx < len(self.rows_data):
                    results.append(self.rows_data[idx])
            except (ValueError, IndexError):
                continue
        return results

    def clear(self):
        """Clears all table rows."""
        self.rows_data = []
        for item in self.tree.get_children():
            self.tree.delete(item)
