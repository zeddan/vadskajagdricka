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
        
            // take a snapshot of the video
            context.drawImage(video, 0, 0, 640, 480);
        
            var img = canvas.toDataURL();
            var b64 = img.split(",")[1];

            var i = new Image();
            i.src = img;
            parseService.setImage(i);
        
            $http.post('http://localhost:5000/api/picture', {"image": b64})
            .then(function(res) {
                parseService.setImageResponse(res);
                $location.path("/picture");
            }, function(err) {
                if (err.status == 422) {
                    $scope.errorMessage = "We couldn't identify any face in " +
                                          "your picture, please try again."
                }

                console.log("error fetching imageResponse: ", err);
            });

        };
    }]);

    app.controller('PictureController', [
    '$scope',
    '$http',
    'parseService',
    function($scope, $http, parseService) {

        // convert image response to a b64 json string
        var jsonb64 = btoa(JSON.stringify(parseService.imageResponse));

        // fetch beverage
        $http.get('http://localhost:5000/api/beverages?' + jsonb64)
        .then(function(res) {
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

    app.controller('AboutController', [
    '$scope',
    function($scope) {
    
    }]);


})();
