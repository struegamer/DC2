window.DC2 = {
  Widgets:{},
  Utilities:{},
  Forms:{}
};

DC2.Widgets.FormSubmit = function(selector) {
  this.container=$(selector);
  console.log(this.container);
  this.container.on('keypress',this.container,this.submitForm.bind(this));
};

DC2.Widgets.FormSubmit.prototype.submitForm = function (event) {
  if (event && event.which == 13) {
    this.container.submit();
  }
};

$(document).ready(function() {

  $('form').each(function() {
    if ($(this).attr('id') != null ) {
      DC2.Forms[$(this).attr('id')]=new DC2.Widgets.FormSubmit("#"+$(this).attr('id'));
    }
  });
});
