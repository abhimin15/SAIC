$(function(){
	$("#searchinput").keyup(function(){
		$.ajax({
			type:  "POST" ,
			url:  "/portal/search/" ,
			data: {
				'search_byName': $(".searchname").val() ,
				'search_byYear': $(".searchyear").val() ,
				'search_byDepartment': $("searchdept").val() ,
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
			} ,
			success: searchSuccess ,
			dataType: 'html'
		});
	});
});
function searchSuccess(data, textStatus, jqXHR){
	console.log("post is working");
	$('.results').html(data);
}