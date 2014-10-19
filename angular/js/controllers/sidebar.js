ex.controller('sidebarController', function ($scope, $location, commandsFactory, popularService) {
    popularService.getPopularCommands().query(function (data) {
	$scope.popularCommands = data;
    });

    popularService.getPopularExamples().query(function (data) {
	$scope.popularExamples = data;
    });

    $scope.search = function () {
	// todo: some loading bar
	commandsFactory.get({ name:$scope.phrase }).$promise.then(
	    function () {
		$location.path('/commands/'+$scope.phrase);
		$scope.$apply();
	    },
	    function () {
		alert('no command found');
	    }
	);
    };
});