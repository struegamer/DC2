DC2.Pages.Admin.Backends.Sysusers.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_backend_sysusers');
  new DC2.Widgets.DataList('#list_backend_sysusers_index');
};

$(document).ready(function() {
  new DC2.Pages.Admin.Backends.Sysusers.Index();
});

