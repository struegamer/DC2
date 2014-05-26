'use strict';

var gkad_controllers = angular.module('gkautodiscovery.controllers', []);

gkad_controllers.controller('MainController', function($scope) {

  $scope.isCollapsed = false;

  $scope.collapseLeft = function(event) {
    if ($scope.isCollapsed) {
      $scope.isCollapsed = false;
    } else {
      $scope.isCollapsed = true;
    }
    console.log('collapseLeft clicked');
  }
});

gkad_controllers.controller('DHCPController', ['$scope', 'DHCPNetworks', function($scope, DHCPNetworks) {
  if ($scope.dhcp_networks == undefined || $scope.dhcp_networks == null) {
    $scope.dhcp_networks = DHCPNetworks.list();
  }

  $scope.refreshDHCPNetworks = function(event) {
    $scope.dhcp_networks = DHCPNetworks.list();
  }
}]);

gkad_controllers.controller('SocketController', ['$scope', 'SockClient', function($scope, SockClient) {
  $scope.isConnected = false;
  console.log(SockClient);
  SockClient.on('connect', function(ev) {
    console.log('connected');
    $scope.isConnected=true;
  });
  SockClient.on('discovered_device', function(ev, data) {
    console.log(ev)
    console.log(data);
  });
  SockClient.on('disconnect', function(ev) {
    console.log('disconnected');
    $scope.isConnected=true;
  });
}]);