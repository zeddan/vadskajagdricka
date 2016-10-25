(function() {

    'use strict';

    var app = angular.module('filters', []);

    app.filter('price', function() {
        return function(price) {
            return price + " SEK";
        };
    });

    app.filter('alcohol', function() {
        return function(alcohol) {
            return Math.round(alcohol * 100) + " %";
        };
    });

    app.filter('volume', function() {
        return function(volume) {
            return volume + " l";
        };
    });

})();
