


function load_list(listBox, list, type){

	// clear out the list box first
	// and indices are changed dynamically
	// somewhere in the DOM manager
	// as you remove items
	
	var options = listBox[0].getElementsByTagName('OPTION');
	
	while (options.length != 0){
		listBox[0].removeChild(options[0]);
	}
	
	
	// if it is a custodian type, there is special ProcessingInstruction
	// for the email and type (e.g., MAIL OR GROUPS)
	
	if(type == "custodian"){
		
		for(var i=0; i < list.length; i++){
			let option = document.createElement("option");
			var temp = list[i];
			console.log("temp=", temp);
			var entrytext = temp[type];
			var entrytype = temp['type'];
			option.setAttribute('value', entrytype);
			let optionText = document.createTextNode(entrytext);
			option.appendChild(optionText);
			listBox[0].appendChild(option);
		};
		
		console.log("listBox[0]=", listBox[0]);
		
	}
	else{
	
	
		for(var i=0; i < list.length; i++){
			let option = document.createElement("option");
			var temp = list[i];
			var entry = temp[type];
			option.setAttribute('value', entry);
			let optionText = document.createTextNode(entry);
			option.appendChild(optionText);
			listBox[0].appendChild(option);
		
		};
	}
	
	return
}

async function get_matter_by_name(matter_name, options){
	
	let  myurl = new URL("http://127.0.0.1:8000/get_matter_by_name");

    myurl.searchParams.set('matter_name', matter_name);
	
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
		
			
			var data = await response.json();
			var matter = data['matter'];
			
			console.log("data=", data);
			console.log("matter=", matter);
			
			
			// check to make sure the type of matter corresponds 
			// to the dialog (custodian vs organization) that
			// is trying to load this
			console.log("matter type: ", matter['matterType']);
			console.log("options=", options);

			
			if((options == option_custodians) && (matter['matterType'] != type_custodian)){
				
				alert("Wrong matter type: " + matter['matterType'] )
				return null;
			}
				
			if((options == option_organizations) && (matter['matterType'] != type_organization)){
				
				alert("Wrong matter type: " + matter['matterType'] )
				return null;
			}
			
			var matter_name = matter['matterName'];
			var matter_id = matter['matterId'];
			var state = matter['matterState'];
			
			var num_queries 	= matter['numQueries'];
			
			// TODO: make sure there are  default vaules
			
			var search_count 	= matter['searchCount'];

			var timeSlot 		= matter['timeSlot'];
			var startTime 		= timeSlot['startTime'];
			var endTime 		= timeSlot['endTime'];
			
			var matterInfo = document.getElementsByName("matterInfo");
			var matterId = document.getElementsByName("matterId");
			console.log("matterId=", matterId);
			
			matterId[0].value = matter_id;
			
			// TODO: populate the start/end dates, and the listboxes
			var startDate = document.getElementsByName("startDate");
			var endDate = document.getElementsByName("endDate");
				
			// translate dates from Google Vault format (YYYY-MM-DD) to 
			// menu display (MM/DD/YYYY)
			var temp = startTime.slice(0,10);
			temp = temp.split("-");
			temp = temp[1] + '/' + temp[2] + '/' + temp[0]
			$('[name="startDate"]').val(temp);
				
			var temp = endTime.slice(0,10);
			temp = temp.split("-");
			temp = temp[1] + '/' + temp[2] + '/' + temp[0];
			$('[name="endDate"]').val(temp);
					
			numberQueries = document.getElementsByName("numberQueriesText");
			numberQueries[0].innerHTML = "Num Queries: " + num_queries;
			matterState = document.getElementsByName("matterStateText");
			matterState[0].innerHTML = "Matter State: " + "<br><br>" + state ; // Object.values(matter);
			matterName = document.getElementsByName("matterName");
			//console.log("matterName=", matterName);
			matterName[0].value = matter_name;
				
			
			var startDateEntry 	= document.getElementsByName("startDate");
			var endDateEntry 	= document.getElementsByName("endDate");
				
				
			//var terms 			= matter['terms'];
			//var termList 		= document.getElementsByName("termsListBox");	
			//load_list(termList, terms,"term")
			
			
			//var byTerms = matter['byOrganizationOnly'];

			//	if(byTerms = "True"){
			//		byTermsCheckBox[0].checked = "On";
			//	} else {
			//		byTermsCheckBox[0].checked = "Off";			
			//	}
				
			// set the creation status
			creationStatus = document.getElementsByName("creationStatusText");
				
			var updateText = '<br><br>'	+ search_count + '/' + num_queries;
			creationStatus[0].innerHTML = "Creation Status: <br><br>" + matter['completionStatus'] + updateText;
				
			
			if(options == option_organizations){
			
				var organizationList = document.getElementsByName("selectOrgsListBox");
				
				
				// dialog specific config file entries
				var organizations 	= matter['organizations'];
				
				load_list(organizationList, organizations,"organization")
				
				var terms 			= matter['terms'];
				var termList 		= document.getElementsByName("termsListBox");	
				
				load_list(termList, terms,"term")
			
				var byTermsCheckBox		= document.getElementsByName("byTermsCheckBox");	
				var byTerms = matter['byOrganizationOnly'];

				if(byTerms == "True"){
					byTermsCheckBox[0].checked = "On";
					} else {
					byTermsCheckBox[0].checked = "";			
					}
				
				}
			
			
			if(options == option_custodians){
			
				var custodianList 	= document.getElementsByName("custodiansListBox");
				
				var custodians 	= 	matter['custodianEmails'];
							
				load_list(custodianList, custodians,"custodian")
				
				var terms 			= matter['terms'];
				var termList 		= document.getElementsByName("termsListBox");	
				load_list(termList, terms,"term")
			
			    console.log("matter['byCustodianOnly']",matter['byCustodianOnly']);
				var byTerms = matter['byCustodianOnly'];
				var byTermsCheckBox		= document.getElementsByName("byTermsCheckBox");	

				if(byTerms == "True"){
					byTermsCheckBox[0].checked = "On";
					} else {
					byTermsCheckBox[0].checked = "";			
					}
				
				// set the creation status
				//creationStatus = document.getElementsByName("creationStatusText");
				
				//var updateText = '<br><br>'	+ search_count + '/' + num_queries;
				//creationStatus[0].innerHTML = "Creation Status: <br><br>" + matter['completionStatus'] + updateText;
					
				}
			
			
			if((options == option_counts) || (options == option_exports) || (options == option_downloads)) {
				
				// translate dates from Google Vault format (YYYY-MM-DD) to 
				// menu display (MM/DD/YYYY)
				//var startDate = startTime.slice(0,10);
				//startDate = startDate.split("-");
				//startDate = startDate[1] + '/' + startDate[2] + '/' + startDate[0]

				//var endDate = endTime.slice(0,10);
				//endDate = endDate.split("-");
				//endDate = endDate[1] + '/' + endDate[2] + '/' + endDate[0]
			
			
				//var updateText = '<br><br>'	+ search_count + '/' + num_queries;
				//var datesText = '<br><br>' + 'Start Date: <br><br>' +  startDate + '<br><br>' + 'End Date: <br><br>' + endDate;

				//matterInfo[0].innerHTML = "Queries Created: " + updateText + datesText;
			
				}

			return matter;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}


async function create_matter(matter_config, options){
	matter = {};
	
	if (options == option_custodians){
		var custodians = matter_config['custodianEmails'];	
		var terms = matter_config['terms'];
		matter_config['numQueries'] = custodians.length * terms.length;
	}
	
	if (options == option_organizations){		
		var organizations = matter_config['organizations'];	
		var terms = matter_config['terms'];
		matter_config['numQueries'] = organizations.length * terms.length;	
	}
	
	
	let  myurl = new URL("http://127.0.0.1:8000/create_matter");

    myurl.searchParams.set('matter_config', JSON.stringify(matter_config));
	    
	
	try {
		
		var response = await fetch(myurl);
		
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var matter = data['matter'];
			
			var matter_id = matter['matterId'];
			var state = matter['matterState'];
				
			matterState = document.getElementsByName("matterStateText");
			matterState[0].innerHTML = "Matter State: " + state; // Object.values(matter);
			matterId = document.getElementsByName("matterId");
			matterId[0].value = matter_id;
			numberQueries = document.getElementsByName("numberQueriesText");
			numberQueries[0].innerHTML = "Num Queries: " + "0";
			
			// set the creation status
			creationStatus = document.getElementsByName("creationStatusText");
			creationStatus[0].innerHTML = "Creation Status: <br><br>" + matter['completionStatus'];

			return matter;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	
	return false;
	
}
var myInterval;
var weAreDone = "";

async function updateProgress(){
	
	var today = new Date();
	var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

	let  myurl = new URL("http://127.0.0.1:8000/get_query_progress");
    //myurl.searchParams.set('matter_id', matter_id);
	
	var response = await fetch(myurl);
		
	console.log("response=", response);
		
	if(response.status = 200){
			
		var data = await response.json();
		
		console.log("progress=", data);
		numQueries = data['numQueries'];
		searchCount = data['searchCount'];
		var queryStatus = data['creationStatus'];
		var creationStatus = document.getElementsByName("creationStatusText");
		var progressText = "Queries Created: " + "<br><br>" + JSON.stringify(searchCount) + " / " +  JSON.stringify(numQueries)
		var numberQueries = document.getElementsByName("numberQueriesText");
		
	    if(numQueries == searchCount){
			clearInterval(myInterval);
		}
		
		if(queryStatus.includes("Error") == true){
			progressText += "<br><br>" + queryStatus;
			clearInterval(myInterval);
		}
		
		creationStatus[0].innerHTML = 	progressText;
		numberQueries[0].innerHTML = "Num Queries: " + JSON.stringify(numQueries);
	}
}



async function create_org_queries(matterConfig){
	matter = {};
	let  myurl = new URL("http://127.0.0.1:8000/create_org_queries");
	myurl.searchParams.set('query_config', JSON.stringify(matterConfig));
	

	
	try {
		var response = await fetch(myurl);
		
		if(response.status = 200){
			
			var data = await response.json();
			
			var matterObj = data['matter'];
					
			numQueries = matterObj['numQueries'];
			searchCount = matterObj['searchCount'];
			
			if(numQueries > 0){
				
				// this matter already has queries in it
				// we don't allow more queries to be added
				// at this time
				
				// fill in the user interface, but for now an alert 
				// and return
				alert("queries already exist");
				
				return matterObj;
				
			}
			
			
			console.log("matterObj=", matterObj);
			
			//progress updater
			myInterval = setInterval(updateProgress,2000)
			
			return matterObj;
		}
		
		
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	
	return false;
	
}



async function create_queries(matterConfig){
	matter = {};
	let  myurl = new URL("http://127.0.0.1:8000/create_queries");
	myurl.searchParams.set('query_config', JSON.stringify(matterConfig));
	
	try {
		var response = await fetch(myurl);
		
		if(response.status = 200){
			
			var data = await response.json();
			
			var matterObj = data['matter'];
					
			numQueries = matterObj['numQueries'];
			searchCount = matterObj['searchCount'];
			
			if(numQueries > 0){
				
				// this matter already has queries in it
				// we don't allow more queries to be added
				// at this time
				
				// fill in the user interface, but for now an alert 
				// and return
				alert("queries already exist");
				
				return matterObj;
				
			}
			
			
			console.log("matterObj=", matterObj);
			
			//progress updater
			myInterval = setInterval(updateProgress,2000)
			
			return matterObj;
		}
		
		
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	
	return false;
	
}

async function update_settings(parms){
	matter = {};
	
	let  myurl = new URL("http://127.0.0.1:8000/update_settings");

    myurl.searchParams.set('parms', JSON.stringify(parms));
	
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var settings = data['settings'];
			
			console.log("data=", data);

			
			return settings;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}



async function get_settings(){
	matter = {};
	
	let  myurl = new URL("http://127.0.0.1:8000/get_settings");

    
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var settings = data['settings'];
			
			//console.log("data=", data);
			
			console.log(settings);
			
			var powerUser 			= document.getElementsByName("powerUser");
			var logFiles 			= document.getElementsByName("logFiles");
			var dataFiles 			= document.getElementsByName("dataFiles");
			var sftpIP 				= document.getElementsByName("sftpIP");
			var sftpUsername		= document.getElementsByName("sftpUsername");
			var sftpPassword		= document.getElementsByName("sftpPassword");
			var sharedDrive 		= document.getElementsByName("sharedDrive");
			var exportQueueLimit 	= document.getElementsByName("exportQueueLimit");
			
		
			powerUser[0].value 			= settings['powerUser'];
			logFiles[0].value           = settings['logFiles'];                
			dataFiles[0].value          = settings['dataFiles'];               
			sftpIP[0].value             = settings['sftpIP'];    
			sftpUsername[0].value       = settings['sftpUsername'];    
			sftpPassword[0].value		= settings['sftpPassword']
			sharedDrive[0].value        = settings['sharedDrive'];             
			exportQueueLimit[0].value   = settings['exportQueueLimit'];        
		
			
			return settings;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}




async function update_config(matter_id){
	matter = {};
	
	let  myurl = new URL("http://127.0.0.1:8000/update_config");

    myurl.searchParams.set('matter_id', matter_id);
	
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var matter = data['matter'];
			
			console.log("data=", data);
			console.log("matter=", matter);
			var matter_name = matter['matterName'];
			var state = matter['state'];
			var num_queries = matter['numQueries'];
			var custodians = matter['custodianEmails']
			var terms = matter['terms']
			var timeSlot = matter['timeSlot']
			var startTime = timeSlot['startTime']
			var endTime = timeSlot['endTime']
			
			var custodianList = document.getElementsByName("custodiansListBox");
			var termList = document.getElementsByName("termsListBox");
			var startDateEntry = document.getElementsByName("startDate");
			var endDateEntry = document.getElementsByName("endDate");
			
			return matter;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}

async function updateCountProgress(){
	
	var today = new Date();
	var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

	let  myurl = new URL("http://127.0.0.1:8000/get_count_progress");
    //myurl.searchParams.set('matter_id', matter_id);
	
	var response = await fetch(myurl);
		
	console.log("response=", response);
		
	if(response.status = 200){
			
		var progress = await response.json();
		
		console.log("progress=", progress);
		
		queryCount = progress['queryCount']
		grandTotal = progress['grandTotal']
		numQueries = progress['numQueries']
		
		var countsInfo = document.getElementsByName("countsInfo");
		
		var updateText = '<br><br>'	+ '<font color="blue">' + queryCount + '/' + numQueries;
		var totalsText = '<br><br>' + '<font color="black">' + 'Total Emails: <br><br>' +  '<font color="blue">' + grandTotal;
			
		
		if(queryCount == numQueries){
			totalsText += '<font color="blue">' + "<br><br> Counting Complete, report emailed."
			clearInterval(myInterval);
			}

		countsInfo[0].innerHTML = '<font color="black">' + "Queries Counted: " + updateText + totalsText;
		

	}
}


async function count_matter(matter_id, recipient){
	matter = {};
	
	let export_parms = {"matterId" : matter_id, "recipient" : recipient};

	let  myurl = new URL("http://127.0.0.1:8000/count_matter");
	
    myurl.searchParams.set('export_parms', JSON.stringify(export_parms));

	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var matter = data['matter'];
			
			console.log("data=", data);
			console.log("matter=", matter);
			
			//progress updater
			myInterval = setInterval(updateCountProgress,2000)
			
			return matter;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}

async function updateExportProgress(){
	
	var today = new Date();
	var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

	let  myurl = new URL("http://127.0.0.1:8000/get_export_progress");
	
	var response = await fetch(myurl);
		
	console.log("response=", response);
		
	if(response.status = 200){
			
		var progress = await response.json();
		
		//{"numQueries" : numQueries, "numExports" : numExports, "exportProgress" : exportProgress}
		var numQueries = progress['numQueries'];
		var queryCount = progress['queryCount'];
		var numExports = progress['numExports']
		var exportCount = progress['exportCount'];
		var reportsDone = progress['reportsDone']
		
		console.log("progress=", progress);
		
		var exportsInfo = document.getElementsByName("exportsInfo");
		
		var updateText = '<br><br>'	+ '<font color="blue">' + queryCount + '/' + numQueries;
		var exportText = '<br><br>'	+ '<font color="black">' + 'Exports Progress: ' + '<br><br>' + '<font color="blue">' + exportCount + '/' + numExports;
			
		exportsInfo[0].innerHTML = "Queries Processed: " + updateText + exportText;
		
		
		if(reportsDone == true){
			exportText = '<br><br>'	+ '<font color="black">' + "Exports Complete: " + '<br><br>' + '<font color="blue">' + exportCount + '/' + numExports;
			exportsInfo[0].innerHTML = '<font color="black">' + "Queries Processed: " + '<font color="blue">'+ updateText + exportText;
			clearInterval(myInterval);
			}
	}
}


async function create_exports(matter_id, recipient, exportType, queueSize){
	
	let  myurl = new URL("http://127.0.0.1:8000/create_exports");

	let export_parms = {"matterId" : matter_id, "recipient" : recipient, "exportType" : exportType, "queueSize" : queueSize};

	
    myurl.searchParams.set('export_parms', JSON.stringify(export_parms));
	
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var matter = data['matter'];
			
			console.log("data=", data);
			console.log("matter=", matter);
			
			//progress updater
			myInterval = setInterval(updateExportProgress,10000)
			
			return matter;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}


async function updateDownloadProgress(){
	
	var downloadingFromVault    = 1;
	var separatingMBOX          = 2;
	var uploadingToDrive        = 3;
	var uploadingToSFTP         = 4;
	var downloadsFinished       = 5;
	var noDownloads				= 6;
	
	var updateText = "";
	
	var today = new Date();
	
	var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

	let  myurl = new URL("http://127.0.0.1:8000/get_downloads_progress");
	
	var response = await fetch(myurl);
		
	console.log("response=", response);
		
	if(response.status = 200){
			
		var progress = await response.json();
		
		//{"numQueries" : numQueries, "numExports" : numExports, "exportProgress" : exportProgress}
		numExports = progress['numExports'];
		downloadCount = progress['downloadCount'];
		exportCount = progress['exportCount'];
		downloadsDone = progress['downloadsDone']
		
		downloadStatus 	=	progress['downloadStatus']
		mboxStatus    	=   progress['mboxStatus']
		driveStatus   	=	progress['driveStatus']
		sftpStatus    	=	progress['sftpStatus']
		
		
		console.log("progress=", progress);
		
		var exportsInfo = document.getElementsByName("downloadsInfo");
		
		if(downloadsDone == noDownloads){
			exportsInfo[0].innerHTML = '<br><br>'	+ '<font color="blue">' + 'Warning: No exports in Matter to download...'
			clearInterval(myInterval);
			return
		
		}
		
		
		var vaultText = "Download Progress: " + '<br><br>' + '<font color="blue">' + 'Exports ' + exportCount + '/' + numExports + 
												'<br><br>' + '<font color="red">' + 'Files Downloaded: ' + downloadCount; 
		
		var mboxText = '<br><br>'	+ '<font color="black"> MBOX Status: ' + '<br><br>' + mboxStatus;
		
		var driveText = '<br><br>'	+ '<font color="black"> Google Drive Status: '  + '<br><br>' + driveStatus;
		
		var SFTPText = '<br><br>'	+ '<font color="black"> SFTP Status : ' + '<br><br>'  + sftpStatus;
		
		var finishedText = '<br><br><br><br>'	+ '<font color="blue"> Download Process Complete.' ;
		
		displayText = vaultText + mboxText + driveText + SFTPText
		
		if(downloadsDone == downloadsFinished){
			displayText += finishedText;
			clearInterval(myInterval);
			}
			
		console.log("displayText=", displayText);
		
		exportsInfo[0].innerHTML = displayText;
			
			
	}
}

async function create_downloads(matter_id, recipient, options){
	
	let  myurl = new URL("http://127.0.0.1:8000/create_downloads");

	let export_parms = {"matterId" : matter_id, "recipient" : recipient, "options" : options};

    myurl.searchParams.set('export_parms', JSON.stringify(export_parms));
	
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var matter = data['matter'];
			
			console.log("data=", data);
			console.log("matter=", matter);
			
			//progress updater
			myInterval = setInterval(updateDownloadProgress,10000)
			
			return matter;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}


async function send_email(matter_name, recipient){
	
	let  myurl = new URL("http://127.0.0.1:8000/send_email");
	
	email_parms = {"matter_name" : matter_name, "recipient" : recipient};
	
	console.log("email_parms", email_parms);
	
	console.log("JSON.stringify(email_parms)=", JSON.stringify(email_parms));
	
    myurl.searchParams.set('email_parms', JSON.stringify(email_parms));
	
	console.log("myurl=", myurl);
	
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){
			
			var data = await response.json();
			var matter = data['matter'];
			
			console.log("data=", data);
			console.log("matter=", matter);
			
			//progress updater
			//myInterval = setInterval(updateCountProgress,2000)
			
			return matter;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}



async function get_orginfo(){
	
	let  myurl = new URL("http://127.0.0.1:8000/get_orginfo");

	//let export_parms = {"matterId" : matter_id, "recipient" : recipient, "options" : options};

    //myurl.searchParams.set('export_parms', JSON.stringify(export_parms));
	
	try {
		
		var response = await fetch(myurl);
		console.log("response=", response);
		
		if(response.status = 200){

			var data = await response.json();
			
			console.log("data=", data);

			var orgInfo = data['orgInfo'];

			//console.log("orgInfo=", orgInfo);
			var lines = orgInfo.split('\n');
			console.log("numlines=", lines.length);
			
			var orgList = [];
			
			for (var i=0; i < lines.length;  i++ ){
				
				var org = lines[i].split(',')
				
				var orgType = org[0]
				var orgName = org[1]
				var orgId = org[2]
				
				//console.log("orgType=", orgType, "orgName=", orgName, "orgId=", orgId)
				
				//orgList.push(orgName)
				orgList.push([orgId,orgName])
				
				}
			
			console.log("orgList.length=", orgList.length)
			console.log("orgList=", orgList)
			
			var organizationsList = document.getElementsByName("organizationsListBox");
			
			load_listbox(organizationsList, orgList);

			return orgInfo;
		}
		
	} catch(error) {
		console.log("failure connecting to server, error=", error);
	}

	console.log("at the bottom of do_fetch()");
	return false;
}


