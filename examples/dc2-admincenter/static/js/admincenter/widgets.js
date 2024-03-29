DC2.Widgets.StandardForms= function(selector) {
  this.container=$(selector);
  this.container.on('keypress',this.container,this.submitForm.bind(this));
};


DC2.Widgets.StandardForms.prototype.submitForm = function (event) {
  if (event && event.which == 13) {
    this.container.submit();
  }
};


DC2.Widgets.Tabs=function(selector) {
  this.container=$(selector);
  this.container.find('a[data-toggle="tab"]').on('click',this.container,this.on_tab_click.bind(this));
};

DC2.Widgets.Tabs.prototype.on_tab_click = function(event) {
  event.preventDefault();
  $(event.target).tab('show');
};

DC2.Widgets.Dashboard=function(selector) {
  this.container=$(selector);
  this.container.find('tbody td.data-cell').on('click',this.container,this.on_click.bind(this));
};

DC2.Widgets.Dashboard.prototype.on_click=function(event) {
  window.location.href='/backends/'+$(event.target).parent().attr('data-backend-id');
};

DC2.Widgets.ButtonGroup = {};

DC2.Widgets.ButtonGroup.Index = function(selector) {
  this.container=$(selector);
  var _this=this
  this.container.children('button').each(function(index,value) {
    $(this).on('click',_this.container,_this.action.bind(this));
  });
};

DC2.Widgets.ButtonGroup.Index.prototype.action=function(event) {
  data_type=$(this).attr('data-type');
  switch(data_type) {
    case 'url':
      window.location.href=$(this).attr('data-url');
      break;
    case 'jsfunc':
      if ($(this).attr('data-list')=='true') {
        if ($(this).attr('data-action')=='delete') {
          var data_query='';
          if ($(this).attr('data-query') != undefined) {
            data_query=$(this).attr('data-query');
          }
          $('table.data-list').find('input[type="checkbox"].del_check').each(function() {
            if ($(this).prop('checked')==true) {
              a=$.ajax({
                url:$('table.data-list').attr('data-url-delete')+$(this).val()+'?'+data_query+'&oformat=json',
                contentType:'application/json; charset=utf-8',
                dataType:'json',
                type:'DELETE',
              });
              a.done(function(data) {
                if ('redirect' in data) {
                  window.location.href=data.redirect.url;
                }
              });

            }
          });
        }
      }
      break;
  }
};

DC2.Widgets.DataList = function(selector) {
  this.container=$(selector);
  this.container.find('thead tr th input[type="checkbox"]').on('click',this.container,this.del_check.bind(this));
  this.container.find('tbody tr td.data-cell').on('click',this.container,this.edit.bind(this));
};

DC2.Widgets.DataList.prototype.del_check = function(event) {
  _this=this
  this.container.find('tbody tr td input[type="checkbox"].del_check').each(function() {
    this.checked=_this.container.find('thead tr th input[type="checkbox"]').prop('checked');
  });

};

DC2.Widgets.DataList.prototype.edit = function(event) {
  _this=this;
  window.location.href=$(event.target).parent().attr('data-edit-url');
};



DC2.Widgets.DataForms = function(selector) {
  this.container=$(selector);
  // this.container.find('input[type="text"]').on('keypress',this.container,this.catch_enter.bind(this));
  this.container.find('input[type="button"].btn_save').on('click',this.container,this.save.bind(this));
  this.container.find('input[type="button"].btn_cancel').on('click',this.container,this.cancel.bind(this));
};

DC2.Widgets.DataForms.prototype.save=function(event) {
  _this=this;
  var data={}
  this.container.find('input').each(function(){
    input_type=$(this).attr('type')
    if (input_type != 'button' && input_type != 'checkbox' && input_type != 'radio') {
      data[$(this).attr('name')]=$(this).val();
    } else if (input_type == 'checkbox' || input_type == 'radio') {
      if ($(this).prop('checked')) {
        data[$(this).attr('name')]=$(this).val();
      } else {
        data[$(this).attr('name')]=null;
      }
    }
  });

  a=$.ajax({
    url:this.container.attr('action'),
    type:this.container.attr('method'),
    data:data,
    dataType:'json',
    async:false
  });
  a.done(function(data) {
    if ('redirect' in data) {
      window.location.href=data.redirect.url;
    }
  });
};  

DC2.Widgets.DataForms.prototype.cancel = function(event) {
  window.location.href=$(event.target).attr('data-url');
};

DC2.Widgets.DataForms.prototype.catch_enter = function(event) {
  if (event && event.which == 13) {
    this.container.find('input[type="button"].btn_save').trigger('click');
  }
};

DC2.Widgets.Datatables = function(selector) {
  this.container=$(selector);
  var listtype=this.container.attr('data-list-type');
  this._listType=listtype;
  var columns=null;
  switch(listtype) {
    case 'servers':
      columns=[
        {'mDataProp':'_id','bVisible':false},
        {'mDataProp':'uuid'},
        {'mDataProp':'serial_no'},
        {'mDataProp':'manufacturer'},
        {'mDataProp':'product_name'},
        {'mDataProp':'location'},
        {'mDataProp':'asset_tags'}
      ];
      break;
    case 'hosts':
      columns=[
        {'mDataProp':'_id','bVisible':false},
        {'mDataProp':'server_id','bVisible':false},
        {'mDataProp':'hostname'},
        {'mDataProp':'domainname'},
        {'mDataProp':'environments','sDefaultContent':'No Environment'}
      ];
      break;
    case 'deployment':
      columns=[
      {'mDataProp':'_id','bVisible':false},
      {'mDataProp':'hostname'},
      {'mDataProp':'status'},
      {'mDataProp':'progress'},
      ];
      break;
  }
  var _this=this;
  this.container.dataTable({
    'bDestroy':false,
    'sDom': "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
    'sPaginationType': 'bootstrap',
    'iDisplayLength':25,
    'aoColumns':columns,
    'fnCreatedRow':function(nRow,aData) {
      $(nRow).attr('data-entry-id',aData._id);
      $(nRow).attr('data-entry-type',listtype);
      $(nRow).attr('data-backend-id',_this.container.attr('data-backend-id'));
      $(nRow).on('click',_this.container,_this.on_click);
      $(nRow).rightClick(_this.on_right_click);
    },
  });
  this.container.on('backend-update-'+listtype,this.container,this.backend_update.bind(this));
  this.container.trigger('backend-update-'+listtype);
  return(false);
};


DC2.Widgets.Datatables.prototype.on_right_click = function (event) {
  console.log($(event.target).parent().attr('data-entry-id'));
};
DC2.Widgets.Datatables.prototype.backend_update=function(event) {
  url=this.container.attr('data-retrieval-url');
  a=$.ajax({
    url:url,
    dataType:'json',
    type:'GET',
    context:this,
  });
  a.done(function(data) {
    if ('error' in data && data.error==true) {
    	$('#erroralert h4#error_type').html('Error: '+data.error_type);
        $('#erroralert span#errortext').html(data.error_msg+' ('+data.error_no+')');
        $('#erroralert').addClass('alert-error').show();
        return(false);
    }
    this.container.dataTable().fnClearTable();
    this.container.dataTable().fnAddData(data.datalist);
  });
  return(false);
};

DC2.Widgets.Datatables.prototype.on_click = function(event) {
  dataEntryType=$(event.target).parent().attr('data-entry-type');
  switch(dataEntryType) {
    case 'servers':
      window.location.href='/backends/servers/'+$(event.target).parent().attr('data-entry-id')+'?backend_id='+$(event.target).parent().attr('data-backend-id');
      break;
    case 'hosts':
      window.location.href='/backends/hosts/'+$(event.target).parent().attr('data-entry-id')+'?backend_id='+$(event.target).parent().attr('data-backend-id');
      break;
    case 'deployment':
      console.log('hello');
      window.location.href='/backends/installstate/'+$(event.target).parent().attr('data-entry-id')+'?backend_id='+$(event.target).parent().attr('data-backend-id');
      break;
  }
  return(false);
};

DC2.Widgets.EditTables=function(selector) {
  this.container=$(selector);
  this.container_id=this.container.attr('id');
  this.backend_id=this.container.attr('data-backend-id');
  this.add_row_counter=0;
  this.contentheading=$('#contentheading');
  this.edit_forms=$('.edit_form');

  this.submit_data={};

  this.prepare_tables();
};


DC2.Widgets.EditTables.prototype.prepare_tables=function() {
  var _this=this;
  this.edit_tables=this.container.find('.edit_table');
  this.edit_tables.each(function() {
    var btns=$(this).find('#table_btn_edit_'+$(this).attr('id'));
    _this.prepare_table_buttons(btns,$(this).attr('id'));
    var ident=$(this).attr('id');
    $(this).bind('unbind_remove_buttons',function() {
    	unbind_buttons(_this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'),'click',_this._btn_remove);    	
    });	
    $(this).bind('bind_remove_buttons',function() {
    	bind_buttons(_this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'),'click',_this.container,_this._btn_remove,this);
    });
  });
  var btn_update=this.contentheading.find('.btn.update_entry');
  var btn_cancel=this.contentheading.find('.btn.update_cancel');
  btn_update.on('click',this.container,this._btn_update.bind(this));
  btn_cancel.on('click',this.container,this._btn_cancel.bind(this));
};

DC2.Widgets.EditTables.prototype.prepare_table_buttons=function(btns,ident) {
  var btn_add=btns.find('#'+ident+'_add.btn');
  btn_add.on('click',{selector:this.container,ident:ident},this._btn_add.bind(this));
  //this.unbind_remove_btns(this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'));
  unbind_buttons(this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'),'click',this._btn_remove);
  //this.bind_remove_btns(this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'));
  bind_buttons(this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'),'click',this.container,this._btn_remove,this);
};

DC2.Widgets.EditTables.prototype._btn_update=function(event) {
  console.log('hello');
  var button=$(event.target);
  var controller_path=button.attr('data-controller-path');
  var entry_id=button.attr('data-entry-id');
  var backend_id=button.attr('data-backend-id');
  var all_inputs=this.container.find(':input').not('button');
  console.log(all_inputs);
  var result=this.container.formParams();
  var sectoken=$('input[name="sectoken"]').val();
  console.log(sectoken)
  var a=$.ajax({
    url:controller_path+'/'+entry_id+'?backend_id='+backend_id+'&sectoken='+sectoken,      
    type:'PUT',
    contentType:'application/json; charset=utf-8',
    data:JSON.stringify({'result':result}),
    dataType:'json',
  });
  a.done(function(data) {
    if ('redirect' in data) {
      window.location.href=data.redirect.url
    }
  });
  return(false);
};

DC2.Widgets.EditTables.prototype._btn_cancel=function(event) {
  window.location.href=$(event.target).attr('data-cancel-uri');
  return(false);
};
DC2.Widgets.EditTables.prototype.bind_remove_btns=function(btns) {
  var _this=this;
  btns.each(function() {
    $(this).on('click',_this.container,_this._btn_remove.bind(_this));
  });
};

DC2.Widgets.EditTables.prototype.unbind_remove_btns=function(btns) {
  var _this=this;
  btns.each(function() {
    $(this).off('click',_this._btn_remove);
  });
};

DC2.Widgets.EditTables.prototype._btn_remove=function(event) {
  console.log(this);
  var data_type=$(event.target).attr('data-entry-type');
  var json=null;
  var success=false;
  var remove_follow=false;
  switch(data_type) {
    case 'mac':
      json=new DC2.JSON.Backends.Macs(this.backend_id);
      success=json.delete_mac($(event.target).attr('data-entry-id'));
      break;
    case 'rib':
      json=new DC2.JSON.Backends.Ribs(this.backend_id);
      success=json.delete_rib($(event.target).attr('data-entry-id'));
      break;
    case 'hostclass':
      success=true;
      break;
    case 'hostinterfaces':
      success=true;
      remove_follow=true;
      break;
    default:
      success=true;
      break;
  }
  if (success) {
    if (remove_follow) {
      $(event.target).parent().parent().next().remove();
    }
    $(event.target).parent().parent().remove();

  }
  return(false);
};
DC2.Widgets.EditTables.prototype._btn_add=function(event) {
  event.preventDefault();
  var _this=this
  var add_row=$('#table_row_edit_'+event.data.ident+' table tbody');
  console.log(this.selector)
  this.add_row_counter++;
  var add_row_temp=add_row.clone();
  add_row_temp.find(':input').not('button').each(function() {
    var input_name=$(this).attr('name');
    input_name=input_name.replace('new','new_'+_this.add_row_counter);
    $(this).attr('name',input_name);
    if ($(this)[0].tagName.toLowerCase() == 'select') {
      if ($(this).attr('data-iface-name') != undefined && $(this).attr('data-iface-type') != undefined) {
        var input_id=$(this).attr('id');
        input_id=input_id.replace('_new_','_new_'+_this.add_row_counter+'_');
        $(this).attr('id',input_id);
        $(this).attr('data-iface-name','None_'+_this.add_row_counter);
        _this.new_selection_id=$(this).attr('id');
      }
    }
  });
  this.container.find('#table_edit_'+event.data.ident+' tbody.main_tbody').append(add_row_temp.html());
  console.log(this.new_selection_id);
  $('#div_vlan_None').attr('id','div_vlan_None_'+this.add_row_counter);
  $('#div_bond_None').attr('id','div_bond_None_'+this.add_row_counter);
  new DC2.Widgets.SelectionChange($('#host_interfaces_new_'+this.add_row_counter+'_type'),'iface');
//  this.unbind_remove_btns(this.container.find('#table_edit_'+event.data.ident+' tbody').find('.btn.remove'));
//  this.bind_remove_btns(this.container.find('#table_edit_'+event.data.ident+' tbody').find('.btn.remove'));
  unbind_buttons(this.container.find('#table_edit_'+event.data.ident+' tbody').find('.btn.remove'),'click',this._btn_remove);
  //this.bind_remove_btns(this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'));
  bind_buttons(this.container.find('#table_edit_'+event.data.ident+' tbody').find('.btn.remove'),'click',this.container,this._btn_remove,this);  
  
  return(false);
};


DC2.Widgets.SelectionChange=function(selector,which_type) {
  this.selector=$(selector);
  console.log(selector);
  if (which_type == 'iface') {
    this.iface_name=this.selector.attr('data-iface-name');
    this.iface_type=this.selector.attr('data-iface-type');
    console.log(this.selector.attr('id'));
    switch(this.iface_type) {
      case 'vlan':
        console.log('constructor: vlan');
        $('#div_vlan_'+this.iface_name).show();
        $('#div_bond_'+this.iface_name).hide();
        break;
      case 'bond_1':
      case 'bond_2':
        console.log('constructor: bond');
        $('#div_bond_'+this.iface_name).show();
        $('#div_vlan_'+this.iface_name).hide();
        break;
      default:
        console.log('constructor: default');
        $('#div_bond_'+this.iface_name).hide();
        $('#div_vlan_'+this.iface_name).hide();
        break;
 
    };
    this.selector.on('change',this.selector,this.change_div.bind(this));
  }
};

DC2.Widgets.SelectionChange.prototype.change_div=function(event) {
  var change_val=$(event.target).val();
  console.log('change_div');
  switch(change_val) {
    case 'vlan':
      $('#div_vlan_'+this.iface_name).show();
      $('#div_bond_'+this.iface_name).hide();
      break;
    case 'bond_1':
    case 'bond_2':
      $('#div_vlan_'+this.iface_name).hide();
      $('#div_bond_'+this.iface_name).show();
      break;
    default:
      $('#div_vlan_'+this.iface_name).hide();
      $('#div_bond_'+this.iface_name).hide();
  }
  return(false);
};

DC2.Widgets.Collapsible = function(selector) {
  this.container=$(selector);
  this.target=this.container.attr('data-target');
  if ($(this.target).hasClass('collapsible_hide')) {
    $(this.target).hide();
  };

  this.container.on('click',this.container,this.on_click.bind(this));
};

DC2.Widgets.Collapsible.prototype.on_click=function(event) {
  select=$(event.target).parent().attr('data-target');
  if ($(select).hasClass('collapsible_hide')) {
    $(event.target).removeClass('icon-chevron-right');
    $(event.target).addClass('icon-chevron-down');
    $(select).removeClass('collapsible_hide');
    $(select).addClass('collapsible_show');
    $(select).show();
  } else {
    $(event.target).removeClass('icon-chevron-down');
    $(event.target).addClass('icon-chevron-right');
    $(select).removeClass('collapsible_show');
    $(select).addClass('collapsible_hide');
    $(select).hide();
  }
  return(false);
};

DC2.Widgets.Button={}
DC2.Widgets.Button.Click=function(selector,func) {
  this.selector=selector;
  this.selector.on('click',this.selector,func.bind(this));
};

DC2.Widgets.ClassTemplates=function(selector,table_selector) {
	this.selector=selector;
	this.table_selector=table_selector;
	this.backend_id=this.selector.attr('data-backend_id');
	this.classTemplateButton=this.selector.find('#update_host_classes_with_template');
	this.classTemplateSelector=this.selector.find('#classtemplate');
	this.classTemplateButton.on('click',this.selector,this.btn_classtemplate_click.bind(this));
};

DC2.Widgets.ClassTemplates.prototype.btn_classtemplate_click=function(event) {
	event.preventDefault();
	var template_data=this.loadClassTemplateData(this.classTemplateSelector.val());
	this.cleanTable();
	this.addTableData(template_data);
};

DC2.Widgets.ClassTemplates.prototype.cleanTable=function() {
	var tbody=this.table_selector.find('tbody');
	this.table_selector.trigger('unbind_remove_buttons');
	tbody.find('tr').each(function() {
		$(this).remove();
	});
};

DC2.Widgets.ClassTemplates.prototype.addTableData=function(template_data) {
	var edit_row=$('#table_row_edit_host_defaultclasses').find('tbody');
	console.log(edit_row);
	for (var i=0;i<template_data.datalist.classes.length;i++) {
		var clone=edit_row.clone();
		var name=clone.find('select').attr('name');
		name=name.replace('new',template_data.datalist.classes[i]);
		clone.find('select').attr('name',name);
		clone.find('option').each(function() {
			if ($(this).val()==template_data.datalist.classes[i]) {
				$(this).attr('selected','selected');
			}
		})
		this.table_selector.find('tbody').append(clone.html());
	}
	this.table_selector.trigger('bind_remove_buttons');
};

DC2.Widgets.ClassTemplates.prototype.loadClassTemplateData=function(template_id) {
	var template_data=null;
	var _this=this;
	var a=$.ajax({
		url:'/json/backends/classtemplates/backend_classtemplate_get?backend_id='+this.backend_id+'&template_id='+template_id,
		type:'GET',
		contentType:'application/json; charset=utf8',
		async:false,
	});
	a.done(function(data) {
		template_data=data;
	});
	return(template_data);
};

