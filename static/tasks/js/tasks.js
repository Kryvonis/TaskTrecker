/**
 * Created by Kryvonis on 4/21/17.
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
    .controller('tasksController',
        function ($scope, $http, $window, $mdDialog, $mdToast) {

            // *******************
            // ** Toas settings **
            // *******************
            var last = {
                bottom: false,
                top: true,
                left: false,
                right: true
            };
            $scope.toastPosition = angular.extend({}, last);

            $scope.getToastPosition = function () {
                sanitizePosition();

                return Object.keys($scope.toastPosition)
                    .filter(function (pos) {
                        return $scope.toastPosition[pos];
                    })
                    .join(' ');
            };

            function sanitizePosition() {
                var current = $scope.toastPosition;

                if (current.bottom && last.top) current.top = false;
                if (current.top && last.bottom) current.bottom = false;
                if (current.right && last.left) current.left = false;
                if (current.left && last.right) current.right = false;

                last = angular.extend({}, current);
            }

            $scope.showSimpleToast = function (text) {
                var pinTo = $scope.getToastPosition();

                $mdToast.show(
                    $mdToast.simple()
                        .textContent(text)
                        .position(pinTo)
                        .hideDelay(3000)
                );
            };

            // *********************
            // ** Dialog settings **
            // *********************
            $scope.status = '';
            $scope.operationTitle = 'Add';

            $scope.task = {
                name: '',
                description: ''
            };

            $scope.showEditTask = function (ev, task) {
                if (task) {
                    $scope.operationTitle = 'Edit';
                    $scope.task.name = task.name;
                    $scope.task.id = task.id;
                    $scope.task.description = task.description;
                    if (task.author) {
                        $scope.task.author = task.author.id;
                    }
                }
                else {
                    $scope.operationTitle = 'Add';
                }

                $mdDialog.show({
                    controller: DialogController,
                    templateUrl: 'task.tmpl.html',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    scope: $scope,
                    preserveScope: true,
                    clickOutsideToClose: true
                })
                    .then(function (answer) {
                        $scope.showSimpleToast($scope.operationTitle + 'ed');
                        $scope.getTasks();
                    }, function () {
                    });
            };

            function DialogController($scope, $mdDialog) {
                $scope.hide = function () {
                    $mdDialog.hide();
                };

                $scope.cancel = function () {
                    $mdDialog.cancel();
                };

                $scope.answer = function (answer) {
                    $mdDialog.hide(answer);
                };
            }

            // **********************
            // ** Main controllers **
            // **********************
            $scope.showTitle = 'Done';
            $scope.showAllFlag = true;

            $scope.switchShowAll = function () {

                $scope.showAllFlag = !$scope.showAllFlag;
                if ($scope.showAllFlag) {
                    $scope.showTitle = 'Done';

                } else {
                    $scope.showTitle = 'All';
                }
                $scope.getTasks();

            };

            $scope.parseTasks = function (tasks) {
                tasks.forEach(function (task, i, arr) {
                    if (task.author) {
                        $http.get('api/v1/users/' + task.author + '/')
                            .then(function (res) {
                                task.author = res.data
                            });
                    }
                });
                $scope.tasks = tasks;
            };

            $scope.getTasks = function () {
                if ($scope.showAllFlag) {
                    $http.get('api/v1/tasks/')
                        .then(function (res) {
                            $scope.parseTasks(res.data);
                        })
                        .catch(function (res) {

                        });


                } else {
                    $http
                        .get('api/v1/tasks?status=1')
                        .then(function (res) {
                            $scope.parseTasks(res.data);


                        }).catch(function (res) {
                    });
                }
            };

            $scope.addOrEditTask = function (task, isAdd) {
                if (isAdd === 'Add') {
                    $http.post('api/v1/tasks/', task)
                        .then(function (res) {
                            $scope.showSimpleToast('Added');
                        })
                        .catch(function (res) {
                            $scope.showSimpleToast("Can't add");
                        });

                }
                else {
                    $http.put('api/v1/tasks/' + task.id + '/', task)
                        .then(function (res) {
                            $scope.showSimpleToast('Edited');
                        })
                        .catch(function (res) {
                            $scope.showSimpleToast("Can't edit");
                        });

                }
                $scope.getTasks();
                $window.location.reload();
            };

            $scope.logout = function () {
                $http
                    .post('api/v1/auth/logout/')
                    .then(function (res) {
                        delete sessionStorage.userId;
                        delete sessionStorage.sessionId;
                        sessionStorage.isAuthenticated = false

                    }).catch(function (res) {
                    delete sessionStorage.userId;
                    delete sessionStorage.sessionId;
                    sessionStorage.isAuthenticated = false

                });
                $window.location = '/';

            };
            $scope.getVariables = function () {
                $scope.getTasks();
                $http
                    .get('api/v1/users')
                    .then(function (res) {
                        $scope.users = res.data

                    }).catch(function (res) {

                });

            };

            $scope.deleteTask = function (task) {

                $http.delete('api/v1/tasks/' + task.id)
                    .then(function (res) {
                        $scope.showSimpleToast('Deleted');
                    }).catch(function (res) {
                    $scope.showSimpleToast("Can't delete");
                });

                $scope.getTasks();
                $window.location.reload();

            };

            $scope.doneTask = function (task) {

                var text;

                if (task.status == 0) {
                    task.status = 1;
                    text = 'Marked Done!'
                }
                else {
                    task.status = 0;
                    text = 'Marked Undone!'
                }
                var sendTask = {
                    name: task.name,
                    description: task.description,
                    author: task.author ? task.author.id : null,
                    status: task.status
                };
                $http.put('api/v1/tasks/' + task.id + '/', sendTask)
                    .then(function (res) {
                        $scope.showSimpleToast(text);
                    })
                    .catch(function (res) {
                        $scope.showSimpleToast("Can't mark done ");
                    });


            };

            $scope.getVariables();

        });
