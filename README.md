[comment]: # "Auto-generated SOAR connector documentation"
# BMC Remedy

Publisher: Splunk  
Connector Version: 2.1.1  
Product Vendor: BMC Software  
Product Name: BMC Remedy  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.3.5  

This app supports ticket management functions on incidents in BMC Remedy

[comment]: # " File: README.md"
[comment]: # ""
[comment]: # "  Copyright (c) 2017-2022 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "  you may not use this file except in compliance with the License."
[comment]: # "  You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "      http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "  Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "  the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "  either express or implied. See the License for the specific language governing permissions"
[comment]: # "  and limitations under the License."
[comment]: # ""
Incidents are typically categorized among following types:

-   **User Service Restoration**
    -   Typical ITIL (Information Technology Infrastructure Library) of incident.
-   **User Service Request**
    -   Used to identify incidents that are not related to ITIL definition.
-   **Infrastructure Restoration**
    -   ITIL definition, but more focused on CI (Configuration Item) restoration.
-   **Infrastructure Event**
    -   Used for integration for system management tools.

## Playbook Backward Compatibility

-   A new action parameter has been added in the existing action. Hence, it is requested to the
    end-user to please update their existing playbooks by re-inserting | modifying | deleting the
    corresponding action blocks.

      

    -   A 'offset' action parameter has been added in the 'list tickets' action

-   The existing output data paths have been modified for the 'list tickets' action. Hence, it is
    requested to the end-user to please update their existing playbooks by re-inserting | modifying
    | deleting the corresponding action blocks to ensure the correct functioning of the playbooks
    created on the earlier versions of the app.

## Using a template for the create ticket action

In order to create a ticket from a pre-existing incident template in BMC remedy, the **fields**
action parameter can be used. Passing in a JSON such as,

    {"TemplateID": "$templateid"}

Referencing an existing template id simplifies the ticket creation. For more information refer this
[document](https://docs.bmc.com/docs/bsr/35/creating-incidents-by-passing-a-template-reference-576950232.html#Creatingincidentsbypassingatemplatereference-instance_id)
.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a BMC Remedy asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**url** |  required  | string | Complete URL (e.g. http://mybmc.contoso.com:8008)
**verify_server_cert** |  optional  | boolean | Verify server certificate
**username** |  required  | string | Username
**password** |  required  | password | Password

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied credentials  
[create ticket](#action-create-ticket) - Create incident  
[update ticket](#action-update-ticket) - Update an existing incident  
[get ticket](#action-get-ticket) - Get incident information  
[list tickets](#action-list-tickets) - Get list of incidents  
[set status](#action-set-status) - Set incident status  
[add comment](#action-add-comment) - Add work log information to the incident  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied credentials

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'create ticket'
Create incident

Type: **generic**  
Read only: **False**

Typically the following parameters are required, but this can be configured, therefore the action defines all parameters as optional and relies on the installation to validate the required parameters:<ul><li><b>first_name</b></li><li><b>last_name</b></li><li><b>description</b></li><li><b>reported_source</b></li><li><b>service_type</b></li></ul>If field value is provided individually as well as in <b>fields</b> parameter, then value in <b>fields</b> parameter will be used for creating the incident. For example, to create an incident using <b>fields</b> parameter and assign it to an assignee named User, set the <b>fields</b> parameter to {"First_Name": "Customer First Name", "Last_Name": "Customer Last Name", "Description": "Incident Description", "Service_Type": "User Service Restoration", "Reported Source": "Direct Input", "Status": "Assigned", "Assignee Login ID": "User", "Assignee": "User Name"}<br><b>Note:</b> Only single JSON formatted dictionary is allowed in <b>fields</b> action parameter<br>To add comment set <b>fields</b> parameter to {"Work Log Type": "General Information", "Detailed Description": "Comment to add"}.<br>To create an incident, <b>first_name</b> and <b>last_name</b> are those of the customer that exists in the system.<br>The <b>vault_id</b> parameter takes the vault ID of a file and attaches it to the incident.<br>The attachment should be placed in vault of the container from which the action will be executed, and it would appear in <b>Work Detail</b> section on BMC Remedy.<br>Typical (default installation) values for <b>impact</b> are:<ul><li>1-Extensive/Widespread</li><li>2-Significant/Large</li><li>3-Moderate/Limited</li><li>4-Minor/Localized</li></ul>Typical (default installation) values for <b>urgency</b> are:<ul><li>1-Critical</li><li>2-High</li><li>3-Medium</li><li>4-Low</li></ul>Typical (default installation) values for <b>status</b> are:<ul><li>New</li><li>Assigned</li><li>In Progress</li><li>Pending</li><li>Resolved</li><li>Closed</li><li>Cancelled</li></ul>Typical (default installation) values for <b>reported_source</b> are:<ul><li>Direct Input</li><li>Email</li><li>External Escalation</li><li>Fax</li><li>Self Service</li><li>Systems Management</li><li>Phone</li><li>Voice Mail</li><li>Walk In</li><li>Web</li><li>Other</li><li>BMC Impact Manager Event</li></ul>Typical (default installation) values for <b>service_type</b> are:<ul><li>User Service Restoration</li><li>User Service Request</li><li>Infrastructure Restoration</li><li>Infrastructure Event</li></ul>Typical (default installation) values for <b>work_info_type</b> are:<ul><li>Customer Inbound:<ul><li>Customer Communication</li><li>Customer Follow-up</li><li>Customer Status Update</li></ul></li><li>Customer Outbound<ul><li>Closure Follow Up</li><li>Detail Clarification</li><li>General Information</li><li>Resolution Communications</li><li>Satisfaction Survey</li><li>Status Update</li></ul></li><li>General<ul><li>Incident Task / Action</li><li>Problem Script</li><li>Working Log</li><li>Email System</li><li>Paging System</li><li>BMC Impact Manager Update</li><li>Chat</li></ul></li><li>Vendor<ul><li>Vendor Communication</li></ul></li></ul>Typical (default installation) values of <b>status_reason</b> for a given <b>status</b> are:<ul><li>Pending<ul><li>Automated Resolution Reported</li><li>Client Action Required</li><li>Client Hold</li><li>Future Enhancement</li><li>Infrastructure Change</li><li>Local Site Action Required</li><li>Monitoring Incident</li><li>Purchase Order Approval</li><li>Registration Approval</li><li>Request</li><li>Supplier Delivery</li><li>Support Contact Hold</li><li>Third Party Vendor Action Reqd</li></ul></li><li>Resolved<ul><li>Automated Resolution Reported</li><li>Customer Follow-Up Required</li><li>Future Enhancement</li><li>Monitoring Incident</li><li>No Further Action Required</li><li>Temporary Corrective Action</li></ul></li><li>Closed<ul><li>Automated Resolution Reported</li><li>Infrastructure Change Created</li></ul></li><li>Cancelled<ul><li>No longer a Causal CI</li></ul></li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**first_name** |  optional  | Customer First Name | string |  `bmcremedy first name` 
**last_name** |  optional  | Customer Last Name | string |  `bmcremedy last name` 
**description** |  optional  | Summary | string | 
**impact** |  optional  | Impact | string | 
**urgency** |  optional  | Urgency | string | 
**status** |  optional  | Status | string | 
**reported_source** |  optional  | Reported Source | string | 
**service_type** |  optional  | Incident Type | string | 
**work_info_type** |  optional  | Work Info Type | string | 
**status_reason** |  optional  | Status Reason | string | 
**fields** |  optional  | Fields (JSON format) | string | 
**vault_id** |  optional  | Comma (,) separated vault ID (maximum 3) | string |  `vault id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.description | string |  |   Description 
action_result.parameter.fields | string |  |   {"First_Name": "Customer First Name", "Last_Name": "Customer Last Name", "Description": "Incident Description", "Service_Type": "User Service Restoration", "Reported Source": "Direct Input", "Status": "Assigned", "Assignee Login ID": "User", "Assignee": "User Name"}<br>To add comment set <b>fields</b> parameter to {"Work Log Type": "General Information", "Detailed Description": "Comment to add"} 
action_result.parameter.first_name | string |  `bmcremedy first name`  |  
action_result.parameter.impact | string |  |   4-Minor/Localized 
action_result.parameter.last_name | string |  `bmcremedy last name`  |  
action_result.parameter.reported_source | string |  |   Direct Input 
action_result.parameter.service_type | string |  |   User Service Restoration 
action_result.parameter.status | string |  |   New 
action_result.parameter.status_reason | string |  |   Status Reason 
action_result.parameter.urgency | string |  |   1-Critical 
action_result.parameter.vault_id | string |  `vault id`  |   d766846c37a473ce02fc71e4fa9d471c3a715727 
action_result.parameter.work_info_type | string |  |   General Information 
action_result.data.\*._links.self.\*.href | string |  |  
action_result.data.\*.values.AccessMode | string |  |  
action_result.data.\*.values.AppInstanceServer | string |  |  
action_result.data.\*.values.AppInterfaceForm | string |  |  
action_result.data.\*.values.AppLogin | string |  |  
action_result.data.\*.values.AppPassword | string |  |  
action_result.data.\*.values.ApplyTemplate | string |  |  
action_result.data.\*.values.Area Business | string |  |  
action_result.data.\*.values.Assigned Group | string |  |  
action_result.data.\*.values.Assigned Group ID | string |  |  
action_result.data.\*.values.Assigned Group Shift Name | string |  |  
action_result.data.\*.values.Assigned Support Company | string |  |  
action_result.data.\*.values.Assigned Support Organization | string |  |  
action_result.data.\*.values.Assigned To | string |  |  
action_result.data.\*.values.Assignee | string |  |  
action_result.data.\*.values.Assignee Groups | string |  |  
action_result.data.\*.values.Assignee Groups_parent | string |  |  
action_result.data.\*.values.Assignee Login ID | string |  |  
action_result.data.\*.values.Auto Open Session | string |  |  
action_result.data.\*.values.BiiARS_01 | string |  |  
action_result.data.\*.values.BiiARS_02 | string |  |  
action_result.data.\*.values.BiiARS_03 | string |  |  
action_result.data.\*.values.BiiARS_04 | string |  |  
action_result.data.\*.values.BiiARS_05 | string |  |  
action_result.data.\*.values.Broker Vendor Name | string |  |  
action_result.data.\*.values.CC Business | string |  |  
action_result.data.\*.values.CI Name | string |  |  
action_result.data.\*.values.Categorization Tier 1 | string |  |  
action_result.data.\*.values.Categorization Tier 2 | string |  |  
action_result.data.\*.values.Categorization Tier 3 | string |  |  
action_result.data.\*.values.Chat Session ID | string |  |  
action_result.data.\*.values.Client Sensitivity | string |  |  
action_result.data.\*.values.Client Type | string |  |  
action_result.data.\*.values.ClientLocale | string |  |  
action_result.data.\*.values.Closure Manufacturer | string |  |  
action_result.data.\*.values.Closure Product Category Tier1 | string |  |  
action_result.data.\*.values.Closure Product Category Tier2 | string |  |  
action_result.data.\*.values.Closure Product Category Tier3 | string |  |  
action_result.data.\*.values.Closure Product Model/Version | string |  |  
action_result.data.\*.values.Closure Product Name | string |  |  
action_result.data.\*.values.Company | string |  |  
action_result.data.\*.values.Component_ID | string |  |  
action_result.data.\*.values.Contact Login Id | string |  |  
action_result.data.\*.values.Contact_Company | string |  |  
action_result.data.\*.values.Corporate ID | string |  |  
action_result.data.\*.values.Create Date | string |  |  
action_result.data.\*.values.Created_By | string |  |  
action_result.data.\*.values.Created_From_flag | string |  |  
action_result.data.\*.values.DataTags | string |  |  
action_result.data.\*.values.DatasetId | string |  |  
action_result.data.\*.values.Default City | string |  |  
action_result.data.\*.values.Default Country | string |  |  
action_result.data.\*.values.Department | string |  |  
action_result.data.\*.values.Description | string |  |  
action_result.data.\*.values.Desk Location | string |  |  
action_result.data.\*.values.Detailed_Decription | string |  |  
action_result.data.\*.values.Direct Contact Area Code | string |  |  
action_result.data.\*.values.Direct Contact City | string |  |  
action_result.data.\*.values.Direct Contact Company | string |  |  
action_result.data.\*.values.Direct Contact Corporate ID | string |  |  
action_result.data.\*.values.Direct Contact Country | string |  |  
action_result.data.\*.values.Direct Contact Country Code | string |  |  
action_result.data.\*.values.Direct Contact Department | string |  |  
action_result.data.\*.values.Direct Contact Desk Location | string |  |  
action_result.data.\*.values.Direct Contact Extension | string |  |  
action_result.data.\*.values.Direct Contact First Name | string |  `bmcremedy first name`  |  
action_result.data.\*.values.Direct Contact Internet E-mail | string |  |  
action_result.data.\*.values.Direct Contact Last Name | string |  `bmcremedy last name`  |  
action_result.data.\*.values.Direct Contact Local Number | string |  |  
action_result.data.\*.values.Direct Contact Location Details | string |  |  
action_result.data.\*.values.Direct Contact LoginID | string |  |  
action_result.data.\*.values.Direct Contact Mail Station | string |  |  
action_result.data.\*.values.Direct Contact Middle Initial | string |  |  
action_result.data.\*.values.Direct Contact Organization | string |  |  
action_result.data.\*.values.Direct Contact Phone Number | string |  |  
action_result.data.\*.values.Direct Contact Region | string |  |  
action_result.data.\*.values.Direct Contact Site | string |  |  
action_result.data.\*.values.Direct Contact Site Group | string |  |  
action_result.data.\*.values.Direct Contact Site ID | string |  |  
action_result.data.\*.values.Direct Contact State/Province | string |  |  
action_result.data.\*.values.Direct Contact Street | string |  |  
action_result.data.\*.values.Direct Contact Time Zone | string |  |  
action_result.data.\*.values.Direct Contact Zip/Postal Code | string |  |  
action_result.data.\*.values.Extension Business | string |  |  
action_result.data.\*.values.First_Name | string |  `bmcremedy first name`  |  
action_result.data.\*.values.Flag_Create_Request | string |  |  
action_result.data.\*.values.Generic Categorization Tier 1 | string |  |  
action_result.data.\*.values.Global_OR_Custom_Mapping | string |  |  
action_result.data.\*.values.HPD_CI | string |  |  
action_result.data.\*.values.HPD_CI_FormName | string |  |  
action_result.data.\*.values.HPD_CI_ReconID | string |  |  
action_result.data.\*.values.HPD_TemplateName | string |  |  
action_result.data.\*.values.Impact | string |  |  
action_result.data.\*.values.Impact_OR_Root | string |  |  
action_result.data.\*.values.Incident Number | string |  `bmcremedy incident id`  |   INC000000000137 
action_result.data.\*.values.Incident_Entry_ID | string |  |  
action_result.data.\*.values.InfrastructureEventType | string |  |  
action_result.data.\*.values.InstanceId | string |  |  
action_result.data.\*.values.Internet E-mail | string |  |  
action_result.data.\*.values.KMSGUID | string |  |  
action_result.data.\*.values.Last Modified By | string |  |  
action_result.data.\*.values.Last_Name | string |  `bmcremedy last name`  |  
action_result.data.\*.values.Local Business | string |  |  
action_result.data.\*.values.Login_ID | string |  |  
action_result.data.\*.values.Lookup Keyword | string |  |  
action_result.data.\*.values.Mail Station | string |  |  
action_result.data.\*.values.Manufacturer | string |  |  
action_result.data.\*.values.MaxRetries | string |  |  
action_result.data.\*.values.Middle Initial | string |  |  
action_result.data.\*.values.Modified Chat Session ID | string |  |  
action_result.data.\*.values.Modified Date | string |  |  
action_result.data.\*.values.OptionForClosingIncident | string |  |  
action_result.data.\*.values.Organization | string |  |  
action_result.data.\*.values.Person ID | string |  |  
action_result.data.\*.values.Person Instance ID | string |  |  
action_result.data.\*.values.Phone_Number | string |  |  
action_result.data.\*.values.PortNumber | string |  |   30 
action_result.data.\*.values.Priority | string |  |  
action_result.data.\*.values.Priority Weight | numeric |  |  
action_result.data.\*.values.Product Categorization Tier 1 | string |  |  
action_result.data.\*.values.Product Categorization Tier 2 | string |  |  
action_result.data.\*.values.Product Categorization Tier 3 | string |  |  
action_result.data.\*.values.Product Model/Version | string |  |  
action_result.data.\*.values.Product Name | string |  |  
action_result.data.\*.values.Protocol | string |  |  
action_result.data.\*.values.ReconciliationIdentity | string |  |  
action_result.data.\*.values.Region | string |  |  
action_result.data.\*.values.Reported Date | string |  |  
action_result.data.\*.values.Reported Source | string |  |  
action_result.data.\*.values.Request ID | string |  |  
action_result.data.\*.values.Required Resolution DateTime | string |  |  
action_result.data.\*.values.Resolution | string |  |  
action_result.data.\*.values.Resolution Category Tier 1 | string |  |  
action_result.data.\*.values.Resolution Category Tier 2 | string |  |  
action_result.data.\*.values.Resolution Category Tier 3 | string |  |  
action_result.data.\*.values.Resolution Method | string |  |  
action_result.data.\*.values.SRID | string |  |  
action_result.data.\*.values.SRInstanceID | string |  |  
action_result.data.\*.values.SRMS Registry Instance ID | string |  |  
action_result.data.\*.values.SRMSAOIGuid | string |  |  
action_result.data.\*.values.Schema Name | string |  |  
action_result.data.\*.values.ServiceCI | string |  |  
action_result.data.\*.values.ServiceCI_ReconID | string |  |  
action_result.data.\*.values.Service_Type | string |  |  
action_result.data.\*.values.Short Description | string |  |  
action_result.data.\*.values.Site | string |  |  
action_result.data.\*.values.Site Group | string |  |  
action_result.data.\*.values.Site ID | string |  |  
action_result.data.\*.values.State Province | string |  |  
action_result.data.\*.values.Status | string |  |  
action_result.data.\*.values.Status History | string |  |  
action_result.data.\*.values.Status History.Assigned.timestamp | string |  |  
action_result.data.\*.values.Status History.Assigned.user | string |  |  
action_result.data.\*.values.Status History.Cancelled.timestamp | string |  |  
action_result.data.\*.values.Status History.Cancelled.user | string |  |  
action_result.data.\*.values.Status History.Closed.timestamp | string |  |  
action_result.data.\*.values.Status History.Closed.user | string |  |  
action_result.data.\*.values.Status History.In Progress.timestamp | string |  |  
action_result.data.\*.values.Status History.In Progress.user | string |  |  
action_result.data.\*.values.Status History.New.timestamp | string |  |  
action_result.data.\*.values.Status History.New.user | string |  |  
action_result.data.\*.values.Status History.Pending.timestamp | string |  |  
action_result.data.\*.values.Status History.Pending.user | string |  |  
action_result.data.\*.values.Status History.Resolved.timestamp | string |  |  
action_result.data.\*.values.Status History.Resolved.user | string |  |  
action_result.data.\*.values.Status_Reason | string |  |  
action_result.data.\*.values.Street | string |  |  
action_result.data.\*.values.Submitter | string |  |  
action_result.data.\*.values.TemplateID | string |  |  
action_result.data.\*.values.TemplateID2 | string |  |  
action_result.data.\*.values.Time Zone | string |  |  
action_result.data.\*.values.Unavailability Type | string |  |  
action_result.data.\*.values.Unavailability_Priority | string |  |  
action_result.data.\*.values.Unknown User | string |  |  
action_result.data.\*.values.Urgency | string |  |  
action_result.data.\*.values.VIP | string |  |  
action_result.data.\*.values.Vendor Assignee Groups | string |  |  
action_result.data.\*.values.Vendor Assignee Groups_parent | string |  |  
action_result.data.\*.values.Vendor Group | string |  |  
action_result.data.\*.values.Vendor Group ID | string |  |  
action_result.data.\*.values.Vendor Name | string |  |  
action_result.data.\*.values.Vendor Organization | string |  |  
action_result.data.\*.values.Vendor Ticket Number | string |  |  
action_result.data.\*.values.Zip/Postal Code | string |  |  
action_result.data.\*.values.bOrphanedRoot | string |  |  
action_result.data.\*.values.cell_name | string |  |  
action_result.data.\*.values.first_name2 | string |  `bmcremedy first name`  |  
action_result.data.\*.values.last_name2 | string |  `bmcremedy last name`  |  
action_result.data.\*.values.mc_ueid | string |  |  
action_result.data.\*.values.policy_name | string |  |  
action_result.data.\*.values.policy_type | string |  |  
action_result.data.\*.values.root_component_id_list | string |  |  
action_result.data.\*.values.root_incident_id_list | string |  |  
action_result.data.\*.values.status_incident | string |  |  
action_result.data.\*.values.status_reason2 | string |  |  
action_result.data.\*.values.use_case | string |  |  
action_result.data.\*.values.z1D Char01 | string |  |  
action_result.data.\*.values.z1D Permission Group ID | string |  |  
action_result.data.\*.values.z1D Permission Group List | string |  |  
action_result.data.\*.values.z1D_Action | string |  |  
action_result.data.\*.values.z1D_ActivityDate_tab | string |  |  
action_result.data.\*.values.z1D_Activity_Type | string |  |  
action_result.data.\*.values.z1D_Area_Business | string |  |  
action_result.data.\*.values.z1D_CC_Business | string |  |  
action_result.data.\*.values.z1D_CIUAAssignGroup | string |  |  
action_result.data.\*.values.z1D_CIUASupportCompany | string |  |  
action_result.data.\*.values.z1D_CIUASupportOrg | string |  |  
action_result.data.\*.values.z1D_CI_FormName | string |  |  
action_result.data.\*.values.z1D_Char02 | string |  |  
action_result.data.\*.values.z1D_Command | string |  |  
action_result.data.\*.values.z1D_CommunicationSource | string |  |  
action_result.data.\*.values.z1D_ConfirmGroup | string |  |  
action_result.data.\*.values.z1D_CreatedFromBackEndSynchWI | string |  |  
action_result.data.\*.values.z1D_DC_AreaCode | string |  |  
action_result.data.\*.values.z1D_DC_CountryCode | string |  |  
action_result.data.\*.values.z1D_DC_Extension | string |  |  
action_result.data.\*.values.z1D_DC_Internet_Email | string |  |  
action_result.data.\*.values.z1D_DC_LocalNumber | string |  |  
action_result.data.\*.values.z1D_DC_Phone_Number | string |  |  
action_result.data.\*.values.z1D_Details | string |  |  
action_result.data.\*.values.z1D_Direct Contact Person ID | string |  |  
action_result.data.\*.values.z1D_Extension_Business | string |  |  
action_result.data.\*.values.z1D_Internet_Email | string |  |  
action_result.data.\*.values.z1D_Local_Business | string |  |  
action_result.data.\*.values.z1D_PersonInfo | string |  |  
action_result.data.\*.values.z1D_Person_Match_Found | string |  |  
action_result.data.\*.values.z1D_Phone_Number | string |  |  
action_result.data.\*.values.z1D_SRMInteger | string |  |  
action_result.data.\*.values.z1D_Secure_Log | string |  |  
action_result.data.\*.values.z1D_SupportGroupID | string |  |  
action_result.data.\*.values.z1D_UAAssignmentMethod | string |  |  
action_result.data.\*.values.z1D_View_Access | string |  |  
action_result.data.\*.values.z1D_WorklogDetails | string |  |  
action_result.data.\*.values.z2AF_Act_Attachment_1 | string |  |  
action_result.data.\*.values.z2AF_Act_Attachment_1.href | string |  |  
action_result.data.\*.values.z2AF_Act_Attachment_1.name | string |  |  
action_result.data.\*.values.z2AF_Act_Attachment_1.sizeBytes | string |  |  
action_result.data.\*.values.zTmpEventGUID | string |  |  
action_result.summary.incident_id | string |  `bmcremedy incident id`  |   INC000000000137 
action_result.message | string |  |   Incident id: INC000000000137 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'update ticket'
Update an existing incident

Type: **generic**  
Read only: **False**

This action can be used to assign an incident to a user. Use the <b>fields</b> parameter to set the <b>Status</b>, <b>Assignee Login ID</b> and <b>Assignee</b> values. For example: To assign an incident to the user <b>User</b> set the <b>fields</b> parameter to {"Status": "Assigned", "Assignee Login ID": "User", "Assignee": "User Name"}<br><b>Note:</b> Only single JSON formatted dictionary is allowed in <b>fields</b> action parameter<br>To add comment set <b>fields</b> parameter to {"Work Log Type": "General Information", "Detailed Description": "Comment to add"}.<br>The attachment should be placed in vault of the container from which the action will be executed, and it would appear in <b>Work Detail</b> section on BMC Remedy.<br>Typical (default installation) values for <b>work_info_type</b> are:<ul><li>Customer Inbound:<ul><li>Customer Communication</li><li>Customer Follow-up</li><li>Customer Status Update</li></ul></li><li>Customer Outbound<ul><li>Closure Follow Up</li><li>Detail Clarification</li><li>General Information</li><li>Resolution Communications</li><li>Satisfaction Survey</li><li>Status Update</li></ul></li><li>General<ul><li>Incident Task / Action</li><li>Problem Script</li><li>Working Log</li><li>Email System</li><li>Paging System</li><li>BMC Impact Manager Update</li><li>Chat</li></ul></li><li>Vendor<ul><li>Vendor Communication</li></ul></li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 
**work_info_type** |  optional  | Work Info Type | string | 
**fields** |  optional  | Fields (JSON format) | string | 
**vault_id** |  optional  | Comma (',') separated vault ID (maximum 3) | string |  `vault id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.fields | string |  |   {"First_Name": "Customer First Name", "Last_Name": "Customer Last Name", "Description": "Incident Description", "Service_Type": "User Service Restoration", "Reported Source": "Direct Input", "Status": "Assigned", "Assignee Login ID": "User", "Assignee": "User Name"}<br>To add comment set <b>fields</b> parameter to {"Work Log Type": "General Information", "Detailed Description": "Comment to add"} 
action_result.parameter.id | string |  `bmcremedy incident id`  |   INC000000000137 
action_result.parameter.vault_id | string |  `vault id`  |   d766846c37a473ce02fc71e4fa9d471c3a715727 
action_result.parameter.work_info_type | string |  |   General Information 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Incident updated successfully 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get ticket'
Get incident information

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.id | string |  `bmcremedy incident id`  |   INC000000000137 
action_result.data.\*._links.self.\*.href | string |  |  
action_result.data.\*.entries.\*._links.self.\*.href | string |  |  
action_result.data.\*.entries.\*.values.AccessMode | string |  |  
action_result.data.\*.entries.\*.values.AppInstanceServer | string |  |  
action_result.data.\*.entries.\*.values.AppInterfaceForm | string |  |  
action_result.data.\*.entries.\*.values.AppLogin | string |  |  
action_result.data.\*.entries.\*.values.AppPassword | string |  |  
action_result.data.\*.entries.\*.values.Assigned Group | string |  |  
action_result.data.\*.entries.\*.values.Assigned Group ID | string |  |  
action_result.data.\*.entries.\*.values.Assigned Group Shift ID | string |  |  
action_result.data.\*.entries.\*.values.Assigned Group Shift Name | string |  |  
action_result.data.\*.entries.\*.values.Assigned Support Company | string |  |  
action_result.data.\*.entries.\*.values.Assigned Support Organization | string |  |  
action_result.data.\*.entries.\*.values.Assignee | string |  |  
action_result.data.\*.entries.\*.values.Assignee Groups | string |  |  
action_result.data.\*.entries.\*.values.Assignee Groups_parent | string |  |  
action_result.data.\*.entries.\*.values.Assignee Login ID | string |  |  
action_result.data.\*.entries.\*.values.AttachmentSourceFormName | string |  |  
action_result.data.\*.entries.\*.values.AttachmentSourceGUID | string |  |  
action_result.data.\*.entries.\*.values.Auto Open Session | string |  |  
action_result.data.\*.entries.\*.values.Broker Vendor Name | string |  |  
action_result.data.\*.entries.\*.values.Categorization Tier 1 | string |  |  
action_result.data.\*.entries.\*.values.Categorization Tier 2 | string |  |  
action_result.data.\*.entries.\*.values.Categorization Tier 3 | string |  |  
action_result.data.\*.entries.\*.values.Chat Session ID | string |  |  
action_result.data.\*.entries.\*.values.City | string |  |  
action_result.data.\*.entries.\*.values.ClientLocale | string |  |  
action_result.data.\*.entries.\*.values.Closed Date | string |  |  
action_result.data.\*.entries.\*.values.Closure Manufacturer | string |  |  
action_result.data.\*.entries.\*.values.Closure Product Category Tier1 | string |  |  
action_result.data.\*.entries.\*.values.Closure Product Category Tier2 | string |  |  
action_result.data.\*.entries.\*.values.Closure Product Category Tier3 | string |  |  
action_result.data.\*.entries.\*.values.Closure Product Model/Version | string |  |  
action_result.data.\*.entries.\*.values.Closure Product Name | string |  |  
action_result.data.\*.entries.\*.values.Company | string |  |  
action_result.data.\*.entries.\*.values.Component_ID | string |  |  
action_result.data.\*.entries.\*.values.Contact Client Type | string |  |  
action_result.data.\*.entries.\*.values.Contact Company | string |  |  
action_result.data.\*.entries.\*.values.Contact Sensitivity | string |  |  
action_result.data.\*.entries.\*.values.Corporate ID | string |  |  
action_result.data.\*.entries.\*.values.Country | string |  |  
action_result.data.\*.entries.\*.values.Created_By | string |  |  
action_result.data.\*.entries.\*.values.Customer Login ID | string |  |  
action_result.data.\*.entries.\*.values.Department | string |  |  
action_result.data.\*.entries.\*.values.Description | string |  |  
action_result.data.\*.entries.\*.values.Desk Location | string |  |  
action_result.data.\*.entries.\*.values.Detailed Decription | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Area Code | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact City | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Company | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Corporate ID | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Country | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Country Code | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Department | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Desk Location | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Extension | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact First Name | string |  `bmcremedy first name`  |  
action_result.data.\*.entries.\*.values.Direct Contact Internet E-mail | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Last Name | string |  `bmcremedy last name`  |  
action_result.data.\*.entries.\*.values.Direct Contact Local Number | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Location Details | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Login ID | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Mail Station | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Middle Initial | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Organization | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Person ID | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Phone Number | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Region | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Site | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Site Group | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Site ID | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact State/Province | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Street | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Time Zone | string |  |  
action_result.data.\*.entries.\*.values.Direct Contact Zip/Postal Code | string |  |  
action_result.data.\*.entries.\*.values.Entry ID | string |  |  
action_result.data.\*.entries.\*.values.Estimated Resolution Date | string |  |  
action_result.data.\*.entries.\*.values.First Name | string |  `bmcremedy first name`  |  
action_result.data.\*.entries.\*.values.FirstWIPDate | string |  |  
action_result.data.\*.entries.\*.values.HPD_CI | string |  |  
action_result.data.\*.entries.\*.values.HPD_CI_FormName | string |  |  
action_result.data.\*.entries.\*.values.HPD_CI_ReconID | string |  |  
action_result.data.\*.entries.\*.values.Impact | string |  |  
action_result.data.\*.entries.\*.values.Impact_OR_Root | string |  |  
action_result.data.\*.entries.\*.values.Incident Number | string |  `bmcremedy incident id`  |  
action_result.data.\*.entries.\*.values.InfrastructureEventType | string |  |  
action_result.data.\*.entries.\*.values.InstanceId | string |  |  
action_result.data.\*.entries.\*.values.Internet E-mail | string |  |  
action_result.data.\*.entries.\*.values.KMSGUID | string |  |  
action_result.data.\*.entries.\*.values.Last Acknowledged Date | string |  |  
action_result.data.\*.entries.\*.values.Last Modified By | string |  |  
action_result.data.\*.entries.\*.values.Last Modified Date | string |  |  
action_result.data.\*.entries.\*.values.Last Name | string |  `bmcremedy last name`  |  
action_result.data.\*.entries.\*.values.Last Resolved Date | string |  |  
action_result.data.\*.entries.\*.values.Last _Assigned_Date | string |  |  
action_result.data.\*.entries.\*.values.LastWIPDate | string |  |  
action_result.data.\*.entries.\*.values.Mail Station | string |  |  
action_result.data.\*.entries.\*.values.Manufacturer | string |  |  
action_result.data.\*.entries.\*.values.MaxRetries | string |  |  
action_result.data.\*.entries.\*.values.Middle Initial | string |  |  
action_result.data.\*.entries.\*.values.Modified Chat Session ID | string |  |  
action_result.data.\*.entries.\*.values.Number of Attachments | string |  |  
action_result.data.\*.entries.\*.values.Organization | string |  |   Information Technology 
action_result.data.\*.entries.\*.values.Owner Group | string |  |   Service Desk 
action_result.data.\*.entries.\*.values.Owner Group ID | string |  |   SGP000000000011 
action_result.data.\*.entries.\*.values.Owner Support Company | string |  |   Calbro Services 
action_result.data.\*.entries.\*.values.Owner Support Organization | string |  |   IT Support 
action_result.data.\*.entries.\*.values.Person ID | string |  |  
action_result.data.\*.entries.\*.values.Phone Number | string |  |  
action_result.data.\*.entries.\*.values.PortNumber | string |  |   30 
action_result.data.\*.entries.\*.values.Previous_HPD_CI_ReconID | string |  |  
action_result.data.\*.entries.\*.values.Previous_ServiceCI_ReconID | string |  |  
action_result.data.\*.entries.\*.values.Priority | string |  |  
action_result.data.\*.entries.\*.values.Priority Weight | numeric |  |  
action_result.data.\*.entries.\*.values.Product Categorization Tier 1 | string |  |  
action_result.data.\*.entries.\*.values.Product Categorization Tier 2 | string |  |  
action_result.data.\*.entries.\*.values.Product Categorization Tier 3 | string |  |  
action_result.data.\*.entries.\*.values.Product Model/Version | string |  |  
action_result.data.\*.entries.\*.values.Product Name | string |  |  
action_result.data.\*.entries.\*.values.Protocol | string |  |  
action_result.data.\*.entries.\*.values.Region | string |  |  
action_result.data.\*.entries.\*.values.Reported Date | string |  |  
action_result.data.\*.entries.\*.values.Reported Source | string |  |  
action_result.data.\*.entries.\*.values.Request ID | string |  |  
action_result.data.\*.entries.\*.values.Required Resolution DateTime | string |  |  
action_result.data.\*.entries.\*.values.Resolution | string |  |  
action_result.data.\*.entries.\*.values.Resolution Category | string |  |  
action_result.data.\*.entries.\*.values.Resolution Category Tier 2 | string |  |  
action_result.data.\*.entries.\*.values.Resolution Category Tier 3 | string |  |  
action_result.data.\*.entries.\*.values.Resolution Method | string |  |  
action_result.data.\*.entries.\*.values.Responded Date | string |  |  
action_result.data.\*.entries.\*.values.SRAttachment | string |  |  
action_result.data.\*.entries.\*.values.SRAttachment.href | string |  |  
action_result.data.\*.entries.\*.values.SRAttachment.name | string |  |  
action_result.data.\*.entries.\*.values.SRAttachment.sizeBytes | string |  |  
action_result.data.\*.entries.\*.values.SRID | string |  |  
action_result.data.\*.entries.\*.values.SRInstanceID | string |  |  
action_result.data.\*.entries.\*.values.SRMS Registry Instance ID | string |  |  
action_result.data.\*.entries.\*.values.SRMSAOIGuid | string |  |  
action_result.data.\*.entries.\*.values.Service Type | string |  |  
action_result.data.\*.entries.\*.values.ServiceCI | string |  |  
action_result.data.\*.entries.\*.values.ServiceCI_ReconID | string |  |  
action_result.data.\*.entries.\*.values.Site | string |  |  
action_result.data.\*.entries.\*.values.Site Group | string |  |  
action_result.data.\*.entries.\*.values.Site ID | string |  |  
action_result.data.\*.entries.\*.values.State Province | string |  |  
action_result.data.\*.entries.\*.values.Status | string |  |  
action_result.data.\*.entries.\*.values.Status History.Assigned.timestamp | string |  |  
action_result.data.\*.entries.\*.values.Status History.Assigned.user | string |  |  
action_result.data.\*.entries.\*.values.Status History.Cancelled.timestamp | string |  |  
action_result.data.\*.entries.\*.values.Status History.Cancelled.user | string |  |  
action_result.data.\*.entries.\*.values.Status History.Closed.timestamp | string |  |  
action_result.data.\*.entries.\*.values.Status History.Closed.user | string |  |  
action_result.data.\*.entries.\*.values.Status History.In Progress.timestamp | string |  |  
action_result.data.\*.entries.\*.values.Status History.In Progress.user | string |  |  
action_result.data.\*.entries.\*.values.Status History.New.timestamp | string |  |  
action_result.data.\*.entries.\*.values.Status History.New.user | string |  |  
action_result.data.\*.entries.\*.values.Status History.Pending.timestamp | string |  |  
action_result.data.\*.entries.\*.values.Status History.Pending.user | string |  |  
action_result.data.\*.entries.\*.values.Status History.Resolved.timestamp | string |  |  
action_result.data.\*.entries.\*.values.Status History.Resolved.user | string |  |  
action_result.data.\*.entries.\*.values.Status-History.Assigned.timestamp | string |  |   2021-10-19T06:33:28.000+0000 
action_result.data.\*.entries.\*.values.Status-History.Assigned.user | string |  |   Demo 
action_result.data.\*.entries.\*.values.Status-History.In Progress.timestamp | string |  |   2022-10-20T10:21:57.000+0000 
action_result.data.\*.entries.\*.values.Status-History.In Progress.user | string |  |   appadmin 
action_result.data.\*.entries.\*.values.Status-History.New.timestamp | string |  |   2021-10-19T06:33:28.000+0000 
action_result.data.\*.entries.\*.values.Status-History.New.user | string |  |   Demo 
action_result.data.\*.entries.\*.values.Status_Reason | string |  |  
action_result.data.\*.entries.\*.values.Street | string |  |  
action_result.data.\*.entries.\*.values.Submit Date | string |  |  
action_result.data.\*.entries.\*.values.Submitter | string |  |  
action_result.data.\*.entries.\*.values.TemplateID | string |  |  
action_result.data.\*.entries.\*.values.TimeOfEvent | string |  |  
action_result.data.\*.entries.\*.values.Total Transfers | numeric |  |  
action_result.data.\*.entries.\*.values.Urgency | string |  |  
action_result.data.\*.entries.\*.values.VIP | string |  |  
action_result.data.\*.entries.\*.values.Vendor Assignee Groups | string |  |  
action_result.data.\*.entries.\*.values.Vendor Assignee Groups_parent | string |  |  
action_result.data.\*.entries.\*.values.Vendor Group | string |  |  
action_result.data.\*.entries.\*.values.Vendor Group ID | string |  |  
action_result.data.\*.entries.\*.values.Vendor Name | string |  |  
action_result.data.\*.entries.\*.values.Vendor Organization | string |  |   Information Technology 
action_result.data.\*.entries.\*.values.Vendor Ticket Number | string |  |  
action_result.data.\*.entries.\*.values.Zip/Postal Code | string |  |  
action_result.data.\*.entries.\*.values.bOrphanedRoot | string |  |  
action_result.data.\*.entries.\*.values.cell_name | string |  |  
action_result.data.\*.entries.\*.values.mc_ueid | string |  |  
action_result.data.\*.entries.\*.values.policy_name | string |  |  
action_result.data.\*.entries.\*.values.policy_type | string |  |  
action_result.data.\*.entries.\*.values.root_component_id_list | string |  |  
action_result.data.\*.entries.\*.values.root_incident_id_list | string |  |  
action_result.data.\*.entries.\*.values.status_incident | string |  |  
action_result.data.\*.entries.\*.values.status_reason2 | string |  |  
action_result.data.\*.entries.\*.values.use_case | string |  |  
action_result.data.\*.entries.\*.values.z1D Action | string |  |  
action_result.data.\*.entries.\*.values.z1D Char01 | string |  |  
action_result.data.\*.entries.\*.values.z1D Char02 | string |  |  
action_result.data.\*.entries.\*.values.z1D Permission Group ID | string |  |  
action_result.data.\*.entries.\*.values.z1D Permission Group List | string |  |  
action_result.data.\*.entries.\*.values.z1D_ActivityDate_tab | string |  |  
action_result.data.\*.entries.\*.values.z1D_Activity_Type | string |  |  
action_result.data.\*.entries.\*.values.z1D_AssociationDescription | string |  |  
action_result.data.\*.entries.\*.values.z1D_CI_FormName | string |  |  
action_result.data.\*.entries.\*.values.z1D_Char02 | string |  |  
action_result.data.\*.entries.\*.values.z1D_Command | string |  |  
action_result.data.\*.entries.\*.values.z1D_CommunicationSource | string |  |  
action_result.data.\*.entries.\*.values.z1D_ConfirmGroup | string |  |  
action_result.data.\*.entries.\*.values.z1D_CreatedFromBackEndSynchWI | string |  |  
action_result.data.\*.entries.\*.values.z1D_Details | string |  |  
action_result.data.\*.entries.\*.values.z1D_FormName | string |  |  
action_result.data.\*.entries.\*.values.z1D_InterfaceAction | string |  |  
action_result.data.\*.entries.\*.values.z1D_SR_Instanceid | string |  |  
action_result.data.\*.entries.\*.values.z1D_Secure_Log | string |  |  
action_result.data.\*.entries.\*.values.z1D_Summary | string |  |  
action_result.data.\*.entries.\*.values.z1D_View_Access | string |  |  
action_result.data.\*.entries.\*.values.z1D_WorkInfoSubmitter | string |  |  
action_result.data.\*.entries.\*.values.z1D_WorklogDetails | string |  |  
action_result.data.\*.entries.\*.values.z2AF_Act_Attachment_1 | string |  |  
action_result.data.\*.entries.\*.values.zTmpEventGUID | string |  |  
action_result.data.\*.work_details._links.self.\*.href | string |  |  
action_result.data.\*.work_details.entries.\*._links.self.\*.href | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assign WorkLog Flag | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assigned Group | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assigned Group ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assigned Group Shift ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assigned Group Shift Name | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assigned Support Company | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assigned Support Organization | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assigned To | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assignee | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assignee Groups | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assignee Groups_parent | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assignee Login ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.Assignment Log Created | string |  |  
action_result.data.\*.work_details.entries.\*.values.AttachmentSourceFormName | string |  |  
action_result.data.\*.work_details.entries.\*.values.AttachmentSourceGUID | string |  |  
action_result.data.\*.work_details.entries.\*.values.Broker Vendor Name | string |  |  
action_result.data.\*.work_details.entries.\*.values.ClientLocale | string |  |  
action_result.data.\*.work_details.entries.\*.values.Communication Source | string |  |  
action_result.data.\*.work_details.entries.\*.values.Communication Type | string |  |  
action_result.data.\*.work_details.entries.\*.values.Company | string |  |  
action_result.data.\*.work_details.entries.\*.values.DataTags | string |  |  
action_result.data.\*.work_details.entries.\*.values.Description | string |  |  
action_result.data.\*.work_details.entries.\*.values.Detailed Description | string |  |  
action_result.data.\*.work_details.entries.\*.values.HPD Attachment ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.Incident Entry ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.Incident Number | string |  `bmcremedy incident id`  |  
action_result.data.\*.work_details.entries.\*.values.InstanceId | string |  |  
action_result.data.\*.work_details.entries.\*.values.Last Modified By | string |  |  
action_result.data.\*.work_details.entries.\*.values.Last Modified Date | string |  |  
action_result.data.\*.work_details.entries.\*.values.Number of Attachments | string |  |  
action_result.data.\*.work_details.entries.\*.values.Number of URLs | string |  |  
action_result.data.\*.work_details.entries.\*.values.SR_Instanceid | string |  |  
action_result.data.\*.work_details.entries.\*.values.Secure Work Log | string |  |  
action_result.data.\*.work_details.entries.\*.values.Shared With Vendor | string |  |  
action_result.data.\*.work_details.entries.\*.values.Shifts Flag | string |  |  
action_result.data.\*.work_details.entries.\*.values.Short Description | string |  |  
action_result.data.\*.work_details.entries.\*.values.Status | string |  |  
action_result.data.\*.work_details.entries.\*.values.Status History | string |  |  
action_result.data.\*.work_details.entries.\*.values.Submit Date | string |  |   2020-04-14T17:52:50.000+0000 
action_result.data.\*.work_details.entries.\*.values.Submitter | string |  |  
action_result.data.\*.work_details.entries.\*.values.Thumbnail 1 | string |  |  
action_result.data.\*.work_details.entries.\*.values.Thumbnail 2 | string |  |  
action_result.data.\*.work_details.entries.\*.values.Thumbnail 3 | string |  |  
action_result.data.\*.work_details.entries.\*.values.Total Time Spent | numeric |  |   100000 
action_result.data.\*.work_details.entries.\*.values.URL01 | string |  |  
action_result.data.\*.work_details.entries.\*.values.URL02 | string |  |  
action_result.data.\*.work_details.entries.\*.values.URL03 | string |  |  
action_result.data.\*.work_details.entries.\*.values.Vendor Assignee Groups | string |  |  
action_result.data.\*.work_details.entries.\*.values.Vendor Assignee Groups_parent | string |  |  
action_result.data.\*.work_details.entries.\*.values.View Access | string |  |  
action_result.data.\*.work_details.entries.\*.values.Work Log Date | string |  |  
action_result.data.\*.work_details.entries.\*.values.Work Log ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.Work Log Submit Date | string |  |   2020-04-14T17:52:50.000+0000 
action_result.data.\*.work_details.entries.\*.values.Work Log Submitter | string |  |   Admin 
action_result.data.\*.work_details.entries.\*.values.Work Log Type | string |  |  
action_result.data.\*.work_details.entries.\*.values.WorkLog Action Completed | string |  |  
action_result.data.\*.work_details.entries.\*.values.WorkLog Action Status | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Action | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Action02 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char01 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char02 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char03 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char04 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char05 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char06 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char07 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char08 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char09 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char10 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char11 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char12 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char13 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char14 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char15 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Char16 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Close Dialog | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Integer01 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Integer02 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Integer03 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Integer04 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Last Date Duration Calc | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Lastcount | numeric |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Lastcount02 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Mobile Worklog Upd2 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Page Indicator | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Permission Group ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Permission Group List | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Previous Operation | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D QuickViewWlg Flag | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Status-INC | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D Work Log ID | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_AttachedFileName | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_ConfirmGroup | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_FileNameAttach2 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_FileNameAttach3 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_PrefixHolder | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_PrefixResult | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_SkipIfSmartITInstalled | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_WorkInfo_FileDefaultMsg | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1D_WorkInfo_NotesLabel | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G Disable Worklog Action | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G Enable French | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G Enable German | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G Enable Spanish | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G Enable User Defined 1 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G Enable User Defined 2 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G InitComplete | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G Multi-language | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G_HelpDeskIDPrefix | string |  |  
action_result.data.\*.work_details.entries.\*.values.z1G_Use_Custom_Prefix | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log01 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log01.href | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log01.name | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log01.sizeBytes | numeric |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log02 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log02.href | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log02.name | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log02.sizeBytes | numeric |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log03 | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log03.href | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log03.name | string |  |  
action_result.data.\*.work_details.entries.\*.values.z2AF Work Log03.sizeBytes | numeric |  |  
action_result.data.\*.work_details.entries.\*.values.zTmpEventGUID | string |  |  
action_result.summary.ticket_availability | boolean |  |   False  True 
action_result.message | string |  |   Ticket availability: True 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list tickets'
Get list of incidents

Type: **investigate**  
Read only: **True**

<p>The action supports limiting the number of incidents returned using the <b>limit</b> parameter. The input should be a positive integer. The results are always sorted in descending order based on their last modified date to place the latest modified incidents at the top. For example to get the latest 10 incidents that matched the filter, specify the limit as 10. If <b>limit</b> is zero or not specified, then all incidents will be returned.</p><p>To define a set of criteria to filter incidents, query must be provided in <b>query</b> parameter.<br>Query must contain field label enclosed in single quotation marks(''), and non-numeric values in double quotation marks("").<br>Eg: <b>'Incident Number'="INC000000000001", 'Submit Date'="February 20, 2017"</b><br>If a field name contains single quotation mark, add another single quotation mark next to it.<br>Eg: If field name is <b>Submitter's Phone Number</b>, query must contain field label as <b>'Submitter''s Phone Number'</b><br>More information about using fields in <b>query</b> parameter can be found on <a href="https://docs.bmc.com/docs/ars2008/using-fields-in-the-advanced-search-bar-928611932.html#Usingfieldsintheadvancedsearchbar-4Usingvaluesintheadvancedsearchbar" target='_blank'>Fields in query</a>.<br>Query can accept various operators such as:<br><ol><li><b>Relational and Logical Operators</b>:<ul><li>Relational and Logical operators are useful especially in non-text fields (such as date and time fields) when you want to search for a value within a numerical range.</li><li>Some of the examples are as follows:<br><b>('Submitter'="admin") AND (NOT 'Incident Number'="INC000000000001")</b><br><b>'Impact'="1-Extensive/Widespread" OR 'Urgency'="1-Critical"</b><br><b>'Incident Number' = "INC000000000001"</b><br><b>'Status' != "Closed"</b><br><b>'Submit Date' > "February 28, 2017"</b></li><li>More information about relational and logical operators can be found at <a href="https://docs.bmc.com/docs/ars2008/using-relational-operators-in-the-advanced-search-bar-928611933.html" target='_blank'>Relational and logical Operators link</a>.</li></ul></li><li><b>Keywords in query</b>:<ul><li>Keywords can be used anywhere where character values are accepted.</li><li>Most commonly used keywords are: <b>$DATE$</b>, <b>$NULL$</b>, <b>$TIME$</b>, <b>$TIMESTAMP$</b>, <b>$USER$</b>, and <b>$WEEKDAY$</b>.</li><li>Some of the examples are as follows:<br><b>'Assignee' = $NULL$</b><br><b>'Create date' < ($TIMESTAMP$ - 24\*60\*60)</b></li><li>More information about Keywords can be found at <a href="https://docs.bmc.com/docs/ars2008/using-fields-in-the-advanced-search-bar-928611932.html#Usingfieldsintheadvancedsearchbar-4Usingvaluesintheadvancedsearchbar" target='_blank'>Keywords link</a>.</li></ul></li><li><b>Wildcard symbols</b>:<ul><li>Wildcard symbols can be used to indicate one or more characters.</li><li>Wildcard symbols that can be used in query are: <b>%</b>, <b>_</b>, <b>-</b>, <b>[]</b>, <b>[^]</b></li><li>Some of the examples are as follows:<br><b>'Submitter' LIKE "\*Bob%ton\*"</b><br><b>'Phone Number' LIKE "_ 212 5555454 (66)"</b></li><li>More information about wildcard symbols can be found at <a href="https://docs.bmc.com/docs/ars2008/using-relational-operators-and-wildcard-symbols-in-a-search-928611919.html#Usingrelationaloperatorsandwildcardsymbolsinasearch-281729" target='_blank'>Wildcard symbols link</a>.</li></ul></li></ol>More information about BMC Remedy Query Syntax can be found at <a href="https://docs.bmc.com/docs/ars2008/using-the-advanced-search-bar-928611931.html" target='_blank'>Query Syntax link</a>.</p>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** |  optional  | Additional parameters to query | string | 
**limit** |  optional  | Maximum number of incidents to return | numeric | 
**offset** |  optional  | Set the starting point or offset for the response. The default value is 0 | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   2 
action_result.parameter.offset | numeric |  |   100 
action_result.parameter.query | string |  |   'Incident Number'="INC000000000001" 
action_result.data.\*._links.next.\*.href | string |  |  
action_result.data.\*._links.self.\*.href | string |  |   http://100.26.171.156:8008/api/arsys/v1/entry/HPD:IncidentInterface/INC0000000104%7CINC0000000104 
action_result.data.\*.values.Assigned Group | string |  |   Service Desk 
action_result.data.\*.values.Assignee | string |  |   Alex Jan 
action_result.data.\*.values.Description | string |  |   q3123 
action_result.data.\*.values.First Name | string |  `bmcremedy first name`  |   Alex 
action_result.data.\*.values.Incident Number | string |  `bmcremedy incident id`  |   INC000000000137 
action_result.data.\*.values.Last Name | string |  `bmcremedy last name`  |  
action_result.data.\*.values.Priority | string |  |   Low 
action_result.data.\*.values.Status | string |  |   Assigned 
action_result.summary.total_tickets | numeric |  |   1 
action_result.message | string |  |   Total tickets: 5 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'set status'
Set incident status

Type: **generic**  
Read only: **False**

Typical (default installation) values for <b>status</b> are:<ul><li>New</li><li>Assigned</li><li>In Progress</li><li>Pending</li><li>Resolved</li><li>Closed</li><li>Cancelled</li></ul>Typical (default installation) values of <b>status_reason</b> for a given <b>status</b> are:<ul><li>Pending<ul><li>Automated Resolution Reported</li><li>Client Action Required</li><li>Client Hold</li><li>Future Enhancement</li><li>Infrastructure Change</li><li>Local Site Action Required</li><li>Monitoring Incident</li><li>Purchase Order Approval</li><li>Registration Approval</li><li>Request</li><li>Supplier Delivery</li><li>Support Contact Hold</li><li>Third Party Vendor Action Reqd</li></ul></li><li>Resolved<ul><li>Automated Resolution Reported</li><li>Customer Follow-Up Required</li><li>Future Enhancement</li><li>Monitoring Incident</li><li>No Further Action Required</li><li>Temporary Corrective Action</li></ul></li><li>Closed<ul><li>Automated Resolution Reported</li><li>Infrastructure Change Created</li></ul></li><li>Cancelled<ul><li>No longer a Causal CI</li></ul></li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 
**status** |  required  | Status | string | 
**assignee_login_id** |  optional  | Login ID of assignee | string | 
**assignee** |  optional  | Assignee | string | 
**assigned_support_company** |  optional  | Assigned Support Company | string | 
**assigned_support_organization** |  optional  | Assigned Support Organization | string | 
**assigned_group** |  optional  | Assigned Group | string | 
**status_reason** |  optional  | Status Reason | string | 
**resolution** |  optional  | Resolution | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.assigned_group | string |  |   Service Desk 
action_result.parameter.assigned_support_company | string |  |   Support Inc 
action_result.parameter.assigned_support_organization | string |  |   Information Technology 
action_result.parameter.assignee | string |  |   Alex Jan 
action_result.parameter.assignee_login_id | string |  |   Alex 
action_result.parameter.id | string |  `bmcremedy incident id`  |  
action_result.parameter.resolution | string |  |   Resolution Comment 
action_result.parameter.status | string |  |   Assigned 
action_result.parameter.status_reason | string |  |   Status Reason 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Set status successfully 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'add comment'
Add work log information to the incident

Type: **generic**  
Read only: **False**

Typical (default installation) values for <b>work_info_type</b> are:<ul><li>Customer Inbound:<ul><li>Customer Communication</li><li>Customer Follow-up</li><li>Customer Status Update</li></ul></li><li>Customer Outbound<ul><li>Closure Follow Up</li><li>Detail Clarification</li><li>General Information</li><li>Resolution Communications</li><li>Satisfaction Survey</li><li>Status Update</li></ul></li><li>General<ul><li>Incident Task / Action</li><li>Problem Script</li><li>Working Log</li><li>Email System</li><li>Paging System</li><li>BMC Impact Manager Update</li><li>Chat</li></ul></li><li>Vendor<ul><li>Vendor Communication</li></ul></li></ul>Typical (default installation) values for <b>secure_work_log</b> are:<ul><li>Yes</li><li>No</li></ul>Typical (default installation) values for <b>view_access</b> are:<ul><li>Internal</li><li>Public</li></ul>If the user provides 'description' and 'comment' as input parameters, the priority will be given to 'comment'. so, under the notes section of a particular incident the value of 'comment' will be displayed. If the user provides either 'description' or 'comment', the given input value will be displayed under the notes section.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 
**work_info_type** |  required  | Work Info Type | string | 
**description** |  optional  | Worklog Description | string | 
**comment** |  optional  | Notes | string | 
**secure_work_log** |  optional  | Locked | string | 
**view_access** |  optional  | View Access | string | 
**worklog_submitter** |  optional  | Submit a worklog with a different username or email address | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   Comment 
action_result.parameter.description | string |  |   Description 
action_result.parameter.id | string |  `bmcremedy incident id`  |   INC000000000137 
action_result.parameter.secure_work_log | string |  |   Yes  No 
action_result.parameter.view_access | string |  |  
action_result.parameter.work_info_type | string |  |   General Information 
action_result.parameter.worklog_submitter | string |  |   Username 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Incident updated successfully 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 