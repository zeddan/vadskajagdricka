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

            // the bar is closed between 09:00 and 12:00
            var hour = new Date().getHours();
            if (hour >= 9 && hour <= 12) {
                $location.path("/result/water");
            }
            
            // otherwise, proceed as usual
            else {
                var canvas = document.getElementById('canvas');
                var context = canvas.getContext('2d');
                var video = document.getElementById('video');
            
                // take a snapshot of the video
                context.drawImage(video, 0, 0, 640, 480);
            
                var img = canvas.toDataURL();
                var b64 = img.split(",")[1];

                var i = new Image();
                i.src = img;
                parseService.setImage(i);
            
                var url = 'http://localhost:5000/api/result';
                $http.post(url, {"image": b64}).then(function(res) {
                    parseService.setImageResponse(res);
                    $location.path("/result");
                }, function(err) {
                    if (err.status == 422) {
                        $scope.errorMessage = "We couldn't identify any face in " +
                                            "your picture, please try again."
                    }
                    console.log("error fetching imageResponse: ", err);
                });
            }

        };
    }]);

    app.controller('ResultController', [
    '$scope',
    '$http',
    'parseService',
    function($scope, $http, parseService) {

        var date  = new Date();
        var hour  = date.getHours();
        var month = date.getMonth() + 1;
         
        var url = 'http://localhost:5000/api/beverages';
        var params = {
            'price': parseService.imageResponse.emotionScore,
            'alcohol': parseService.imageResponse.brightness,
            'ecological': parseService.imageResponse.ecological,
            'hour': hour,
            'month': month
        }

        // fetch beverage
        $http.get(url, {'params': params}).then(function(res) {
            $scope.beverage = res.data[0];
            console.log("beverage: ", $scope.beverage);
        }, function(err) {
            console.log("error fetching beverage: ", err);
        });
        
        // "nice XX you got there"
        $scope.labels = parseService.imageResponse.labels;

        // render image
        var canvas = document.getElementById('result_canvas');
        var img = parseService.image;;
        var context = canvas.getContext("2d");
        context.scale(0.45, 0.45);
        context.drawImage(img, 0, 0);

    }]);

    app.controller('WaterController', [
    '$scope',
    function($scope) {
        var date = new Date();
        $scope.hour = date.getHours();
        $scope.min  = date.getMinutes();
        $scope.img = "http://image.flaticon.com/icons/png/512/190/190539.png";
    }]);

    app.controller('AboutController', [
    '$scope',
    function($scope) {
    
    }]);


})();
