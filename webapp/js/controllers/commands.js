ex.controller('commandsController', function ($scope, commandsFactory) {
    commandsFactory.query(function (data) {
	$scope.commands = data;
    });

    $scope.add = function() {
	commandsFactory.save({name: $scope.name, description:$scope.description});
	commandsFactory.query(function (data) {
	    $scope.commands = data;
	});
    };
});