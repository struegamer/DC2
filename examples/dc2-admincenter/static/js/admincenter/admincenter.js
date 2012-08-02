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

DC2.Widgets.Dashboard=function(selector) {
  this.container=$(selector);
  this.container.find('tbody td.data-cell').on('click',this.container,this.on_click.bind(this));
};

DC2.Widgets.Dashboard.prototype.on_click=function(event) {
  window.location.href='/backends/?backend_id='+$(event.target).parent().attr('data-backend-id');
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
  console.log(this.container.attr('method'));
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
  console.log(this.container.attr('method'));

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
  console.log(data);
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
      console.log('dataforms true')
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


});
