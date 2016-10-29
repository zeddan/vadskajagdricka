(function() {

    'use strict';

    var app = angular.module('services', []);

    app.service('parseService', [function() {

        this.setImageResponse = function(res) {
            this.imageResponse = res.data;
        };

        this.setImage = function(image) {
            this.image = image;
        };

        this.setBeverage = function(beverage) {
            this.beverage = beverage;
        }

    }]);

})();
