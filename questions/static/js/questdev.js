// questdev.js
jQuery(function($) {
    // $("#selector").click(function () {
    // });

    $("#chk_response_btn").click(function(){
        $.post("/questions/worksheet/1",function(result){
            console.log(result)
            // $("span").html(result);
        });
    });

    $(document).ready(function() {

    });
})