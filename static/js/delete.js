$(document).ready(function(){

 $('#delete').click(function(){
    
      $.get('/portal/deletePhoto/', {}, function(data){
              if(data.match("success"))
              {

              	window.location = "http://127.0.0.1:8000/portal";
              }
              else{

              	$("#message").html(data);
              }	

           });
});
});
