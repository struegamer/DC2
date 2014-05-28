'use strict';

var gkautodiscovery = angular.module('gkautodiscovery', [
  'ngRoute',
  'btford.socket-io',
  'ui.bootstrap',
  'gkautodiscovery.controllers',
  'gkautodiscovery.services'
]);

gkautodiscovery.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'app/partials/main.html'
      });
  }
]);