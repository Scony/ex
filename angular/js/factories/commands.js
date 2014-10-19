ex.factory('commandsFactory', function ($resource) {
    return $resource('/commands/:name');
});