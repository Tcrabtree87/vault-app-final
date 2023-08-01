
function load_listbox(listBox, list){

	// clear out the list box first
	// and indices are changed dynamically
	// somewhere in the DOM manager
	// as you remove items
	
	var options = listBox[0].getElementsByTagName('OPTION');
	
	while (options.length != 0){
		listBox[0].removeChild(options[0]);
	}
	
	for(var i=0; i < list.length; i++){
		let option = document.createElement("option");

		var entry = list[i]
		option.setAttribute('value', entry[0]);
		let optionText = document.createTextNode(entry[1]);
		option.appendChild(optionText);
		listBox[0].appendChild(option);
		
	};
	return
}