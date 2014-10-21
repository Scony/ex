ex.factory('examplesFactory', function ($resource) {
    return $resource('/examples/:id');
});