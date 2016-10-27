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
                $scope.loading = true;

                var canvas = document.getElementById('canvas');
                var context = canvas.getContext('2d');
                var video = document.getElementById('video');
            
                // take a snapshot of the video
                context.drawImage(video, 0, 0, 640, 480);
            
                // convert image to a b64 string
                var img = canvas.toDataURL();
                var b64 = img.split(",")[1];

                // save the image
                var i = new Image();
                i.src = img;
                parseService.setImage(i);

                fetchImageResponse(b64, function(imageResponse) {
                    parseService.setImageResponse(imageResponse);
                    fetchBeverage(function(beverage) {
                        parseService.setBeverage(beverage);
                        $location.path("/result");
                    });
                });
            
            }

        };

        var fetchImageResponse = function(b64, callback) {
                var url = 'http://localhost:5000/api/picture';
                $http.post(url, {"image": b64}).then(function(res) {
                    callback(res);
                }, function(err) {
                    if (err.status == 422) {
                        var msg = "We couldn't identify any face in your " + 
                                  "picture, please try again."
                        $scope.errorMessage = msg; 
                    }
                });
        }

        var fetchBeverage = function(callback) {
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

            $http.get(url, {'params': params}).then(function(res) {
                callback(res.data[0]);
            });

        }

    }]);

    app.controller('ResultController', [
    '$scope',
    '$http',
    'parseService',
    function($scope, $http, parseService) {

        $scope.beverage = parseService.getBeverage();
        
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
