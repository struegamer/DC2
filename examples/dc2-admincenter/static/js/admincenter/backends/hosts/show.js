DC2.Pages.Backends.Hosts.Show=function() {
  new DC2.Widgets.Tabs('#host_informations');
  new DC2.JSONCalls.Freeipa($('#freeipa_host_check'));
};

$(document).ready(function() {
  new DC2.Pages.Backends.Hosts.Show();
});
