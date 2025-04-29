$(document).ready(function() {

    $(".uo").prop("readonly",true);
    $(".uo").css("background-color","LightGray");
    var Nunits = calculateUO();
    $(".uo").val(Nunits);

    $( ".okclass" ).click(function(event) {
        event.preventDefault();
        var dfrom = new Date($(".dfrom").val());
        var dto = new Date($(".dto").val());
        var tfrom = $(".tfrom").val(); //values are 0 or 1 has defined in the model field
        var tto = $(".tto").val();

        if (dto.getTime() < dfrom.getTime())
            {alert("Days are not in the right order!");
            return false;}

        else if (dto.getTime() == dfrom.getTime() && tto ==0 && tfrom == 1)
            {alert("Sessions are not in the right order!");
            return false;}

        var exp = $("select.experiment").children("option:selected").text();
        var user = $("select.user").children("option:selected").text();
        var group = $("select.group").children("option:selected").text();
        var project = $("select.project").children("option:selected").text();
        var Nunits=$(".uo").val();
        var confirm_text = "You will submit this:"+user+" from "+group+" used "+String(Nunits).bold()+" WU of "+exp+" from "+dfrom.toDateString().bold()+"/"+$(".tfrom").children("option:selected").text().bold()+" to "+dto.toDateString().bold()+"/"+$(".tto").children("option:selected").text().bold()+". The project to use is: "+project+".";
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
            var dfrom = $(".dfrom").val();
            var dto = $(".dto").val();

            var tfrom = $(".tfrom").val(); //values are 0 or 1 has defined in the model field
            var tto = $(".tto").val();
            var ndays = Number(elapsed_days(new Date(dfrom),new Date(dto)));
            var Nnights = Number($(".nights").val())
            if (Nnights > ndays){alert("You cannot do more nights than days"); return 0;}
            var Nunits = new Number(2*ndays + Nnights);
            if (tfrom != 0){Nunits-=1;}
            if (tto == 0){Nunits-=1;}
            var exp = $("select.experiment").children("option:selected").text();
            if (exp == 'UV (A125)' || exp == 'IR (A125)' || exp == 'Electrochimie (A125)')
                {Nunits=$(".uo").val();}

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

    $(".datepicker").change(function(){
        var dfrom = new Date($(".dfrom").val());
        var dto = new Date($(".dto").val());
        if (dto < dfrom)
            {alertc("Date to cannot be before Date from!");
            $(".dto").val(dfrom.yyyymmdd());}
    })

    $(".time").change(function() {
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

    $("select.experiment").change(function() {
        var exp = $(this).children("option:selected").text();
        var Nunits = calculateUO();
        $(".uo").val(Nunits);

        if (exp == 'UV (A125)' || exp == 'IR (A125)' || exp == 'Electrochimie (A125)')
            {$(".uo").prop("readonly",false);
            $(".uo").css("background-color","white");
            $(".nightcol").css("display","none");
            $(".to_col").css("display","none");}
        else {$(".uo").prop("readonly",true);
            $(".uo").css("background-color","LightGray");
            $(".nightcol").css("display","block");
            $(".to_col").css("display","block");}
        });

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