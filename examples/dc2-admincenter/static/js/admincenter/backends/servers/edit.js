DC2.Pages.Backends.Servers.Edit=function() {
  new DC2.Widgets.Tabs('#server_informations');
  new DC2.Widgets.EditTables('#server');
};

$(document).ready(function() {
  new DC2.Pages.Backends.Servers.Edit();
});


