ex.factory('exampleCommandsFactory', function ($resource) {
    return $resource('/examples/:id/commands',{id:'@id'},{});
});