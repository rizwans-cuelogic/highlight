function StPara(runtime, element) {

	var p= $('p#par');
    p.html(function(index, oldHtml) {
        return oldHtml.replace(/\b(\w+?)\b/g, '<span class="word">$1</span>')
    });

    var handleUrl4 = runtime.handlerUrl(element, 'get_initial_keyword');
    var handlerUrl2 = runtime.handlerUrl(element, 'get_keyword');

    $(".word").each(function(index) {
        $(this).addClass(this.innerHTML.toLowerCase());
        var lesson_id = $('#hd-field').val()
        data = {}
        data.lesson_id = lesson_id
        $.ajax({
                type: "POST",
                url: handleUrl4,
                data: JSON.stringify(data),
                success: function(result){
                    if (result['status']=='success'){
                    	
                        word_list=result['list']
                       
                        for (var key in word_list) {
    						$("." + key.toLowerCase()).css("color", "blue");
    						$("." + key.toLowerCase()).attr("title",word_list[key]);
    						$("." + key.toLowerCase()).tooltipster({
    							
    						});
    						$("." + key.toLowerCase()).removeAttr('title');
   						}
                    }
                }                  
            });
	});
	
}