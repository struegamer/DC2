DC2.Pages.Backends.Index=function() {
  $('.list-btn-group').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.ButtonGroup.Index('#'+$(this).attr('id'));
    }
  });

};
