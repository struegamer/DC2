window.DC2 = {
  Widgets:{},
  Utilities:{},
  Forms:{},
  JSONCalls:{}
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

$(document).ready(function() {

  $('.std-form').each(function() {
    if ($(this).attr('id') != null ) {
      DC2.Forms[$(this).attr('id')]=new DC2.Widgets.StandardForms("#"+$(this).attr('id'));
    }
  }); 
  $('.btn-group').each(function() {
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
});
