// Code goes here

var demo = angular.module('demo', ['ngRoute']);
demo.config(function($routeProvider){
  $routeProvider.when('/', {
    controller: 'testController',
    templateUrl: 'test.html'
  })
})

var controllers = {};
controllers.testController = function($scope){
   $scope.first = "Info";
    $scope.customers=[
        {name:'jerry',city:'chicago'},
        {name:'tom',city:'houston'},
        {name:'enslo',city:'taipei'}
    ];
}

demo.controller(controllers)