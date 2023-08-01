class SettingsDialog extends AppDialog {
	constructor(element, action){
		
		function settingsFunction(){ 
		
					//alert("Settings")
					
					var power_user = powerUser.entryField.value;
					var log_files = logFiles.entryField.value;
					var data_files = dataFiles.entryField.value;
					var sftp_ip = sftpIP.entryField.value;
					var shared_drive = sharedDrive.entryField.value;
					var queue_limit = exportQueueLimit.entryField.value;
					var sftp_user = sftpUsername.entryField.value;
					var sftp_password = sftpPassword.entryField.value;
					
					
					var settings_parms = { 
								settingsParms : { 		"powerUser" : power_user,
														"sftpUsername" : sftp_user,
														"sftpPassword" : sftp_password,
														"logFiles" : log_files,
														"dataFiles" : data_files,
														"sftpIP" : sftp_ip,
														"sharedDrive" : shared_drive,
														"exportQueueLimit" : queue_limit
									}
														
							}
							
					console.log(settings_parms);
					
					
					// grab the settings and save them
					// to a configuration file
					var matter = new VaultMatter();			
					var settings_info = matter.updateSettings(settings_parms);
					
					
		};
		
		super(element, action, settingsFunction, 450, 600);
		
		// create a form
		var matterForm = document.createElement('form');
		matterForm.setAttribute('name', 'matterForm');

		// add to the div in the DOM
		this.div.appendChild(matterForm);
		
		// Email Address for application user
		var powerUserLabel = new TextLabel(matterForm, "powerUserLabel", "User Email ", 20, 30);
		var powerUser = new EntryField(matterForm, "powerUser", 20, 50);
		powerUser.entryField.style.backgroundColor = "cyan";

		// directory for logs
		var logFilesLabel = new TextLabel(matterForm, "logFilesLabel", "Logfiles Directory ", 20, 80);
		var logFiles = new EntryField(matterForm, "logFiles", 20, 100);
		logFiles.entryField.setAttribute("readonly","readonly");
		logFiles.entryField.style.backgroundColor = "cyan";

		
		// directory for config files
		var dataFilesLabel = new TextLabel(matterForm, "dataFilesLabel", "Datafiles Directory ", 20, 130);
		var dataFiles = new EntryField(matterForm, "dataFiles", 20, 150);
		dataFiles.entryField.setAttribute("readonly","readonly");
		dataFiles.entryField.style.backgroundColor = "cyan";

		// IP Address for SFTP Server
		var sftpIPLabel = new TextLabel(matterForm, "sftpIPLabel", "SFTP IP Address", 20, 180);
		var sftpIP = new EntryField(matterForm, "sftpIP", 20, 200);
		
		
		// SFTP Server Username
		var sftpUsernameLabel = new TextLabel(matterForm, "sftpUsernameLabel", "SFTP Username", 20, 230);
		var sftpUsername = new EntryField(matterForm, "sftpUsername", 20, 250);
		
		// Google Shared Drive
		var sharedDriveLabel = new TextLabel(matterForm, "sharedDriveLabel", "Shared Drive", 20, 280);
		var sharedDrive = new EntryField(matterForm, "sharedDrive", 20, 310);
		sharedDrive.entryField.setAttribute("readonly","readonly");
		sharedDrive.entryField.style.backgroundColor = "cyan";

		// # Export Queue Limit
		var exportQueueLimit = new TextLabel(matterForm, "exportQueueLimitLabel", "Export Queue Limit ", 320, 30);
		var exportQueueLimit = new EntryField(matterForm, "exportQueueLimit", 320, 50);
		exportQueueLimit.entryField.setAttribute("readonly","readonly");
		exportQueueLimit.entryField.style.backgroundColor = "cyan";

		// SFTP Password
		var sftpPassword = new TextLabel(matterForm, "sftpPasswordLabel", "SFTP Password", 320, 230);
		var sftpPassword = new EntryField(matterForm, "sftpPassword", 320, 250);
		sftpPassword.entryField.setAttribute('type','password');
		
		
		
		// initialize the form variables
		// from the configuration file
	
		var matter = new VaultMatter();			
		var settings_info = matter.getSettings();
		

		
	
	}
}
