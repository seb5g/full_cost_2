$(document).ready(function() {
    $(".uo").prop("readonly",true);
    $(".uo").css("background-color","LightGray");
    $(".durationcol").css("display","block");
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

    function elapsed_days(d1,d2){
        var flag = true;
        var dtmp = new Date(d1.getTime());
        var ndays = 0;
        var ndays_tot = 0;

        if (d1.getTime() != d2.getTime())
            {while (flag){
                dtmp.setDate(dtmp.getDate()+1);
                if (!(dtmp.getDay() == 0 || dtmp.getDay() == 6)) //remove weekend days
                    {ndays += 1;};
                ndays_tot += 1;
                if (dtmp.getTime() >= d2.getTime() || ndays_tot>=365){break;};
                }

            return ndays+1;}
        else {return 1};
        }

    function calculateUO(){

        try {
            var exp = $("select.experiment").children("option:selected").text();
            if (exp.includes("Four"))
                {Nunits=Math.ceil($(".seconds").val()/(3600*24));}
            else {Nunits=Math.round($(".seconds").val()/360)/10;}
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

    $(".seconds").change(function() {
        var Nunits = calculateUO();
        $(".uo").val(Nunits);
    })

    $(".dto").change(function() {
        var Nunits = calculateUO();
        $(".uo").val(Nunits);
    })

    $(".dfrom").change(function() {
        var Nunits = calculateUO();
        $(".uo").val(Nunits);
    })

    $("select.experiment").change(function() {
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