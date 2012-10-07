DC2.Pages.Admin.Ribs.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_rib');
  new DC2.Widgets.DataList('#list_ribs_index');
};

$(document).ready(function() {
  new DC2.Pages.Admin.Ribs.Index();
});
