# File: bmcremedy_consts.py
#
# Copyright (c) 2017-2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#

BMCREMEDY_CONFIG_SERVER = "url"
BMCREMEDY_CONFIG_API_USERNAME = "username"
BMCREMEDY_CONFIG_API_PASSWORD = "password"  # pragma: allowlist secret
BMCREMEDY_CONFIG_CLIENT_ID = "client_id"
BMCREMEDY_CONFIG_CLIENT_SECRET = "client_secret"  # pragma: allowlist secret
BMCREMEDY_BASIC = "Basic"
BMCREMEDY_OAUTH = "BMC SSO (interactive)"
BMCREMEDY_CONFIG_SERVER_CERT = "verify_server_cert"
BMCREMEDY_CONFIG_AUTH_TYPE = "auth_type"
BMCREMEDY_REST_RESP_TOKEN_SUCCESS = 200
BMCREMEDY_REST_RESP_CREATE_SUCCESS = 201
BMCREMEDY_REST_RESP_NO_CONTENT = 204
BMCREMEDY_REST_RESP_BAD_REQUEST = 400
BMCREMEDY_REST_RESP_BAD_REQUEST_MESSAGE = "Bad Request"
BMCREMEDY_REST_RESP_UNAUTHORIZED = 401
BMCREMEDY_REST_RESP_UNAUTHORIZED_MESSAGE = "Unauthorized"
BMCREMEDY_REST_RESP_FORBIDDEN = 403
BMCREMEDY_REST_RESP_FORBIDDEN_MESSAGE = "Forbidden"
BMCREMEDY_REST_RESP_NOT_FOUND = 404
BMCREMEDY_REST_RESP_NOT_FOUND_MESSAGE = "Not found"
BMCREMEDY_REST_RESP_METHOD_NOT_ALLOWED = 405
BMCREMEDY_REST_RESP_METHOD_NOT_ALLOWED_MESSAGE = "Method not allowed"
BMCREMEDY_REST_RESP_INTERNAL_SERVER_ERROR = 500
BMCREMEDY_REST_RESP_INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error"
BMCREMEDY_ERROR_API_UNSUPPORTED_METHOD = "Unsupported method {method}"
BMCREMEDY_EXCEPTION_OCCURRED = "Exception occurred"
BMCREMEDY_TOKEN_ENDPOINT = "/api/jwt/login"
BMCREMEDY_ERROR_SERVER_CONNECTIVITY = "Connection failed"
BMC_ASSET_PARAM_CHECK_LIST_ERRORS = ["unauthorized_client", "invalid_client", "invalid_grant", "invalid_request"]
BMCREMEDY_ERROR_FROM_SERVER = "API failed. Status code: {status}. Details: {detail}"
BMCREMEDY_ERROR_JSON_PARSE = "Unable to parse the fields parameter into a dictionary.\nResponse text - {raw_text}"
BMCREMEDY_REST_RESP_OTHER_ERROR_MESSAGE = "Unknown error occurred"
BMCREMEDY_LIST_TICKETS = "/api/arsys/v1/entry/HPD:IncidentInterface?fields=values(Incident Number,First Name," \
                         "Last Name,Description,Status,Priority,Assigned Group,Assignee)"
BMCREMEDY_GET_TICKET = "/api/arsys/v1/entry/HPD:IncidentInterface"
BMCREMEDY_CREATE_TICKET = "/api/arsys/v1/entry/HPD:IncidentInterface_Create"
BMCREMEDY_COMMENT_ENDPOINT = "/api/arsys/v1/entry/HPD:WorkLog"
BMCREMEDY_SUMMARY_ERROR = "Error while summarizing {action_name} action"
BMCREMEDY_TEST_CONNECTIVITY_MESSAGE = "Querying endpoint to test connectivity"
BMCREMEDY_TEST_CONNECTIVITY_FAIL = "Connectivity test failed"
BMCREMEDY_TEST_CONNECTIVITY_PASS = "Connectivity test succeeded"
BMCREMEDY_LOCATION_NOT_FOUND = "Not able to find link to get the newly created incident"
BMCREMEDY_INCIDENT_NUMBER_NOT_FOUND = "Not able to find incident id"
BMCREMEDY_REQUIRED_PARAM_OAUTH = "ERROR: {0} is a required parameter for OAuth Authentication, please specify one."
BMCREMEDY_REQUIRED_PARAM_BASIC = "ERROR: {0} is a required parameter for Basic Authentication, please specify one."
BMCREMEDY_REQUIRED_PARAM_PORTS = "ERROR: {0} is a required parameter for OAuth Authentication and Action run, please specify in valid ports."
BMCREMEDY_JSON_LIMIT = "limit"
BMCREMEDY_JSON_QUERY = "query"
BMCREMEDY_JSON_OFFSET = 'offset'
BMCREMEDY_INCIDENT_NUMBER = "id"
BMCREMEDY_COMMENT_ACTIVITY_TYPE = "work_info_type"
BMCREMEDY_JSON_FIELDS = "fields"
BMCREMEDY_JSON_VAULT_ID = "vault_id"
BMCREMEDY_UNKNOWN_VAULT_ID = "Invalid or unknown vault ID"
BMCREMEDY_ATTACHMENT_LIMIT_EXCEED = "Maximum 3 attachments can be provided"
BMCREMEDY_DEFAULT_PAGE_LIMIT = 100
BMCREMEDY_DEFAULT_OFFSET = 0
BMCREMEDY_ENCODE_TEMPLATE_FILE = """--{boundary}
Content-Disposition: form-data; name="{name}"; filename="{filename}"
Content-Type: {contenttype}
Content-Transfer-Encoding: binary

{value}
""".replace('\n', '\r\n')
BMCREMEDY_ENCODE_TEMPLATE = """--{boundary}
Content-Transfer-Encoding: 8bit
Content-Type: application/json; charset=UTF-8
Content-Disposition: form-data; name="{name}"

{value}
""".replace('\n', '\r\n')
BMCREMEDY_URL_NOT_FOUND = "Update link not found for the given incident id"
BMCREMEDY_TOKEN_GENERATION_ERROR_MESSAGE = "Failed to generate token"
BMCREMEDY_ERROR_FETCHING_URL = "Error while fetching url: {error}"
BMCREMEDY_JSON_LOADS_ERROR = "Error while converting string to dictionary: {}"
BMCREMEDY_REST_CALL_ERROR = "Exception while making request: {error}"
BMCREMEDY_JSON_STATUS = "status"
BMCREMEDY_BLANK_PARAM_ERROR_SUBSTRING = "records have been found for the Incident contact information you have provided"
BMCREMEDY_CUSTOM_ERROR_MESSAGE = "\nThis can happen if required parameters are not specified in the action.\n"
BMCREMEDY_ADD_COMMENT_MESSAGE = "Comment added successfully"
BMCREMEDY_SET_STATUS_MESSAGE = "Set status successful"
BMCREMEDY_UPDATE_SUCCESSFUL_MESSAGE = "Incident updated successfully"
BMCREMEDY_GET_COMMENT_ERROR = "Error while getting comments for incident ID: {id}"
BMCREMEDY_ERROR_INVALID_FIELDS = "Please provide a valid value in the '{field}' parameter"
BMCREMEDY_ENCRYPTION_ERROR = "Error occurred while encrypting the state file"
BMCREMEDY_DECRYPTION_ERROR = "Error occurred while decrypting the state file"

# Constants relating to 'get_error_message_from_exception'
BMCREMEDY_ERROR_CODE_MESSAGE = "Error code unavailable"
BMCREMEDY_ERROR_UNAVAILABLE_MESSAGE = "Error message unavailable. Please check the asset configuration and|or action parameters."
BMCREMEDY_PARSE_ERROR_MESSAGE = "Unable to parse the error message. Please check the asset configuration and|or action parameters."

# Constants relating to 'validate_integer'
BMCREMEDY_VALID_INT_MESSAGE = "Please provide a valid integer value in the '{param}' parameter"
BMCREMEDY_NON_NEG_NON_ZERO_INT_MESSAGE = "Please provide a valid non-zero positive integer value in '{param}' parameter"
BMCREMEDY_NON_NEG_INT_MESSAGE = "Please provide a valid non-negative integer value in the '{param}' parameter"

BMCREMEDY_STATE_FILE_CORRUPT_ERROR = ("Error occurred while loading the state file due to its unexpected format. "
                                    "Resetting the state file with the default format. Please try again")
BMCREMEDY_FIELDS_PARAM_ERROR_MESSAGE = ("Please provide JSON formatted dictionary in the 'fields' action parameter "
                                  "e.g: {\"First_Name\": \"Customer First Name\", \"Last_Name\": \"Customer Last Name\", "
                                  "\"Description\": \"Incident Description\", \"Service_Type\": \"User Service Restoration\", "
                                  "\"Reported Source\": \"Direct Input\", \"Status\": \"Assigned\", "
                                  "\"Assignee Login ID\": \"User\", \"Assignee\": \"User Name\"}")

# Dictionary that maps each error code with its corresponding message
ERROR_RESPONSE_DICT = {
    BMCREMEDY_REST_RESP_BAD_REQUEST: BMCREMEDY_REST_RESP_BAD_REQUEST_MESSAGE,
    BMCREMEDY_REST_RESP_UNAUTHORIZED: BMCREMEDY_REST_RESP_UNAUTHORIZED_MESSAGE,
    BMCREMEDY_REST_RESP_FORBIDDEN: BMCREMEDY_REST_RESP_FORBIDDEN_MESSAGE,
    BMCREMEDY_REST_RESP_NOT_FOUND: BMCREMEDY_REST_RESP_NOT_FOUND_MESSAGE,
    BMCREMEDY_REST_RESP_METHOD_NOT_ALLOWED: BMCREMEDY_REST_RESP_METHOD_NOT_ALLOWED_MESSAGE,
    BMCREMEDY_REST_RESP_INTERNAL_SERVER_ERROR: BMCREMEDY_REST_RESP_INTERNAL_SERVER_ERROR_MESSAGE
}

# List containing http codes to be considered as success
SUCCESS_RESPONSE_CODES = [BMCREMEDY_REST_RESP_TOKEN_SUCCESS, BMCREMEDY_REST_RESP_CREATE_SUCCESS,
                          BMCREMEDY_REST_RESP_NO_CONTENT]

# List of parameters that will be considered for adding attachment to an incident
ADD_ATTACHMENT_PARAMS_LIST = ["Work Log Type", "View Access", "Secure Work Log", "Detailed Description"]

# Timeout
BMCREMEDY_DEFAULT_TIMEOUT = 30
