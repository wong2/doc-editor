documents.fetch({
    add: true,
	success: function() {
		window.app_router = new AppRouter;
		if (location.hash.indexOf("edit") < 0) {
			app_router.navigate("#/add");
		}
		Backbone.history.start();
	}
});
