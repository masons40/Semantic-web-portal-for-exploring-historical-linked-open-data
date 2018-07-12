$( document ).ready(function() {
	
	$('#menuBtn').click(function(){
		$('#menuToShow').toggle("slow");
		
	});
	
	$('.saveIcons').click(function(){
		var attr = $(this).attr('data-id');
		$('#' + attr).toggle("show")
	});

	$('.imageToShow').click(function(){
		var attr = $(this).attr('data-id');
		$('#' + attr).toggle("show")
	});
	
});