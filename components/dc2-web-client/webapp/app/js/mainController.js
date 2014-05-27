'use strict';

var gkad_controllers = angular.module('gkautodiscovery.controllers', []);

gkad_controllers.controller('MainController', function($scope) {

  $scope.isCollapsed = false;
  $scope.$on('SocketController:discovered',function(event, data) {
    if ($scope.discovered_racks == undefined) {
      $scope.discovered_racks = {};
    }
    rackname=data.rack_no+'.'data.cluster_no+'.'+data.dcname;
    $scope.discovered_racks[rackname]={};
    $scope.discovered_racks[rackname]['rack'] = rackname;
    $scope.discovered_racks[rackname]['data'] = data;

  });
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

gkad_controllers.controller('SocketController', ['$rootScope','$scope', 'SockClient', function($rootScope,$scope, SockClient) {
  $scope.isConnected = false;
  SockClient.on('connect', function(ev) {
    console.log('connected');
    $scope.isConnected=true;
  });
  SockClient.on('discovered_device', function(ev, data) {
    if ($scope.messages == undefined) {
        $scope.messages = [];
    }
    if ($scope.messages.length > 5) {
      $scope.messages.shift();
    }
    $scope.messages.push("New discovery: "+ev.rack_no+ev.cluster_no+ev.dcname);
    $rootScope.$broadcast('SocketController:discovered',ev)
  });
  SockClient.on('disconnect', function(ev) {
    console.log('disconnected');
    $scope.isConnected=false;

  });
  SockClient.on('heartbeat', function(ev) {
    console.log('Heartbeat');
    console.log(ev);
  });
}]);