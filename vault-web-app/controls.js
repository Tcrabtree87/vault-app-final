class ControlGroup {
		constructor(form, name, title, left, top) {
			
		// create a form
		//var controlGroupForm = document.createElement('form');
		//controlGroupForm.setAttribute('name', 'controlGroupForm');
		//$( controlGroupForm).css("width", 125);
		//$( controlGroupForm).css("height", 125);

		// create fieldset
		var fieldSet = document.createElement('fieldset');
		fieldSet.setAttribute('name', 'fieldSet');
		//fieldSet.setAttribute('class', 'checkall');
		fieldSet.setAttribute('data-role','controlgroup');
		fieldSet.setAttribute('class','controlgroup');

		//fieldSet.className = 'checkone';
		console.log("className=", fieldSet.className);
		
		
		var myRadioButton1 = new RadioButton(fieldSet, "myRadioButton", 50, 30);
		var myRadioButton2 = new RadioButton(fieldSet, "myRadioButton", 50, 50);
		var myRadioButton3 = new RadioButton(fieldSet, "myRadioButton", 50, 70);

		form.appendChild(fieldSet);

		$( fieldSet ).css("position" , "absolute");	
		$( fieldSet ).css("top" , top);	
		$( fieldSet ).css("left" , left);
		$( fieldSet).css("width", 125);
		$( fieldSet).css("height", 125);		
		
			
		}
}

class ParagraphInfo {
		constructor(form, name, title, left, top){
		// text info
		var text = document.createElement("p");
	
		text.setAttribute("name",name);
		text.innerHTML = title;
		text.style.fontWeight = "bold";
	
		$( text ).css("position" , "absolute");	
		$( text ).css("top" , top);	
		$( text ).css("left" , left);		
		

		form.appendChild(text);
			
		}
		
}


class AlertInfo {
		constructor(form, name, title, left, top){
		// text info
		var alert = document.createElement("p");
	
		alert.setAttribute("name",name);
		alert.innerHTML = title;
		alert.style.fontWeight = "bold";
	
		$( alert ).css("position" , "absolute");	
		$( alert ).css("top" , top);	
		$( alert ).css("left" , left);
		$( alert ).css("background-color" , 'lightgoldenrodyellow');
		//$(this).css('background-color', 'red'
		
		
		$( alert ).insertBefore('#btnSubmit');
		$( alert ).delay(3000);
		
		$( alert ).fadeOut(function() {
			$(this).remove(); 
		});
		
		//$(function() {
			//$('<div>Success</div>')
			//.insertBefore('#btnSubmit')
			//.delay(3000)
			//.fadeOut(function() {
			//$(this).remove(); 
			//});
			//});



		form.appendChild(alert);
			
		}
		
}


class TextInfo {
		constructor(form, name, title, left, top){
		// text info
		var text = document.createElement("Text");
	
		text.setAttribute("name",name);
		text.innerHTML = title;
		text.style.fontWeight = "bold";
	
		$( text ).css("position" , "absolute");	
		$( text ).css("top" , top);	
		$( text ).css("left" , left);		
		

		form.appendChild(text);
			
		}
		
}

class TextLabel {
		
		constructor(form, name, title, left, top){
		
		var label = document.createElement("Label");
	
		label.setAttribute("name",name);
		label.innerHTML = title;
		label.style.fontWeight = "bold";
	
		$( label ).css("position" , "absolute");	
		$( label ).css("top" , top);	
		$( label ).css("left" , left);		
		

		form.appendChild(label);
			
		}
		
}

class DateField {
	
		constructor(form, name, left, top){
			
		var entryField = document.createElement("input");
	
		entryField.setAttribute("name",name);
	
		$( entryField ).css("position" , "absolute");	
		$( entryField ).css("top" , top);	
		$( entryField ).css("left" , left);		
		
		 $( function() {
			$( entryField ).datepicker();
		} );
		

		form.appendChild(entryField);
			
		}

}






class CSVPicker {

		//<form id="myForm">
		//<input type="file" id="csvFile" accept=".csv" />
		//<br />
		//<input type="submit" value="Submit" />
		//</form>


		constructor(form, name, left, top){

		var csvField = document.createElement("input");
		this.csvField = csvField;
		csvField.type = "file";
		csvField.accept = ".csv";
	
		csvField.setAttribute("name",name);
	
		$( csvField ).css("position" , "absolute");	
		$( csvField ).css("top" , top);	
		$( csvField ).css("left" , left);		
		

		form.appendChild(csvField);
			
		}
		
}




		


class EntryField {
		constructor(form, name, left, top){


		var entryField = document.createElement("input");
		this.entryField = entryField;
	
		entryField.setAttribute("name",name);
	
		$( entryField ).css("position" , "absolute");	
		$( entryField ).css("top" , top);	
		$( entryField ).css("left" , left);		
		

		form.appendChild(entryField);
			
		}
		
}



class PushButton {
		constructor(form, name, title, left, top, myListner){
			
		var pushButton = document.createElement('button');
		pushButton.setAttribute("name", name);
		
		pushButton.innerText = title;
		pushButton.style.fontWeight = "bold";
		
		$( pushButton ).css("position" , "absolute");
		$( pushButton ).css("left" , left);
		$( pushButton ).css("top" , top);
		
		form.appendChild(pushButton);
		pushButton.addEventListener('click', (event) => {
						// When there is a "click"
						// it shows an alert in the browser
						//alert('In PushButton!')

						event.preventDefault();
						
						myListner();
						//console.log (pushButton);

					});

		}
		
}

class ListBox {
		constructor(form, name, left, top){
		// create a custodian listbox
		var listBox = document.createElement('select');
		// this will be needed to populate
		// this listbox from a .CSV file
		this.listBox = listBox;  
		listBox.setAttribute('name', name);
		listBox.setAttribute('size', '15');
		listBox.setAttribute('multiple', '');
		
		$( listBox ).css("position" , "absolute");
		$( listBox).css("left" , left);
		$( listBox ).css("top" , top);
		$( listBox).css("width", 225);
		
		// add to the div in the DOM
		form.appendChild(listBox);
			
		}
}

class RadioButton {
		constructor(form, name, left, top, myListner){
			
		this.radioButton = document.createElement('input');
		//var state = "off";
		
		//this.radioButton = radioButton;
		this.state = "off";
		
		
		this.radioButton.type = 'radio';
		this.radioButton.name = name;
		this.radioButton.id = 'id-' + name;
		
		this.radioButton.setAttribute("name", name);
		this.radioButton.style.fontWeight = "bold";
		
		$( this.radioButton ).css("position" , "absolute");
		$( this.radioButton ).css("left" , left);
		$( this.radioButton ).css("top" , top);
		
		//$( radioButton ).id = name;
	
		
		this.radioButton.addEventListener('click', () => {
											
					if(this.state == "off"){
						
						this.state = "on";
						this.radioButton.checked = true;
					}
					
					
					//event.preventDefault();
					myListner();
						
					});
					
										
		form.appendChild(this.radioButton);	
			
		}
}


class CheckBox {
		constructor(form, name, left, top){
			
			this.checkBox = document.createElement('input');
			
			this.checkBox.type = 'checkbox';
			//checkBox.title = "Query Names with Terms";
			this.checkBox.setAttribute("name", name);
			
			//checkBox.innerText = 'Create Query Names with Terms';
			this.checkBox.style.fontWeight = "bold";
			
			$( this.checkBox ).css("position" , "absolute");
			$( this.checkBox ).css("left" , left);
			$( this.checkBox ).css("top" , top);
			
			this.checkBox.addEventListener('click', () => {
							// When there is a "click"
							// it shows an alert in the browser
							console.log (this.checkBox.checked);
							//alert('checkBox!')
						});
						
											
			form.appendChild(this.checkBox);	
				
		};
		
		
		
}


