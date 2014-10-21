ex.service('votesService', function ($resource) {
    this.getUpVoteResource = function() {
	return $resource('/examples/:id/upvotes',{id:'@id'},{});
    }
    this.getDownVoteResource = function() {
	return $resource('/examples/:id/downvotes',{id:'@id'},{});
    }
});