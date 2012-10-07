DC2.Pages.Admin.Backends.Pxemethods.Index=function() {
  new DC2.Widgets.ButtonGroup.Index('#btngrp_backend_pxemethods');
  new DC2.Widgets.DataList('#list_backend_pxemethods_index');
  new DC2.Widgets.Button.Click($('.btn_updateHW'),function(event) {
    event.preventDefault();
    console.log($(event.target).attr('data-url'));
    var a=$.ajax({
      url:$(event.target).attr('data-url'),
        type:'GET',
        dataType:'json',
        contentType:'application/json; charset-utf-8',
    });
    a.done(function(data) {
      console.log(data);
      if ('redirect' in data) {
        window.location.href=data.redirect.url;
      }
    });

  });
};

$(document).ready(function() {
  new DC2.Pages.Admin.Backends.Pxemethods.Index();
});

