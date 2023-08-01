


class HelperDialog {
	constructor(element, action, appFunction, height, width){
		console.log(element.icon);
		this.div = document.createElement('div');
		this.dialog = document.createElement('dialog');
				
		// default height, 450.  default width, 600		
		$(this.div).dialog(this.dialog);
		$(this.div).dialog("option", "height", height);
		$(this.div).dialog("option", "width", width);
		
		this.dialog.setAttribute('name', 'matterDialog');
		
		$(this.div).css("background-color" ,"#64F592");
		
		$(this.div).dialog("option", "autoOpen", true);
		$(this.div).dialog("option", "draggable", true);
		$(this.div).dialog("option", "resizeable", false);
		$(this.div).dialog("option", "closeOnEscape", true);
		
		var dialogButtons = {
				CreateQueries:{ 
                    class: 'leftButton',
                    text: action,
					style:"margin-right:250px",
					position : "absolute",
                    click : function  (){
                        //alert(action);
						appFunction();
						$(this).dialog('destroy');
                    }
                },
				Cancel:{ 
                    class: 'leftButton',
                    text: 'Close',
					style:"margin-right:50px",
					position : "absolute",
                    click : function (){
                        //alert('Cancel');

						$(this).dialog('destroy');
						console.log(this);
                    }
				}
			}
			
		this.dialogButtons = dialogButtons;
		
		$( this.dialog).resizable({ disabled: true }); //doesnt work

		$(this.div).dialog("option", "buttons", this.dialogButtons);
		
		this.div.appendChild(this.dialog);
	
		$(this.div).prev(".ui-widget-header").css("background", "#5CD1FF");
		$(this.div).prev(".ui-widget-header").hide();
		//$(this.div).prev(".ui-widget-header").css("background", "#5CD1FF");
		//$(this.div).dialog('option', 'dialogClass', 'noTitleStuff');

	}

};


class LittleDialog {
	constructor(element, action, height, width){
		console.log(element.icon);
		this.div = document.createElement('div');
		this.dialog = document.createElement('dialog');
				
		// default height, 450.  default width, 600		
		$(this.div).dialog(this.dialog);
		$(this.div).dialog("option", "height", height);
		$(this.div).dialog("option", "width", width);
		
		this.dialog.setAttribute('name', 'littleDialog');
		
		$(this.div).css("background-color" ,"#64F592");
		
		$(this.div).dialog("option", "autoOpen", true);
		$(this.div).dialog("option", "draggable", true);
		$(this.div).dialog("option", "resizeable", false);
		$(this.div).dialog("option", "closeOnEscape", true);
		
		$( this.dialog).resizable({ disabled: true }); //doesnt work
		
		this.div.appendChild(this.dialog);
	
		$(this.div).prev(".ui-widget-header").css("background", "#5CD1FF");
		//$(this.div).prev(".ui-widget-header").hide();
		//$(this.div).prev(".ui-widget-header").css("background", "#5CD1FF");
		//$(this.div).dialog('option', 'dialogClass', 'noTitleStuff');

	};
};

class CSVDialog extends HelperDialog {
	constructor(element, action, box){

			//constructor(element, action, appFunction, height, width){

		var listBox = box.listBox;
		
		super(element, action, csvFunction, 200, 500);
		
		// create a form
		var dialogForm = document.createElement('form');
		dialogForm.setAttribute('name', 'dialogForm');
		// add to the div in the DOM
		this.div.appendChild(dialogForm);
		
		// create CSV Picker
		var myCSVPicker = new CSVPicker(dialogForm, "myCSVPicker", 20, 20);
		
		// OK Button
		//var okButton = new PushButton(dialogForm, "OK", "OK",20, 50, csvFunction);
	
		// Cancel Button
		//var cancelButton = new PushButton(dialogForm, "Cancel", "Cancel",100, 50, cancelFunction);
		
		async function csvFunction(){ 
		
						
						
						const input = myCSVPicker.csvField.files[0];
						console.log("filename=", myCSVPicker.csvField.files[0]);
						const reader = new FileReader();
						reader.onload = function (e) {
							const text = e.target.result;
						
							//console.log("listBox=", listBox);
							//console.log("listBox.name=",listBox.name);
						
							var lines = text.split("\n");
							
							//this.lines = lines;	
							
							
							//clearList(listBox.name);
							var options = listBox.getElementsByTagName('OPTION');
							var length = options.length;
							console.log("length=", length);
							
							// clear out the list box first
							// funky, i know but other methods
							// didnt work becuse the list length 
							// and indices are changed dynamically
							// somewhere in the DOM manager
							// as you remove items
							while (options.length != 0){
								listBox.removeChild(options[0]);
							}
						
							for(var i=0; i < lines.length; i++){
								console.log(lines[i]);
								//console.log(lines[i].replace(/(""")/g, '"'));
								let temp = lines[i].replace(/(""")/g, '"');
								let line = temp.split(',');
								console.log(line);
								let option = document.createElement("option");
								option.setAttribute('value', line[1]);
								let optionText = document.createTextNode(line[0]);
								option.appendChild(optionText);
								listBox.appendChild(option);
								
							};

						};
						
						reader.readAsText(input);
								
						};

		// TODO: need to make this just close the .CSV window
		function cancelFunction(){ 

						console.log("$('littleDialog')=",$('littleDialog'));
						console.log("$(this)=",$(this));
						
						// these work but don't do the right thing
						//dialogForm.remove();
						//window.parent.$('.ui-dialog-content:visible').dialog('close');
								
						};
		
	}
	
}

class AppDialog {
	constructor(element, action, appFunction, height, width){
		console.log(element.icon);
		this.div = document.createElement('div');
		this.dialog = document.createElement('dialog');
				
		// default height, 450.  default width, 600		
		$(this.div).dialog(this.dialog);
		$(this.div).dialog("option", "height", height);
		$(this.div).dialog("option", "width", width);
		
		this.dialog.setAttribute('name', 'matterDialog');
		
		$(this.div).css("background-color" ,"#64F592");
		
		$(this.div).dialog("option", "autoOpen", true);
		$(this.div).dialog("option", "draggable", true);
		$(this.div).dialog("option", "resizeable", false);
		$(this.div).dialog("option", "closeOnEscape", true);
		
		var dialogButtons = {
				CreateQueries:{ 
                    class: 'leftButton',
                    text: action,
					style:"margin-right:250px",
					position : "absolute",
                    click : function  (){
                        //alert(action);
						appFunction();
                    }
                },
				Cancel:{ 
                    class: 'leftButton',
                    text: 'Close',
					style:"margin-right:50px",
					position : "absolute",
                    click : function (){
                        //alert('Cancel');

						$(this).dialog('destroy');
						console.log(this);
                    }
				}
			}
			
		this.dialogButtons = dialogButtons;
		
		$( this.dialog).resizable({ disabled: true }); //doesnt work

		$(this.div).dialog("option", "buttons", this.dialogButtons);
		
		this.div.appendChild(this.dialog);
	
		$(this.div).prev(".ui-widget-header").css("background", "#5CD1FF");
		$(this.div).prev(".ui-widget-header").hide();
		//$(this.div).prev(".ui-widget-header").css("background", "#5CD1FF");
		//$(this.div).dialog('option', 'dialogClass', 'noTitleStuff');

	}

};

