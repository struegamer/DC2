DC2.Pages.Admin.Pxe.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_pxe');
  new DC2.Widgets.DataList('#list_pxe_index');
};

$(document).ready(function() {
  new DC2.Pages.Admin.Pxe.Index();
});
