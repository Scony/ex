ex.controller('examplesController', function ($scope, examplesFactory) {
    examplesFactory.query(function (data) {
    	$scope.examples = data;
    });

    $scope.add = function() {
    	examplesFactory.save({example: $scope.example, description:$scope.description});
	examplesFactory.query(function (data) {
    	    $scope.examples = data;
	});
    };
});
