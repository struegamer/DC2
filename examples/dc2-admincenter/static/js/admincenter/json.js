DC2.JSON.Backends={};
DC2.JSON.Backends.Macs=function(backend_id) {
  this.url='/json/backends/macs/';
  this.backend_id=backend_id;
  this.success=false;
};
DC2.JSON.Backends.Macs.prototype.delete_mac=function(mac_id) {
  var success=false;
  var a=$.ajax({
    url:this.url+'backend_mac_delete',
    type:'GET',
    data:{'backend_id':this.backend_id,'mac_id':mac_id},
    dataType:'json',
    async:false,
  });
  a.done(function(data) {
    success=true;
  });
  if (success) {
    return true;
  } else {
    return false;
  }
};

DC2.JSON.Backends.Ribs=function(backend_id) {
  this.url='/json/backends/ribs/';
  this.backend_id=backend_id;
  this.success=false;
};

DC2.JSON.Backends.Ribs.prototype.delete_rib=function(rib_id) {
  var success=false;
  var a=$.ajax({
    url:this.url+'backend_rib_delete',
    type:'GET',
      data:{'backend_id':this.backend_id,'rib_id':rib_id},
      dataType:'json',
      async:false,
  });
  a.done(function(data) {
    success=true;
  });
  return success;
};

