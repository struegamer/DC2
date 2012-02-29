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
#asset(qx/icon/${qx.icontheme}/16/actions/go-next.png);
#asset(qx/icon/${qx.icontheme}/16/actions/go-previous.png);

************************************************************************ */

qx.Class.define("dc2.dialogs.EditClassTemplates",
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this._createLayout();
  },
  events: {
      'addData':"qx.event.type.Data",
      'updateData':"qx.event.type.Data"
  },
  members:{
    _edit_id:null,
    _edit_name:null,
    _edit_description:null,
    _edit_defaultclasses:null,
    _edit_templateclasses:null,
    _btn_move_left:null,
    _btn_move_right:null,
    _tbl_defaultclasses:null,
    _tbl_classtemplates:null,
    _createLayout:function() {
      this.set({
        modal:true,
        padding:3,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this.setWidth(500);
      this.setLayout(new qx.ui.layout.VBox(5));
      this.setResizable(false,true,true,false);
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.Grid(5,5);
      layout.setColumnFlex(1,1);
      layout.setRowFlex(3,1);
      comp.setLayout(layout);
      this._edit_name=new qx.ui.form.TextField();
      this._edit_description=new qx.ui.form.TextField();
      this._edit_defaultclasses=new qx.ui.form.List();
      this._edit_defaultclasses.setSelectionMode("multi");
      this._edit_defaultclasses.setDraggable(true);
      this._edit_defaultclasses.setDroppable(true);
      this._edit_defaultclasses.addListener("dragstart",this._dragstartDefaultClasses,this);
      this._edit_defaultclasses.addListener("droprequest",this._droprequestDefaultClasses,this);
      this._edit_defaultclasses.addListener("drop",this._dropDefaultClasses,this)
      this._edit_templateclasses=new qx.ui.form.List();
      this._edit_templateclasses.setSelectionMode("multi");
      this._edit_templateclasses.setDroppable(true);
      this._edit_templateclasses.setDraggable(true);
      this._edit_templateclasses.addListener("drop",this._dropTemplateClasses,this);      
      this._edit_templateclasses.addListener("dragstart",this._dragstartTemplateClasses,this);
      this._edit_templateclasses.addListener("droprequest",this._droprequestTemplateClasses,this);
      comp.add(new qx.ui.basic.Label("Name"),{row:0,column:0});
      comp.add(new qx.ui.basic.Label("Description"),{row:1,column:0});
      comp.add(this._edit_name,{row:0,column:1});
      comp.add(this._edit_description,{row:1,column:1});
      comp.add(this._initializeClassesBar(),{row:2,column:0,colSpan:2});
      comp.add(new qx.ui.basic.Label("Drag Items"),{row:3,column:0,colSpan:2});
      this.add(comp,{flex:1});
      this.add(this._initializeButtonBar());
      this._fillDefaultClasses();
    }, 
    /*
     * Private Methods
     */
    _initializeButtonBar:function() {
      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnOk=new qx.ui.form.Button('Ok','icon/16/actions/dialog-ok.png');
      var btnCancel=new qx.ui.form.Button('Cancel','icon/16/actions/dialog-cancel.png');
      btnOk.addListener("execute",this._clkBtnOk,this);
      btnCancel.addListener("execute",this._clkBtnCancel,this);
      comp.add(btnCancel);
      comp.add(btnOk);
      return(comp);
    },
    _initializeClassesBar:function() {
      var comp=new qx.ui.container.Composite();
      var layout=new qx.ui.layout.HBox(5);
      comp.setLayout(layout);
            
      var comp2=new qx.ui.container.Composite();
      var layout2=new qx.ui.layout.VBox(5);
      comp2.setLayout(layout2);
      comp2.add(new qx.ui.basic.Label("Default Classes"));
      comp2.add(this._edit_defaultclasses);
      
      var comp3=new qx.ui.container.Composite();
      var layout3=new qx.ui.layout.VBox(5);
      comp3.setLayout(layout3);
      comp3.add(new qx.ui.basic.Label("Template Classes"));
      comp3.add(this._edit_templateclasses);
      
      comp.add(comp2,{flex:1});
      comp.add(comp3,{flex:1});
      return(comp);
    },
    _fillDefaultClasses:function() {
      if (this._tbl_defaultclasses == null) {
        this._tbl_defaultclasses=new dc2.models.DefaultClasses(dc2.helpers.BrowserCheck.RPCUrl(false));
      }
      var defclasses=this._tbl_defaultclasses.getAll();
      for (var i=0; i<defclasses.length;i++) {
        this._edit_defaultclasses.add(new qx.ui.form.ListItem(defclasses[i]["classname"],null,defclasses[i]["classname"]));
      }

    },
    /*
     * Event Methods
     */
    _clkBtnOk:function(e) {
      var data={};
      data["_id"]=this._edit_id;
      data["name"]=this._edit_name.getValue()
      data["description"]=this._edit_description.getValue();
      data["classes"]=[];
      var selection=this._edit_templateclasses.getChildren();
      for (var i=0;i<selection.length;i++) {
        data["classes"].push(selection[i].getModel());        
      }
      if (data["_id"] != "" && data["_id"] != null) {
        this.fireDataEvent("updateData",data);
      } else {
        this.fireDataEvent("addData",data);
      }
      this.close();
    },
    _clkBtnCancel:function(e) {
      this.close();
    },
    _editFieldFocus:function(e) {
      if (e.getTarget().classname == "qx.ui.form.TextField") {
        e.getTarget().setTextSelection(0);
      }
    },    
    _dragstartDefaultClasses:function(e) {
      e.addType("items");
      e.addAction("copy");
      e.addAction("move");
    },
    _dragstartTemplateClasses:function(e) {
      e.addType("items");
      e.addAction("copy");
      e.addAction("move");      
    },
    _droprequestDefaultClasses:function(e) {
      var action=e.getCurrentAction();
      var type=e.getCurrentType();
      var result;
      if (type=="items") {
        result=this._edit_defaultclasses.getSelection();
        if (action=="copy") {
          var copy=[];
          for (var i=0;i<result.length;i++) {
            copy[i]=result[i].clone();
          }
          result=copy;
        }
        if (action=="move") {
          var selection=this._edit_defaultclasses.getSelection();
          for (var i=0;i<selection.length;i++) {
            this._edit_defaultclasses.remove(selection[i]);
          }
        }
        e.addData(type,result);
      }      
    },
    _droprequestTemplateClasses:function(e) {
      var action=e.getCurrentAction();
      var type=e.getCurrentType();
      var result;
      if (type=="items") {
        result=this._edit_templateclasses.getSelection();
        if (action=="copy") {
          var copy=[];
          for (var i=0; i<result.length;i++) {
            copy[i]=result[i].clone();
          }
          result=copy;
        }
        if (action=="move") {
          var selection=this._edit_templateclasses.getSelection();
          for (var i=0;i<selection.length;i++) {
            this._edit_templateclasses.remove(selection[i]);
          }
        }
        e.addData(type,result);
      }
    },
    _dropDefaultClasses:function(e) {
      var items=e.getData("items");
      for (var i=0;i<items.length;i++) {
        this._edit_defaultclasses.add(items[i]);
      }
      items=this._edit_defaultclasses.getChildren();
      var items1=[];
      for (var i=0;i<items.length;i++) {
        items1[i]=items[i].clone();
      }
      items1.sort(function(a,b) {
        var av=a.getLabel();
        var bv=b.getLabel();
        return av < bv ? -1 :( av == bv ? 0 : 1 );
      });
      this._edit_defaultclasses.removeAll();
      for (var i=0;i<items1.length;i++) {
        this._edit_defaultclasses.add(items1[i]);
      }
    },
    _dropTemplateClasses:function(e) {
      var items=e.getData("items");     
      for (var i=0;i<items.length;i++) {
        this._edit_templateclasses.add(items[i]);
      }
      items=this._edit_templateclasses.getChildren();
      var items1=[];
      for (var i=0;i<items.length;i++) {
        items1[i]=items[i].clone();
      }
      items1.sort(function(a,b) {
        var av=a.getLabel();
        var bv=b.getLabel();
        return av < bv ? -1 :( av == bv ? 0 : 1 );
      });
      this._edit_templateclasses.removeAll();
      for (var i=0;i<items1.length;i++) {
        this._edit_templateclasses.add(items1[i]);
      }      
    },
    /* 
     * Public Methods
     */
    setData:function(data) {
      if (data != null) {
        this._edit_id=data["_id"];
        this._edit_name.setValue(data["name"]);
        this._edit_description.setValue(data["description"]);
        this._edit_defaultclasses.removeAll();
        this._edit_templateclasses.removeAll();
        this._fillDefaultClasses();
        
        if (this._edit_id != null) {
          this._edit_name.setEnabled(false);
          if (this._tbl_classtemplates==null) {
            this._tbl_classtemplates=new dc2.models.ClassTemplates(dc2.helpers.BrowserCheck.RPCUrl(false));          
          }
          var record=this._tbl_classtemplates.getClassTemplateRecord(this._edit_id);
          for (var i=0;i<record["classes"].length;i++) {
            this._edit_templateclasses.add(new qx.ui.form.ListItem(record["classes"][i],null,record["classes"][i]));
            var found=this._edit_defaultclasses.findItem(record["classes"][i]);
            if (found != null) {
              this._edit_defaultclasses.remove(found);
            }
          }
        } else {
          this._edit_name.setEnabled(true);
        }
      }
    }
  }
});
