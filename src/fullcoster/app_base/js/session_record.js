$(document).ready(function() {

    $(".uo").prop("readonly",true);
    $(".uo").css("background-color","LightGray");
    $(".dto").css("display","none");

    var Nunits = calculateUO();
    $(".uo").val(Nunits);

    $(".fibclass").change(function () {
      var fibId = $(this).val();  // get the selected country ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: "load-experiments/",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'fib': fibId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $(".experiment").html(data);  // replace the contents of the city input with the data that came from the server
        }
      });

      $.ajax({                       // initialize an AJAX request
        url: "load-sessions/",                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'fib': fibId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $(".time").html(data);
        }
      });
    });


    $( ".okclass" ).click(function(event) {
        event.preventDefault();
        var dfrom = new Date($(".dfrom").val());
        var dto = new Date($(".dto").val());
        var tfrom = $(".tfrom").val(); //values are 'AM' or 'PM' has defined in the model field
        var tto = $(".tto").val();

        if (dto.getTime() < dfrom.getTime())
            {alert("Days are not in the right order!");
            return false;}

        else if (dto.getTime() == dfrom.getTime() && tto =='AM' && tfrom == 'PM')
            {alert("Sessions are not in the right order!");
            return false;}

        var exp = $("select.experiment").children("option:selected").text();
        var user = $("select.user").children("option:selected").text();
        var group = $("select.group").children("option:selected").text();
        var project = $("select.project").children("option:selected").text();
        var Nunits=$(".uo").val();
        var confirm_text = "You will submit this:"+user+" from "+group+" used "+String(Nunits).bold()+
        " WU of "+exp+" from "+dfrom.toDateString().bold()+"/"+$(".tfrom").children("option:selected").text().bold()+
        " to "+dfrom.toDateString().bold()+"/"+$(".tto").children("option:selected").text().bold()+
        ". The project to use is: "+project+".";
        confirmation(confirm_text,event)
        //var retVal = confirm(confirm_text);
        //if( retVal != true ){
        //    return false;}
        });



    function calculateUO(){

        try {
            var tfrom = new Number($(".tfrom").val()); //values are '0' or '1' or '2" has defined in the model field
            console.log(tfrom)
            var tto = new Number($(".tto").val());
            console.log(tfrom)
            var Nunits = tto-tfrom+1;
            console.log(Nunits)

            return Nunits;
           }
        catch (error) {alert("catch triggered"+error);return 0}
    }

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