DC2.Pages.Backends.Show=function() {
  new DC2.Widgets.Tabs('#dc_inventory');
  $('.datatable-lists').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.Datatables('#'+$(this).attr('id'));
    }
  });
};

$(document).ready(function() {
  new DC2.Pages.Backends.Show();
});
