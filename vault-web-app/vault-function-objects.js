

//
//	VaultFunctions
//


var VaultFunctions = function()
{
    this.info = "I am vault superclass";
    console.log("SuperClass:");
};



VaultFunctions.prototype.createOrgQueries = function(matterConfig)
{

	var matter = create_org_queries(matterConfig);
	
	return matter;
};

VaultFunctions.prototype.createQueries = function(matterConfig)
{

	var matter = create_queries(matterConfig);
	
	return matter;
};

VaultFunctions.prototype.getMatterByName = function(matter_name, options)
{

	var matter = get_matter_by_name(matter_name, options);
	
	return matter;
};

VaultFunctions.prototype.getMatter = function(matter_id)
{

	var matter = get_matter(matter_id);

	return matter;
};

VaultFunctions.prototype.createMatter = function(matter_config, options)
{

	var matter = create_matter(matter_config, options);
	
	return matter;
};

VaultFunctions.prototype.updateConfig = function(matter_id)
{
	
	var matter = update_config(matter_id);
	
	return matter;
};

VaultFunctions.prototype.count = function(matter_id, recipient)
{
	
	var matter = count_matter(matter_id, recipient);
	
	return matter;
};

VaultFunctions.prototype.sendEmail = function(matter_name, recipient)
{
	
	var matter = send_email(matter_name, recipient);
	
	return matter;
};

VaultFunctions.prototype.createExports = function(matter_id, recipient, exportType, queueSize)
{
	
	var matter = create_exports(matter_id, recipient, exportType, queueSize);
	
	return matter;
};


VaultFunctions.prototype.downloadExports = function(matter_id, recipient, options)
{
	
	var matter = create_downloads(matter_id, recipient, options);
	
	return matter;
};


VaultFunctions.prototype.updateSettings = function(parms)
{
	
	var settings = update_settings(parms);
	
	return settings;
};


VaultFunctions.prototype.getSettings = function()
{
	
	var settings = get_settings();
	
	return settings;
};

VaultFunctions.prototype.getOrgInfo = function()
{
	
	var orgInfo = get_orginfo();
	
	return orgInfo;
};




//
//	VaultMatter
//


var VaultMatter = function(){
	
	console.log("in VaultMatter constructor");
	
    VaultFunctions.call(this);
	
};

VaultMatter.prototype = Object.create(VaultFunctions.prototype);
VaultMatter.prototype.constructor = VaultMatter;



VaultMatter.prototype.createOrgQueries = function(matterDetails)
{
	response = Object.getPrototypeOf(VaultMatter.prototype).createOrgQueries.call(this, matterDetails);
	
	return response;
};



VaultMatter.prototype.createQueries = function(matterDetails)
{
	response = Object.getPrototypeOf(VaultMatter.prototype).createQueries.call(this, matterDetails);
	
	return response;
};


VaultMatter.prototype.getMatterByName = function(matter_name, options)
{

    matter = Object.getPrototypeOf(VaultMatter.prototype).getMatterByName.call(this, matter_name, options);
    
	return matter;
};


VaultMatter.prototype.createMatter = function(matter_config, options)
{
    matter_name = Object.getPrototypeOf(VaultMatter.prototype).createMatter.call(this, matter_config, options);
	
	return matter_name;
};


VaultMatter.prototype.getMatter = function(matter_id, matterDetailsText)
{
    matter_name = Object.getPrototypeOf(VaultMatter.prototype).getMatter.call(this, matter_id, matterDetailsText);
	
	return matter_name;
};


VaultMatter.prototype.create = function(matter_name)
{
    matter = Object.getPrototypeOf(VaultMatter.prototype).getMatter.call(this, matter_name, options);
	
	return matter_name;
};

VaultMatter.prototype.updateConfig = function(matter_id)
{
	// call superclass
    matter = Object.getPrototypeOf(VaultMatter.prototype).updateConfig.call(this, matter_id);
    
	return matter_name;
};

VaultMatter.prototype.count = function(matter_id, recipient)
{
	// call superclass
    matter = Object.getPrototypeOf(VaultMatter.prototype).count.call(this, matter_id, recipient);
    
	return matter;
};

VaultMatter.prototype.sendEmail = function(matter_name, recipient)
{
	// call superclass
    matter = Object.getPrototypeOf(VaultMatter.prototype).sendEmail.call(this, matter_name, recipient);
    
	return matter;
};

VaultMatter.prototype.createExports = function(matter_id, recipient, exportType, queueSize)
{
	// call superclass
    matter = Object.getPrototypeOf(VaultMatter.prototype).createExports.call(this, matter_id, recipient, exportType, queueSize);
    
	return matter;
};

VaultMatter.prototype.downloadExports = function(matter_id, recipient, options)
{
	// call superclass
    matter = Object.getPrototypeOf(VaultMatter.prototype).downloadExports.call(this, matter_id, recipient, options);
    
	return matter;
};

VaultMatter.prototype.updateSettings = function(parms)
{
	// call superclass
    settings = Object.getPrototypeOf(VaultMatter.prototype).updateSettings.call(this, parms);
    
	return settings;
};


VaultMatter.prototype.getSettings = function()
{
	// call superclass
    settings = Object.getPrototypeOf(VaultMatter.prototype).getSettings.call(this);
    
	return settings;
};

VaultMatter.prototype.getOrgInfo = function()
{
	// call superclass
    orgInfo = Object.getPrototypeOf(VaultMatter.prototype).getOrgInfo.call(this);
    
	return orgInfo;
};


