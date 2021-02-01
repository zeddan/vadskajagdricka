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
      var decimals = alcohol.toString().split(".")[1].length;
      if (decimals <= 2)
        return Math.round(alcohol * 100) + " %";
      else if (decimals == 3)
        return (alcohol * 100).toFixed(1) + " %";
      else if (decimals == 4)
        return (alcohol * 100).toFixed(2) + " %";
    };
  });

  app.filter('volume', function() {
    return function(volume) {
      return volume + " l";
    };
  });
})();
