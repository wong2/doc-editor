var EditorView = Backbone.View.extend({
	el: $("#editor"),
	events: {
		"click .submit-button": "save"
	},
	render: function(model) {
		this.$("#titleInput").val(model.get("title"));
		this.$("#contentInput").val(model.get("content"));
		this.model = model;
	},
	save: function() {
        var me = this;
		var title = this.$("#titleInput").val(),
            content = this.$("#contentInput").val();
		var isNew = this.model.isNew();
		this.model.save({title: title, content: content}, {
            success: function(){
                me.showResult("success");
                if (isNew) {
                    documents.add(me.model);
                    app_router.navigate("#/edit/" + me.model.get("id"));
                }
            },
            error: function(){
                me.showResult("error");
            }
        });
	},
    showResult: function(result){
        // result could be "success" or "error"
        var className = {success:"success", error:"danger"}[result],
            tip = {success:"Saved!", error:"Error!"}[result];
        var btn = this.$(".submit-button");
        btn.removeClass("primary").addClass(className);
        btn.val(tip);
        setTimeout(function() {
            btn.val("Save")
            btn.removeClass(className).addClass("primary");
        }, 2000);
    }
});
var editor = new EditorView();

var DocTitleRow = Backbone.View.extend({
	tagName: "li",
	className: "doc-titles",
	template: _.template($("#doc-title-templ").html()),
    events: {
        "click .delete-button": "deleteDocument"
    },
	initialize: function() {
		$("#doc-list").append(this.el);
		this.model.bind('change', this.render, this);
	},
	render: function() {
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
	},
    deleteDocument: function(){
        var me = this;
        this.model.destroy({
            success: function(){
                $(me.el).remove();
                if(location.hash.split("/")[2] == me.model.get("id")){
                    app_router.navigate("#/add", true);
                }
            }
        });
    }
});

