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
                        for(i=0; i<word_list.length;i++){
                            word= word_list[i].toLowerCase()
                            $("." + word.toLowerCase()).css("color", "blue");
                        }
                    }
                }                  
            });
	});

	p.click(function(event) { 
        if(this.id != event.target.id) {
            
            $("#keyword").text(event.target.innerHTML);
            var key = event.target.innerHTML
            var lesson_id = $('#hd-field').val()
            data={}
            data.key = key
            data.lesson_id = lesson_id
            $.ajax({
                type: "POST",
                url: handlerUrl2,
                data: JSON.stringify(data),
                success: function(result){
                    
                    if( result['status'] == 'success'){
                    	$("#pop").css("display", "block");
                        $('#defination').text(result['defination']);
                    }    
                    else{
                        $('#defination').val("");
                    }
                }
            });
        }
    });

     $('[data-popup-close]').on('click', function(e)  {
        var targeted_popup_class = jQuery(this).attr('data-popup-close');
        $('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
        $('input#defination').val("");
        e.preventDefault();
    });	
}