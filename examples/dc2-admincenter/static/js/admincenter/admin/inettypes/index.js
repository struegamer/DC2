DC2.Pages.Admin.Inettypes.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_inettypes');
  new DC2.Widgets.DataList('#list_inettypes_index');
};

$(document).ready(function() {
  new DC2.Pages.Admin.Inettypes.Index();
});
