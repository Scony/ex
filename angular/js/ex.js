var ex = angular.module('ex', ['ngRoute', 'ngResource']);

ex.config(function ($routeProvider) {
    $routeProvider
	.when('/', {
	    templateUrl: 'root.html'
	})
	.when('/commands', {
	    controller: 'commandsController',
	    templateUrl: 'commands.html'
	})
	.when('/commands/:name', {
	    controller: 'commandController',
	    templateUrl: 'command.html'
	})
	.when('/examples', {
	    controller: 'examplesController',
	    templateUrl: 'examples.html'
	})
	.when('/examples/:id', {
	    controller: 'exampleController',
	    templateUrl: 'example.html'
	})
	.otherwise({ redirectTo: '/' });
});
