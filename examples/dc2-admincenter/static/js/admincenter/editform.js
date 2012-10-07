DC2.EditForm.Environments=function(selector) {
  this.selector=selector;
  this.btnAdd=this.selector.find('.btnAdd');
  this.btnAdd.on('click',this.selector,this.on_btnAdd_click.bind(this));
  this.selector.find('button.btnRemove').on('click',this.selector,this.on_btnRemove_click.bind(this));
  this.btnSave=this.selector.find('.btnSave');
  this.btnSave.on('click',this.selector,this.on_btnSave_click.bind(this));
  this.btnCancel=this.selector.find('.btnCancel');
  this.btnCancel.on('click',this.selector,this.on_btnCancel_click.bind(this));
  this.addRow=this.selector.find('#add_row_environment.add-table-row tbody');
  this.rowCounter=0;
};


DC2.EditForm.Environments.prototype.on_btnAdd_click=function(event) {
  var table=this.selector.find('table.edit-table tbody');
  var temp_row=this.addRow.clone();
  this.rowCounter++;
  var _this=this;
  temp_row.find(':input').not('button').each(function() {
    var name=$(this).attr('name');
    name=name.replace('new','new_'+_this.rowCounter);
    $(this).attr('name',name);
  });
  table.append(temp_row.html());
  this.selector.find('button.btnRemove').off('click');
  this.selector.find('button.btnRemove').on('click',this.selector,this.on_btnRemove_click.bind(this));
  event.preventDefault();
};

DC2.EditForm.Environments.prototype.on_btnRemove_click=function(event) {
  $(event.target).parent().parent().remove();
  event.preventDefault();
};

DC2.EditForm.Environments.prototype.on_btnCancel_click=function(event) {
  event.preventDefault();
  window.location.href=$(event.target).attr('data-cancel-url');
};

DC2.EditForm.Environments.prototype.on_btnSave_click=function(event) {
  event.preventDefault();
    console.log(this.selector.find('form').attr('action'));
    var put_url=this.selector.find('form').attr('action');
    var sectoken=this.selector.find(':input[name=sectoken]').val();
    var result=this.selector.find('form').formParams();
    var action_type='POST'
    if ($(event.target).attr('data-action')=='new') {
      action_type='POST';
    } else if ($(event.target).attr('data-action')=='edit') {
      action_type='PUT';
    }
    var a=$.ajax({
      url:put_url+'&sectoken='+sectoken,      
      type:action_type,
      contentType:'application/json; charset=utf-8',
      data:JSON.stringify({'result':result}),
      dataType:'json',
    });
    a.done(function(data) {
      if ('redirect' in data) {
        if (data.redirect.absolute=='true') {
          window.location.href=data.redirect.url;
        }
      }
    });
};

DC2.EditForm.ClassTemplates=function(selector) {
  this.selector=selector;
  this.defaultclasses=this.selector.find('#defaultclasses');
  this.template_classes=this.selector.find('#template_classes');
  this.btnPlus=this.selector.find('.btnPlus');
  this.btnPlus.on('click',this.selector,this.on_btnPlus_click.bind(this));
  this.btnMinus=this.selector.find('.btnMinus');
  this.btnMinus.on('click',this.selector,this.on_btnMinus_click.bind(this));
  this.btnSave=this.selector.find('.btnSave');
  this.btnSave.on('click',this.selector,this.on_btnSave_click.bind(this));
  this.btnCancel=this.selector.find('.btnCancel');
  this.btnCancel.on('click',this.selector,this.on_btnCancel_click.bind(this));
};

DC2.EditForm.ClassTemplates.prototype.on_btnPlus_click=function(event) {
  event.preventDefault();
  var _this=this;
  this.defaultclasses.find('option:selected').each(function () {
    _this.template_classes.append(this);
  });
  this.sort_options(this.template_classes);
};

DC2.EditForm.ClassTemplates.prototype.sort_options=function(select_selector) {
  var options=select_selector.find('option');
  options.sort(function(a,b) {
    if (a.text > b.text) {
      return 1;
    } else if (a.text < b.text) {
      return -1;
    } else {
      return 0;
    }
  });
  select_selector.empty().append(options);
};

DC2.EditForm.ClassTemplates.prototype.on_btnMinus_click=function(event) {
  event.preventDefault();
  var _this=this;
  this.template_classes.find('option:selected').each(function() {
    _this.defaultclasses.append(this);
  })
  this.sort_options(this.defaultclasses);

};

DC2.EditForm.ClassTemplates.prototype.on_btnSave_click=function(event) {
  event.preventDefault();
  var action_type=$(event.target).attr('data-action');
  var action_method='POST';
  if (action_type=='add') {
    action_method='POST';
  } else if (action_type=='edit') {
    action_method='PUT'
  }
  var put_url=this.selector.find('form').attr('action');
  var sectoken=this.selector.find(':input[name=sectoken]').val();
  var result=this.selector.find('form').formParams();
  var a=$.ajax({
    url:put_url+'&sectoken='+sectoken,
      type:action_method,
      contentType:'application/json; charset=utf-8',
      data:JSON.stringify({'result':result}),
      dataType:'json',
  });
  a.done(function(data) {
    if ('redirect' in data) {
      if (data.redirect.absolute=='true') {
        window.location.href=data.redirect.url;
      }
    }
  });
};

DC2.EditForm.ClassTemplates.prototype.on_btnCancel_click=function(event) {
  event.preventDefault();
  window.location.href=$(event.target).attr('data-cancel-url');

};

DC2.EditForm.DefaultClasses=function(selector) {
  this.selector=selector;
  this.btnSave=this.selector.find('.btnSave');
  this.btnCancel=this.selector.find('.btnCancel');
  this.btnSave.on('click',this.selector,this.on_btnSave_click.bind(this));
  this.btnCancel.on('click',this.selector,this.on_btnCancel_click.bind(this));
};

DC2.EditForm.DefaultClasses.prototype.on_btnSave_click=function(event) {
  event.preventDefault();
  var action_type=$(event.target).attr('data-action');
  var action_method='POST';
  if (action_type=='add') {
    action_method='POST';
  } else if (action_type=='edit') {
    action_method='PUT'
  }
  var put_url=this.selector.find('form').attr('action');
  var sectoken=this.selector.find(':input[name=sectoken]').val();
  var result=this.selector.find('form').formParams();
  var a=$.ajax({
    url:put_url+'&sectoken='+sectoken,
      type:action_method,
      contentType:'application/json; charset=utf-8',
      data:JSON.stringify({'result':result}),
      dataType:'json',
  });
  a.done(function(data) {
    if ('redirect' in data) {
      if (data.redirect.absolute=='true') {
        window.location.href=data.redirect.url;
      }
    }
  });
};

DC2.EditForm.DefaultClasses.prototype.on_btnCancel_click=function(event) {
  event.preventDefault();
  window.location.href=$(event.target).attr('data-cancel-url');
};


DC2.EditForm.SysGroups=function(selector) {
  this.selector=selector;
  console.log('sysgroups');
  this.btnSave=this.selector.find('.btnSave');
  this.btnCancel=this.selector.find('.btnCancel');
  this.btnSave.on('click',this.selector,this.on_btnSave_click.bind(this));
  this.btnCancel.on('click',this.selector,this.on_btnCancel_click.bind(this));
};

DC2.EditForm.SysGroups.prototype.on_btnSave_click=function(event) {
  event.preventDefault();
  var action_type=$(event.target).attr('data-action');
  var action_method='POST';
  if (action_type=='new') {
    action_method='POST';
  } else if (action_type=='edit') {
    action_method='PUT'
  }
  var put_url=this.selector.find('form').attr('action');
  var sectoken=this.selector.find(':input[name=sectoken]').val();
  var result=this.selector.find('form').formParams();
  console.log(result);
  var a=$.ajax({
    url:put_url+'&sectoken='+sectoken,
      type:action_method,
      contentType:'application/json; charset=utf-8',
      data:JSON.stringify({'result':result}),
      dataType:'json',
  });
  a.done(function(data) {
    if ('redirect' in data) {
      if (data.redirect.absolute=='true') {
        window.location.href=data.redirect.url;
      }
    }
  });
};

DC2.EditForm.SysGroups.prototype.on_btnCancel_click=function(event) {
  event.preventDefault();
  window.location.href=$(event.target).attr('data-cancel-url');
};


DC2.EditForm.SysUsers=function(selector) {
  this.selector=selector;
  this.btnSave=this.selector.find('.btnSave');
  this.btnCancel=this.selector.find('.btnCancel');
  this.btnSave.on('click',this.selector,this.on_btnSave_click.bind(this));
  this.btnCancel.on('click',this.selector,this.on_btnCancel_click.bind(this));
};

DC2.EditForm.SysUsers.prototype.on_btnSave_click=function(event) {
  event.preventDefault();
  var action_type=$(event.target).attr('data-action');
  var action_method='POST';
  if (action_type=='new') {
    action_method='POST';
  } else if (action_type=='edit') {
    action_method='PUT'
  }
  var put_url=this.selector.find('form').attr('action');
  var sectoken=this.selector.find(':input[name=sectoken]').val();
  var result=this.selector.find('form').formParams();
  console.log(result);
  var a=$.ajax({
    url:put_url+'&sectoken='+sectoken,
      type:action_method,
      contentType:'application/json; charset=utf-8',
      data:JSON.stringify({'result':result}),
      dataType:'json',
  });
  a.done(function(data) {
    if ('redirect' in data) {
      if (data.redirect.absolute=='true') {
        window.location.href=data.redirect.url;
      }
    }
  });

};

DC2.EditForm.SysUsers.prototype.on_btnCancel_click=function(event) {
  event.preventDefault();
  window.location.href=$(event.target).attr('data-cancel-url');
};


DC2.EditForm.PXEMethods=function(selector) {
  this.selector=selector;
  this.btnSave=this.selector.find('.btnSave');
  this.btnCancel=this.selector.find('.btnCancel');
  this.btnSave.on('click',this.selector,this.on_btnSave_click.bind(this));
  this.btnCancel.on('click',this.selector,this.on_btnCancel_click.bind(this));
};

DC2.EditForm.PXEMethods.prototype.on_btnSave_click=function(event) {
  event.preventDefault();
  var action_type=$(event.target).attr('data-action');
  var action_method='POST';
  if (action_type=='new') {
    action_method='POST';
  } else if (action_type=='edit') {
    action_method='PUT'
  }
  var put_url=this.selector.find('form').attr('action');
  var sectoken=this.selector.find(':input[name=sectoken]').val();
  var result=this.selector.find('form').formParams();
  console.log(result);
  var a=$.ajax({
    url:put_url+'&sectoken='+sectoken,
      type:action_method,
      contentType:'application/json; charset=utf-8',
      data:JSON.stringify({'result':result}),
      dataType:'json',
  });
  a.done(function(data) {
    if ('redirect' in data) {
      if (data.redirect.absolute=='true') {
        window.location.href=data.redirect.url;
      }
    }
  });
};

DC2.EditForm.PXEMethods.prototype.on_btnCancel_click=function(event) {
  event.preventDefault();
  console.log($(event.target).attr('data-cancel-url'));
  window.location.href=$(event.target).attr('data-cancel-url');
};
