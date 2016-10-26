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
                templateUrl: 'static/partials/landing.html',
                controller: 'IndexController'
            })
            .when('/picture', {
                templateUrl: 'static/partials/picture.html',
                controller: 'PictureController'
            })
            .when('/picture/water', {
                templateUrl: 'static/partials/water.html',
                controller: 'WaterController'
            })
            .when('/about', {
                templateUrl: 'static/partials/about.html',
                controller: 'AboutController'
            })
            .otherwise({
                redirectTo: '/'
            });

            $locationProvider.html5Mode(true);
    }]);
})();
