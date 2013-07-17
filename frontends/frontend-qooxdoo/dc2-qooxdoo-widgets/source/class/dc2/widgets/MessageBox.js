/*
    (DC)² - DataCenter Deployment Control
    Copyright (C) 2010, 2011, 2012, 2013  Stephan Adig <sh@sourcecode.de>

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
/*
#asset(qx/icon/${qx.icontheme}/32/status/dialog-error.png)
#asset(qx/icon/${qx.icontheme}/32/status/dialog-information.png)
#asset(qx/icon/${qx.icontheme}/32/status/dialog-warning.png)
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-ok.png);
#asset(qx/icon/${qx.icontheme}/16/actions/dialog-cancel.png);
 */

qx.Class.define('dc2.widgets.MessageBox',
{
  extend: qx.ui.window.Window,
  construct:function(dialog_type,dialog_title,dialog_detail_error_text) {
    this.base(arguments);
    this._dialog_type=dialog_type;
    this._dialog_title=dialog_title;
    this._dialog_detail_error_text=dialog_detail_error_text;
    this.createContent();

  },
  members:{
    _dialog_type:null,
    _dialog_title:null,
    _dialog_detail_error_text:null,
    createContent:function() {
      this.set({
        modal:true,
        showClose:true,
        showMaximize:false,
        showMinimize:false
      });
      this.setCaption(this._dialog_title);
      this.setLayout(new qx.ui.layout.VBox(5));
      // this.setResizable(false,false,false,false);
      this.setResizable(false,true,true,false);
      this.add(this._createLayout(),{flex:1});
      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnOk=new qx.ui.form.Button("Ok");
      // var btnCancel=new qx.ui.form.Button("Cancel");
      btnOk.addListener("execute",this._btnOk,this);
      // btnCancel.addListener("execute",this._btnCancel,this);
      // comp.add(btnCancel);
      comp.add(btnOk);
      this.add(comp);
      this.center();
      this.focus();
      this.show();
    },
    _createLayout:function() {
      var comp1=new qx.ui.container.Composite(new qx.ui.layout.HBox(5));
      var icon="";
      if (this._dialog_type=="error") {
        icon="icon/32/status/dialog-error.png";
      } else if (this._dialog_type="warning") {
        icon="icon/32/status/dialog-warning.png";
      } else if (this._dialog_type="information") {
        icon="icon/32/status/dialog-information.png";
      }
      comp1.add(new qx.ui.basic.Atom(this._dialog_detail_error_text,icon));
      return(comp1);
    },
    _btnOk:function(e) {
      this.close();
    },
    _btnCancel:function(e) {
      this.close();
    }
  }
});
