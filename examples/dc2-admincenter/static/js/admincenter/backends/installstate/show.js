DC2.Pages.Backends.Deployments.Show=function() {
  new DC2.Widgets.Tabs('#installstate_information');
  new DC2.JSONCalls.Freeipa($('#freeipa_host_check'));

};

$(document).ready(function() {
  new DC2.Pages.Backends.Deployments.Show();
});
