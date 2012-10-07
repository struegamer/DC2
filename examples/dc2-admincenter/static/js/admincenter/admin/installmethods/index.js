DC2.Pages.Admin.Installmethods.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_installmethods');
  new DC2.Widgets.DataList('#list_installmethods_index');
};

$(document).ready(function() {
  new DC2.Pages.Admin.Installmethods.Index();
});
