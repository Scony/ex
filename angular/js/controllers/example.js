ex.controller('exampleController', function ($scope, $routeParams, examplesFactory, exampleCommandsFactory) {
    examplesFactory.get({ id:$routeParams.id }, function (data) { // todo: if 404 then redirect to 404 page
	$scope.example = data['example'];
    	$scope.description = data['description'];
    });
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