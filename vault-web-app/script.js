
//$.getScript("controls.js"); //, function() {
//   alert("Script loaded but not necessarily executed.");
//});

//jQuery.getScript( url [, success ] )
//jQuery.getScript( "controls.js" );
//<script src="controls.js"> 

//$.getScript( "controls.js", function( data, textStatus, jqxhr ) {
//  console.log( data ); // Data returned
//  console.log( textStatus ); // Success
//  console.log( jqxhr.status ); // 200
//  console.log( "Load was performed." );
//});

//var timeOut;






class SampleDialog extends AppDialog {
	constructor(element, action){

		function sampleFunction(){ 
						alert("perform sample function");

								
						};
		
		super(element, action, sampleFunction);
		
		// create a form
		var matterForm = document.createElement('form');
		matterForm.setAttribute('name', 'matterForm');
		// add to the div in the DOM
		this.div.appendChild(matterForm);
	
		// create a Label
		var myLabel = new TextLabel(matterForm, "myLabel", "myLabel", 50, 50);
		// create entry field
		var myEntryField = new EntryField(matterForm, "myEntryField", 50, 75);
		// create a Label
		var dateLabel = new TextLabel(matterForm, "dateLabel", "Date Field", 50, 100);
		
		// create date picker
		var myDateField = new DateField(matterForm, "myEntryField", 50, 125);
		
		// create push button
		
		function myListner(){
			alert("myListner");
			
			
			};
		
		var myPushButton = new PushButton(matterForm, "myPushButton", "myPushButton", 50, 150, myListner);
		
		
		// create list box
		var myListBox = new ListBox(matterForm, "myEntryField", 300, 50);
		// create check box
		var myListBox = new CheckBox(matterForm, "myEntryCheckbox", 50, 200);
		// create date picker
		
		// sample text
		var myTextInfo = new TextInfo(matterForm, "myText", "myText", 80, 200);
		
		// sample control group
		//var myContainer = new ControlGroup(matterForm, "myContainer", "myContainer", 50, 230);
		//$(myContainer).controlgroup( "option", "type", "vertical") ;
		
		var myRadioButton1 = new RadioButton(matterForm, "myRadioButton", 100, 230);
		var myRadioButton2 = new RadioButton(matterForm, "myRadioButton", 100, 250);
		var myRadioButton3 = new RadioButton(matterForm, "myRadioButton", 100, 270);

		
		
	}
	
}

