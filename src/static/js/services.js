(function() {

    'use strict';

    var app = angular.module('services', []);

    app.service('parseService', [function() {

        this.setImageResponse = function(res) {
            this.imageResponse = res.data;
        };

        this.getImageResponse = function() {
            return this.imageResponse;
        };

        this.setImage = function(image) {
            this.image = image;
        };

        this.getImage = function() {
            return this.image;
        };

        this.setBeverage = function(beverage) {
            this.beverage = beverage;
            console.log(beverage);
        }

        this.getBeverage = function() {
            return this.beverage;
            console.log(beverage);
        }

    }]);

})();
