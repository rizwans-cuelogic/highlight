/* Javascript for HighXBlock. */
function HighXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var handlerUrl1 = runtime.handlerUrl(element, 'save_paragraph');
    var handlerUrl2 = runtime.handlerUrl(element, 'get_keyword');
    var handlerUrl3 = runtime.handlerUrl(element, 'save_keyword');
    var handleUrl4 = runtime.handlerUrl(element, 'get_initial_keyword');

    $( "#submit" ).click(function() {
    
        lesson_id=$('#submit').val();
        paragraph = $('#para').val();
        paragraph = paragraph.trim()
        data = {}
        data.lesson_id = lesson_id;
        data.paragraph = paragraph
        if ( paragraph.length != 0){
            $.ajax({
                type: "POST",
                url: handlerUrl1,
                data: JSON.stringify(data),
                success: function(result){
                if(result['status']=='success'){
                    alert("paragraph updated successfully");
                    $('.par p').text(result['paragraph'])
                    window.location.reload(false);
                    }
                }
            });
        }
        else{
            alert("please add something ");
        }
    });

    var p= $('p#par');
    p.html(function(index, oldHtml) {
        return oldHtml.replace(/\b(\w+?)\b/g, '<span class="word">$1</span>')
    });

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
            
            $("#pop").css("display", "block");
            $("#keyword").val(event.target.innerHTML);
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
                        $('#defination').val(result['defination']);
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

    $('#save').click(function() {
        var lesson_id = $('#hd-field').val()
        var key = $('#keyword').val()
        var def = $('#defination').val()
        if (def != ''){
            data={}
            data.key = key
            data.lesson_id = lesson_id
            data.def =def
            $.ajax({
                type: "POST",
                url: handlerUrl3,
                data: JSON.stringify(data),
                success: function(result){
                    $('#defination').val("");
                    $("." + result['keyword'].toLowerCase()).css("color", "blue");
                    $('[data-popup=popup-1]').fadeOut(350);
                    $('input#defination').val("");
                }
            });
        }
        else{
            alert("defination is required");
        }
    });


}
