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


qx.Class.define('dc2.widgets.DialogWidget',
{
  extend: qx.ui.window.Window,
  construct:function() {
    this.base(arguments);
    this.createContent();

  },
  events: {
    'evDlgOk':'qx.event.type.Data'
  },
  members:{
    createContent:function() {
      this.set({
    	  modal:true,
		    showClose:true,
		    showMaximize:false,
		    showMinimize:false
	    });
      this.setLayout(new qx.ui.layout.VBox(5));
      // this.setResizable(false,false,false,false);
      this.setResizable(false,true,true,false);
      this.add(this._createLayout(),{flex:1});
      var comp=new qx.ui.container.Composite(new qx.ui.layout.HBox(5).set({alignX:'right'}));
      var btnOk=new qx.ui.form.Button("Ok");
      var btnCancel=new qx.ui.form.Button("Cancel");
      btnOk.addListener("execute",this._btnOk,this);
      btnCancel.addListener("execute",this._btnCancel,this);
      comp.add(btnCancel);
      comp.add(btnOk);
      this.add(comp);
      this.center();
      this.focus();
    },
    _createLayout:function() {
      return new qx.ui.basic.Label("TestWidget");
    },
    _getData:function() {
      return null;
    },
    _btnOk:function(e) {
      this.fireDataEvent("evDlgOk",this._getData());
      this.close();
    },
    _btnCancel:function(e) {
      this.close();
    }
  }
});
