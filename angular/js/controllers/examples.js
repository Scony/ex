ex.controller('examplesController', function ($scope, examplesFactory) {
    examplesFactory.query(function (data) {
    	$scope.examples = data;
    });

    // $scope.add = function() {
    // 	commandsFactory.save({name: $scope.name, description:$scope.description});
    // 	commandsFactory.query(function (data) {
    // 	    $scope.commands = data;
    // 	});
    // };
});
