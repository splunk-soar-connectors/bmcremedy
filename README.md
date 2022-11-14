[comment]: # "Auto-generated SOAR connector documentation"
# BMC Remedy

Publisher: Splunk  
Connector Version: 2\.1\.0  
Product Vendor: BMC Software  
Product Name: BMC Remedy  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.3\.5  

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
    end-user to please update their existing playbooks by re-inserting \| modifying \| deleting the
    corresponding action blocks.

      

    -   A 'offset' action parameter has been added in the 'list tickets' action

-   The existing output data paths have been modified for the 'list tickets' action. Hence, it is
    requested to the end-user to please update their existing playbooks by re-inserting \| modifying
    \| deleting the corresponding action blocks to ensure the correct functioning of the playbooks
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
**url** |  required  | string | Complete URL \(e\.g\. http\://mybmc\.contoso\.com\:8008\)
**verify\_server\_cert** |  optional  | boolean | Verify server certificate
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

Typically the following parameters are required, but this can be configured, therefore the action defines all parameters as optional and relies on the installation to validate the required parameters\:<ul><li><b>first\_name</b></li><li><b>last\_name</b></li><li><b>description</b></li><li><b>reported\_source</b></li><li><b>service\_type</b></li></ul>If field value is provided individually as well as in <b>fields</b> parameter, then value in <b>fields</b> parameter will be used for creating the incident\. For example, to create an incident using <b>fields</b> parameter and assign it to an assignee named User, set the <b>fields</b> parameter to \{"First\_Name"\: "Customer First Name", "Last\_Name"\: "Customer Last Name", "Description"\: "Incident Description", "Service\_Type"\: "User Service Restoration", "Reported Source"\: "Direct Input", "Status"\: "Assigned", "Assignee Login ID"\: "User", "Assignee"\: "User Name"\}<br><b>Note\:</b> Only single JSON formatted dictionary is allowed in <b>fields</b> action parameter<br>To add comment set <b>fields</b> parameter to \{"Work Log Type"\: "General Information", "Detailed Description"\: "Comment to add"\}\.<br>To create an incident, <b>first\_name</b> and <b>last\_name</b> are those of the customer that exists in the system\.<br>The <b>vault\_id</b> parameter takes the vault ID of a file and attaches it to the incident\.<br>The attachment should be placed in vault of the container from which the action will be executed, and it would appear in <b>Work Detail</b> section on BMC Remedy\.<br>Typical \(default installation\) values for <b>impact</b> are\:<ul><li>1\-Extensive/Widespread</li><li>2\-Significant/Large</li><li>3\-Moderate/Limited</li><li>4\-Minor/Localized</li></ul>Typical \(default installation\) values for <b>urgency</b> are\:<ul><li>1\-Critical</li><li>2\-High</li><li>3\-Medium</li><li>4\-Low</li></ul>Typical \(default installation\) values for <b>status</b> are\:<ul><li>New</li><li>Assigned</li><li>In Progress</li><li>Pending</li><li>Resolved</li><li>Closed</li><li>Cancelled</li></ul>Typical \(default installation\) values for <b>reported\_source</b> are\:<ul><li>Direct Input</li><li>Email</li><li>External Escalation</li><li>Fax</li><li>Self Service</li><li>Systems Management</li><li>Phone</li><li>Voice Mail</li><li>Walk In</li><li>Web</li><li>Other</li><li>BMC Impact Manager Event</li></ul>Typical \(default installation\) values for <b>service\_type</b> are\:<ul><li>User Service Restoration</li><li>User Service Request</li><li>Infrastructure Restoration</li><li>Infrastructure Event</li></ul>Typical \(default installation\) values for <b>work\_info\_type</b> are\:<ul><li>Customer Inbound\:<ul><li>Customer Communication</li><li>Customer Follow\-up</li><li>Customer Status Update</li></ul></li><li>Customer Outbound<ul><li>Closure Follow Up</li><li>Detail Clarification</li><li>General Information</li><li>Resolution Communications</li><li>Satisfaction Survey</li><li>Status Update</li></ul></li><li>General<ul><li>Incident Task / Action</li><li>Problem Script</li><li>Working Log</li><li>Email System</li><li>Paging System</li><li>BMC Impact Manager Update</li><li>Chat</li></ul></li><li>Vendor<ul><li>Vendor Communication</li></ul></li></ul>Typical \(default installation\) values of <b>status\_reason</b> for a given <b>status</b> are\:<ul><li>Pending<ul><li>Automated Resolution Reported</li><li>Client Action Required</li><li>Client Hold</li><li>Future Enhancement</li><li>Infrastructure Change</li><li>Local Site Action Required</li><li>Monitoring Incident</li><li>Purchase Order Approval</li><li>Registration Approval</li><li>Request</li><li>Supplier Delivery</li><li>Support Contact Hold</li><li>Third Party Vendor Action Reqd</li></ul></li><li>Resolved<ul><li>Automated Resolution Reported</li><li>Customer Follow\-Up Required</li><li>Future Enhancement</li><li>Monitoring Incident</li><li>No Further Action Required</li><li>Temporary Corrective Action</li></ul></li><li>Closed<ul><li>Automated Resolution Reported</li><li>Infrastructure Change Created</li></ul></li><li>Cancelled<ul><li>No longer a Causal CI</li></ul></li></ul>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**first\_name** |  optional  | Customer First Name | string |  `bmcremedy first name` 
**last\_name** |  optional  | Customer Last Name | string |  `bmcremedy last name` 
**description** |  optional  | Summary | string | 
**impact** |  optional  | Impact | string | 
**urgency** |  optional  | Urgency | string | 
**status** |  optional  | Status | string | 
**reported\_source** |  optional  | Reported Source | string | 
**service\_type** |  optional  | Incident Type | string | 
**work\_info\_type** |  optional  | Work Info Type | string | 
**status\_reason** |  optional  | Status Reason | string | 
**fields** |  optional  | Fields \(JSON format\) | string | 
**vault\_id** |  optional  | Comma \(,\) separated vault ID \(maximum 3\) | string |  `vault id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.description | string | 
action\_result\.parameter\.fields | string | 
action\_result\.parameter\.first\_name | string |  `bmcremedy first name` 
action\_result\.parameter\.impact | string | 
action\_result\.parameter\.last\_name | string |  `bmcremedy last name` 
action\_result\.parameter\.reported\_source | string | 
action\_result\.parameter\.service\_type | string | 
action\_result\.parameter\.status | string | 
action\_result\.parameter\.status\_reason | string | 
action\_result\.parameter\.urgency | string | 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.parameter\.work\_info\_type | string | 
action\_result\.data\.\*\.\_links\.self\.\*\.href | string | 
action\_result\.data\.\*\.values\.AccessMode | string | 
action\_result\.data\.\*\.values\.AppInstanceServer | string | 
action\_result\.data\.\*\.values\.AppInterfaceForm | string | 
action\_result\.data\.\*\.values\.AppLogin | string | 
action\_result\.data\.\*\.values\.AppPassword | string | 
action\_result\.data\.\*\.values\.ApplyTemplate | string | 
action\_result\.data\.\*\.values\.Area Business | string | 
action\_result\.data\.\*\.values\.Assigned Group | string | 
action\_result\.data\.\*\.values\.Assigned Group ID | string | 
action\_result\.data\.\*\.values\.Assigned Group Shift Name | string | 
action\_result\.data\.\*\.values\.Assigned Support Company | string | 
action\_result\.data\.\*\.values\.Assigned Support Organization | string | 
action\_result\.data\.\*\.values\.Assigned To | string | 
action\_result\.data\.\*\.values\.Assignee | string | 
action\_result\.data\.\*\.values\.Assignee Groups | string | 
action\_result\.data\.\*\.values\.Assignee Groups\_parent | string | 
action\_result\.data\.\*\.values\.Assignee Login ID | string | 
action\_result\.data\.\*\.values\.Auto Open Session | string | 
action\_result\.data\.\*\.values\.BiiARS\_01 | string | 
action\_result\.data\.\*\.values\.BiiARS\_02 | string | 
action\_result\.data\.\*\.values\.BiiARS\_03 | string | 
action\_result\.data\.\*\.values\.BiiARS\_04 | string | 
action\_result\.data\.\*\.values\.BiiARS\_05 | string | 
action\_result\.data\.\*\.values\.Broker Vendor Name | string | 
action\_result\.data\.\*\.values\.CC Business | string | 
action\_result\.data\.\*\.values\.CI Name | string | 
action\_result\.data\.\*\.values\.Categorization Tier 1 | string | 
action\_result\.data\.\*\.values\.Categorization Tier 2 | string | 
action\_result\.data\.\*\.values\.Categorization Tier 3 | string | 
action\_result\.data\.\*\.values\.Chat Session ID | string | 
action\_result\.data\.\*\.values\.Client Sensitivity | string | 
action\_result\.data\.\*\.values\.Client Type | string | 
action\_result\.data\.\*\.values\.ClientLocale | string | 
action\_result\.data\.\*\.values\.Closure Manufacturer | string | 
action\_result\.data\.\*\.values\.Closure Product Category Tier1 | string | 
action\_result\.data\.\*\.values\.Closure Product Category Tier2 | string | 
action\_result\.data\.\*\.values\.Closure Product Category Tier3 | string | 
action\_result\.data\.\*\.values\.Closure Product Model/Version | string | 
action\_result\.data\.\*\.values\.Closure Product Name | string | 
action\_result\.data\.\*\.values\.Company | string | 
action\_result\.data\.\*\.values\.Component\_ID | string | 
action\_result\.data\.\*\.values\.Contact Login Id | string | 
action\_result\.data\.\*\.values\.Contact\_Company | string | 
action\_result\.data\.\*\.values\.Corporate ID | string | 
action\_result\.data\.\*\.values\.Create Date | string | 
action\_result\.data\.\*\.values\.Created\_By | string | 
action\_result\.data\.\*\.values\.Created\_From\_flag | string | 
action\_result\.data\.\*\.values\.DataTags | string | 
action\_result\.data\.\*\.values\.DatasetId | string | 
action\_result\.data\.\*\.values\.Default City | string | 
action\_result\.data\.\*\.values\.Default Country | string | 
action\_result\.data\.\*\.values\.Department | string | 
action\_result\.data\.\*\.values\.Description | string | 
action\_result\.data\.\*\.values\.Desk Location | string | 
action\_result\.data\.\*\.values\.Detailed\_Decription | string | 
action\_result\.data\.\*\.values\.Direct Contact Area Code | string | 
action\_result\.data\.\*\.values\.Direct Contact City | string | 
action\_result\.data\.\*\.values\.Direct Contact Company | string | 
action\_result\.data\.\*\.values\.Direct Contact Corporate ID | string | 
action\_result\.data\.\*\.values\.Direct Contact Country | string | 
action\_result\.data\.\*\.values\.Direct Contact Country Code | string | 
action\_result\.data\.\*\.values\.Direct Contact Department | string | 
action\_result\.data\.\*\.values\.Direct Contact Desk Location | string | 
action\_result\.data\.\*\.values\.Direct Contact Extension | string | 
action\_result\.data\.\*\.values\.Direct Contact First Name | string |  `bmcremedy first name` 
action\_result\.data\.\*\.values\.Direct Contact Internet E\-mail | string | 
action\_result\.data\.\*\.values\.Direct Contact Last Name | string |  `bmcremedy last name` 
action\_result\.data\.\*\.values\.Direct Contact Local Number | string | 
action\_result\.data\.\*\.values\.Direct Contact Location Details | string | 
action\_result\.data\.\*\.values\.Direct Contact LoginID | string | 
action\_result\.data\.\*\.values\.Direct Contact Mail Station | string | 
action\_result\.data\.\*\.values\.Direct Contact Middle Initial | string | 
action\_result\.data\.\*\.values\.Direct Contact Organization | string | 
action\_result\.data\.\*\.values\.Direct Contact Phone Number | string | 
action\_result\.data\.\*\.values\.Direct Contact Region | string | 
action\_result\.data\.\*\.values\.Direct Contact Site | string | 
action\_result\.data\.\*\.values\.Direct Contact Site Group | string | 
action\_result\.data\.\*\.values\.Direct Contact Site ID | string | 
action\_result\.data\.\*\.values\.Direct Contact State/Province | string | 
action\_result\.data\.\*\.values\.Direct Contact Street | string | 
action\_result\.data\.\*\.values\.Direct Contact Time Zone | string | 
action\_result\.data\.\*\.values\.Direct Contact Zip/Postal Code | string | 
action\_result\.data\.\*\.values\.Extension Business | string | 
action\_result\.data\.\*\.values\.First\_Name | string |  `bmcremedy first name` 
action\_result\.data\.\*\.values\.Flag\_Create\_Request | string | 
action\_result\.data\.\*\.values\.Generic Categorization Tier 1 | string | 
action\_result\.data\.\*\.values\.Global\_OR\_Custom\_Mapping | string | 
action\_result\.data\.\*\.values\.HPD\_CI | string | 
action\_result\.data\.\*\.values\.HPD\_CI\_FormName | string | 
action\_result\.data\.\*\.values\.HPD\_CI\_ReconID | string | 
action\_result\.data\.\*\.values\.HPD\_TemplateName | string | 
action\_result\.data\.\*\.values\.Impact | string | 
action\_result\.data\.\*\.values\.Impact\_OR\_Root | string | 
action\_result\.data\.\*\.values\.Incident Number | string |  `bmcremedy incident id` 
action\_result\.data\.\*\.values\.Incident\_Entry\_ID | string | 
action\_result\.data\.\*\.values\.InfrastructureEventType | string | 
action\_result\.data\.\*\.values\.InstanceId | string | 
action\_result\.data\.\*\.values\.Internet E\-mail | string | 
action\_result\.data\.\*\.values\.KMSGUID | string | 
action\_result\.data\.\*\.values\.Last Modified By | string | 
action\_result\.data\.\*\.values\.Last\_Name | string |  `bmcremedy last name` 
action\_result\.data\.\*\.values\.Local Business | string | 
action\_result\.data\.\*\.values\.Login\_ID | string | 
action\_result\.data\.\*\.values\.Lookup Keyword | string | 
action\_result\.data\.\*\.values\.Mail Station | string | 
action\_result\.data\.\*\.values\.Manufacturer | string | 
action\_result\.data\.\*\.values\.MaxRetries | string | 
action\_result\.data\.\*\.values\.Middle Initial | string | 
action\_result\.data\.\*\.values\.Modified Chat Session ID | string | 
action\_result\.data\.\*\.values\.Modified Date | string | 
action\_result\.data\.\*\.values\.OptionForClosingIncident | string | 
action\_result\.data\.\*\.values\.Organization | string | 
action\_result\.data\.\*\.values\.Person ID | string | 
action\_result\.data\.\*\.values\.Person Instance ID | string | 
action\_result\.data\.\*\.values\.Phone\_Number | string | 
action\_result\.data\.\*\.values\.PortNumber | string | 
action\_result\.data\.\*\.values\.Priority | string | 
action\_result\.data\.\*\.values\.Priority Weight | numeric | 
action\_result\.data\.\*\.values\.Product Categorization Tier 1 | string | 
action\_result\.data\.\*\.values\.Product Categorization Tier 2 | string | 
action\_result\.data\.\*\.values\.Product Categorization Tier 3 | string | 
action\_result\.data\.\*\.values\.Product Model/Version | string | 
action\_result\.data\.\*\.values\.Product Name | string | 
action\_result\.data\.\*\.values\.Protocol | string | 
action\_result\.data\.\*\.values\.ReconciliationIdentity | string | 
action\_result\.data\.\*\.values\.Region | string | 
action\_result\.data\.\*\.values\.Reported Date | string | 
action\_result\.data\.\*\.values\.Reported Source | string | 
action\_result\.data\.\*\.values\.Request ID | string | 
action\_result\.data\.\*\.values\.Required Resolution DateTime | string | 
action\_result\.data\.\*\.values\.Resolution | string | 
action\_result\.data\.\*\.values\.Resolution Category Tier 1 | string | 
action\_result\.data\.\*\.values\.Resolution Category Tier 2 | string | 
action\_result\.data\.\*\.values\.Resolution Category Tier 3 | string | 
action\_result\.data\.\*\.values\.Resolution Method | string | 
action\_result\.data\.\*\.values\.SRID | string | 
action\_result\.data\.\*\.values\.SRInstanceID | string | 
action\_result\.data\.\*\.values\.SRMS Registry Instance ID | string | 
action\_result\.data\.\*\.values\.SRMSAOIGuid | string | 
action\_result\.data\.\*\.values\.Schema Name | string | 
action\_result\.data\.\*\.values\.ServiceCI | string | 
action\_result\.data\.\*\.values\.ServiceCI\_ReconID | string | 
action\_result\.data\.\*\.values\.Service\_Type | string | 
action\_result\.data\.\*\.values\.Short Description | string | 
action\_result\.data\.\*\.values\.Site | string | 
action\_result\.data\.\*\.values\.Site Group | string | 
action\_result\.data\.\*\.values\.Site ID | string | 
action\_result\.data\.\*\.values\.State Province | string | 
action\_result\.data\.\*\.values\.Status | string | 
action\_result\.data\.\*\.values\.Status History | string | 
action\_result\.data\.\*\.values\.Status History\.Assigned\.timestamp | string | 
action\_result\.data\.\*\.values\.Status History\.Assigned\.user | string | 
action\_result\.data\.\*\.values\.Status History\.Cancelled\.timestamp | string | 
action\_result\.data\.\*\.values\.Status History\.Cancelled\.user | string | 
action\_result\.data\.\*\.values\.Status History\.Closed\.timestamp | string | 
action\_result\.data\.\*\.values\.Status History\.Closed\.user | string | 
action\_result\.data\.\*\.values\.Status History\.In Progress\.timestamp | string | 
action\_result\.data\.\*\.values\.Status History\.In Progress\.user | string | 
action\_result\.data\.\*\.values\.Status History\.New\.timestamp | string | 
action\_result\.data\.\*\.values\.Status History\.New\.user | string | 
action\_result\.data\.\*\.values\.Status History\.Pending\.timestamp | string | 
action\_result\.data\.\*\.values\.Status History\.Pending\.user | string | 
action\_result\.data\.\*\.values\.Status History\.Resolved\.timestamp | string | 
action\_result\.data\.\*\.values\.Status History\.Resolved\.user | string | 
action\_result\.data\.\*\.values\.Status\_Reason | string | 
action\_result\.data\.\*\.values\.Street | string | 
action\_result\.data\.\*\.values\.Submitter | string | 
action\_result\.data\.\*\.values\.TemplateID | string | 
action\_result\.data\.\*\.values\.TemplateID2 | string | 
action\_result\.data\.\*\.values\.Time Zone | string | 
action\_result\.data\.\*\.values\.Unavailability Type | string | 
action\_result\.data\.\*\.values\.Unavailability\_Priority | string | 
action\_result\.data\.\*\.values\.Unknown User | string | 
action\_result\.data\.\*\.values\.Urgency | string | 
action\_result\.data\.\*\.values\.VIP | string | 
action\_result\.data\.\*\.values\.Vendor Assignee Groups | string | 
action\_result\.data\.\*\.values\.Vendor Assignee Groups\_parent | string | 
action\_result\.data\.\*\.values\.Vendor Group | string | 
action\_result\.data\.\*\.values\.Vendor Group ID | string | 
action\_result\.data\.\*\.values\.Vendor Name | string | 
action\_result\.data\.\*\.values\.Vendor Organization | string | 
action\_result\.data\.\*\.values\.Vendor Ticket Number | string | 
action\_result\.data\.\*\.values\.Zip/Postal Code | string | 
action\_result\.data\.\*\.values\.bOrphanedRoot | string | 
action\_result\.data\.\*\.values\.cell\_name | string | 
action\_result\.data\.\*\.values\.first\_name2 | string |  `bmcremedy first name` 
action\_result\.data\.\*\.values\.last\_name2 | string |  `bmcremedy last name` 
action\_result\.data\.\*\.values\.mc\_ueid | string | 
action\_result\.data\.\*\.values\.policy\_name | string | 
action\_result\.data\.\*\.values\.policy\_type | string | 
action\_result\.data\.\*\.values\.root\_component\_id\_list | string | 
action\_result\.data\.\*\.values\.root\_incident\_id\_list | string | 
action\_result\.data\.\*\.values\.status\_incident | string | 
action\_result\.data\.\*\.values\.status\_reason2 | string | 
action\_result\.data\.\*\.values\.use\_case | string | 
action\_result\.data\.\*\.values\.z1D Char01 | string | 
action\_result\.data\.\*\.values\.z1D Permission Group ID | string | 
action\_result\.data\.\*\.values\.z1D Permission Group List | string | 
action\_result\.data\.\*\.values\.z1D\_Action | string | 
action\_result\.data\.\*\.values\.z1D\_ActivityDate\_tab | string | 
action\_result\.data\.\*\.values\.z1D\_Activity\_Type | string | 
action\_result\.data\.\*\.values\.z1D\_Area\_Business | string | 
action\_result\.data\.\*\.values\.z1D\_CC\_Business | string | 
action\_result\.data\.\*\.values\.z1D\_CIUAAssignGroup | string | 
action\_result\.data\.\*\.values\.z1D\_CIUASupportCompany | string | 
action\_result\.data\.\*\.values\.z1D\_CIUASupportOrg | string | 
action\_result\.data\.\*\.values\.z1D\_CI\_FormName | string | 
action\_result\.data\.\*\.values\.z1D\_Char02 | string | 
action\_result\.data\.\*\.values\.z1D\_Command | string | 
action\_result\.data\.\*\.values\.z1D\_CommunicationSource | string | 
action\_result\.data\.\*\.values\.z1D\_ConfirmGroup | string | 
action\_result\.data\.\*\.values\.z1D\_CreatedFromBackEndSynchWI | string | 
action\_result\.data\.\*\.values\.z1D\_DC\_AreaCode | string | 
action\_result\.data\.\*\.values\.z1D\_DC\_CountryCode | string | 
action\_result\.data\.\*\.values\.z1D\_DC\_Extension | string | 
action\_result\.data\.\*\.values\.z1D\_DC\_Internet\_Email | string | 
action\_result\.data\.\*\.values\.z1D\_DC\_LocalNumber | string | 
action\_result\.data\.\*\.values\.z1D\_DC\_Phone\_Number | string | 
action\_result\.data\.\*\.values\.z1D\_Details | string | 
action\_result\.data\.\*\.values\.z1D\_Direct Contact Person ID | string | 
action\_result\.data\.\*\.values\.z1D\_Extension\_Business | string | 
action\_result\.data\.\*\.values\.z1D\_Internet\_Email | string | 
action\_result\.data\.\*\.values\.z1D\_Local\_Business | string | 
action\_result\.data\.\*\.values\.z1D\_PersonInfo | string | 
action\_result\.data\.\*\.values\.z1D\_Person\_Match\_Found | string | 
action\_result\.data\.\*\.values\.z1D\_Phone\_Number | string | 
action\_result\.data\.\*\.values\.z1D\_SRMInteger | string | 
action\_result\.data\.\*\.values\.z1D\_Secure\_Log | string | 
action\_result\.data\.\*\.values\.z1D\_SupportGroupID | string | 
action\_result\.data\.\*\.values\.z1D\_UAAssignmentMethod | string | 
action\_result\.data\.\*\.values\.z1D\_View\_Access | string | 
action\_result\.data\.\*\.values\.z1D\_WorklogDetails | string | 
action\_result\.data\.\*\.values\.z2AF\_Act\_Attachment\_1 | string | 
action\_result\.data\.\*\.values\.z2AF\_Act\_Attachment\_1\.href | string | 
action\_result\.data\.\*\.values\.z2AF\_Act\_Attachment\_1\.name | string | 
action\_result\.data\.\*\.values\.z2AF\_Act\_Attachment\_1\.sizeBytes | string | 
action\_result\.data\.\*\.values\.zTmpEventGUID | string | 
action\_result\.summary\.incident\_id | string |  `bmcremedy incident id` 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update ticket'
Update an existing incident

Type: **generic**  
Read only: **False**

This action can be used to assign an incident to a user\. Use the <b>fields</b> parameter to set the <b>Status</b>, <b>Assignee Login ID</b> and <b>Assignee</b> values\. For example\: To assign an incident to the user <b>User</b> set the <b>fields</b> parameter to \{"Status"\: "Assigned", "Assignee Login ID"\: "User", "Assignee"\: "User Name"\}<br><b>Note\:</b> Only single JSON formatted dictionary is allowed in <b>fields</b> action parameter<br>To add comment set <b>fields</b> parameter to \{"Work Log Type"\: "General Information", "Detailed Description"\: "Comment to add"\}\.<br>The attachment should be placed in vault of the container from which the action will be executed, and it would appear in <b>Work Detail</b> section on BMC Remedy\.<br>Typical \(default installation\) values for <b>work\_info\_type</b> are\:<ul><li>Customer Inbound\:<ul><li>Customer Communication</li><li>Customer Follow\-up</li><li>Customer Status Update</li></ul></li><li>Customer Outbound<ul><li>Closure Follow Up</li><li>Detail Clarification</li><li>General Information</li><li>Resolution Communications</li><li>Satisfaction Survey</li><li>Status Update</li></ul></li><li>General<ul><li>Incident Task / Action</li><li>Problem Script</li><li>Working Log</li><li>Email System</li><li>Paging System</li><li>BMC Impact Manager Update</li><li>Chat</li></ul></li><li>Vendor<ul><li>Vendor Communication</li></ul></li></ul>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 
**work\_info\_type** |  optional  | Work Info Type | string | 
**fields** |  optional  | Fields \(JSON format\) | string | 
**vault\_id** |  optional  | Comma \(','\) separated vault ID \(maximum 3\) | string |  `vault id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.fields | string | 
action\_result\.parameter\.id | string |  `bmcremedy incident id` 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.parameter\.work\_info\_type | string | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get ticket'
Get incident information

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.id | string |  `bmcremedy incident id` 
action\_result\.data\.\*\.\_links\.self\.\*\.href | string | 
action\_result\.data\.\*\.entries\.\*\.\_links\.self\.\*\.href | string | 
action\_result\.data\.\*\.entries\.\*\.values\.AccessMode | string | 
action\_result\.data\.\*\.entries\.\*\.values\.AppInstanceServer | string | 
action\_result\.data\.\*\.entries\.\*\.values\.AppInterfaceForm | string | 
action\_result\.data\.\*\.entries\.\*\.values\.AppLogin | string | 
action\_result\.data\.\*\.entries\.\*\.values\.AppPassword | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assigned Group | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assigned Group ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assigned Group Shift ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assigned Group Shift Name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assigned Support Company | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assigned Support Organization | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assignee | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assignee Groups | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assignee Groups\_parent | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Assignee Login ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.AttachmentSourceFormName | string | 
action\_result\.data\.\*\.entries\.\*\.values\.AttachmentSourceGUID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Auto Open Session | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Broker Vendor Name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Categorization Tier 1 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Categorization Tier 2 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Categorization Tier 3 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Chat Session ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.City | string | 
action\_result\.data\.\*\.entries\.\*\.values\.ClientLocale | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Closed Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Closure Manufacturer | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Closure Product Category Tier1 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Closure Product Category Tier2 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Closure Product Category Tier3 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Closure Product Model/Version | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Closure Product Name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Company | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Component\_ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Contact Client Type | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Contact Company | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Contact Sensitivity | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Corporate ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Country | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Created\_By | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Customer Login ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Department | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Description | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Desk Location | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Detailed Decription | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Area Code | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact City | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Company | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Corporate ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Country | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Country Code | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Department | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Desk Location | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Extension | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact First Name | string |  `bmcremedy first name` 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Internet E\-mail | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Last Name | string |  `bmcremedy last name` 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Local Number | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Location Details | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Login ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Mail Station | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Middle Initial | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Organization | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Person ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Phone Number | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Region | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Site | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Site Group | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Site ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact State/Province | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Street | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Time Zone | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Direct Contact Zip/Postal Code | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Entry ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Estimated Resolution Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.First Name | string |  `bmcremedy first name` 
action\_result\.data\.\*\.entries\.\*\.values\.FirstWIPDate | string | 
action\_result\.data\.\*\.entries\.\*\.values\.HPD\_CI | string | 
action\_result\.data\.\*\.entries\.\*\.values\.HPD\_CI\_FormName | string | 
action\_result\.data\.\*\.entries\.\*\.values\.HPD\_CI\_ReconID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Impact | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Impact\_OR\_Root | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Incident Number | string |  `bmcremedy incident id` 
action\_result\.data\.\*\.entries\.\*\.values\.InfrastructureEventType | string | 
action\_result\.data\.\*\.entries\.\*\.values\.InstanceId | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Internet E\-mail | string | 
action\_result\.data\.\*\.entries\.\*\.values\.KMSGUID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Last Acknowledged Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Last Modified By | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Last Modified Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Last Name | string |  `bmcremedy last name` 
action\_result\.data\.\*\.entries\.\*\.values\.Last Resolved Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Last \_Assigned\_Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.LastWIPDate | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Mail Station | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Manufacturer | string | 
action\_result\.data\.\*\.entries\.\*\.values\.MaxRetries | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Middle Initial | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Modified Chat Session ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Number of Attachments | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Organization | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Owner Group | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Owner Group ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Owner Support Company | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Owner Support Organization | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Person ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Phone Number | string | 
action\_result\.data\.\*\.entries\.\*\.values\.PortNumber | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Previous\_HPD\_CI\_ReconID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Previous\_ServiceCI\_ReconID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Priority | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Priority Weight | numeric | 
action\_result\.data\.\*\.entries\.\*\.values\.Product Categorization Tier 1 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Product Categorization Tier 2 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Product Categorization Tier 3 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Product Model/Version | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Product Name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Protocol | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Region | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Reported Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Reported Source | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Request ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Required Resolution DateTime | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Resolution | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Resolution Category | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Resolution Category Tier 2 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Resolution Category Tier 3 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Resolution Method | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Responded Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRAttachment | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRAttachment\.href | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRAttachment\.name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRAttachment\.sizeBytes | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRInstanceID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRMS Registry Instance ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.SRMSAOIGuid | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Service Type | string | 
action\_result\.data\.\*\.entries\.\*\.values\.ServiceCI | string | 
action\_result\.data\.\*\.entries\.\*\.values\.ServiceCI\_ReconID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Site | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Site Group | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Site ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.State Province | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Assigned\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Assigned\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Cancelled\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Cancelled\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Closed\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Closed\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.In Progress\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.In Progress\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.New\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.New\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Pending\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Pending\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Resolved\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status History\.Resolved\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status\-History\.Assigned\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status\-History\.Assigned\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status\-History\.In Progress\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status\-History\.In Progress\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status\-History\.New\.timestamp | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status\-History\.New\.user | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Status\_Reason | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Street | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Submit Date | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Submitter | string | 
action\_result\.data\.\*\.entries\.\*\.values\.TemplateID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.TimeOfEvent | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Total Transfers | numeric | 
action\_result\.data\.\*\.entries\.\*\.values\.Urgency | string | 
action\_result\.data\.\*\.entries\.\*\.values\.VIP | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Vendor Assignee Groups | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Vendor Assignee Groups\_parent | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Vendor Group | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Vendor Group ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Vendor Name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Vendor Organization | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Vendor Ticket Number | string | 
action\_result\.data\.\*\.entries\.\*\.values\.Zip/Postal Code | string | 
action\_result\.data\.\*\.entries\.\*\.values\.bOrphanedRoot | string | 
action\_result\.data\.\*\.entries\.\*\.values\.cell\_name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.mc\_ueid | string | 
action\_result\.data\.\*\.entries\.\*\.values\.policy\_name | string | 
action\_result\.data\.\*\.entries\.\*\.values\.policy\_type | string | 
action\_result\.data\.\*\.entries\.\*\.values\.root\_component\_id\_list | string | 
action\_result\.data\.\*\.entries\.\*\.values\.root\_incident\_id\_list | string | 
action\_result\.data\.\*\.entries\.\*\.values\.status\_incident | string | 
action\_result\.data\.\*\.entries\.\*\.values\.status\_reason2 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.use\_case | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D Action | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D Char01 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D Char02 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D Permission Group ID | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D Permission Group List | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_ActivityDate\_tab | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_Activity\_Type | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_AssociationDescription | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_CI\_FormName | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_Char02 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_Command | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_CommunicationSource | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_ConfirmGroup | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_CreatedFromBackEndSynchWI | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_Details | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_FormName | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_InterfaceAction | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_SR\_Instanceid | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_Secure\_Log | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_Summary | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_View\_Access | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_WorkInfoSubmitter | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z1D\_WorklogDetails | string | 
action\_result\.data\.\*\.entries\.\*\.values\.z2AF\_Act\_Attachment\_1 | string | 
action\_result\.data\.\*\.entries\.\*\.values\.zTmpEventGUID | string | 
action\_result\.data\.\*\.work\_details\.\_links\.self\.\*\.href | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.\_links\.self\.\*\.href | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assign WorkLog Flag | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assigned Group | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assigned Group ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assigned Group Shift ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assigned Group Shift Name | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assigned Support Company | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assigned Support Organization | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assigned To | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assignee | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assignee Groups | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assignee Groups\_parent | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assignee Login ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Assignment Log Created | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.AttachmentSourceFormName | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.AttachmentSourceGUID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Broker Vendor Name | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.ClientLocale | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Communication Source | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Communication Type | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Company | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.DataTags | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Description | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Detailed Description | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.HPD Attachment ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Incident Entry ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Incident Number | string |  `bmcremedy incident id` 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.InstanceId | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Last Modified By | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Last Modified Date | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Number of Attachments | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Number of URLs | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.SR\_Instanceid | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Secure Work Log | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Shared With Vendor | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Shifts Flag | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Short Description | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Status | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Status History | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Submit Date | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Submitter | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Thumbnail 1 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Thumbnail 2 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Thumbnail 3 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Total Time Spent | numeric | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.URL01 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.URL02 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.URL03 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Vendor Assignee Groups | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Vendor Assignee Groups\_parent | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.View Access | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Work Log Date | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Work Log ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Work Log Submit Date | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Work Log Submitter | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.Work Log Type | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.WorkLog Action Completed | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.WorkLog Action Status | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Action | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Action02 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char01 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char02 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char03 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char04 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char05 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char06 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char07 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char08 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char09 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char10 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char11 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char12 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char13 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char14 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char15 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Char16 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Close Dialog | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Integer01 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Integer02 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Integer03 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Integer04 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Last Date Duration Calc | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Lastcount | numeric | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Lastcount02 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Mobile Worklog Upd2 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Page Indicator | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Permission Group ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Permission Group List | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Previous Operation | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D QuickViewWlg Flag | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Status\-INC | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D Work Log ID | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_AttachedFileName | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_ConfirmGroup | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_FileNameAttach2 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_FileNameAttach3 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_PrefixHolder | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_PrefixResult | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_SkipIfSmartITInstalled | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_WorkInfo\_FileDefaultMsg | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1D\_WorkInfo\_NotesLabel | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G Disable Worklog Action | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G Enable French | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G Enable German | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G Enable Spanish | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G Enable User Defined 1 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G Enable User Defined 2 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G InitComplete | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G Multi\-language | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G\_HelpDeskIDPrefix | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z1G\_Use\_Custom\_Prefix | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log01 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log01\.href | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log01\.name | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log01\.sizeBytes | numeric | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log02 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log02\.href | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log02\.name | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log02\.sizeBytes | numeric | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log03 | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log03\.href | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log03\.name | string | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.z2AF Work Log03\.sizeBytes | numeric | 
action\_result\.data\.\*\.work\_details\.entries\.\*\.values\.zTmpEventGUID | string | 
action\_result\.summary\.ticket\_availability | boolean | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list tickets'
Get list of incidents

Type: **investigate**  
Read only: **True**

<p>The action supports limiting the number of incidents returned using the <b>limit</b> parameter\. The input should be a positive integer\. The results are always sorted in descending order based on their last modified date to place the latest modified incidents at the top\. For example to get the latest 10 incidents that matched the filter, specify the limit as 10\. If <b>limit</b> is zero or not specified, then all incidents will be returned\.</p><p>To define a set of criteria to filter incidents, query must be provided in <b>query</b> parameter\.<br>Query must contain field label enclosed in single quotation marks\(''\), and non\-numeric values in double quotation marks\(""\)\.<br>Eg\: <b>'Incident Number'="INC000000000001", 'Submit Date'="February 20, 2017"</b><br>If a field name contains single quotation mark, add another single quotation mark next to it\.<br>Eg\: If field name is <b>Submitter's Phone Number</b>, query must contain field label as <b>'Submitter''s Phone Number'</b><br>More information about using fields in <b>query</b> parameter can be found on <a href="https\://docs\.bmc\.com/docs/ars2008/using\-fields\-in\-the\-advanced\-search\-bar\-928611932\.html\#Usingfieldsintheadvancedsearchbar\-4Usingvaluesintheadvancedsearchbar" target='\_blank'>Fields in query</a>\.<br>Query can accept various operators such as\:<br><ol><li><b>Relational and Logical Operators</b>\:<ul><li>Relational and Logical operators are useful especially in non\-text fields \(such as date and time fields\) when you want to search for a value within a numerical range\.</li><li>Some of the examples are as follows\:<br><b>\('Submitter'="admin"\) AND \(NOT 'Incident Number'="INC000000000001"\)</b><br><b>'Impact'="1\-Extensive/Widespread" OR 'Urgency'="1\-Critical"</b><br><b>'Incident Number' = "INC000000000001"</b><br><b>'Status' \!= "Closed"</b><br><b>'Submit Date' > "February 28, 2017"</b></li><li>More information about relational and logical operators can be found at <a href="https\://docs\.bmc\.com/docs/ars2008/using\-relational\-operators\-in\-the\-advanced\-search\-bar\-928611933\.html" target='\_blank'>Relational and logical Operators link</a>\.</li></ul></li><li><b>Keywords in query</b>\:<ul><li>Keywords can be used anywhere where character values are accepted\.</li><li>Most commonly used keywords are\: <b>$DATE$</b>, <b>$NULL$</b>, <b>$TIME$</b>, <b>$TIMESTAMP$</b>, <b>$USER$</b>, and <b>$WEEKDAY$</b>\.</li><li>Some of the examples are as follows\:<br><b>'Assignee' = $NULL$</b><br><b>'Create date' < \($TIMESTAMP$ \- 24\*60\*60\)</b></li><li>More information about Keywords can be found at <a href="https\://docs\.bmc\.com/docs/ars2008/using\-fields\-in\-the\-advanced\-search\-bar\-928611932\.html\#Usingfieldsintheadvancedsearchbar\-4Usingvaluesintheadvancedsearchbar" target='\_blank'>Keywords link</a>\.</li></ul></li><li><b>Wildcard symbols</b>\:<ul><li>Wildcard symbols can be used to indicate one or more characters\.</li><li>Wildcard symbols that can be used in query are\: <b>%</b>, <b>\_</b>, <b>\-</b>, <b>\[\]</b>, <b>\[^\]</b></li><li>Some of the examples are as follows\:<br><b>'Submitter' LIKE "\*Bob%ton\*"</b><br><b>'Phone Number' LIKE "\_ 212 5555454 \(66\)"</b></li><li>More information about wildcard symbols can be found at <a href="https\://docs\.bmc\.com/docs/ars2008/using\-relational\-operators\-and\-wildcard\-symbols\-in\-a\-search\-928611919\.html\#Usingrelationaloperatorsandwildcardsymbolsinasearch\-281729" target='\_blank'>Wildcard symbols link</a>\.</li></ul></li></ol>More information about BMC Remedy Query Syntax can be found at <a href="https\://docs\.bmc\.com/docs/ars2008/using\-the\-advanced\-search\-bar\-928611931\.html" target='\_blank'>Query Syntax link</a>\.</p>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** |  optional  | Additional parameters to query | string | 
**limit** |  optional  | Maximum number of incidents to return | numeric | 
**offset** |  optional  | Set the starting point or offset for the response\. The default value is 0 | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.offset | numeric | 
action\_result\.parameter\.query | string | 
action\_result\.data\.\*\.\_links\.next\.\*\.href | string | 
action\_result\.data\.\*\.\_links\.self\.\*\.href | string | 
action\_result\.data\.\*\.values\.Assigned Group | string | 
action\_result\.data\.\*\.values\.Assignee | string | 
action\_result\.data\.\*\.values\.Description | string | 
action\_result\.data\.\*\.values\.First Name | string |  `bmcremedy first name` 
action\_result\.data\.\*\.values\.Incident Number | string |  `bmcremedy incident id` 
action\_result\.data\.\*\.values\.Last Name | string |  `bmcremedy last name` 
action\_result\.data\.\*\.values\.Priority | string | 
action\_result\.data\.\*\.values\.Status | string | 
action\_result\.summary\.total\_tickets | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'set status'
Set incident status

Type: **generic**  
Read only: **False**

Typical \(default installation\) values for <b>status</b> are\:<ul><li>New</li><li>Assigned</li><li>In Progress</li><li>Pending</li><li>Resolved</li><li>Closed</li><li>Cancelled</li></ul>Typical \(default installation\) values of <b>status\_reason</b> for a given <b>status</b> are\:<ul><li>Pending<ul><li>Automated Resolution Reported</li><li>Client Action Required</li><li>Client Hold</li><li>Future Enhancement</li><li>Infrastructure Change</li><li>Local Site Action Required</li><li>Monitoring Incident</li><li>Purchase Order Approval</li><li>Registration Approval</li><li>Request</li><li>Supplier Delivery</li><li>Support Contact Hold</li><li>Third Party Vendor Action Reqd</li></ul></li><li>Resolved<ul><li>Automated Resolution Reported</li><li>Customer Follow\-Up Required</li><li>Future Enhancement</li><li>Monitoring Incident</li><li>No Further Action Required</li><li>Temporary Corrective Action</li></ul></li><li>Closed<ul><li>Automated Resolution Reported</li><li>Infrastructure Change Created</li></ul></li><li>Cancelled<ul><li>No longer a Causal CI</li></ul></li></ul>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 
**status** |  required  | Status | string | 
**assignee\_login\_id** |  optional  | Login ID of assignee | string | 
**assignee** |  optional  | Assignee | string | 
**assigned\_support\_company** |  optional  | Assigned Support Company | string | 
**assigned\_support\_organization** |  optional  | Assigned Support Organization | string | 
**assigned\_group** |  optional  | Assigned Group | string | 
**status\_reason** |  optional  | Status Reason | string | 
**resolution** |  optional  | Resolution | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.assigned\_group | string | 
action\_result\.parameter\.assigned\_support\_company | string | 
action\_result\.parameter\.assigned\_support\_organization | string | 
action\_result\.parameter\.assignee | string | 
action\_result\.parameter\.assignee\_login\_id | string | 
action\_result\.parameter\.id | string |  `bmcremedy incident id` 
action\_result\.parameter\.resolution | string | 
action\_result\.parameter\.status | string | 
action\_result\.parameter\.status\_reason | string | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add comment'
Add work log information to the incident

Type: **generic**  
Read only: **False**

Typical \(default installation\) values for <b>work\_info\_type</b> are\:<ul><li>Customer Inbound\:<ul><li>Customer Communication</li><li>Customer Follow\-up</li><li>Customer Status Update</li></ul></li><li>Customer Outbound<ul><li>Closure Follow Up</li><li>Detail Clarification</li><li>General Information</li><li>Resolution Communications</li><li>Satisfaction Survey</li><li>Status Update</li></ul></li><li>General<ul><li>Incident Task / Action</li><li>Problem Script</li><li>Working Log</li><li>Email System</li><li>Paging System</li><li>BMC Impact Manager Update</li><li>Chat</li></ul></li><li>Vendor<ul><li>Vendor Communication</li></ul></li></ul>Typical \(default installation\) values for <b>secure\_work\_log</b> are\:<ul><li>Yes</li><li>No</li></ul>Typical \(default installation\) values for <b>view\_access</b> are\:<ul><li>Internal</li><li>Public</li></ul>If the user provides 'description' and 'comment' as input parameters, the priority will be given to 'comment'\. so, under the notes section of a particular incident the value of 'comment' will be displayed\. If the user provides either 'description' or 'comment', the given input value will be displayed under the notes section\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `bmcremedy incident id` 
**work\_info\_type** |  required  | Work Info Type | string | 
**description** |  optional  | Worklog Description | string | 
**comment** |  optional  | Notes | string | 
**secure\_work\_log** |  optional  | Locked | string | 
**view\_access** |  optional  | View Access | string | 
**worklog\_submitter** |  optional  | Submit a worklog with a different username or email address | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.description | string | 
action\_result\.parameter\.id | string |  `bmcremedy incident id` 
action\_result\.parameter\.secure\_work\_log | string | 
action\_result\.parameter\.view\_access | string | 
action\_result\.parameter\.work\_info\_type | string | 
action\_result\.parameter\.worklog\_submitter | string | 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 