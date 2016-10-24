(function() {

    'use strict';

    var app = angular.module('services', []);

    app.service('parseService', [function() {

        this.parse = function(res) {
            this.imageResponse = res.data;
            console.log(this.imageResponse);
        };

        this.setImage = function(image) {
            this.image = image;
        };

        this.getImage = function() {
            return this.image;
        };

        this.setBeverages = function(beverages) {
            this.beverages = beverages;
        };

        this.getBeverages = function() {
            return this.beverages;
        };

    }]);

})();
