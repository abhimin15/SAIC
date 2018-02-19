$(document).ready(function(){

 $('#upload').click(function(){
    var file;
    photoUpload=$("#uploadPhoto").val();
	
     $.get('/portal/photo/', {photo:photoUpload}, function(data){
               $('#message').html(data);
		
       });

});

});
