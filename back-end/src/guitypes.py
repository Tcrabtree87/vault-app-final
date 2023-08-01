# matter types

type_custodian 			= "custodian";
type_organization 		= "organization";
type_systemwide 		= "systemwide";
type_consolidated 		= "consolidated";

matter_state_created  	= "created"
matter_state_queries  	= "queries"
matter_state_counted  	= "counted"
matter_state_exported 	= "exported"
matter_state_downloaded = "downloaded"


# internal states during a download

downloadingFromVault    = 1
seperatingMBOX          = 2
uploadingToDrive        = 3
uploadingToSFTP         = 4 
downloadsFinished       = 5
noDownloads             = 6