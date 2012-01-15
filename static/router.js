var AppRouter = Backbone.Router.extend({
	routes: {
		"/edit/:id": "edit",
		"/add": "add"
	},
	edit: function(id) {
		documents.get(id).fetch({
			success: function(model) {
				editor.render(model);
			}
		});
	},
	add: function() {
		editor.render(new Document);
	}
});

