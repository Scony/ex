ex.controller('commandController', function ($scope, $routeParams, commandsFactory, commandExamplesFactory, votesService) {
    $scope.name = $routeParams.name;
    commandsFactory.get({ name:$routeParams.name }, function (data) { // todo: if 404 then redirect to 404 page
	$scope.description = data['description'];
    });
    commandExamplesFactory.query({ name:$routeParams.name }, function(data) {
    	$scope.examples = data;
    });

    $scope.upVote = function(id) {
	votesService.getUpVoteResource().save({ id:id });
	commandExamplesFactory.query({ name:$routeParams.name }, function(data) {
    	    $scope.examples = data;
	});
    };

    $scope.downVote = function(id) {
	votesService.getDownVoteResource().save({ id:id });
	commandExamplesFactory.query({ name:$routeParams.name }, function(data) {
    	    $scope.examples = data;
	});
    };
});