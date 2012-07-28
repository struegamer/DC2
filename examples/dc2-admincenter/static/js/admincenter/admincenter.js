window.DC2 = {
  Widgets:{},
  Utilities:{},
  Forms:{}
};

DC2.Widgets.FormSubmit = function(selector) {
  this.container=$(selector);
  this.container.on('keypress',this.container,this.submitForm.bind(this));
};


DC2.Widgets.FormSubmit.prototype.submitForm = function (event) {
  if (event && event.which == 13) {
    this.container.submit();
  }
};

DC2.Widgets.ButtonGroup = {};

DC2.Widgets.ButtonGroup.Index = function(selector) {
  this.container=$(selector);
  var _this=this
  this.container.children('button').each(function(index,value) {
    $(this).on('click',_this.container,_this.action.bind(this));
  });
};

DC2.Widgets.ButtonGroup.Index.prototype.action=function(event) {
  data_type=$(this).attr('data-type');
  switch(data_type) {
    case 'url':
      window.location.href=$(this).attr('data-url');
      break;
    case 'jsfunc':
      if ($(this).attr('data-list')=='true') {
        if ($(this).attr('data-action')=='delete') {
          $('table.data-list').find('input[type="checkbox"].del_check').each(function() {
            a=$.ajax({
              url:$('table.data-list').attr('data-url-delete')+$(this).val(),
              type:'DELETE',
              // complete:function() { window.location.href=$('table.data-list').attr('data-url-delete'); }
            });
          });
        }
      }
      break;
  }
};


DC2.Widgets.DataList = function(selector) {
  this.container=$(selector);
  this.container.find('thead tr th input[type="checkbox"]').on('click',this.container,this.del_check.bind(this));
  this.container.find('tbody tr td.data-cell').on('click',this.container,this.edit.bind(this));
};

DC2.Widgets.DataList.prototype.del_check = function(event) {
  _this=this
  this.container.find('tbody tr td input[type="checkbox"].del_check').each(function() {
    this.checked=_this.container.find('thead tr th input[type="checkbox"]').prop('checked');
  });

};

DC2.Widgets.DataList.prototype.edit = function(event) {
  _this=this;
  window.location.href=$(event.target).parent().attr('data-edit-url');
};



$(document).ready(function() {

  $('form').each(function() {
    if ($(this).attr('id') != null ) {
      DC2.Forms[$(this).attr('id')]=new DC2.Widgets.FormSubmit("#"+$(this).attr('id'));
    }
  });
  $('.btn-group').each(function() {
    if ($(this).attr('id') != null ) {
      new DC2.Widgets.ButtonGroup.Index('#'+$(this).attr('id'));
    }
  });
  $('.data-list').each(function() {
    if ($(this).attr('id') != null) {
      new DC2.Widgets.DataList('#'+$(this).attr('id'));
    }
  });
});
