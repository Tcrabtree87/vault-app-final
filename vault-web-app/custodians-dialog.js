

class CustodianQueryDialog extends AppDialog {
	constructor(element, action){
		
    
		super(element, action, custodianQueryFunction, 450, 900);
	
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
		
		
		// Informational Updates //
		// Matter State
		var matterStateText = new ParagraphInfo(matterForm, "matterStateText", "Matter State...", 220, 30);
		
		// Number Queries
		var numberQueriesText = new ParagraphInfo(matterForm, "numberQueriesText", "Number Queries...", 220, 90);
		
		// Creation Status
		var creationStatusText = new ParagraphInfo(matterForm, "creationStatusText", "Pending...", 220, 120);
		
		
		// Push Buttons to Get, Create Matter
		function getMyMatter() {
			console.log("materName=", matterName);
			
			var matter = new VaultMatter();
			
			var matterConfig = matter.getMatterByName(matterName.entryField.value, option_custodians);
			
			//var matterConfig = matter.getMatter(matterId.entryField.value, true);
			console.log("matterConfig=", matterConfig);
			
		};
			
		function createMyMatter() {
			//alert("create my matter");
			
			var matterConfig = getMatterConfig();
			
			matterConfig['matterState'] = matter_state_created;
			
			if(matterConfig == null){
				return;
			}
			
			console.log("matterConfig=", matterConfig);

			var matter = new VaultMatter();
						
			matter.createMatter(matterConfig);
			
		
		}
		

		
		var getMatter = new PushButton(matterForm, "getMatter", "Get Matter", 20, 120, getMyMatter);
		var createMatter = new PushButton(matterForm, "CreateMatter", "Create Matter", 20, 150, createMyMatter);
		
		// Start and End Dates
		
		var startDateLabel = new TextLabel(matterForm, "startDateLabel", "Start Date", 20, 180);
		var startDate = new DateField(matterForm, "startDate", 20, 200);
		var endDateLabel = new TextLabel(matterForm, "endDateLabel", "End Date", 20, 230);
		var endDate = new DateField(matterForm, "endDate", 20, 250);
		
		// create list box
		
		var custodiansLabel = new TextLabel(matterForm, "custodiansLabel", "Custodians", 400, 20);
		var custodiansListBox = new ListBox(matterForm, "custodiansListBox", 400, 40);
		var loadCustodians = new PushButton(matterForm, "loadCustodians", "Load Custodians", 400, 300, myCustodians);
		
		
		function myCustodians(){

			var csvDialog = new CSVDialog(element,"OK", custodiansListBox);
		
		}
		
		
		var termsLabel = new TextLabel(matterForm, "termsLabel", "Terms", 650, 20);
		var termsListBox = new ListBox(matterForm, "termsListBox", 650, 40);
		var loadTerms = new PushButton(matterForm, "loadTerms", "Load Terms", 650, 300, myTerms);
	
	
		function myTerms() {
			
			//alert("load my terms");
			
			var csvDialog = new CSVDialog(element,"OK", termsListBox);
			
		}
		
		// check for privilege
		//var privilegeLabel = new TextLabel(matterForm, "privilegeLabel", "Privilege Report", 40, 290);
		//var privilegeCheckBox = new CheckBox(matterForm, "privilegeCheckBox", 20, 290);
		
		// create byTerms check box
		var byTermsLabel = new TextLabel(matterForm, "byTermsLabel", "Query Names without Terms", 40, 310);
		var byTermsCheckBox = new CheckBox(matterForm, "byTermsCheckBox", 20, 310);
		
		// create system wide check box
		var systemWideLabel = new TextLabel(matterForm, "systemWide", "System Wide Search", 40, 330);
		var systemWideCheckBox = new CheckBox(matterForm, "systemWideCheckBox", 20, 330);
		
		
		function getList(listBoxName, listType){
		

		var list= []; 
		
		var listbox = document.getElementsByName(listBoxName);
		
		var length = listbox[0].options.length;
		
		if (length == 0) {
			return null;
		}
		
		list = listbox[0].options;
		console.log("list=", list);
		var finalList = [];
		
		
		
		
		for(var i=0; i < length; i++){
			
			var entryValue = list[i].value;
			var entryText = list[i].innerText;
			console.log("entryValue=", entryValue);
			console.log("entryText=", entryText);
			var entrytext = entryText.replace(/[\r]/g,'');
			var entryvalue = entryValue.replace(/[\r]/g,'');
			
			
			if(listType == "term"){
				var listEntry = {term : entrytext};
			}
			if(listType == "custodian"){
				// for custodians, the list that comes out of the list box
				// contains the email, and what type it is, e.g. MAIL, or GROUPS.
				// This corresponds to the type of query to create for Google Vault API
				// on the backend.
				
				
				var listEntry = {custodian : entrytext, "type" : entryvalue};
			}
			finalList.push(listEntry);
		}
		
		console.log("finalList=", finalList);
		
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
		function getByCustodian(){
			var checked =  $('[name="byTermsCheckBox"]').val();
			
			if (checked == "On"){
				return "True";
			} else {
				return "False";
			}
			
			return checked;
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
		
		function getCustodians(){
			  
			var nameList = getList("custodiansListBox", "custodian");
			
			console.log("nameList=",nameList);
		
			return nameList;
			
		};
		
		function getTerms(){
		
			var termList = getList("termsListBox", "term");
			
			console.log("termList=",termList);
		
			return termList;
			
		};

		function getMatterConfig(){
			
	
			console.log("terms=", getTerms());
			console.log("custodians=", getCustodians());
			
			
			var matterConfig = {"byCustodianOnly" : getByCustodian(),
								"matterName" : getMatterName(),
								"matterId" : getMatterId(),
								"searchMethod": getSystemWide(), // ACCOUNT OR ENTIRE_ORG
								//"timeSlot" : {"startTime" : getStartDate(), "endTime" : getEndDate() },
								"timeSlot" : getTimeSlot(),
								"terms" : getTerms(),				 // list of dictionary's
								"custodianEmails" : getCustodians(),  //list of dictionary's
								"matterType" : type_custodian,
								// standard config items for initial
								// creation
								// zero initially, will be #custodians x #terms
								"numQueries" : 0, 
								// zero initially, will increment as queries are created in matter
								"searchCount" : 0, 
								// zero initially, will increment as exports are created in matter
								"exportCount" : 0,
								// zero initially, will increment as downloads are created in matter
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
			
			if(matterConfig['custodianEmails'] == null ) {
				alert("custodianEmails");
				return null;
			}
			
			
			// date range check
			var date1 = {};
			var date2 = {};
			date1 =  $('[name="startDate"]').val();
			date2 =  $('[name="endDate"]').val();
			console.log("date1=", date1);
			console.log("date2=", date2);
			
			if (date1 > date2){
				alert("invalid date range");
				return null;
			}
			
			return matterConfig;
			
		}
		
		function custodianQueryFunction(){ 
			
			//alert("perform custodian query function");
			
			var matterConfig = getMatterConfig();
			
			console.log("matterConfig=", matterConfig);
			
			if(matterConfig == null){
				alert("configuration not correct");
				return;
			}
			
			var creationStatus = document.getElementsByName("creationStatusText");
			
			if( creationStatus[0].innerHTML == "Creation Status: <br><br>Queries Created") {
				console.log("creationStatus=", creationStatus[0].innerHTML);
				alert("Queries already created for this matter");
				return
			}
			
			console.log("matterConfig=", matterConfig);
			
			var custodianEmails = matterConfig['custodainEmails'];
			
			
			var terms = matterConfig['terms'];
			
			//for (var term of terms) {
			//	console.log("term=", term);
			//}
			
			console.log(custodianEmails);
			console.log(terms);
			
			matterConfig['matterState'] = matter_state_queries;
			
			
			var matter = new VaultMatter();
			
			matter.createQueries(matterConfig);
			
			};
	
	}; // end of constructor
}