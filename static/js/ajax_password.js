$(document).ready(function(){

 $('#recover').click(function(){
    var roll_no;
    email=$("#emailId_pass").val();
	
     $.post('/pass_recovery/', {emailId:email}, function(data){
               $('#message').html(data);
		
           });
});



});
