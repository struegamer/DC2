DC2.KeyHandler.SubmitOnReturn=function(selector) {
  this.selector=selector;
  this.selector.on('keypress',this.selector,this.submitForm.bind(this));
};

DC2.KeyHandler.SubmitOnReturn.prototype.submitForm=function(event) {
  if (event && event.which == 13) {
    this.selector.submit();
  }
};

