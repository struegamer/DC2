DC2.Pages.Backends.Servers.Show=function() {
  new DC2.Widgets.Tabs('#server_informations');
  new DC2.Widgets.Button.Click($('#delete_server'),function (event) {
	  event.preventDefault();
	  var server_id=$(event.target).attr('data-server-id');
	  var backend_id=$(event.target).attr('data-backend-id');
	  var a=$.ajax({
		  url:'/admin/json/backends/servers/backend_server_delete?backend_id='+backend_id+'&server_id='+server_id,
		  type:'DELETE',
		  contentType:'application/json; charset=utf-8',
		  dataType:'json',
		  async:false,
	  });
	  a.done(function(data) {
		 if ('redirect' in data) {
			 window.location.href=data.redirect.url;
		 }
	  });
  });
};

$(document).ready(function() {
  new DC2.Pages.Backends.Servers.Show();
});
