(function() {
  'use strict';

  var app = angular.module('vadskajagdricka', [
    'ngRoute',
    'controllers',
    'services',
    'filters'
  ])

  app.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/', {
          templateUrl: 'static/partials/home.html',
          controller: 'IndexController'
        })
        .when('/result', {
          templateUrl: 'static/partials/result.html',
          controller: 'ResultController'
        })
        .when('/result/water', {
          templateUrl: 'static/partials/water.html',
          controller: 'WaterController'
        })
        .when('/api', {
          templateUrl: 'static/partials/api.html'
        })
        .otherwise({
          redirectTo: '/'
        });

      $locationProvider.html5Mode(true);
    }]);
})();
