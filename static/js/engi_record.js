$(document).ready(function() {

    $(".uo").prop("readonly",true);
    $(".uo").css("background-color","LightGray");
    var Nunits = calculateUO();
    $(".uo").val(Nunits);

    $( ".okclass" ).click(function(event) {
        event.preventDefault();
        var dfrom = new Date($(".dfrom").val());

        var exp = $("select.experiment").children("option:selected").text();
        var user = $("select.user").children("option:selected").text();
        var group = $("select.group").children("option:selected").text();
        var project = $("select.project").children("option:selected").text();
        var Nunits=$(".uo").val();
        var confirm_text = "You will submit this:"+user+" from "+group+" used "+String(Nunits).bold()+" WU of "+exp+" the "+dfrom.toDateString().bold()+". The project to use is: "+project+".";
        confirmation(confirm_text,event)
        //var retVal = confirm(confirm_text);
        //if( retVal != true ){
        //    return false;}
        });

    function calculateUO(){

        try {
            var dfrom = $(".dfrom").val();
            var tfrom = $(".tfrom").val(); //values are 0 or 1 has defined in the model field
            var tto = $(".tto").val();
            var exp = $("select.experiment").children("option:selected").text();
            if (exp == "LASFAR Abdelouahed" | exp == "PERTEL Christian")
                {Nunits=(tto-tfrom+1)*0.25;}
            else {Nunits=(tto-tfrom+1)*0.5;}

            return Nunits;
           }
        catch (error) {alert("catch triggered"+error);return 0}
    }

    $("select.experiment").change(function() {
        var exp = $(this).children("option:selected").text();
        var Nunits = calculateUO();
        $(".uo").val(Nunits);
    });

    $("select.workon").change(function() {
        $.ajax({                       // initialize an AJAX request
            url: "workon/",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
            data: {
              'workon': $(this).children("option:selected").val()       // add the country id to the GET parameters
            },
            success: function (data) {   // `data` is the return of the `load_cities` view function
              $("body").html(data);
            }
        });
    });


    $("select.time").change(function() {
        if ($(".tto").prop('selectedIndex') < $(".tfrom").prop('selectedIndex')){
            $(".tto").prop('selectedIndex', $(".tfrom").prop('selectedIndex'));
            alertc("Your session cannot end before it started");
        }
        var Nunits = calculateUO();
        $(".uo").val(Nunits);
    })

    function alertc(confirm_text, event){
    $("<div></div>").appendTo("body")
    .html("<div><p>"+confirm_text+"</p></div>")
    .dialog({
        title: "Confirm Dialog" ,
        width:500, height:300,
        modal:true,
        resizable: false,
        show: { effect: "drop", direction: "left" },
        hide:{effect:"blind"},

        buttons: {
            Ok: function() {
                  $( this ).dialog( "close" );
            },

            }
        });
    }


    function confirmation(confirm_text, event){
    $("<div></div>").appendTo("body")
    .html("<div><p>"+confirm_text+"</p></div>")
    .dialog({
        title: "Confirm Dialog" ,
        width:500, height:300,
        modal:true,
        resizable: false,
        show: { effect: "drop", direction: "left" },
        hide:{effect:"blind"},

        buttons: {
            Yes: function() {
                $(".formclass").submit();
            },
            Cancel: function() {

                $( this ).dialog( "close" );
                }
            }
        });
    }

});