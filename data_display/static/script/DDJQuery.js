$( document ).ready(function() {
    $(".imageContained").click(function() {
		$(".imageBox").toggle();
	});
	$(".icon").click(function () {
		$("div>form").toggleClass("menuItem");
	});
	$(".dropBtn").click(function () {
		$(".dropdown-content").toggle();
	});
	$(".saveIcons").click(function(){
		var att = $(this).attr("data-id");
		$("#" + att).toggle();
		
	});
	$('.testClass').click(function(){
		var attr = $(this).attr('data-id');
		$('#' + attr).toggle();
	});
	$('[data-toggle="tooltip"]').tooltip();  
	$("#select1").change(function() {
		if ($(this).data('options') === undefined) {
			
			$(this).data('options', $('#select2 option').clone());
		}
		var id = $(this).val();

		var choice = $(this).val();
		var options = $(this).data('options');
		
		var opt = []
		if(choice === "Questionnaire"){
			var attributeList = ['label','Note','Type','Title','hasAuthor','Publication Year','Has Multimedia'];
			var attributeListVals = ['rdfs:label','oldcan:note','rdf:type','oldcan:title','oldcan:hasAuthor','oldcan:publicationYear','oldcan:hasMultimedia'];
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeListVals[i]+">"+attributeList[i]+"</option>";
			}
		}else if(choice == "Question"){
			var attributeList = ['Combined Id','Number','Original Question','Short Question','Is Question Of'];
			var attributeListVals = ['oldcan:CombinedId','oldcan:number','oldcan:originalQuestion','oldcan:shortQuestion','oldcan:isQuestionOf'];
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeListVals[i]+">"+attributeList[i]+"</option>";
			}
		}else if(choice == "Source"){
			var attributeList = ['Title','Label','Has Subtitle','Volume Title','Volume','Series Title','Series Number','Edition','Place Of Publication',
			'Year Of Publication','Publisher','isbn','Page Range','Has URL','hyperl Link Creation Date','Creator','Editor','Has Short Title',
			'Long Title','Reference Quotation Page','Quotation Column','Original Data','Checked','Note','Has Multimedia'];
			var attributeListVals = ['dc:title','rdfs:label','fabio:hasSubtitle','oldcan:volumeTitle','prism:volume','oldcan:seriesTitle','oldcan:seriesNumber'
			,'oldcan:edition','oldcan:placeOfPublication','oldcan:yearOfPublication','dct:publisher','prism:isbn','prism:PageRange','fabio:hasURL'
			,'oldcan:hyperlLinkCreationDate','dct:creator','oldcan:editor','fabio:hasShortTitle','oldcan:longTitle','oldcan:referenceQuotationPage'
			,'oldcan:quotationColumn','oldcan:originalData','oldcan:checked','oldcan:note','oldcan:hasmultimedia'];
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeListVals[i]+">"+attributeList[i]+"</option>";
			}
		}else if(choice == "Multimedia"){
			var attributeList = ['File Name','Title','Label','Released','Checked','Note','Type'];
			var attributeListVals = ['oldcan:fileName','dc:title','rdfs:label','oldcan:released','oldcan:checked','oldcan:note','rdf:type'];
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeList[i]+">"+attributeList[i]+"</option>";
			}
		}else if(choice == "PaperSlip"){
			var attributeList = ['Label','Catalog','Drawer','Section','Virtual','Source','Source Paragraph','Source Number','Source Quoted'
			,'Source Quoted Page','Source Paragraph','Source Quoted Map','Source Quoted Number','Year Of Record','Location','Original Etymology'
			,'Revised Etymology','Facts','Comment','Original Reference','Revised Reference','Original Data','Released','Checked','Note','Has Source',
			'Has Multimedia'];
			
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeList[i]+">"+attributeList[i]+"</option>";
			}
		}else if(choice == "PaperSlipRecord"){
			var attributeList = ['Title','Label','Grammar','Paper Slip Record Classification','Contains Question','Has Lemma','Has Reference Lemma',
			'Has Paper Slip','Has Paper Slip Record Note','Has Multimedia','Definition','Note'];
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeList[i]+">"+attributeList[i]+"</option>";
			}
		}else if(choice == "Person"){
			var attributeList = ['First Name','Last Name','Label','Birthday','Birth Month','Birth Year','Birth Place','Death Place','Death Day',
			'Death Month','Death Year','Death Place','Gender','Address','Postcode','Place','Email','Telephone','Course Of Address','Contact Person',
			'Relations','Has Education'];
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeList[i]+">"+attributeList[i]+"</option>";
			}
		}else if(choice == "Lemma"){
			var attributeList = ['Type','Composed Of','Derived From','Label','High German','wbo','wboHomographe','wboSort','dbo','dboHomographe'
			,'dboSort','dboType','wboDefinition','Release','Checked','Note','Has Lemma','Has Multimedia'];
			for(var i=0;i<attributeList.length;i++){
				opt[i] = "<option value="+attributeList[i]+">"+attributeList[i]+"</option>";
			}
		}
		
		$('#select2').html(opt);
	});
});