import sys
import tkinter as tk
import warnings
from logging import getLogger
from tkinter import ttk
from typing import Any, Dict, List, Optional, Tuple, Union

from thonny import get_workbench, ui_utils
from thonny.languages import tr
from thonny.tktextext import TextFrame
from thonny.ui_utils import CommonDialog, MappingCombobox, ems_to_pixels

logger = getLogger(__name__)

LABEL_PADDING_EMS = 1
SEPARATOR_HEIGHT_EMS = 2


class ConfigurationDialog(CommonDialog):
    last_shown_tab_index = 0

    def __init__(self, master, page_records_with_order):
        super().__init__(master)
        self.title(tr("Thonny options"))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.backend_restart_required = False
        self.gui_restart_required = False

        main_frame = ttk.Frame(self)  # otherwise there is wrong color background with clam
        main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self._notebook = ttk.Notebook(main_frame)
        self._notebook.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky=tk.NSEW,
            padx=self.get_medium_padding(),
            pady=(self.get_medium_padding(), 0),
        )
        self._notebook.enable_traversal()
        if sys.platform == "darwin":
            # otherwise the new page content won't load immediately
            self._notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_idletasks(), True)

        self._ok_button = ttk.Button(main_frame, text=tr("OK"), command=self._ok, default="active")
        self._cancel_button = ttk.Button(main_frame, text=tr("Cancel"), command=self._cancel)
        self._ok_button.grid(
            row=1,
            column=1,
            padx=(0, self.get_medium_padding()),
            pady=(self.get_medium_padding(), self.get_medium_padding()),
        )
        self._cancel_button.grid(
            row=1,
            column=2,
            padx=(0, self.get_medium_padding()),
            pady=(self.get_medium_padding(), self.get_medium_padding()),
        )

        self._page_records = []
        for key, title, page_class, _ in sorted(
            page_records_with_order, key=lambda r: (r[3], r[0])
        ):
            try:
                spacer = ttk.Frame(self)
                spacer.rowconfigure(0, weight=1)
                spacer.columnconfigure(0, weight=1)
                page = page_class(spacer)
                page.key = key
                page.dialog = self
                self._page_records.append((key, title, page))
                page.grid(sticky=tk.NSEW, pady=(15, 10), padx=15)
                self._notebook.add(spacer, text=title)
            except Exception as e:
                logger.exception("Could not create configuration page %s", key, exc_info=e)

        self.bind("<Return>", self._ok, True)
        self.bind("<Escape>", self._cancel, True)

        self._notebook.select(self._notebook.tabs()[ConfigurationDialog.last_shown_tab_index])

    def select_page(self, key):
        for i, tab in enumerate(self._notebook.tabs()):
            if self._page_records[i][0] == key:
                self._notebook.select(tab)

    def _ok(self, event=None):
        for _, title, page in self._page_records:
            try:
                if page.apply() is False:
                    return
            except Exception:
                get_workbench().report_exception("Error when applying options in " + title)

        self.destroy()

    def _cancel(self, event=None):
        for _, title, page in self._page_records:
            try:
                page.cancel()
            except Exception:
                get_workbench().report_exception("Error when cancelling options in " + title)

        self.destroy()

    def destroy(self):
        ConfigurationDialog.last_shown_tab_index = self._notebook.index(self._notebook.select())
        super().destroy()


class ConfigurationPage(ttk.Frame):
    """This is an example dummy implementation of a configuration page.

    It's not required that configuration pages inherit from this class
    (can be any widget), but the class must have constructor with single parameter
    for getting the master."""

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.dialog = None  # type: Optional[ConfigurationDialog]

    def add_checkbox(
        self, flag_name, description, row=None, column=0, padx=0, pady=0, columnspan=1, tooltip=None
    ):
        warnings.warn(
            "Consider using thonny.config_ui.add_option_checkbox instead", DeprecationWarning
        )
        variable = get_workbench().get_variable(flag_name)
        checkbox = ttk.Checkbutton(self, text=description, variable=variable)
        checkbox.grid(
            row=row, column=column, sticky=tk.W, padx=padx, pady=pady, columnspan=columnspan
        )

        if tooltip is not None:
            ui_utils.create_tooltip(checkbox, tooltip)

    def add_combobox(
        self, variable, values, row=None, column=0, padx=0, pady=0, columnspan=1, width=None
    ):
        warnings.warn(
            "Consider using thonny.config_ui.add_option_combobox instead", DeprecationWarning
        )
        if isinstance(variable, str):
            variable = get_workbench().get_variable(variable)
        combobox = ttk.Combobox(
            self,
            exportselection=False,
            textvariable=variable,
            state="readonly",
            height=15,
            width=width,
            values=values,
        )
        combobox.grid(
            row=row, column=column, sticky=tk.W, pady=pady, padx=padx, columnspan=columnspan
        )
        return variable

    def add_entry(self, option_name, row=None, column=0, pady=0, padx=0, columnspan=1, **kw):
        warnings.warn(
            "Consider using thonny.config_ui.add_option_entry instead", DeprecationWarning
        )
        variable = get_workbench().get_variable(option_name)
        entry = ttk.Entry(self, textvariable=variable, **kw)
        entry.grid(row=row, column=column, sticky=tk.W, pady=pady, columnspan=columnspan, padx=padx)

    def apply(self):
        """Apply method should return False, when page contains invalid
        input and configuration dialog should not be closed."""
        pass

    def cancel(self):
        """Called when dialog gets cancelled"""
        pass


def add_option_checkbox(
    master: tk.Widget,
    option_name: str,
    description: str,
    row: Optional[int] = None,
    column: int = 0,
    columnspan: int = 3,
    pady: Union[Tuple, int, str] = 0,
    padx: Union[Tuple, int, str] = 0,
    tooltip: Optional[str] = None,
) -> ttk.Checkbutton:
    if row is None:
        row = master.grid_size()[1]
    variable = get_workbench().get_variable(option_name)

    checkbox = ttk.Checkbutton(master, text=description, variable=variable)
    checkbox.grid(row=row, column=column, columnspan=columnspan, sticky=tk.W, padx=padx, pady=pady)

    return checkbox


def add_option_combobox(
    master: tk.Widget,
    option_name: str,
    description: str,
    choices: Union[List[Any], Dict[str, Any]],
    height: int = 15,
    width: Optional[int] = None,
    row: Optional[int] = None,
    column: int = 0,
    label_columnspan: int = 1,
    label_pady: Union[Tuple, int, str] = 0,
    label_padx: Union[Tuple, int, str, None] = None,
    combobox_columnspan: int = 1,
    combobox_pady: Union[Tuple, int, str] = 0,
    combobox_padx: Union[Tuple, int, str] = 0,
    tooltip: Optional[str] = None,
) -> ttk.Combobox:
    if row is None:
        row = master.grid_size()[1]

    if label_padx is None:
        label_padx = (0, ems_to_pixels(LABEL_PADDING_EMS))

    label = ttk.Label(master, text=description)
    label.grid(
        row=row, column=0, columnspan=label_columnspan, sticky="w", pady=label_pady, padx=label_padx
    )

    if isinstance(choices, list):
        mapping = {str(x): x for x in choices}
    else:
        assert isinstance(choices, dict)
        mapping = choices

    variable = get_workbench().get_variable(option_name)
    combobox = MappingCombobox(
        master,
        mapping=mapping,
        exportselection=False,
        value_variable=variable,
        height=height,
        width=width,
    )
    combobox.grid(
        row=row,
        column=column + 1,
        columnspan=combobox_columnspan,
        sticky="w",
        pady=combobox_pady,
        padx=combobox_padx,
    )

    return combobox


def add_option_entry(
    master: tk.Widget,
    option_name: str,
    description: str,
    width: Optional[int] = None,
    row: Optional[int] = None,
    column: int = 0,
    label_columnspan: int = 1,
    label_pady: Union[Tuple, int, str] = 0,
    label_padx: Union[Tuple, int, str, None] = None,
    entry_columnspan: int = 1,
    entry_pady: Union[Tuple, int, str] = 0,
    entry_padx: Union[Tuple, int, str] = 0,
    tooltip: Optional[str] = None,
) -> ttk.Entry:
    if row is None:
        row = master.grid_size()[1]

    if label_padx is None:
        label_padx = (0, ems_to_pixels(LABEL_PADDING_EMS))

    label = ttk.Label(master, text=description)
    label.grid(
        row=row, column=0, columnspan=label_columnspan, sticky="w", pady=label_pady, padx=label_padx
    )

    variable = get_workbench().get_variable(option_name)
    entry = ttk.Entry(
        master,
        textvariable=variable,
        width=width,
    )
    entry.grid(
        row=row,
        column=column + 1,
        columnspan=entry_columnspan,
        sticky="w",
        pady=entry_pady,
        padx=entry_padx,
    )

    return entry


def add_option_box_for_list_of_strings(
    master: tk.Widget,
    option_name: str,
    description: str,
    height: int = 15,
    width: Optional[int] = None,
    row: Optional[int] = None,
    column: int = 0,
    label_columnspan: int = 3,
    label_pady: Union[Tuple, int, str] = 0,
    label_padx: Union[Tuple, int, str] = 0,
    box_columnspan: int = 3,
    box_pady: Union[Tuple, int, str] = 0,
    box_padx: Union[Tuple, int, str] = 0,
    tooltip: Optional[str] = None,
) -> TextFrame:
    if row is None:
        row = master.grid_size()[1]

    label = ttk.Label(master, text=description)
    label.grid(
        row=row, column=0, columnspan=label_columnspan, sticky="w", pady=label_pady, padx=label_padx
    )

    text_frame = TextFrame(
        master,
        horizontal_scrollbar_class=ui_utils.AutoScrollbar,
        wrap="none",
        font="TkDefaultFont",
        # cursor="arrow",
        padx=ems_to_pixels(0.3),
        pady=ems_to_pixels(0.3),
        height=height,
        width=width,
        borderwidth=1,
        undo=True,
        relief="groove",
    )
    text_frame.grid(
        row=row + 1,
        column=column,
        columnspan=box_columnspan,
        sticky="nsew",
        pady=box_pady,
        padx=box_padx,
    )

    lines = get_workbench().get_option(option_name, [])
    text_frame.text.insert("1.0", "\n".join(lines) + "\n")

    return text_frame


def add_text_row(
    master: tk.Widget,
    description: str,
    font: Union[str, tk.font.Font] = "TkDefaultFont",
    row: Optional[int] = None,
    column: int = 0,
    columnspan: int = 3,
    pady: Union[Tuple, int, str] = 0,
    padx: Union[Tuple, int, str] = 0,
) -> ttk.Label:
    if row is None:
        row = master.grid_size()[1]

    label = ttk.Label(master, text=description, font=font)
    label.grid(row=row, column=column, columnspan=columnspan, sticky="w", pady=pady, padx=padx)

    return label


def add_vertical_separator(
    master: tk.Widget,
    row: Optional[int] = None,
    column: int = 0,
    height: Union[str, int, None] = None,
) -> ttk.Frame:
    if row is None:
        row = master.grid_size()[1]

    if height is None:
        height = ems_to_pixels(SEPARATOR_HEIGHT_EMS)

    frame = ttk.Frame(master, height=height, width="1c")
    frame.grid(row=row, column=column)

    return frame
