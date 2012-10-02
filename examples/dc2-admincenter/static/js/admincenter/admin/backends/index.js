DC2.Pages.Admin.Backends.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_backends');
  new DC2.Widgets.DataList('#list_backend_index');
};

$(document).ready(function() {
  new DC2.Pages.Admin.Backends.Index();
});
