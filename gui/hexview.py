# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import sys
import enum
import pprint
import data
import data as mydata
import functions
import components

from .templates import *
from .stylesheets import *

class HexView(data.QFrame):
    # Class variables
    name             = None
    _parent          = None
    main_form        = None
    current_icon     = None
    icon_manipulator = None
    savable          = data.CanSave.NO
    save_name        = None
    # Reference to the custom context menu
    context_menu     = None
    
    def __init__(self, file_path, parent, main_form):
        super().__init__(parent)
        self.name = os.path.basename(file_path)
        self.save_name = file_path
        self._parent = parent
        self.main_form = main_form
        
        self.current_icon = functions.create_icon('various/node_template.png')
        self.icon_manipulator = components.IconManipulator(
            parent=self, tab_widget=parent
        )
        self.icon_manipulator.update_icon(self)
        
        # Initialize widgets
        self.__initialize_view()
        
        # Update style
        self.update_style()
        
        # Show the file data
        self.reload_file()
    
    def __initialize_view(self):
        # Initialize view element caches
        self.__cache_views = {}
        self.__cache_labels = {}
        self.__cache_buttons = {}
        self.__cache_comboboxes = {}
        
        # Layout
        layout = create_layout(layout=LayoutType.Vertical)
        layout.setSizeConstraint(data.QLayout.SizeConstraint.SetNoConstraint)
        self.setLayout(layout)
        
        # Scroll area
        scroll_area = create_scroll_area()
        layout.addWidget(scroll_area)
        # Main view
        main_view = create_groupbox_with_layout(
            parent=self,
            name="HexMainView",
            borderless=True,
            layout=LayoutType.Vertical,
        )
        scroll_area.setWidget(main_view)
        self.__cache_views["main"] = main_view
        main_layout = main_view.layout()
        
        # Function for adding items
#        def add_items(button_groups, parent, in_layout):
#            for g,d in button_groups.items():
#                # Add group
#                new_group = wg.create_groupbox_with_layout(
#                    parent=parent,
#                    name=g,
#                    borderless=True,
#                    vertical=False,
#                    margins=(2,2,2,2),
#                    spacing=2,
#                    h_size_policy=data.QSizePolicy.Policy.Fixed,
#                    v_size_policy=data.QSizePolicy.Policy.Fixed,
#                )
#                in_layout.addWidget(new_group)
#                self.__cache_views[g] = new_group
#                
#                # Add the comboboxes, if any
#                if "comboboxes" in d.keys():
#                    for k,v in d["comboboxes"].items():
#                        new_combobox = wg.create_advancedcombobox(
#                            parent=new_group,
#                            no_selection_text=v["initial-text"],
#                        )
#                        if "items" in v.keys():
#                            for cbi in v["items"]:
#                                new_combobox.add_item(cbi)
#                        if "selected-item" in v.keys():
#                            new_combobox.set_selected_name(v["selected-item"])
#                        if v["disabled"] == True:
#                            new_combobox.disable()
#                        self.__cache_comboboxes[v["name"]] = new_combobox
#                        new_group.layout().addWidget(new_combobox)
#                        new_group.layout().setAlignment(
#                            new_combobox,
#                            data.Qt.AlignmentFlag.AlignLeft | data.Qt.AlignmentFlag.AlignVCenter
#                        )
#                    
#                # Add buttons to group
#                for k,v in d["buttons"].items():
#                    if "icon-path" in v.keys() or "icon" in v.keys():
#                        new_button = wg.create_pushbutton(
#                            parent=new_group,
#                            name=v["name"],
#                            icon_name=v["icon-path"],
#                            tooltip=v["tooltip"],
#                            statustip=v["tooltip"],
#                            click_func=v["click-func"],
#                            disabled=v["disabled"],
#                            style="debugger",
#                        )
#                    else:
#                        new_button = wg.create_pushbutton(
#                            parent=new_group,
#                            name=v["name"],
#                            text=v["text"],
#                            tooltip=v["tooltip"],
#                            statustip=v["tooltip"],
#                            click_func=v["click-func"],
#                            disabled=v["disabled"],
#                            style="debugger",
#                        )
#                    self.__cache_buttons[v["name"]] = new_button
#                    new_group.layout().addWidget(new_button)
#                    new_group.layout().setAlignment(
#                        new_button,
#                        data.Qt.AlignmentFlag.AlignLeft | data.Qt.AlignmentFlag.AlignVCenter
#                    )
        
        # Table cache
        self.cache_table = {}
        
        ## Main table
        new_table = HexTable(self, self.main_form)
        new_table.setObjectName("MainTable")
        tooltip = "This table is used for displaying hex data."
        new_table.setToolTip(tooltip)
        new_table.setStatusTip(tooltip)
        main_layout.addWidget(new_table)
        self.cache_table["main"] = new_table
    
    
    """
    Events
    """
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.main_form.view.indication_check()
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.main_form.view.indication_check()
        self.main_form.last_focused_widget = self._parent
    
    def hasFocus(self):
        return self.cache_table["main"].hasFocus()
    
    
    """
    General
    """
    def show_file_hex_data(self, byte_data):
        table = self.cache_table["main"]
        
        # Clean the model
        model = table.model()
        if model is not None:
            table.setModel(None)
            model.deleteLater()
        
        # Table Settings
        table.verticalHeader().hide()
        table.setSelectionBehavior(data.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(data.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(data.QAbstractItemView.SelectionMode.SingleSelection)
#        table.itemSelectionChanged.connect(self._table_selection_changed)
#        table.itemClicked.connect(self._table_item_clicked)
        
        table.setSortingEnabled(False)
        table.setUpdatesEnabled(False)
        
        verticalHeader = table.verticalHeader()
        verticalHeader.setSectionResizeMode(mydata.QHeaderView.ResizeMode.Fixed)
        horizontalHeader = table.horizontalHeader()
        horizontalHeader.setSectionResizeMode(mydata.QHeaderView.ResizeMode.Fixed)
        
        # Size of a row (usually 16)
        size = 16
        
        # Parse the data into lists of 'size'
        chunks = [byte_data[x:x+size] for x in range(0, len(byte_data), size)]
        
        # Add the data
        address = 0
        address_offset = 0
        rows = []
        for row_number,chunk in enumerate(chunks):
            if len(chunk) < size:
                chunk_length = len(chunk)
                chunk_list = [ f"{chunk[i]:02x}" if i < chunk_length else " " for i in range(size) ]
            else:
                chunk_list = [ f"{c:02x}" for c in chunk ]
            # Address
            current_address = address + address_offset
            address_offset += size
            address_string = "{:04x}".format(current_address)
            # ASCII string
            ascii_list = []
            for num in chunk:
                char = chr(num)
                if char in """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """:
                    ascii_list.append(char)
                else:
                    ascii_list.append('.')
            ascii_string = ''.join(ascii_list)
            # Create row
            row = [ address_string ] + chunk_list + [ ascii_string ]
            rows.append(row)
        
        model = HexTableModel(rows, table)
        table.setModel(model)
        
        # Column widths
        widths = [
            100,
            *[40 for x in range(size)],
            140,
        ]
        for i,w in enumerate(widths):
            table.setColumnWidth(i, w)
        
        table.setUpdatesEnabled(True)
    
    def reload_file(self):
        with open(self.save_name, "rb") as f:
            content = f.read()
        self.show_file_hex_data(content)
    
    def update_style(self):
        # Frame
        self.setStyleSheet(StyleSheetFrame.standard())
        
        # Table style
        for k, v in self.cache_table.items():
            v.horizontalHeader().setSectionResizeMode(data.QHeaderView.ResizeMode.ResizeToContents)
            v.verticalScrollBar().setContextMenuPolicy(data.Qt.ContextMenuPolicy.NoContextMenu)
            v.horizontalScrollBar().setContextMenuPolicy(data.Qt.ContextMenuPolicy.NoContextMenu)
        
        # Rest
        for k,v in self.__cache_buttons.items():
            v.update_style()
        for k,v in self.__cache_labels.items():
            v.update_style()
        for k,v in self.__cache_comboboxes.items():
            v.update_style()


class HexTable(data.QTableView):
    def __init__(self, parent, main_form):
        super().__init__(parent)
        self.main_form = main_form
    
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.main_form.view.indication_check()
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.main_form.view.indication_check()
        parent = self.parent()
        while not hasattr(parent, "_parent"):
            parent = parent.parent()
        self.main_form.last_focused_widget = parent._parent


class HexTableModel(data.QAbstractTableModel):
    def __init__(self, row_data, parent=None):
        super().__init__(parent)
        self.__row_data = row_data
        self.__last_index = len(row_data[0]) - 1
        self.__headers = {
            0: "Address",
            self.__last_index: "ASCII"
        }
        for i in range(len(row_data[0]) - 2):
            self.__headers[i+1] = "{:02x}".format(i)
    
    def rowCount(self, parent=None):
        return len(self.__row_data)

    def columnCount(self, parent=None):
        return len(self.__row_data[0]) if self.rowCount() else 0

    def data(self, index, role=mydata.Qt.ItemDataRole.DisplayRole):
        if role == mydata.Qt.ItemDataRole.DisplayRole:
            return self.__row_data[index.row()][index.column()]
        
        elif role == mydata.Qt.ItemDataRole.TextAlignmentRole:
            column = index.column()
            if column == self.__last_index:
                return mydata.Qt.AlignmentFlag.AlignLeft | mydata.Qt.AlignmentFlag.AlignVCenter
            else:
                return mydata.Qt.AlignmentFlag.AlignHCenter | mydata.Qt.AlignmentFlag.AlignVCenter
    
    def headerData(self, section, orientation, role=mydata.Qt.ItemDataRole.DisplayRole):
        if orientation == mydata.Qt.Orientation.Horizontal and role == mydata.Qt.ItemDataRole.DisplayRole:
            return self.__headers[section]
        return super().headerData(section, orientation, role)