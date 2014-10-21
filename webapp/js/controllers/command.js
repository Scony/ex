ex.controller('commandController', function ($scope, $routeParams, $location, commandsFactory, commandExamplesFactory, votesService) {
    $scope.name = $routeParams.name;
    commandsFactory.get({ name:$routeParams.name }).$promise.then(
	function (data) {
	    $scope.description = data['description'];
	},
	function () {
	    $location.path('/404');
	    $scope.$apply();
	}
    );
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