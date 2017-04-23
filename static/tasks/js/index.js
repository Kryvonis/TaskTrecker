/**
 * Created by Kryvonis on 3/23/17.
 */
angular.module('app', ['ngRoute', 'ngMaterial', 'ngMessages', 'ngCookies'])

    .config(
        function ($interpolateProvider, $httpProvider, $mdThemingProvider) {
            $mdThemingProvider.theme('docs-dark', 'default')
                .primaryPalette('yellow')
                .dark();

            $interpolateProvider.startSymbol('[[');
            $interpolateProvider.endSymbol(']]');
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        }
    )
    .controller('loginController',
        function ($scope, $http, $window) {
            $scope.isAuthenticated = sessionStorage.isAuthenticated;
            $scope.login = function (credentials) {
                $http
                    .post('api/v1/auth/login/', credentials)
                    .then(function (res) {
                        sessionStorage.userId = res.data.user.id;
                        sessionStorage.sessionId = res.data.id;
                        sessionStorage.isAuthenticated = true;
                        $window.location = '/tasks';

                    }).catch(function (res) {
                    $scope.result = 'email or password are not corrects';
                });

            };

        });




