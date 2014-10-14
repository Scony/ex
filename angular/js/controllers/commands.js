ex.controller('commandsController', function ($scope, commandFactory) {
    commandFactory.query(function (data) {
	$scope.commands = data;
    });

    $scope.add = function() {
	commandFactory.save({name: $scope.name, description:$scope.description});
	alert($scope.name + '::' + $scope.description);
    };
});