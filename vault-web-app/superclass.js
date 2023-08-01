var SuperClass = function()
{
    this.info = "I am superclass";
    console.log("SuperClass:");
};

SuperClass.prototype.printInfo = function()
{
    console.log("printing from superclass printInfo");
    console.log("printinfo");
    console.log(this.info);
};

var SubClass = function(){
    SuperClass.call(this);
};

SubClass.prototype = Object.create(SuperClass.prototype);
SubClass.prototype.constructor = SubClass;

SubClass.prototype.printInfo = function()
{
    console.log("calling superclass");
    Object.getPrototypeOf(SubClass.prototype).printInfo.call(this);
    console.log("called superclass");
};
