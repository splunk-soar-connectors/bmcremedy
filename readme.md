[comment]: # " File: readme.md"
[comment]: # ""
[comment]: # "  Copyright (c) 2019-2021 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under the Apache License, Version 2.0 (the \"License\");"
[comment]: # "  you may not use this file except in compliance with the License."
[comment]: # "  You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "      http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "  Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "  the License is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
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
    end-user to please update their existing playbooks by inserting \| modifying \| deleting the
    corresponding action blocks for this action on the earlier versions of the app.


    -   A 'offset' action parameter has been added in the 'list tickets' action

-   The existing output data paths have been modified for the 'list tickets' action. Hence, it is
    requested to the end-user to please update their existing playbooks by re-inserting \| modifying
    \| deleting the corresponding action blocks to ensure the correct functioning of the playbooks
    created on the earlier versions of the app.
