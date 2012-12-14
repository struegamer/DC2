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
	  if ('error' in data && data.error==true) {
		  this.container.removeClass('label-success').addClass('label-important').html('Error: '+data.error_type+' ('+data.error_msg+')');
		  return(false);
	  }	  
	  this.container.html(data.server_count);
  });
  return(false);
};

DC2.JSONCalls.BackendStats.prototype.backend_hosts_stats=function(event,backend_id) {
  a=this.do_remote('backend_hosts_stats',{'backend_id':backend_id});
  a.done(function(data) {
	  if ('error' in data && data.error==true) {
		  this.container.removeClass('label-success').addClass('label-important').html('Error: '+data.error_type+' ('+data.error_msg+')');
		  return(false);
	  }	  	  
    this.container.html(data.host_count);
  });
  return(false);
};

DC2.JSONCalls.BackendStats.prototype.backend_deployment_stats=function(event,backend_id,what) {
  a=this.do_remote('backend_deployment_stats',{'backend_id':backend_id,'status':what});
  a.done(function(data) {
	  if ('error' in data && data.error==true) {
		  this.container.removeClass('label-success').addClass('label-important').html('Error: '+data.error_type+' ('+data.error_msg+')');
		  return(false);
	  }	  	  	  
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


DC2.JSONCalls.Freeipa = function(selector) {
	this.container=selector;
	this.freeipa_container=this.container.find('.freeipa')	
	this.type=this.freeipa_container.attr('data-type');
	this.backend_id=this.freeipa_container.attr('data-backend-id')
	this.data_id=null;
	this.action=this.freeipa_container.attr('data-action')
	if (this.type=='host') {
		this.data_id=this.freeipa_container.attr('data-host-id');		
	}
	
	if (this.action=='check') {
		console.log(this.freeipa_container);
		this.freeipa_container.on('freeipa_check.'+this.type+'.update',this.freeipa_container,this.do_host_check.bind(this));
	}
	this.freeipa_container.trigger('freeipa_check.'+this.type+'.update');

};

DC2.JSONCalls.Freeipa.prototype.do_remote = function(url) {
	var spinnerIMG=$('<img class="spinner" src="/static/img/ajax/kit-spinner.gif"></img>');
	var _this=this;
	var a=$.ajax({
		url:url,
		type:'GET',
		contentType:'application/json; charset=utf-8',
		dataType:'json',
		context:this,
		beforeSend:function(xhr,settings) {
			_this.freeipa_container.html(spinnerIMG);
			console.log(_this.freeipa_container);
		}
	});
	return(a);
};

DC2.JSONCalls.Freeipa.prototype.do_add=function(event) {
	console.log(this.backend_id);
}

DC2.JSONCalls.Freeipa.prototype.do_host_check=function(event) {
	console.log(this.backend_id)
	var a=this.do_remote('/json/freeipa/hosts/check?backend_id='+this.backend_id+'&host_id='+this.data_id);
	var _this=this;
	a.done(function(data) {
		if (data.in_freeipa==true) {
			_this.freeipa_container.remove('.spinner');			
			_this.freeipa_container.addClass('label label-success');
			_this.freeipa_container.html('True');
		} else {
			_this.freeipa_container.remove('.spinner');
			_this.freeipa_container.addClass('label label-important');
			_this.freeipa_container.html('False');
		}
	});
};
