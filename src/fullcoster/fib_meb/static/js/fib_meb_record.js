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
        var tfrom = $(".tfrom").val();
        var tto = $(".tto").val();

        var exp = $("select.experiment").children("option:selected").text();
        var user = $("select.user").children("option:selected").text();
        var group = $("select.group").children("option:selected").text();
        var project = $("select.project").children("option:selected").text();
        var Nunits=$(".wu").val();
        var confirm_text = "You will submit this:"+user+" from "+group+" did "+String(Nunits).bold()+" sessions of "+exp+" the "+dfrom.toDateString().bold()+". The project to use is: "+project+".";
        confirmation(confirm_text,event)
        //var retVal = confirm(confirm_text);
        //if( retVal != true ){
        //    return false;}
        });



    function calculatewu(){

        try {
            var dfrom = $(".dfrom").val();

            var tfrom = $(".tfrom").val(); //values are 0,  1...  has defined in the model field sessions
            var tto = $(".tto").val();

            var Nunits = new Number(tto - tfrom + 1);

            return Nunits;
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