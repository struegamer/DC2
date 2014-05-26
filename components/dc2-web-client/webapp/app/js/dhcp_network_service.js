var gkad_services = angular.module('gkautodiscovery.services', ['ngResource']);

gkad_services.factory('DHCPNetworks', ['$resource', function($resource) {
  console.log('loading factory')
  return $resource('http://localhost:5000/api/v1/dhcp/networks', {},{
    list: {method: 'GET', params:null, isArray:true}
  });
}]);

gkad_services.factory('SockClient', function(socketFactory) {
  var myConnection = io.connect('http://localhost:5000/updates');
  console.log(myConnection)
  var mySocket = socketFactory({
    prefix:'',
    ioSocket: myConnection
  });
  return mySocket;
});
