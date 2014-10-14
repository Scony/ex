ex.factory('commandFactory', function ($resource) {
    return $resource('/commands/:name');
});