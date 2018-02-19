$(document).ready(function(){


$('#travelForm').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_register_post();
});

function create_register_post() {
    console.log("create post is working!")
    var csrftoken = getCookieRegister('csrftoken'); 
    var arrival_mode=$("#arrival_mode").val();
    var arrival_number=$("#arrival_number").val();
    var arrival_time=$("#arrival_time").val();
    var arrival_date=$("#arrival_datepicker").val();
    var pickup=$("#pickup").val();
    var drop=$("#drop").val();
    var departure_mode=$("#departure_mode").val();
    var departure_time=$("#departure_time").val();
    var departure_date=$("#departure_datepicker").val();
    //console.log(email);// sanity check
    if(arrival_mode.trim()!="" && arrival_time.trim()!="" && arrival_date.trim()!=""){
            $("#errorTravelForm").text("");
        if(confirm("This will update the data. Do you really want to proceed.")){
    $.ajax({

        url : "/portal/travel/", // the endpoint
        type : "POST", // http method
        data : { arrival_mode:arrival_mode,arrival_number:arrival_number,arrival_time:arrival_time,arrival_date:arrival_date,pickup:pickup,drop:drop,departure_mode:departure_mode,departure_time:departure_time,departure_date:departure_date}, // data sent with the post request
 	 beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        		}
    		},
        // handle a successful response
        success : function(data) {
           
        	if(data.match("success")){
        		$("#success-alert").fadeTo(2000, 500).slideUp(500, function(){
                    $("#success-alert").slideUp(500);
                });
        	}
        	else{
            alert(data);// remove the value from the input
          

            }
            //console.log(json); // log the returned json to the console
          //  console.log(email); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }


    });
}


}
else{

alert("Mandatory fields can not be empty");

}

};

function getCookieRegister(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
 


});
