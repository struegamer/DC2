DC2.Pages.Admin.Backends.Sysusers.AddEdit=function() {
  new DC2.EditForm.SysUsers($('#edit_systemusers'));
};

$(document).ready(function() {
  new DC2.Pages.Admin.Backends.Sysusers.AddEdit();
});
