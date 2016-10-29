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

            // we don't want users to hammer the snap button
            if ($scope.snapped) return;

            // the bar is closed between 09:00 and 12:00
            var hour = new Date().getHours();
            hour = 22;
            if (hour >= 9 && hour <= 12) {
                $location.path("/result/water");
            }

            // otherwise, proceed as usual
            else {
                $scope.snapped = true;

                var canvas = document.getElementById('canvas');
                var context = canvas.getContext('2d');
                var video = document.getElementById('video');

                // take a snapshot of the video
                context.drawImage(video, 0, 0, 500, 375);

                // convert image to a b64 string
                var img = canvas.toDataURL();
                var b64 = img.split(",")[1];

                // save the image
                var i = new Image();
                i.src = img;
                parseService.setImage(i);

                // replace streaming video with the image
                context.drawImage(i, 0, 0);

                setTimeout(function() {
                    $scope.loading = true;
                }, 500);

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
                var req = {
                    method: 'POST',
                    url: 'http://localhost:5000/api/picture',
                    headers: {'Content-Type': 'application/json'},
                    data: {'image': b64}
                }

                $http(req).then(function(res) {
                    console.log(res);
                    callback(res);
                }, function(err) {
                    if (err.status == 422) {
                        var msg = "We couldn't identify any face in your " +
                                  "picture, please try again."
                        $scope.errorMessage = msg;
                        $scope.snapped = false;
                        $scope.loading = false;
                    }
                });
        }

        var fetchBeverage = function(callback) {
            var date  = new Date();
            var hour  = date.getHours();
            var month = date.getMonth() + 1;

            var url = 'http://localhost:5000/api/beverages';
            var params = {
                'price_score': parseService.imageResponse.emotion_score,
                'alcohol_score': parseService.imageResponse.color_score,
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

        // no need to proceed without data
        if (!parseService.imageResponse) return;

        // get the labels and the beverage
        $scope.beverage = parseService.beverage;
        $scope.labels = parseService.imageResponse.labels;

        // render image
        var canvas = document.getElementById('result_canvas');
        var img = parseService.image;;
        var context = canvas.getContext("2d");
        context.scale(0.55, 0.55);
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
