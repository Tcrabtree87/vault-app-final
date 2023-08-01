

class CountsDialog extends AppDialog {
	constructor(element, action){
		
		function countsFunction(){ 
		
			//alert("perform counts function")
			
			var matter_id = matterId.entryField.value;
			
			if(matter_id == ""){
				alert("empty matter id");
				return
			}
			
			var email_address = emailName.entryField.value;
			console.log("email_address=", email_address);
			
			if(email_address == ""){
				alert("enter email address for report");
				return;
			}
			
			// information alert that the counting process is starting
			//var countsAlert = new AlertInfo(matterForm, "matterInfo", "count process starting...", 450, 20);
			
						
			var matter = new VaultMatter();			
			var matter_info = matter.count(matter_id, email_address);
			
			//TODO: update matter configuration state
			//matterConfig['matterState'] = matter_state_counted;
			
			console.log("matter_info=", matter_info);
			
		};
		
		super(element, action, countsFunction, 450, 600);
		
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
		var getMatter = new PushButton(matterForm, "getMatter", "Get Matter", 20, 120,getMatterByName);
		
		// Push Buttons to Get, Create Matter
		function getMatterByName() {
			
			var matter_name = matterName.entryField.value;
			
			console.log("mater_name=", matter_name);
			
			
			if(matter_name == ""){
				alert("enter a valid matter name");
				return 
			}
			
			var matter = new VaultMatter();
			
			var matterConfig = matter.getMatterByName(matter_name, option_counts);
			
			console.log("matterConfig=", matterConfig);
			
		};

		// Email Address to get report delivered to
		var emailNameLabel = new TextLabel(matterForm, "emailNameLabel", "Email for report", 20, 200);
		var emailName = new EntryField(matterForm, "emailName", 20, 230);

		// create check box
		//var bySizeLabel = new TextLabel(matterForm, "bySizeLabel", "Get Size in Report", 40, 260);
		//var bySizeCheckBox = new CheckBox(matterForm, "bySizeCheckBox", 20, 260);



		// Informational Updates //
		
		// Matter State
		var matterStateText = new ParagraphInfo(matterForm, "matterStateText", "Matter State...", 220, 30);
		
		// Number Queries
		var numberQueriesText = new ParagraphInfo(matterForm, "numberQueriesText", "Number Queries...", 220, 90);
		
		// Creation Status
		var creationStatusText = new ParagraphInfo(matterForm, "creationStatusText", "Pending...", 220, 120);
		

		// matter info
		//var matterInfo = new ParagraphInfo(matterForm, "matterInfo", "matter info...", 250, 20);
		
		// counts info
		var countsInfo = new ParagraphInfo(matterForm, "countsInfo", "counts info...", 450, 20);
	}
}

