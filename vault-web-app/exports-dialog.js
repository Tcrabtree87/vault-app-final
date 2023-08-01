
class ExportsDialog extends AppDialog {
	constructor(element, action){
		
		super(element, action, exportsFunction, 450, 600);

		
		var export_type = "MBOX"; // default to MBOX
		//var queueSize = 10;
		
		function exportsFunction(){ 
			//alert("perform exports function")
			
			var matter_id = matterId.entryField.value;
			
			if(matter_id == ""){
				alert("empty matter id");
				return
			}
			
			// check to see if exports exist already
			
			
			
			
			
			var email_address = emailName.entryField.value;
			console.log("email_address=", email_address);
			
			if(email_address == ""){
				alert("enter email address for report");
				return;
			}
			
			var queue_size = queueSize.entryField.value;
			
			if(queue_size == ""){
				alert("enter number of simultaneous exports");
				return;
			}
			
			if(pstRadioButton.state == "on"){
				
				export_type = "PST";
			} 
			else {
				export_type = "MBOX";
			}
			
			
			
			var matter = new VaultMatter();			
			
			var matter_info = matter.createExports(matter_id, email_address, export_type, queue_size);
			
			
			//TODO: update matter configuration state
			//matterConfig['matterState'] = matter_state_exported;
			
			};
		
		
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
		
		function getMatterByName() {
			
			var matter_name = matterName.entryField.value;
			
			console.log("mater_name=", matter_name);
			
			if(matter_name == ""){
				alert("enter a valid matter name");
				return 
			}
			
			var matter = new VaultMatter();
			
			var matterConfig = matter.getMatterByName(matter_name, option_exports);
			
			console.log("matterConfig=", matterConfig);
			
		};
		
		// Email Address to get report delivered to
		var emailNameLabel = new TextLabel(matterForm, "emailNameLabel", "Email for report", 20, 300);
		var emailName = new EntryField(matterForm, "emailName", 20, 320);

		// Informational Updates //
		
		// Matter State
		var matterStateText = new ParagraphInfo(matterForm, "matterStateText", "Matter State...", 220, 30);
		
		// Number Queries
		var numberQueriesText = new ParagraphInfo(matterForm, "numberQueriesText", "Number Queries...", 220, 90);
		
		// Creation Status
		var creationStatusText = new ParagraphInfo(matterForm, "creationStatusText", "Pending...", 220, 120);

		// matter info
		//var matterInfo = new TextInfo(matterForm, "matterInfo", "matter info...", 250, 40);
		
		// export info
		var exportsInfo = new TextInfo(matterForm, "exportsInfo", "exports info...", 450, 40);
		
		var exportTypesLabel = new TextLabel(matterForm, "exportTypesLabel", "Export Types", 20, 160);
		
		var pstButtonLabel = new TextLabel(matterForm, "pstButtonLabel", "PST", 20, 210);
		var mboxButtonLabel = new TextLabel(matterForm, "mboxButtonLabel", "MBOX", 20, 190);
		
		var pstRadioButton = new RadioButton(matterForm, "pstRadioButton", 80, 210, pstRadioButtonListner);
		var mboxRadioButton = new RadioButton(matterForm, "mboxRadioButton", 80, 190, mboxRadioButtonListner);
		
		mboxRadioButton.state = "on";
		mboxRadioButton.radioButton.checked = true;
		
		function pstRadioButtonListner () {
			
			console.log("pstRadioButton.state",pstRadioButton.state);
		
			if(pstRadioButton.state == "on") {
				mboxRadioButton.state = "off";
				mboxRadioButton.radioButton.checked = false;
				this.exportType = "PST";
			} 
			
				
		}
		
		function mboxRadioButtonListner () {
			
			console.log("mboxRadioButton.state",mboxRadioButton.state);
			
			if(mboxRadioButton.state == "on") {
				pstRadioButton.state = "off";
				pstRadioButton.radioButton.checked = false;
				this.exportType = "MBOX";
			} 
			
		}
		
		var queueSizeLabel = new TextLabel(matterForm, "queueSizeLabel", "#Simultaneous Exports", 20, 240);
		var queueSize = new EntryField(matterForm, "queueSize", 20, 260);
		
		
		queueSize.entryField.value = 10;
		
		
		
		
		
		
		
	}
}