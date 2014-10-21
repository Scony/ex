ex.factory('commandExamplesFactory', function ($resource) {
    return $resource('/commands/:name/examples');
});