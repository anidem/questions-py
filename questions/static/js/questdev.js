// questdev.js
jQuery(function($) {
    // Using validation to check for the presence of an input
    $( "#noteform" ).submit(function( event ) {
        event.preventDefault();
        $.ajax({
            url : "/note/add/",
            type : "POST",
            data : $( "#noteform" ).serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
                $('#notes').append('<div class="message"><span class="ts">' + json.modified + '</span> ' + json.subject + ': ' + json.text + '</div>');
                $('#noteform').trigger("reset");
            },

            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + errmsg ); // provide a bit more info about the error to the console
            }
        });        
    });

    $(document).ready(function() {

    });
})