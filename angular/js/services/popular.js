ex.service('popularService', function ($resource) {
    this.getPopularCommands = function() {
	return $resource('/popular/commands');
    }
    this.getPopularExamples = function() {
	return $resource('/popular/examples');
    }
});