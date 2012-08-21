window.DC2 = {
  Widgets:{},
  Utilities:{},
  Forms:{},
  JSONCalls:{},
  JSON:{}
};

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
          $('table.data-list').find('input[type="checkbox"].del_check').each(function() {
            if ($(this).prop('checked')==true) {
              a=$.ajax({
                url:$('table.data-list').attr('data-url-delete')+$(this).val()+'?oformat=json',
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
      {'mDataProp':'status'}
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
    console.log(this._listType);
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
    case 'installstate':
      break;
  }
  return(false);
};



DC2.JSONCalls.BackendStats = function(selector) {
  this.container=$(selector);
  datatype=this.container.attr('data-backend-type');
  backend_id=0;
  if (this.container.attr('data-backend-id')) {
    backend_id=this.container.attr('data-backend-id');
  }
  switch(datatype) {
    case 'backendstats':
      this.container.on('backendstats.'+datatype+'.update',this.container,this.backendstats.bind(this));
      break;
    case 'backend_servers_stats':
      this.container.on('backendstats.'+datatype+'.update',this.container,this.backend_servers_stats(this,backend_id));
      break;
    case 'backend_hosts_stats':
      this.container.on('backendstats.'+datatype+'.update',this.container,this.backend_hosts_stats(this,backend_id));
      break;
    case 'backend_deployment_stats':
      this.container.on('backendstats.'+datatype+'.update',this.container,this.backend_deployment_stats(this,backend_id,this.container.attr('data-deployment-status')));
      break;
  }
  this.container.trigger('backendstats.'+datatype+'.update');
};

DC2.JSONCalls.BackendStats.prototype.backendstats=function(event) {
  a=this.do_remote('backendstats',null);
  a.done(function(data) {
    this.container.html(data.backend_count);
  });
  return(false);
};

DC2.JSONCalls.BackendStats.prototype.backend_servers_stats=function(event,backend_id) {
  a=this.do_remote('backend_servers_stats',{'backend_id':backend_id});
  a.done(function(data) {
    this.container.html(data.server_count);
  });
  return(false);
};

DC2.JSONCalls.BackendStats.prototype.backend_hosts_stats=function(event,backend_id) {
  a=this.do_remote('backend_hosts_stats',{'backend_id':backend_id});
  a.done(function(data) {
    this.container.html(data.host_count);
  });
  return(false);
};

DC2.JSONCalls.BackendStats.prototype.backend_deployment_stats=function(event,backend_id,what) {
  a=this.do_remote('backend_deployment_stats',{'backend_id':backend_id,'status':what});
  a.done(function(data) {
    if ('status' in data) {
      switch(data.status) {
        case 'all':
          break;
        case 'deploy':
          this.container.html(data.count);
          break;
        case 'localboot':
          this.container.html(data.count);
          break;
      }
    }
  });
  return(false);
};

DC2.JSONCalls.BackendStats.prototype.do_remote = function(datatype,data) {
  a=$.ajax({
    url:'/json/backends/' + datatype,
    type:'GET',
    data:data,
    dataType:'json',
    context:this,
  });
  return(a);
};

DC2.JSONCalls.Servers = function(selector) {
  this.container=$(selector);
  var datatype=this.container.attr('data-type');
  var backend_id=this.container.attr('data-backend-id');
  var server_id=this.container.attr('data-server-id');
  switch(datatype) {
    case 'backend_server_get_host':
      this.container.on('backends_server.'+datatype+'.update',this.container,this.get_host(this,backend_id,server_id));
      break;
  }
  this.container.trigger('backends_server.'+datatype+'.update');
};

DC2.JSONCalls.Servers.prototype.do_remote = function(datatype,data) {
  a=$.ajax({
    url:'/json/backends/servers/'+datatype,
    type:'GET',
    data:data,
    dataType:'json',
    context:this,
  });
  return(a);
};

DC2.JSONCalls.Servers.prototype.get_host = function(event,backend_id,server_id) {
  var a=this.do_remote('backend_server_get_host',{'backend_id':backend_id,'server_id':server_id});
  a.done(function(data) {
    console.log(data);
  });
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
    console.log($(this).attr('id'));
    var btns=$(this).find('#table_btn_edit_'+$(this).attr('id'));
    _this.prepare_table_buttons(btns,$(this).attr('id'));
  });
  var btn_update=this.contentheading.find('.btn.update_entry');
  var btn_cancel=this.contentheading.find('.btn.update_cancel');
  btn_update.on('click',this.container,this._btn_update.bind(this));
  btn_cancel.on('click',this.container,this._btn_cancel.bind(this));
};

DC2.Widgets.EditTables.prototype.prepare_table_buttons=function(btns,ident) {
  var btn_add=btns.find('#'+ident+'_add.btn');
  btn_add.on('click',{selector:this.container,ident:ident},this._btn_add.bind(this));
  this.unbind_remove_btns(this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'));
  this.bind_remove_btns(this.container.find('#table_edit_'+ident+' tbody').find('.btn.remove'));
};

DC2.Widgets.EditTables.prototype._btn_update=function(event) {
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
  console.log(add_row.find(':input').not('button'));
  this.add_row_counter++;
  var add_row_temp=add_row.clone();
  add_row_temp.find(':input').not('button').each(function() {
    var input_name=$(this).attr('name');
    input_name=input_name.replace('new','new_'+_this.add_row_counter);
    $(this).attr('name',input_name);
  });
  console.log($(add_row_temp));
  this.container.find('#table_edit_'+event.data.ident+' tbody.main_tbody').append(add_row_temp.html());
  this.unbind_remove_btns(this.container.find('#table_edit_'+event.data.ident+' tbody').find('.btn.remove'));
  this.bind_remove_btns(this.container.find('#table_edit_'+event.data.ident+' tbody').find('.btn.remove'));
  return(false);
};


DC2.Widgets.SelectionChange=function(selector) {
  this.selector=$(selector);
  this.iface_name=this.selector.attr('data-iface-name');
  $('.div_vlan').hide();
  $('.div_bond').hide();
  this.selector.on('change',this.selector,this.change_div.bind(this));
};

DC2.Widgets.SelectionChange.prototype.change_div=function(event) {
  console.log($(event.target).val());
  console.log(this.iface_name);
  var change_val=$(event.target).val();
  switch(change_val) {
    case 'vlan':
      console.log('hier');
      $('#div_vlan_'+this.iface_name).show();
      $('#div_bond_'+this.iface_name).hide();
      break;
    case 'bond_1':
    case 'bond_2':
      $('#div_vlan_'+this.iface_name).hide();
      $('#div_bond_'+this.iface_name).show();
      break;
  }
};

DC2.Widgets.Collapsible = function(selector) {
  console.log(selector);
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

DC2.JSON.Backends={};
DC2.JSON.Backends.Macs=function(backend_id) {
  this.url='/json/backends/macs/';
  this.backend_id=backend_id;
  this.success=false;
};
DC2.JSON.Backends.Macs.prototype.delete_mac=function(mac_id) {
  var success=false;
  var a=$.ajax({
    url:this.url+'backend_mac_delete',
    type:'GET',
    data:{'backend_id':this.backend_id,'mac_id':mac_id},
    dataType:'json',
    async:false,
  });
  a.done(function(data) {
    success=true;
  });
  if (success) {
    return true;
  } else {
    return false;
  }
};

DC2.JSON.Backends.Ribs=function(backend_id) {
  this.url='/json/backends/ribs/';
  this.backend_id=backend_id;
  this.success=false;
};

DC2.JSON.Backends.Ribs.prototype.delete_rib=function(rib_id) {
  var success=false;
  var a=$.ajax({
    url:this.url+'backend_rib_delete',
    type:'GET',
      data:{'backend_id':this.backend_id,'rib_id':rib_id},
      dataType:'json',
      async:false,
  });
  a.done(function(data) {
    success=true;
  });
  return success;
};

$(document).ready(function() {

  $('.std-form').each(function() {
    if ($(this).attr('id') != null ) {
      DC2.Forms[$(this).attr('id')]=new DC2.Widgets.StandardForms("#"+$(this).attr('id'));
    }
  }); 
  $('.select-change-div').each(function() {
    if ($(this).attr('id') != null ) {
      new DC2.Widgets.SelectionChange('#'+$(this).attr('id'));
    }
  });
  $('.list-btn-group').each(function() {
    if ($(this).attr('id') != null ) {
      new DC2.Widgets.ButtonGroup.Index('#'+$(this).attr('id'));
    }
  });
  $('.data-list').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.DataList('#'+$(this).attr('id'));
    }
  });
  $('.data-form').each(function() {
    if ($(this).attr('id') != null && $(this).attr('data-remote')=='True') {
      new DC2.Widgets.DataForms('#'+$(this).attr('id'));
    }
  });
  $('.backendstats').each(function() {
    if ($(this).attr('id') != null ) {
      new DC2.JSONCalls.BackendStats('#'+$(this).attr('id'));
    }
  });
  $('.remote_backend_servers').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.JSONCalls.Servers('#'+$(this).attr('id'));
    }
  });

  $('.dashboard').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.Dashboard('#'+$(this).attr('id'));
    }
  });

  $('.datatable-lists').each(function() {
    if ($(this).attr('id') != null) {
      datatables={};
      datatables[$(this).attr('id')]=new DC2.Widgets.Datatables('#'+$(this).attr('id'));
    }
  });

  $('.widget-tab').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.Tabs('#'+$(this).attr('id'));
    }
  });
  $('.edit').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.EditTables('#'+$(this).attr('id'));
    }
  });

  $('.collapsible').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.Collapsible('#'+$(this).attr('id'));
    }
  });
});
