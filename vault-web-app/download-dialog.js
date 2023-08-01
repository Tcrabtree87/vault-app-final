	
class DownloadsDialog extends AppDialog {
	constructor(element, action){
		
		function downloadsFunction(){ 
			
			//alert("perform downloads function");
			
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
			
			// get values of checkboxes
			var seperateMBOX  = seperateMboxCheckBox.checkBox.checked;
			var uploadToDrive = uploadToDriveCheckBox.checkBox.checked;
			var uploadToSFTP  = uploadToSFTPCheckBox.checkBox.checked;
			
			var options = { "seperateMBOX" : seperateMBOX, "uploadToDrive" : uploadToDrive, "uploadToSFTP" : uploadToSFTP };
			
			var matter = new VaultMatter();			
			
			var matter_info = matter.downloadExports(matter_id, email_address, options);
			
			//TODO: update matter configuration state
			//matterConfig['matterState'] = matter_state_downloaded;
			//
			//
			//var matterConfig = matter.getMatterByName(matter_name, option_downloads);
			
			//console.log("matterConfig=", matterConfig);
			//
			//
			
		}
		
		super(element, action, downloadsFunction, 550, 750);
		
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
		var getMatter = new PushButton(matterForm, "getMatter", "Get Matter", 20, 120, getMatterByName);
		//var exportMatter = new PushButton(matterForm, "exportMatter", "Export Matter", 20, 150);
		
		function getMatterByName() {
			
			var matter_name = matterName.entryField.value;
			
			console.log("mater_name=", matter_name);
			
			if(matter_name == ""){
				alert("enter a valid matter name");
				return 
			}
			
			var matter = new VaultMatter();
			
			var matterConfig = matter.getMatterByName(matter_name, option_downloads);
			
			console.log("matterConfig=", matterConfig);
			
		};

		// Email Address to get report delivered to
		var emailNameLabel = new TextLabel(matterForm, "emailNameLabel", "Email for report", 20, 280);
		var emailName = new EntryField(matterForm, "emailName", 20, 310);

		// matter info
		//var matterInfo = new TextInfo(matterForm, "matterInfo", "matter info...", 250, 40);
		
		// Informational Updates //
		
		// Matter State
		var matterStateText = new ParagraphInfo(matterForm, "matterStateText", "Matter State...", 220, 30);
		
		// Number Queries
		var numberQueriesText = new ParagraphInfo(matterForm, "numberQueriesText", "Number Queries...", 220, 90);
		
		// Creation Status
		var creationStatusText = new ParagraphInfo(matterForm, "creationStatusText", "Pending...", 220, 120);
		
		
		
		// downloads info
		var downloadsInfo = new TextInfo(matterForm, "downloadsInfo", "downloads info...", 425, 40);
		
		// create check box to seperate MBOX files
		var seperateMboxLabel = new TextLabel(matterForm, "seperateMboxLabel", "Seperate MBOX", 20, 170);
		var seperateMboxCheckBox = new CheckBox(matterForm, "seperateMboxCheckBox", 150, 170);
		
		// create check box to upload to Google Shared Drive
		var uploadToDriveLabel = new TextLabel(matterForm, "uploadToDriveLabel", "Upload to Drive", 20, 200);
		var uploadToDriveCheckBox = new CheckBox(matterForm, "uploadToDriveCheckBox", 150, 200);
		
		// create check box to upload to SFTP Server
		var uploadToSFTPLabel = new TextLabel(matterForm, "uploadToSFTPLabel", "Upload to SFTP", 20, 230);
		var uploadToSFTPCheckBox = new CheckBox(matterForm, "uploadToSFTPCheckBox", 150, 230);
		
		
		// create check box to make PDF's
		//var pdfLabel = new TextLabel(matterForm, "pdfLabel", "Make PDF's", 20, 190);
		//var pdfCheckBox = new CheckBox(matterForm, "pdfCheckBox", 150, 190);
	}
}
