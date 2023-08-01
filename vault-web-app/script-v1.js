var timeOut;



class AppDialog {
	constructor(element){
		console.log(element.icon);
		this.div = document.createElement('div');
		this.dialog = document.createElement('dialog');
				
				
		$(this.div).dialog(this.dialog);
		$(this.div).dialog("option", "height", 450);
		$(this.div).dialog("option", "width", 600);
		$(this.div).css("background-color" ,"#64F592");
		
		$(this.div).dialog("option", "autoOpen", true);
		$(this.div).dialog("option", "draggable", true);
		$(this.div).dialog("option", "closeOnEscape", true);

		this.div.appendChild(this.dialog);
	
		$(this.div).prev(".ui-widget-header").css("background", "#5CD1FF");
		
		

	}
}

class CreateDialog extends AppDialog {
	constructor(element){
	super(element);
				
		
	// create label
				
	var matterIdLabel = document.createElement("Label");
	
	matterIdLabel.setAttribute("matterIdLabel",matterIdLabel);
	matterIdLabel.innerHTML = "Matter ID";
	matterIdLabel.style.fontWeight = "bold";
	
	$( matterIdLabel ).css("position" , "relative");
	//
	$( matterIdLabel ).css("left" , 10);
	$( matterIdLabel ).css("top" , 10);
	
	this.div.appendChild(matterIdLabel);
	
	// create entry field
	var matterId = document.createElement("INPUT");
	
	matterId.setAttribute("type", "text");
	matterId.setAttribute("name", "matterId");
	$( matterId ).css("position" , "relative");
	$( matterId ).css("left" , 50);
	$( matterId ).css("top" , 10);
	
	
	
	this.div.appendChild(matterId);
	
	// create text output
				
				
	var matterInfo = document.createElement('text');
	matterInfo.innerText = 'matter details...';
	matterInfo.setAttribute("name", "matterInfo");
	$( matterInfo ).css("position" , "relative");
	$( matterInfo ).css("right" , 90);
	$( matterInfo ).css("top" , 40);
	

	this.div.appendChild(matterInfo);

	// create new Get Matter button
				
	var getMatter = document.createElement('button');
	getMatter.innerText = 'Get Matter';
	getMatter.style.fontWeight = "bold";

	$( getMatter ).css("position" , "relative");
	$( getMatter ).css("right" , 360);
	$( getMatter ).css("top" , 40);
	
	this.div.appendChild(getMatter);
	
	getMatter.addEventListener('click', () => {
					// When there is a "click"
					// it shows an alert in the browser
					console.log (getMatter);
					alert('Get Matter!')
				});
				

	// create new Create Matter button
				
	var createMatter = document.createElement('button');
	createMatter.innerText = 'Create Matter';
	createMatter.style.fontWeight = "bold";

	$( createMatter ).css("position" , "relative");
	$( createMatter ).css("right" , 10);
	$( createMatter ).css("bottom" , 180);
	
	createMatter.addEventListener('click', () => {
					// When there is a "click"
					// it shows an alert in the browser
					console.log (createMatter);
					alert('Create Matter!')
				});
				
									
	this.div.appendChild(createMatter);		

	// create label for listbox
				
	var listLabel = document.createElement("Label");
	listLabel.setAttribute("listLabel",listLabel);
	listLabel.innerHTML = "Custodians";
	listLabel.style.fontWeight = "bold";
	

	$( listLabel ).css("position" , "relative");
	$( listLabel ).css("left" , 280);
	$( listLabel ).css("bottom" , 250);

	this.div.appendChild(listLabel);


	// create a listbox
	var custodianList = document.createElement('select');
	custodianList.setAttribute('name', 'custodianList');
	custodianList.setAttribute('size', '15');
	custodianList.setAttribute('multiple', '');
	
	$( custodianList ).css("position" , "relative");
	$( custodianList ).css("left" , 200);
	$( custodianList ).css("top" , 20);
	//$( custodianList ).css("top" , 20);


	// add to the div in the DOM
	this.div.appendChild(custodianList);
	
	const opt1 = document.createElement("option");
	const opt2 = document.createElement("option");
	
	opt1.value = "1";
	opt1.text = "Jane Doe";

	opt2.value = "2";
	opt2.text = "John Lee";
	
	for (var i=0; i < 25; i++) {
		const opt = document.createElement("option");
		opt.value = i; //"1";
		opt.text = "Jane Doe";
		custodianList.add(opt, null);
		//custodianList.add(opt2, null);
	
		}
				
				
	// create a form
	var matterForm = document.createElement('form');
	matterForm.setAttribute('name', 'matterForm');
		// add to the div in the DOM
	this.div.appendChild(matterForm);
	
	
	}
	
	createControls() {

	console.log("test");
    
    }
	
				
	
}

class Item {
    constructor(icon, backgroundColor) {
        this.$element = $(document.createElement("div"));
        this.icon = icon;
        this.$element.addClass("item");
        this.$element.css("background-color", backgroundColor);
        var i = document.createElement("i");
        $(i).addClass("fi-" + icon);
        this.$element.append(i);
        this.prev = null;
        this.next = null;
        this.isMoving = false;
        var element = this;
		
		this.$element.on("dblclick", function() {
			
			//alert("mousedown");
			console.log("dblclick");
			//console.log(menu);
			//console.log(this);
			//console.log(element);
			
			if(element.icon == "upload") {
				console.log(element.icon);
				
				var div = document.createElement('div');


				
				// create label
				
				var matterIdLabel = document.createElement("Label");
				matterIdLabel.setAttribute("matterIdLabel",matterIdLabel);
				matterIdLabel.innerHTML = "Matter ID";
				matterIdLabel.style.fontWeight = "bold";

				$( matterIdLabel ).css("position" , "relative");
				$( matterIdLabel ).css("left" , 20);
				$( matterIdLabel ).css("bottom" , 240);
				
				
				div.appendChild(matterIdLabel);
				
				
				
				// create entry field
				var matterId = document.createElement("INPUT");
				
				matterId.setAttribute("type", "text");
				matterId.setAttribute("name", "matterId");
				$( matterId ).css("position" , "relative");
				$( matterId ).css("left" , 50);
				$( matterId ).css("bottom" , 240);
				
				
				
				div.appendChild(matterId);


				
				// create new Get Matter button
				
				var getMatter = document.createElement('button');
				getMatter.innerText = 'Get Matter';
				getMatter.style.fontWeight = "bold";

				$( getMatter ).css("position" , "relative");
				$( getMatter ).css("right" , 235);
				$( getMatter ).css("bottom" , 210);
				
				
												
				div.appendChild(getMatter);
				
				getMatter.addEventListener('click', () => {
					// When there is a "click"
					// it shows an alert in the browser
					console.log (getMatter);
					alert('Get Matter!')
				});
				

				// create new Create Matter button
				
				var createMatter = document.createElement('button');
				createMatter.innerText = 'Create Matter';
				createMatter.style.fontWeight = "bold";

				$( createMatter ).css("position" , "relative");
				$( createMatter ).css("right" , 350);
				$( createMatter ).css("bottom" , 180);
				
				
												
				div.appendChild(createMatter);
				
				createMatter.addEventListener('click', () => {
					// When there is a "click"
					// it shows an alert in the browser
					console.log (createMatter);
					alert('Create Matter!')
				});
				


				
				// create text output
				
				
				var matterInfo = document.createElement('text');
				matterInfo.innerText = 'matter details...';
				matterInfo.setAttribute("name", "matterInfo");
				$( matterInfo ).css("position" , "relative");
				$( matterInfo ).css("right" , 200);
				$( matterInfo ).css("bottom" , 210);
				

				div.appendChild(matterInfo);
				
				//var id = document.getElementById("#matterInfo");
				//console.log("id=", id);

				$( matterInfo ).css("background" , "#ffffff");


				// create label for listbox
				
				var listLabel = document.createElement("Label");
				listLabel.setAttribute("listLabel",listLabel);
				listLabel.innerHTML = "Custodians";
				listLabel.style.fontWeight = "bold";
				div.appendChild(listLabel);

				$( listLabel ).css("position" , "relative");
				$( listLabel ).css("right" , 30);
				$( listLabel ).css("bottom" , 240);


				// create a listbox
				var custodianList = document.createElement('select');
				custodianList.setAttribute('name', 'custodianList');
				custodianList.setAttribute('size', '15');
				custodianList.setAttribute('multiple', '');
				
				$( custodianList ).css("position" , "relative");
				$( custodianList ).css("right" , 110);
				//$( custodianList ).css("bottom" , 10);
				$( custodianList ).css("top" , 20);


				// add to the div in the DOM
				div.appendChild(custodianList);
				
				const opt1 = document.createElement("option");
				const opt2 = document.createElement("option");
				
				opt1.value = "1";
				opt1.text = "Jane Doe";

				opt2.value = "2";
				opt2.text = "John Lee";
				
				for (i=0; i < 25; i++) {
					const opt = document.createElement("option");
					opt.value = i; //"1";
					opt.text = "Jane Doe";
					custodianList.add(opt, null);
					//custodianList.add(opt2, null);
				
				}
				
				


				//var id = $("#matterInfo");
				//console.log("id=", id);
				// note - div and this, and id are null until dialog loads..., 
				// not sure why

				
										
				$( div ).css("background-color" ,"#64F592");
				

				
				var dialog = $(div).dialog(
					{
					autoOpen: true,
					draggable : true,
					title: "Get Matter",	
					//class: "ui-shadow ui-btn ui-corner-all ui-btn-inline",
					//class: "ui-shadow ui-corner-all",
					//dialogClass: "no-close",
					height : 450,
					width : 800,
					closeOnEscape: false,
					
					buttons: {
                GetSize:{ 
                    class: 'leftButton',
                    text: 'Get Size',
					style:"margin-right:150px",
					position : "absolute",
                    click : function (){
                        alert('get size');
                    }
                },
				    GetCount:{ 
                    class: 'leftButton',
                    text: 'Get Count',
					style:"margin-right:50px",
					position : "absolute",
                    click : function (){
                        alert('get count');
                    }
                }
                
            } // buttons
				  
					
			}); // dialog

			$( div ).prev(".ui-widget-header").css("background", "#5CD1FF");
			
			console.log(dialog)
	

			} // if upload
				
				
			if(element.icon == "page-export-doc") {
				console.log(element.icon);
				}
				
			if(element.icon == "zoom-in") {
				
				var createDialog = new CreateDialog(element);
				
				}
				
			if(element.icon == "target") {
				console.log(element.icon);
				}
			
			if(element.icon == "page-csv") {
				console.log(element.icon);
				}
			
			
			
		});
		
        this.$element.on("mousemove", function() {
            clearTimeout(timeOut);
            timeOut = setTimeout(function() {
                if (element.next && element.isMoving) {
                    element.next.moveTo(element);
                } 
            }, 10);
        });
    }
    
    moveTo(item) {
        anime({
            targets: this.$element[0],
            left: item.$element.css("left"),
            top: item.$element.css("top"),
            duration: 700,
            elasticity: 500
        });
        if (this.next) {
            this.next.moveTo(item);
        }
    }

    updatePosition() {    
        anime({
            targets: this.$element[0],
            left: this.prev.$element.css("left"),
            top: this.prev.$element.css("top"),
            duration: 80
        });
        
        if (this.next) {
            this.next.updatePosition();
        }
    }
}

class Menu {
    constructor(menu) {
        this.$element = $(menu);
        this.size = 0;
        this.first = null;
        this.last = null;
        this.timeOut = null;
        this.hasMoved = false;
        this.status = "closed";
    }
    
    add(item) {
        var menu = this;
        if (this.first == null) {
            this.first = item;
            this.last = item;
            this.first.$element.on("mouseup", function() {
                if (menu.first.isMoving) {
                    menu.first.isMoving = false;        
                } else {
                    menu.click();
                }
            }); 
            item.$element.draggable(
                {
                    start: function() {
                        menu.close();
                        item.isMoving = true;
                    }  
                },
                {
                    drag: function() {
                        if (item.next) {
                            item.next.updatePosition();
                        }
                    }
                },
                {
                    stop: function() {
                        item.isMoving = false;
                        item.next.moveTo(item);
                    }
                }
            );
        } else {
            this.last.next = item;
            item.prev = this.last;
            this.last = item;
        }
        this.$element.after(item.$element);
        
        
    }
    
    open() {
        this.status = "open";
        var current = this.first.next;
        var iterator = 1;
        var head = this.first;
        var sens = head.$element.css("left") < head.$element.css("right") ? 1 : -1;
        while (current != null) {
            anime({
                targets: current.$element[0],
                left: parseInt(head.$element.css("left"), 10) + (sens * (iterator * 50)),
                top: head.$element.css("top"),
                duration: 500
            });
            iterator++;
            current = current.next;
        }    
    }
    
    close() {
        this.status = "closed";
        var current = this.first.next;
        var head = this.first;
        var iterator = 1;
        while (current != null) {
            anime({
                targets: current.$element[0],
                left: head.$element.css("left"),
                top: head.$element.css("top"),
                duration: 500
            });
            iterator++;
            current = current.next;
        }
    }
    
    click() {
        if (this.status == "closed") {
            this.open();
        } else {
            this.close();
        }
    }
    
}

var menu = new Menu("#myMenu");
var item1 = new Item("list");
var item2 = new Item("target", "#5CD1FF");
var item3 = new Item("zoom-in", "#64F592");
var item4 = new Item("page-export-doc", "#FF5C5C");
var item5 = new Item("upload", "#FFF15C");
var item6 = new Item("page-csv", "#9acd32");



menu.add(item1);
menu.add(item2);
menu.add(item3);
menu.add(item4);
menu.add(item5);
menu.add(item6);



$(document).delay(50).queue(function(next) {
    menu.open();
    next();
    $(document).delay(1000).queue(function(next) {
        menu.close();
        next();
    });
});