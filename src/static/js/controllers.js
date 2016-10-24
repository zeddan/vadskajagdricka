(function() {
    'use strict';

    var app = angular.module('controllers', ['ngCookies']);

    app.controller('IndexController', [
    '$scope',
    '$http',
    '$cookies',
    '$location',
    'parseService',
    function ($scope, $http, $cookies, $location, parseService) {

        if ($cookies.get("camera_access") === 'true') {
            navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
                var video = document.getElementById('video');
                video.src = window.URL.createObjectURL(stream);
                video.play();
                $scope.$apply(function() {
                    $scope.cameraAccess = true;
                });
            });
        }
        
        $scope.requestCamera = function() { 
            if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
                    var video = document.getElementById('video');
                    video.src = window.URL.createObjectURL(stream);
                    video.play();
                    $scope.$apply(function() {
                        $scope.cameraAccess = true;
                        $cookies.put("camera_access", 'true');
                    });
                });
            }
        };
        
        $scope.snap = function() {
            var canvas = document.getElementById('canvas');
            var context = canvas.getContext('2d');
            var video = document.getElementById('video');
        
            context.drawImage(video, 0, 0, 640, 480);
        
            var img = canvas.toDataURL();
            var b64 = img.split(",")[1];

            var i = new Image();
            i.src = img;
            parseService.setImage(i);
        
            $http.post('http://localhost:5000/api/picture', {"image": b64})
            .then(function(res) {
                console.log(res); 
        
                parseService.parse(res);
                parseService.setImage(img);

                var jsonb64 = btoa(JSON.stringify(res.data));
        
                $http.get('http://localhost:5000/api/beverages?' + jsonb64)
                .then(function(res) {
                    console.log(res); 
                    parseService.setBeverages(res);
                }, function(err) {
                    console.log(err); 
                });
        
            }, function(err) {
                console.log("error"); 
                console.log(err); 
            });

            $location.path("/picture");

        };
    }]);

    app.controller('PictureController', [
    '$scope',
    'parseService',
    function($scope, parseService) {
        // $scope.labels = parseService.imageResponse.labels;
        $scope.imageResponse = parseService.imageResponse; 
        $scope.labels = ['Clothing Hat'];
        var canvas = document.getElementById('result_canvas');
        var img = parseService.getImage();;
        var context = canvas.getContext("2d");
        context.scale(0.45, 0.45);
        context.drawImage(img, 0, 0);

        // $scope.beverages = parseService.getBeverages();

        $scope.name  = "Adelsö";
        $scope.name2 = "Rocket Indian Pale Ale";
        $scope.price = "27:80 SEK";
        $scope.alcohol = "4%";
        $scope.volume  = "330 ml";
        



    }]);

    function AboutController($scope) {
        
    }

})();
