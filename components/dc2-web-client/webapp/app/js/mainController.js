'use strict';

var gkad_controllers = angular.module('gkautodiscovery.controllers', []);

gkad_controllers.controller('MainController', function($scope) {

  $scope.isCollapsed = false;
  $scope.$on('SocketController:discovered_rack', function(event, data) {
    if ($scope.discovered_racks == undefined) {
      $scope.discovered_racks = {};
    }
    var rackname = data['rack_no']+'.'+data['cluster_no']+'.'+data['dcname'];
    if (!(rackname in $scope.discovered_racks)) {
      $scope.discovered_racks[rackname]={};
      $scope.discovered_racks[rackname]['rack'] = rackname;
      $scope.discovered_racks[rackname]['data'] = data;
      $scope.discovered_racks[rackname]['devices'] = [];
    }

  });

  $scope.$on('SocketController:discovered_device', function(event, data) {
    if (data) {
      var rackname = data['rack_no']+'.'+data['cluster_no']+'.'+data['dcname'];
      if (rackname in $scope.discovered_racks) {
        if (!('devices' in $scope.discovered_racks[rackname])) {
          $scope.discovered_racks[rackname]['devices']=[];
        }
        $scope.discovered_racks[rackname]['devices'].push(data['device_type']);
      }
    }
  })
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
    $scope.isConnected=true;
  });
  SockClient.on('discovered_rack', function(ev, data) {
    if ($scope.messages == undefined) {
        $scope.messages = [];
    }
    if ($scope.messages.length > 4) {
      $scope.messages.shift();
    }
    $scope.messages.push("New discovery: "+ev.rack_no+'.'+ev.cluster_no+'.'+ev.dcname);
    $rootScope.$broadcast('SocketController:discovered_rack',ev)
  });
  SockClient.on('discovered_device', function(ev, data) {
    console.log(ev);
    if ($scope.messages == undefined) {
      $scope.messages = [];
    }
    if ($scope.messages.length > 4) {
      $scope.messages.shift();
    }
    $scope.messages.push("New device: "+ev.device_type+' ('+ev.rack_no+'.'+ev.cluster_no+'.'+ev.dcname+')');
    $rootScope.$broadcast('SocketController:discovered_device', ev);
  })
  SockClient.on('disconnect', function(ev) {
    $scope.isConnected=false;

  });
}]);

gkad_controllers.controller('RackController', ['$rootScope', '$scope', function($rootScope, $scope) {
  console.log("RackController: ");
  $scope.rack_collapsed=false;
  $scope.rack = $scope.rackoon;
  $scope.rackCollapse = function(event) {
    if ($scope.rack_collapsed) {
      $scope.rack_collapsed=false;
    } else {
      $scope.rack_collapsed=true;
    }
  };
}]);