class OrgQueryDialog extends AppDialog {
	constructor(element, action){
		
		// this function is moved to the bottom
		//function orgQueryFunction(){ alert("perform organization query function")};
		
		super(element, action, orgQueryFunction, 450, 900);
		
		// create a form
		var matterForm = document.createElement('form');
		matterForm.setAttribute('name', 'matterForm');
		
		// add to the div in the DOM
		this.div.appendChild(matterForm);
	
		// Matter ID
		var matterIdLabel = new TextLabel(matterForm, "matterIdLabel", "Matter ID", 20, 20);
		var matterId = new EntryField(matterForm, "matterId", 20, 40);

		// Matter Name
		var matterNameLabel = new TextLabel(matterForm, "matterNameLabel", "Matter Name", 20, 70);
		var matterName = new EntryField(matterForm, "matterName", 20, 90);
		
		// Push Buttons to Get, Create Matter
		var getMatter = new PushButton(matterForm, "getMatter", "Get Matter", 20, 120,getMyMatter);
		var createMatter = new PushButton(matterForm, "CreateMatter", "Create Matter", 20, 150,createMyMatter);
		
		
		// Push Buttons to Get, Create Matter
		function getMyMatter() {
			console.log("materName=", matterName);
			
			var matter = new VaultMatter();
			
			var matterConfig = matter.getMatterByName(matterName.entryField.value, option_organizations);
			
			//var matterConfig = matter.getMatter(matterId.entryField.value, true);
			
			console.log("matterConfig=", matterConfig);
			
		};
			
		function createMyMatter() {
			//alert("create my matter");
			
			var matterConfig = getMatterConfig();
			
			if(matterConfig == null){
				alert("null matter config");
				return;
			}
			
			console.log("matterConfig=", matterConfig);


			var matter = new VaultMatter();
						
			matter.createMatter(matterConfig, option_organizations);
			
		
		}
		
		/////
		//	Matter Creation and retrieval support routines
		/////
		
		function getList(listBoxName, listType){
		

		var list= []; 
		
		var listbox = document.getElementsByName(listBoxName);
		
		var length = listbox[0].options.length;
		
		if (length == 0) {
			return null;
		}
		
		list = listbox[0].options;
		var finalList = [];
		for(var i=0; i < length; i++){
			
			var entry = list[i].text;
			//var entry = list[i].value;
			console.log("entry=", entry);
			//entry = entry.replace(/[\r]/g,'');
			
			if(listType == "term"){
				var listEntry = {term : entry};
			}
			
			//if(listType == "custodian"){
			//	var listEntry = {custodian : entry};
			//}
			
			if(listType == "organization"){
				
				//var listEntry = {organization : entry};
				var listEntry = {organization : list[i].text, organization_id : list[i].value};
				console.log("listEntry=", listEntry);

			}
			
			finalList.push(listEntry);
		}
		return finalList;
		
		
		};
	
		function getMatterId(){
			return matterId.entryField.value;
		};
		
		function getMatterName(){
			return matterName.entryField.value;
		};
		
		function getTimeSlot(){
			
			console.log("getStartDate()", getStartDate());
			console.log("getEndDate()", getEndDate());
			
			if(getStartDate() == null){
				return null;
			}
			
			if(getEndDate() == null){
				return null;
			}
			
			return {"startTime" : getStartDate(), "endTime" : getEndDate() };
		}

		
		function getStartDate(){
			var dateField = {};
			dateField =  $('[name="startDate"]').val();
			if(dateField == ""){
				return null;
			}
			var temp = dateField.toString().split('/');
			var finalDate = temp[2] + '-' + temp[0] + '-' + temp[1] + "T00:00:00Z";
			return finalDate; 
		};
		
		function getEndDate(){
			var dateField = {};
			dateField =  $('[name="endDate"]').val();
			if(dateField == ""){
				return null;
			}
			var temp = dateField.toString().split('/');
			var finalDate = temp[2] + '-' + temp[0] + '-' + temp[1] + "T00:00:00Z";
			return finalDate; 
		};
		
		function getByOrganization(){
			var checked =  $('[name="byTermsCheckBox"]').val();
			console.log("getByOrganization:checked", checked);
			if (checked == "On"){
				return "True";
			}
			else {
				return "False";
			}
			//return checked;
		};
		
		function getSystemWide(){
			
			var checked =  $('[name="systemWideCheckBox"]').val();
			
			// ACCOUNT OR ENTIRE_ORG
			
			if(checked == true){
				return "ENTIRE_ORG";
			}
			else{
				return "ACCOUNT";
			}
			
			return checked;
			//return systemWideCheckBox.checkBox.value;
		};
		
		function getPrivilege(){
			var checked =  $('[name="privilegeCheckBox"]').val();
			return checked;
		};
		
		function getOrganizations(){
			  
			var orgList = getList("selectOrgsListBox", "organization");
			
			console.log("orgList=",orgList);
		
			return orgList;
			
		};
		
		function getTerms(){
		
			var termList = getList("termsListBox", "term");
			
			console.log("termList=",termList);
		
			return termList;
			
		};
		
		function getMatterConfig(){
			
	
			console.log("terms=", getTerms());
			console.log("organizations=", getOrganizations());
			
			
			var matterConfig = {"byOrganizationOnly" : getByOrganization(),
									"matterName" : getMatterName(),
									"matterId" : getMatterId(),
									//"searchMethod": getSystemWide(), // ACCOUNT OR ENTIRE_ORG
									//"timeSlot" : {"startTime" : getStartDate(), "endTime" : getEndDate() },
									"timeSlot" : getTimeSlot(),
									"terms" : getTerms(),				 // list of dictionary's
									"organizations" : getOrganizations(),  //list of dictionary's
									"matterType" : type_organization,
									// standard config items for initial
									// creation
									// zero initially, will increment as queries are created in matter
									// zero initially, will be #custodians x #terms
									"numQueries" : 0, 
									// zero initially, will increment as queries are created in matter
									"searchCount" : 0, 
									"exportCount" : 0,
									// zero initially, will increment as queries are created in matter
									"downloadCount" : 0,
									"startCount" : 1,
									"exportQueueLength" : 10,
									"exportType" : "MBOX", 
									"severeFname" : "-severe-error.csv",
									"errorFname" : "-query-error.csv", 
									"warningFname" : "-query-warning.csv",
									"apiFname" : "-query-api.csv",
									"exportsFname" : "-exports.csv",
									"countsFname" : "-counts.csv",
									"corpus": "MAIL",
									"dataScope": "ALL_DATA",
									"timeZone": "America/Los_Angeles",
									"completionStatus" : "Pending",
									"matterState" : "Pending"
									};

			
			if(matterConfig['matterName'] == ""){
				alert("empty matterName");
				return null;
			}
			
			if(matterConfig['timeSlot'] == null) {
				alert("empty timeSlot");
				return null;
			}
			
			if(matterConfig['terms'] == null) {
				alert("empty terms");
				return null;
			}
			
			if(matterConfig['organizations'] == null ) {
				alert("empty organizations");
				return null;
			}
			
			// date range check
			var date1 = {};
			var date2 = {};
			date1 =  $('[name="startDate"]').val();
			date2 =  $('[name="endDate"]').val();
			console.log("date1=", date1);
			console.log("date2=", date2);
			
			//if (date1 >= date2){
			//	alert("invalid date range");
			//	return null;
			//}

			return matterConfig;
			
		}
		
		
		//
		// construct the rest of the dialog
		//
		
		// Informational Updates //
		
		// Matter State
		var matterStateText = new ParagraphInfo(matterForm, "matterStateText", "Matter State...", 220, 30);
		
		// Number Queries
		var numberQueriesText = new ParagraphInfo(matterForm, "numberQueriesText", "Number Queries...", 220, 90);
		
		// Creation Status
		var creationStatusText = new ParagraphInfo(matterForm, "creationStatusText", "Pending...", 220, 120);
		
		// Start and End Dates
		var startDateLabel = new TextLabel(matterForm, "startDateLabel", "Start Date", 20, 190);
		var startDate = new DateField(matterForm, "startDate", 20, 210);
		var endDateLabel = new TextLabel(matterForm, "endDateLabel", "End Date", 20, 250);
		var endDate = new DateField(matterForm, "endDate", 20, 270);
		
		// create list box
		var selectOrgsLabel = new TextLabel(matterForm, "selectOrgsLabel", "Organizations", 400, 20);
		var selectOrgsListBox = new ListBox(matterForm, "selectOrgsListBox", 400, 40);
		var loadSelectOrgs = new PushButton(matterForm, "loadSelectOrgs", "Load Orgs", 400, 300,myOrgs);
		
		
		function myOrgs(){

			var orgSelectDialog = new OrgSelectDialog(element,"Select Orgs");

		}
		
		var termsLabel = new TextLabel(matterForm, "termsLabel", "Terms", 650, 20);
		var termsListBox = new ListBox(matterForm, "termsListBox", 650, 40);
		var loadTerms = new PushButton(matterForm, "loadTerms", "Load Terms", 650, 300, myTerms);
		
		
		function myTerms(){
			
			var csvDialog = new CSVDialog(element,"OK", termsListBox);
			
		}
		
		
		// create check box
		var byTermsCheckBox = new CheckBox(matterForm, "byTermsCheckBox", 20, 320);
		var byTermsLabel = new TextLabel(matterForm, "byTermsLabel", "Query Names without Terms", 40, 320);
		
		// create the queries
		
		function orgQueryFunction(){ 
			
			//alert("perform custodian query function");
			
			var matterConfig = getMatterConfig();
			
			if(matterConfig == null){
				alert("configuration not correct");
				return;
			}
			
			
			console.log("matterConfig=", matterConfig);
			
			var organizations = matterConfig['organizations'];
			
			
			var terms = matterConfig['terms'];
			
			//for (var term of terms) {
			//	console.log("term=", term);
			//}
			
			console.log(organizations);
			console.log(terms);
			
			var matter = new VaultMatter();
			
			matter.createOrgQueries(matterConfig);
			
			var creationStatus = document.getElementsByName("creationStatusText");
			
			if( creationStatus[0].innerHTML == "Creation Status: <br><br>Queries Created") {
				console.log("creationStatus=", creationStatus[0].innerHTML);
				alert("Queries already created for this matter");
				return
			}
			
			
			};
		
		
	} // end of constructor
}
