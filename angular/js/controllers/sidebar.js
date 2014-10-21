ex.controller('sidebarController', function ($scope, $location, commandsFactory, popularService) {
    popularService.getPopularCommands().query(function (data) {
	$scope.popularCommands = data;
    });

    popularService.getPopularExamples().query(function (data) {
	$scope.popularExamples = data;
    });

    $scope.search = function () {
	$location.path('/commands/'+$scope.phrase);
	$scope.$apply();
    };
});