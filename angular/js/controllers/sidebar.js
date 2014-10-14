ex.controller('sidebarController', function ($scope, popularService) {
    popularService.getPopularCommands().query(function (data) {
	$scope.popularCommands = data;
    });

    popularService.getPopularExamples().query(function (data) {
	$scope.popularExamples = data;
    });

    $scope.search = function () {
	alert($scope.phrase);
    };
});