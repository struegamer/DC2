DC2.Pages.Backends.Hosts.Edit=function() {
  new DC2.Widgets.Tabs('#host_informations');
  new DC2.Widgets.EditTables('#hosts');
  $('.collapsible').each(function() {
    if ($(this).attr('id')!=null) {
      new DC2.Widgets.Collapsible('#'+$(this).attr('id'));
    }
  });
  $('.select-change-div').each(function() {
    if ($(this).attr('id') != null && $(this).attr('data-iface-type')!=undefined) {
      new DC2.Widgets.SelectionChange('#'+$(this).attr('id'),'iface');
    }
  });

};

$(document).ready(function() {
  new DC2.Pages.Backends.Hosts.Edit();
});


