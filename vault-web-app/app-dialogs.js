


class OrgSelectDialog extends HelperDialog {
	constructor(element, action){
		
		super(element, action, orgFunction, 450,450);
		
		//var selectedOrgs = [];
		
		function orgFunction(){ 
		
		
		//alert("monitor current tasks");
		
		
		//console.log("listbox=",organizationsListBox.listBox);
		
		console.log("length=",organizationsListBox.listBox.options.length);
		
		var selectedOrgs = [];
		
		for (var i=0; i < organizationsListBox.listBox.options.length; i++){
			
			//console.log("entry=",organizationsListBox.listBox.options[i]);
			
			if(organizationsListBox.listBox.options[i].selected == true){
				
				console.log("value=", organizationsListBox.listBox.options[i].value);
				console.log("text=", organizationsListBox.listBox.options[i].text);
				selectedOrgs.push([organizationsListBox.listBox.options[i].value, organizationsListBox.listBox.options[i].text])
				
				}
		
			}
			
		console.log("selectedOrgs=", selectedOrgs);
		
		
		var selectOrgsList = document.getElementsByName("selectOrgsListBox");
		
		load_listbox(selectOrgsList, selectedOrgs);
		
		//console.log("this=", this);
		//$(this).destroy().remove();

		}
		
		
		// create a form
		var matterForm = document.createElement('form');
		matterForm.setAttribute('name', 'matterForm');

		// add to the div in the DOM
		this.div.appendChild(matterForm);
		
		// create list box
		var organizationsLabel = new TextLabel(matterForm, "organizationsLabel", "Organizations", 100, 20);
		var organizationsListBox = new ListBox(matterForm, "organizationsListBox", 100, 40);
		//var loadOrganizations = new PushButton(matterForm, "loadOrganizations", "Load Orgs", 100, 300, getOrgs);
		
				
		//function getOrgs(){

			//alert("get orgs");
			//var csvDialog = new CSVDialog(element,"CSV Action", custodiansListBox);
			
		var matter = new VaultMatter();
			
		var orgInfo = matter.getOrgInfo();
			
		console.log("orgInfo=", orgInfo);
			

			
		//}
		

		// matter info
		//var matterInfo = new TextInfo(matterForm, "matterInfo", "matter info...", 20, 40);
		
		// uploads info
		//var taskInfo = new TextInfo(matterForm, "taskInfo", "tasks info...", 350, 40);
		
	}
}






class TasksDialog extends AppDialog {
	constructor(element, action){
		
		function tasksFunction(){ alert("monitor current tasks")};
		
		super(element, action, tasksFunction, 450, 600);
		
		// create a form
		var matterForm = document.createElement('form');
		matterForm.setAttribute('name', 'matterForm');

		// add to the div in the DOM
		this.div.appendChild(matterForm);

		// matter info
		var matterInfo = new TextInfo(matterForm, "matterInfo", "matter info...", 20, 40);
		
		// uploads info
		var taskInfo = new TextInfo(matterForm, "taskInfo", "tasks info...", 350, 40);
		
	}
}

