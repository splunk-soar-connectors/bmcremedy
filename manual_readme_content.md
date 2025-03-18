Incidents are typically categorized among following types:

- **User Service Restoration**
  - Typical ITIL (Information Technology Infrastructure Library) of incident.
- **User Service Request**
  - Used to identify incidents that are not related to ITIL definition.
- **Infrastructure Restoration**
  - ITIL definition, but more focused on CI (Configuration Item) restoration.
- **Infrastructure Event**
  - Used for integration for system management tools.

## Playbook Backward Compatibility

- A new action parameter has been added in the existing action. Hence, it is requested to the
  end-user to please update their existing playbooks by re-inserting | modifying | deleting the
  corresponding action blocks.

  - A 'offset' action parameter has been added in the 'list tickets' action

- The existing output data paths have been modified for the 'list tickets' action. Hence, it is
  requested to the end-user to please update their existing playbooks by re-inserting | modifying
  | deleting the corresponding action blocks to ensure the correct functioning of the playbooks
  created on the earlier versions of the app.

## Using a template for the create ticket action

In order to create a ticket from a pre-existing incident template in BMC remedy, the **fields**
action parameter can be used. Passing in a JSON such as,

```
{"TemplateID": "$templateid"}
```

Referencing an existing template id simplifies the ticket creation. For more information refer this
[document](https://docs.bmc.com/docs/bsr/35/creating-incidents-by-passing-a-template-reference-576950232.html#Creatingincidentsbypassingatemplatereference-instance_id)
.
