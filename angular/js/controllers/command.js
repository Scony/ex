ex.controller('commandController', function ($scope, $routeParams, commandsFactory, commandExamplesFactory) {
    $scope.name = $routeParams.name;
    commandsFactory.get({ name:$routeParams.name }, function (data) { // todo: if 404 then redirect to 404 page
	$scope.description = data['description'];
    });
    commandExamplesFactory.query({ name:$routeParams.name }, function(data) {
    	$scope.examples = data;
    });

    $scope.upVote = function(id) {
	// todo: upvote
    };

    $scope.downVote = function(id) {
	// todo: downvote
    };
});