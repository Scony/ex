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
	.otherwise({ redirectTo: '/' });
});
