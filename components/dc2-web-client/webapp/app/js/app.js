'use strict';

var gkautodiscovery = angular.module('gkautodiscovery', [
  'ngRoute'
]);

gkautodiscovery.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'app/partials/main.html'
      });
  }
]);