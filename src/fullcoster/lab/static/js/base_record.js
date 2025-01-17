$(document).ready(function() {

    if ($(".activity").children('option').length == 1)
        {$(".activity_div").css("display","none");}

    $('.has-popover').popover({'trigger':'hover'});

    $(".usercol").css("display","none");


    $(".user").change(function() {
        var user = $(this).children("option:selected").text();
        if (user == "OTHER Name")
            {$(".user_other").val("");
            $(".usercol").css("display","block");}
        else {$(".user_other").val("XXX");
                $(".usercol").css("display","none");}
    })


    $(".asteriskField").css("display","none");
    //$(".uo").val(0);

    $('form').on('keydown', 'input[type=number]', function(e) {
        if ( e.which == 38 || e.which == 40 )
            e.preventDefault();
        });


    $(".btn-danger").click(function(event){
        var r = confirm("Are you sure you want to delete this extraction?");
        return r
    });


});