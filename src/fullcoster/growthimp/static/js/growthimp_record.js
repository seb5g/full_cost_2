/*

The template tag {{'activity'}} will be replaced by the Activity object type specifying the Activity

*/

$(document).ready(function() {

    $(".wu").prop("readonly",true);
    $(".wu").css("background-color","LightGray");
    var Nunits = calculatewu();
    $(".wu").val(Nunits);

    $( ".okclass" ).click(function(event) {
        event.preventDefault();
        var dfrom = new Date($(".dfrom").val());
        var tfrom = $(".tfrom").val(); //values are 0 or 1 has defined in the model field
        var tto = $(".tto").val();

        var exp = $("select.experiment").children("option:selected").text();
        var user = $("select.user").children("option:selected").text();
        var group = $("select.group").children("option:selected").text();
        var project = $("select.project").children("option:selected").text();
        var Nunits=$(".wu").val();
        var confirm_text = "You will submit this:"+user+" from "+group+" used "+String(Nunits).bold()+" WU of "+exp+" the "+dfrom.toDateString().bold()+" from "+$(".tfrom").val().bold()+" to "+ $(".tto").val().bold() + ". The project to use is: "+project+".";
        confirmation(confirm_text,event)
        //var retVal = confirm(confirm_text);
        //if( retVal != true ){
        //    return false;}
        });

    function calculatewu(){

        try {
            var dfrom = $(".dfrom").val();
            var tfrom = $(".tfrom").val();
            var tto = $(".tto").val();
            now = new Date();
            now_date_string = now.toISOString().split('T')[0]
            date_from = new Date(now_date_string + " " + tfrom);
            date_to = new Date(now_date_string + " " + tto);

            var wu_quantity = 0.0002777778;
            Nseconds = (date_to.getTime() - date_from.getTime()) / 1000;
            var Nunits = new Number(Nseconds * wu_quantity);
            if (Nunits < 0)
                {alert("Set Times are not in the right order!");
                return 0;}
            return Math.round(Nunits*10)/10;
           }
        catch (error) {alert("catch triggered"+error);return 0}
    }

    Date.prototype.yyyymmdd = function() {
      var mm = (this.getMonth() + 1).toString(); // getMonth() is zero-based
      var dd = this.getDate().toString();
      var month = [mm.length===2 ? '' : '0', mm].join('')
      var year = this.getFullYear()
      var day = [dd.length===2 ? '' : '0', dd].join('')
      return year+'-'+month+'-'+day
    };

    $(".time").change(function() {
        var Nunits = calculatewu();
        $(".wu").val(Nunits);
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