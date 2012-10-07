DC2.Pages.Index=function() {
  new DC2.KeyHandler.SubmitOnReturn($('#loginform'));
  //
  // DashBoard
  //
  $('.backendstats').each(function() {
    if ($(this).attr('id') != null ) {
      new DC2.JSONCalls.BackendStats('#'+$(this).attr('id'));
    }
  });
  $('.dashboard').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.Dashboard('#'+$(this).attr('id'));
    }
  });
};
  
$(document).ready(function() {
  new DC2.Pages.Index();
});

