/*
    (DC)² - DataCenter Deployment Control
    Copyright (C) 2010, 2011, 2012  Stephan Adig <sh@sourcecode.de>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/


/* ************************************************************************

#asset(qx/icon/${qx.icontheme}/16/actions/list-add.png)
#asset(qx/icon/${qx.icontheme}/16/actions/list-remove.png)
#asset(qx/icon/${qx.icontheme}/16/actions/view-refresh.png)
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-ok.png);
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-cancel.png);
#asset(qx/icon/${qx.icontheme}/16/actions/system-search.png);

************************************************************************ */

qx.Class.define('dc2.widgets.TableWidget',
    {
      extend:qx.ui.container.Composite,
      construct:function(options) {
        qx.Class.include(qx.ui.table.Table,qx.ui.table.MTableContextMenu);
        this.base(arguments);        
        this._options={
          enableAddEntry:false,
          enableEditEntry:false,
          enableViewEntry:false,
          enableDeleteEntry:false,
          enableReloadTable:false,
          enableExtraButtons:false,
          cellRenderer:null,
          columnVisibility:null,
          searchFunctions:null,
          contextMenus:null,
          editDialog:null,
          viewDialog:null,
          addDialog:null,
          tableModel:null,
          extraButtons:null,
          columnVisibilityButton:true
        };
        if (options!==null) {
          for (var i in options) {
            this._options[i]=options[i];
          }
        }
        if ("tableModel" in this._options) {
          this._tablemodel=this._options.tableModel;
        }
        if ("editDialog" in this._options && "enableEditEntry" in this._options) {
          this._editDialog=this._options.editDialog;
        }
        if ("viewDialog" in this._options && "enableViewEntry" in this._options) {
          this._viewDialog=this._options.viewDialog;
        }
        if ("addDialog" in this._options && "enableAddEntry" in this._options) {
          this._addDialog=this._options.addDialog;
        }
        if ("extraButtons" in this._options && "enableExtraButtons" in this._options) {
          this._extraButtons=this._options.extraButtons;
        }

        this._createContent();
      },
      members: {
        _table:null,
        _tablemodel:null,
        _editDialog:null,
        _viewDialog:null,
        _addDialog:null,
        _options:null,
        _extraButtons:null,
        _searchDialog:null,
        _searchData:null,
        _buttonBar:null,
        _createContent:function() {
          
          this.setLayout(new qx.ui.layout.Dock());
          this._table=new qx.ui.table.Table(this._tablemodel.getTableModel());
          this._table.setShowCellFocusIndicator(false);
          if ("columnVisibilityButton" in this._options) {
            this._table.setColumnVisibilityButtonVisible(this._options["columnVisibilityButton"]);
          }
          if ("columnVisibility" in this._options) {
            if (this._options.columnVisibility != null) {
              for (var i=0;i<this._options.columnVisibility.length;++i) {
                var tcm=this._table.getTableColumnModel();
                tcm.setColumnVisible(this._options.columnVisibility[i].column,this._options.columnVisibility[i].visible);
              }
            }
          }          
          this.add(this._table,{edge:"center"});
          this._buttonBar=this._createButtonBar();
          if (this._extraButtons != null) {
            for (var i=0;i<this._extraButtons.length;i++) {
              var button=new qx.ui.form.Button(this._extraButtons[i]["title"]);
              button.addListener("execute",this._extraButtons[i]["callback"],this._extraButtons[i]["context"])
              this._buttonBar.add(button);
            }
          }
          this.add(this._buttonBar,{edge:"north"});          
          if (this._options.searchFunctions!==null && this._options.searchFunctions.searchDialog!=null) {
            this.getApplicationRoot().add(this._options.searchFunctions.searchDialog);
          }
          if (this._options.enableEditEntry) {
            this._table.addListener("cellDblclick",this._cellDblClick,this);
            this._editDialog.addListener("updateData",this._updateData,this);
            this._editDialog.addListener("close",this._closeEditDialog,this);
            this._editDialog.addListenerOnce("appear",function(e) { this._editDialog.center(); },this);
          }
          if (this._options.enableViewEntry) {
            this._table.addListener("cellDblclick",this._viewDblClick,this);
            this._viewDialog.addListener("close",this._closeEditDialog,this);
            this._viewDialog.addListenerOnce("appear",function(e) { this._viewDialog.center(); },this);
          }
          if (this._options.enableAddEntry) {
            this._addDialog.addListener("addData",this._addData,this);
            this._addDialog.addListener("close",this._closeEditDialog,this);
            this._addDialog.addListenerOnce("appear",function(e) { this._addDialog.center(); },this);
          }
        },
        _createButtonBar:function() {
          var buttonBar=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'left'}));
          buttonBar.__btnAdd=new qx.ui.form.Button("Add","icon/16/actions/list-add.png");
          buttonBar.__btnDelete=new qx.ui.form.Button("Delete","icon/16/actions/list-remove.png");
          buttonBar.__btnReload=new qx.ui.form.Button("Reload","icon/16/actions/view-refresh.png");
          buttonBar.__btnSearch=new qx.ui.form.Button("Search","icon/16/actions/system-search.png");
          buttonBar.__btnSearchClear=new qx.ui.form.Button("Clear Search",null);
          buttonBar.add(buttonBar.__btnAdd);
          buttonBar.add(buttonBar.__btnDelete);
          buttonBar.add(buttonBar.__btnReload);
          buttonBar.add(buttonBar.__btnSearch);
          buttonBar.add(buttonBar.__btnSearchClear);
          buttonBar.__btnAdd.setEnabled(this._options.enableAddEntry);
          buttonBar.__btnDelete.setEnabled(this._options.enableDeleteEntry);
          buttonBar.__btnReload.setEnabled(this._options.enableReloadTable);
          if (this._options.searchFunctions !== null && this._options.searchFunctions.searchDialog != null) {
            buttonBar.__btnSearch.setEnabled(true);
            buttonBar.__btnSearchClear.setEnabled(false);
            buttonBar.__btnSearchClear.exclude();
            buttonBar.__btnSearch.addListener("execute",this._btnBarSearch,this);
            buttonBar.__btnSearchClear.addListener("execute",this._btnBarSearchClear,this);
          } else {
            buttonBar.__btnSearch.setEnabled(false);
            buttonBar.__btnSearchClear.setEnabled(false);
            buttonBar.__btnSearch.exclude();
            buttonBar.__btnSearchClear.exclude();
          }
          if (this._options.enableAddEntry) {
            buttonBar.__btnAdd.setEnabled(true);
            buttonBar.__btnAdd.addListener("execute",this._btnBarAdd,this);
          } else {
            buttonBar.__btnAdd.exclude();
          }
          if (this._options.enableReloadEntry) {
            buttonBar.__btnReload.setEnabled(true);
            buttonBar.__btnReload.addListener("execute",this._btnBarReload,this);
          } else  {
            buttonBar.__btnReload.exclude();
          }
          if (this._options.enableDeleteEntry) {
            buttonBar.__btnDelete.setEnabled(true);
            buttonBar.__btnDelete.addListener("execute",this._btnBarDelete,this);
          } else {
            buttonBar.__btnDelete.exclude();
          }
          return(buttonBar);
        },
        _btnBarAdd:function(e) {
          this.setEnabled(false);
          this._addDialog.setData(this._tablemodel.getEmptyData());
          this._addDialog.setCaption("Add "+this._tablemodel.getModelCaption());
          this._addDialog.show();          
        },
        _btnBarDelete:function(e) {
          var row_data=this._table.getTableModel().getRowDataAsMap(this._table.getFocusedRow());
          if (row_data != null) {
            var response=this._tablemodel.deleteData(row_data);
            if (response != true) {
              // TODO: Add dialogbox
            } else {
              if (this._searchData != null) {
                this._tablemodel.listData(this._searchData);
              } else {
                this._tablemodel.listData(null);
              }
            }
          }
        },
        _btnBarReload:function(e) {
          if (this._searchData != null) {
            this._tablemodel.listData(this._searchData);
          } else {
            this._tablemodel.listData(null);
          }
        },
        _btnBarSearch:function(e) {
          if (this._options.searchFunctions !== null && this._options.searchFunctions.searchDialog != null) {
            this._options.searchFunctions.searchDialog.setCaption("Search");
            this._options.searchFunctions.searchDialog.show();
            this._options.searchFunctions.searchDialog.addListener("evDlgOk",function(e) {
              if (e.getData() != null) {
                this._searchData=e.getData();
                this._tablemodel.listData(this._searchData);
                this._buttonBar.__btnSearchClear.setEnabled(true);
                this._buttonBar.__btnSearchClear.show();
              }
            }, this);
          }
        },
        _btnBarSearchClear:function(e) {
          this._searchData=null;
          this._tablemodel.listData(null);
	        this._buttonBar.__btnSearchClear.setEnabled(false);
                this._buttonBar.__btnSearchClear.exclude();
        },
        _addData:function(e) {
          var result=this._tablemodel.addData(e.getData());
          if (result != true) {
            // TODO: Add dialogbox
          } else {
            if (this._searchData != null) {
              this._tablemodel.listData(this._searchData);
            } else {
              this._tablemodel.listData(null);
            }
          }
        },
        _updateData:function(e) {
          var result=this._tablemodel.updateData(e.getData());
          if (result != true) {
            // TODO: Add dialogbox
          } else {
            if (this._searchData != null) {
              this._tablemodel.listData(this._searchData);
            } else {
              this._tablemodel.listData(null);
            }
          }          
        },      
        showData:function() {
          this._tablemodel._tableModel.removeRows(this._tablemodel._tableModel.getRowCount());
          this._tablemodel.listData(null);
        },
        _cellDblClick:function(e) {         
          this.setEnabled(false);
          this._editDialog.setData(this._table.getTableModel().getRowData(e.getRow()));
          this._editDialog.setCaption("Edit "+this._tablemodel.getModelCaption());
          this._editDialog.show();
        },
        _viewDblClick:function(e) {
          this.setEnabled(false);
          this._viewDialog.setData(this._table.getTableModel().getRowData(e.getRow()));
          this._viewDialog.setCaption("View "+this._tablemodel.getModelCaption());
          this._viewDialog.show();
        },
        _closeEditDialog:function(e) {
          this.setEnabled(true);
        },
        getSelectedRowData:function() {
          return(this._table.getTableModel().getRowData(this._table.getFocusedRow()));
        }
      }
    }
);

