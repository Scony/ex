ex.controller('exampleController', function ($scope, $routeParams, $location, examplesFactory, exampleCommandsFactory) {
    examplesFactory.get({ id:$routeParams.id }).$promise.then(
	function (data) {
	    $scope.example = data['example'];
    	    $scope.description = data['description'];
	},
	function () {
	    $location.path('/404');
	    $scope.$apply();
	}
    );
    exampleCommandsFactory.query({ id:$routeParams.id }, function(data) {
    	$scope.commands = data;
    });

    $scope.add = function() {
    	exampleCommandsFactory.save({ id:$routeParams.id, command:$scope.name }); // handle add error
	exampleCommandsFactory.query({ id:$routeParams.id }, function(data) {
    	    $scope.commands = data;
	});
    };
});