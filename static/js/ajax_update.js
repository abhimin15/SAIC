$(document).ready(function(){


$('#updateForm').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_update_post();
});

function create_update_post() {
    console.log("create post is working!")
    var csrftoken = getCookieRegister('csrftoken'); 
    var firstName=$("#firstName").val();
    var lastName=$("#lastName").val();
    var gender=$("#gender").val();
    var course=$("#course").val();
    var dob=$("#dob").val();
    var address_permanent=$("#address").val();
    var city_permanent=$("#city").val();
    var zip_permanent=$("#zipCode").val();
    var address_present=$("#presentaddress").val();
     var branch=$("#branch").val();
    var city_present=$("#presentcity").val();
    var organisation=$("#organisation").val();    

    var zip_present=$("#presentzipCode").val();
    var designation=$("#designation").val();
    var mobile=$("#mobile").val();
    var year=$("#year").val();
    //console.log(email);// sanity check
   
   

    $.ajax({

        url : "/portal/update/", //the endpoint
        type : "POST", // http method
        data : { firstName:firstName,lastName:lastName,gender:gender, course:course,address_permanent:address_permanent,city_permanent:city_permanent,
        zip_permanent:zip_permanent,address_present:address_present,city_present:city_present,zip_present:zip_present,designation:designation,
        mobile:mobile,year:year,organisation:organisation,branch:branch,dob:dob}, // data sent with the post request
 	 beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        		}
    		},
        // handle a successful response
        success : function(data) {
            
        	if(data.match("success")){
        		alert("Succesfully Updated");
                window.location="http://"+window.location.host+"/portal";
        	}
        	else{
            $('#errorUpdate').html(data); // remove the value from the input
            

            }
            //console.log(json); // log the returned json to the console
          //  console.log(email); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $("#progressRegister").hide();
            $('#errorRegister').html("Error in Connection"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }


    });
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
