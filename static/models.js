var Document = Backbone.Model.extend({
	urlRoot: "/documents"
});
var Documents = Backbone.Collection.extend({
	model: Document,
	url: "/documents"
});
var documents = new Documents;
documents.bind("add", function(doc) {
	(new DocTitleRow({
		model: doc
	})).render();
});

