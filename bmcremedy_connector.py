# File: bmcremedy_connector.py
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

import json
import os
import re
import time

import encryption_helper
import phantom.app as phantom
import phantom.rules as ph_rules
import requests
from bs4 import BeautifulSoup
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

# Local imports
import bmcremedy_consts as consts
from request_handler import RequestStateHandler  # noqa
from request_handler import _get_dir_name_from_app_name


class RetVal3(tuple):
    def __new__(cls, val1, val2=None, val3=None):
        return tuple.__new__(RetVal3, (val1, val2, val3))


class BmcremedyConnector(BaseConnector):
    """ This is an AppConnector class that inherits the BaseConnector class.
    It implements various actions supported by BMC Remedy and helper methods required to run the actions.
    """

    def __init__(self):

        # Calling the BaseConnector's init function
        super(BmcremedyConnector, self).__init__()
        self._base_url = None
        self._api_username = None
        self._api_password = None
        self._verify_server_cert = None
        self._state = dict()
        self.rsh = None
        self.auth_type = None
        self._access_token = None
        self._refresh_token = None
        return

    def _decrypt_state(self, state, salt):
        """
        Decrypts the state.

        :param state: state dictionary
        :param salt: salt used for decryption
        :return: decrypted state
        """
        if not state.get("is_encrypted"):
            return state

        token = state.get("token")
        oauth_token = state.get("oauth_token")
        if token:
            state["token"] = encryption_helper.decrypt(token, salt)
        if oauth_token:
            token_list = ['access_token', 'id_token', 'refresh_token']
            for token_name in token_list:
                if state['oauth_token'].get(token_name):
                    state['oauth_token'][token_name] = encryption_helper.decrypt(  # pylint: disable=E1101
                        state['oauth_token'][token_name],
                        salt
                    )
        return state

    def _encrypt_state(self, state, salt):
        """
        Encrypts the state.

        :param state: state dictionary
        :param salt: salt used for encryption
        :return: encrypted state
        """

        token = state.get("token")
        oauth_token = state.get("oauth_token")
        if token:
            state["token"] = encryption_helper.encrypt(token, salt)
        if oauth_token:
            token_list = ['access_token', 'id_token', 'refresh_token']
            for token_name in token_list:
                if state['oauth_token'].get(token_name):
                    state['oauth_token'][token_name] = encryption_helper.encrypt(  # pylint: disable=E1101
                        state['oauth_token'][token_name],
                        salt
                    )
            state[consts.BMCREMEDY_CONFIG_CLIENT_ID] = self.get_config()[consts.BMCREMEDY_CONFIG_CLIENT_ID]
        state["is_encrypted"] = True

        return state

    def load_state(self):
        """
        Load the contents of the state file to the state dictionary and decrypt it.

        :return: loaded state
        """
        state = super().load_state()
        # if not isinstance(state, dict):
        #     self.debug_print("Resetting the state file with the default format")
        #     state = {
        #         "app_version": self.get_app_json().get('app_version')
        #     }
        #     return state
        try:
            state = self._decrypt_state(state, self.get_asset_id())
        except Exception as e:
            self.error_print(consts.BMCREMEDY_DECRYPTION_ERROR, e)
            state = None

        return state

    def save_state(self, state):
        """
        Encrypt and save the current state dictionary to the the state file.

        :param state: state dictionary
        :return: status
        """
        try:
            state = self._encrypt_state(state, self.get_asset_id())
        except Exception as e:
            self.error_print(consts.BMCREMEDY_ENCRYPTION_ERROR, e)
            return phantom.APP_ERROR

        return super().save_state(state)

    def initialize(self):
        """ This is an optional function that can be implemented by the AppConnector derived class. Since the
        configuration dictionary is already validated by the time this function is called, it's a good place to do any
        extra initialization of any internal modules. This function MUST return a value of either phantom.APP_SUCCESS or
        phantom.APP_ERROR. If this function returns phantom.APP_ERROR, then AppConnector::handle_action will not get
        called.
        """

        config = self.get_config()

        # Initialize configuration parameters
        self._base_url = config[consts.BMCREMEDY_CONFIG_SERVER].strip('/')
        self._api_username = config.get(consts.BMCREMEDY_CONFIG_API_USERNAME)
        self._api_password = config.get(consts.BMCREMEDY_CONFIG_API_PASSWORD)
        self._verify_server_cert = config.get(consts.BMCREMEDY_CONFIG_SERVER_CERT, False)
        self.rsh = RequestStateHandler(self.get_asset_id())
        self.auth_type = config.get(consts.BMCREMEDY_CONFIG_AUTH_TYPE, consts.BMCREMEDY_BASIC)
        test_asset_connectivity_oauth = False

        # Load any saved configurations
        self._state = self.load_state()
        if not isinstance(self._state, dict):
            self.debug_print("Resetting the state file with the default format")
            self._state = {"app_version": self.get_app_json().get("app_version")}
            if self.auth_type == consts.BMCREMEDY_OAUTH:
                return self.set_status(phantom.APP_ERROR, consts.BMCREMEDY_STATE_FILE_CORRUPT_ERROR)

        if len(config.get("ports").split(',')) != 2:
            return self.set_status(phantom.APP_ERROR, consts.BMCREMEDY_REQUIRED_PARAM_PORTS.format("ports"))

        if self.auth_type == consts.BMCREMEDY_BASIC:
            required_params = ["username", "password"]
            for key in required_params:
                if not config.get(key):
                    return self.set_status(phantom.APP_ERROR, consts.BMCREMEDY_REQUIRED_PARAM_BASIC.format(key))
            if self.get_action_identifier() != phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY:
                if not self._state.get("token", False):
                    return self.set_status(phantom.APP_ERROR, "Required tokens not found in state file. Please run test connectivity first...")
        elif self.auth_type == consts.BMCREMEDY_OAUTH:
            required_params = [consts.BMCREMEDY_CONFIG_CLIENT_ID, consts.BMCREMEDY_CONFIG_CLIENT_SECRET]
            for key in required_params:
                if not config.get(key):
                    return self.set_status(phantom.APP_ERROR, consts.BMCREMEDY_REQUIRED_PARAM_OAUTH.format(key))
            if self.get_action_identifier() == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY:
                test_asset_connectivity_oauth = True
            else:
                if not self._state.get("oauth_token", False):
                    return self.set_status(phantom.APP_ERROR, "Required tokens not found in state file. Please run test connectivity first...")
        else:
            return self.set_status(phantom.APP_ERROR, "Please provide a valid authentication mechanism to use")

        if test_asset_connectivity_oauth:
            self._base_url += f':{config.get("ports").split(",")[1].strip()}'
        else:
            self._base_url += f':{config.get("ports").split(",")[0].strip()}'

        self.is_oauth_token_exist = self.auth_type in [consts.BMCREMEDY_OAUTH] and \
            not self._state.get("oauth_token", {}).get("access_token")
        self._is_client_id_changed = (self._state.get(consts.BMCREMEDY_CONFIG_CLIENT_ID) and config.get(consts.BMCREMEDY_CONFIG_CLIENT_ID)) and \
            self._state.get(consts.BMCREMEDY_CONFIG_CLIENT_ID) != config.get(consts.BMCREMEDY_CONFIG_CLIENT_ID)

        # Return response_status
        return phantom.APP_SUCCESS

    def _check_login_status(self, response):

        if not hasattr(response, 'headers'):
            return phantom.APP_ERROR, "Response missing headers, cannot determine success"
            # return action_result.set_status(phantom.APP_ERROR, "Response missing headers, cannot determine success")

        x_ar_messages = response.headers.get('x-ar-messages')
        if not x_ar_messages:
            return phantom.APP_SUCCESS

        # will need to parse the messages
        try:
            x_ar_messages = json.loads(x_ar_messages)
        except Exception as e:
            return phantom.APP_ERROR, "Unable to process X-AR-Messages. Exception - {}".format(e)
            # return action_result.set_status(phantom.APP_ERROR, "Unable to process X-AR-Messages")

        for curr_msg_dict in x_ar_messages:
            message_text = curr_msg_dict.get('messageText')
            if not message_text:
                continue
            if 'login failed' in message_text.lower():
                return phantom.APP_ERROR, "Login failed, please check your credentials"
                # return action_result.set_status(phantom.APP_ERROR, "Login failed, please check your credentials")

        return phantom.APP_SUCCESS

    def _get_error_message_from_exception(self, e):
        """ This method is used to get appropriate error message from the exception.
        :param e: Exception object
        :return: error message
        """

        error_code = None
        error_message = consts.BMCREMEDY_ERROR_UNAVAILABLE_MESSAGE

        self.error_print("Error occurred.", e)

        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_message = e.args[1]
                elif len(e.args) == 1:
                    error_message = e.args[0]
        except Exception as e:
            self.error_print("Error occurred while fetching exception information. Details: {}".format(str(e)))

        if not error_code:
            error_text = "Error Message: {}".format(error_message)
        else:
            error_text = "Error Code: {}. Error Message: {}".format(error_code, error_message)

        return error_text

    def _validate_integer(self, action_result, parameter, key, allow_zero=False):
        """
        Validate an integer.

        :param action_result: Action result or BaseConnector object
        :param parameter: input parameter
        :param key: input parameter message key
        :allow_zero: whether zero should be considered as valid value or not
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS, integer value of the parameter or None in case of failure
        """
        if parameter is not None:
            try:
                if not float(parameter).is_integer():
                    return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_VALID_INT_MESSAGE.format(param=key)), None

                parameter = int(parameter)
            except Exception:
                return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_VALID_INT_MESSAGE.format(param=key)), None

            if parameter < 0:
                return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_NON_NEG_INT_MESSAGE.format(param=key)), None
            if not allow_zero and parameter == 0:
                return action_result.set_status(
                    phantom.APP_ERROR,
                    consts.BMCREMEDY_NON_NEG_NON_ZERO_INT_MESSAGE.format(param=key)
                ), None

        return phantom.APP_SUCCESS, parameter

    def _parse_html_response(self, response):

        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
               element.extract()
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except Exception:
            error_text = "Cannot parse error details"

        if not error_text:
            error_text = "Empty response and no information received"
        message = "Status Code: {}. Error Details: {}".format(status_code, error_text)
        message = message.replace('{', '{{').replace('}', '}}')
        return message

    def _generate_api_token(self, action_result):
        """ Generate new token based on the credentials provided. Token generated is valid for 60 minutes.

        :param action_result: object of ActionResult class
        :return: Token, Message
        """

        # Prepare request headers
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Prepare request body
        payload = {'username': self._api_username, 'password': self._api_password}

        # Make call
        response_status, response_dict, response = self._make_rest_call(consts.BMCREMEDY_TOKEN_ENDPOINT, action_result,
                                                              headers=headers, data=payload)

        # Something went wrong with the request
        if phantom.is_fail(response_status):
            return None, "Failed to generate token"

        if not response_dict:
            self.debug_print(consts.BMCREMEDY_TOKEN_GENERATION_ERROR_MESSAGE)
            return None, consts.BMCREMEDY_TOKEN_GENERATION_ERROR_MESSAGE

        # check the header for any message that denote a failure
        ret_val = self._check_login_status(response)
        if phantom.is_fail(ret_val):
            return None, "Failed while checking login status"

        # Saving the token to be used in subsequent actions
        self._state['token'] = response_dict["content"].decode("utf-8")

        return True, response_dict["content"].decode("utf-8")

    def _provide_attachment_details(self, attachment_list, action_result):
        """ Helper function that is used to get attachment from the vault, and provide attachment details which can be
        used to add attachment to an incident.

        :param attachment_list: list of vault IDs
        :param action_result: object of ActionResult class
        :return: status (success/failure) and (add_attachment_params_dict dictionary having attachment related
                            information and attachment_data dictionary containing attachment) / None
        """

        file_obj = []
        filename = []
        attachment_data = dict()
        add_attachment_params_dict = dict()

        attachment_list = [value.strip() for value in attachment_list.split(',') if value.strip()]
        if not attachment_list:
            self.debug_print(consts.BMCREMEDY_ERROR_INVALID_FIELDS.format(field='vault_id'))
            return action_result.set_status(
                phantom.APP_ERROR,
                consts.BMCREMEDY_ERROR_INVALID_FIELDS.format(field='vault_id')
            ), None, None

        # At most, three attachments should be provided
        if len(attachment_list) > 3:
            self.debug_print(consts.BMCREMEDY_ATTACHMENT_LIMIT_EXCEED)
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_ATTACHMENT_LIMIT_EXCEED), None, None

        try:
            # Searching for file with vault id in current container
            _, _, files_array = (ph_rules.vault_info(container_id=self.get_container_id()))
            files_array = list(files_array)
            for vault_id in attachment_list:
                file_found = False
                for file_data in files_array:
                    if file_data[consts.BMCREMEDY_JSON_VAULT_ID] == vault_id:
                        # Getting filename to use
                        filename.append(file_data['name'])
                        # Reading binary data of file
                        with open(file_data.get('path'), 'rb') as f:
                            file_obj.append(f.read())
                        file_found = True
                        break
                if not file_found:
                    self.debug_print("{}: {}".format(consts.BMCREMEDY_UNKNOWN_VAULT_ID, vault_id))
                    return action_result.set_status(
                        phantom.APP_ERROR,
                        "{}: {}".format(consts.BMCREMEDY_UNKNOWN_VAULT_ID, vault_id)
                    ), None, None
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return action_result.set_status(phantom.APP_ERROR, error_message), None, None

        for index, value in enumerate(file_obj):
            add_attachment_params_dict['z2AF Work Log0{}'.format(index + 1)] = filename[index]
            attachment_data['attach-z2AF Work Log0{}'.format(index + 1)] = (filename[index], value)

        return phantom.APP_SUCCESS, add_attachment_params_dict, attachment_data

    def _add_attachment(self, attachment_data, action_result):
        """ Helper function used to add attachment to an incident.

        :param attachment_data: dictionary containing details of attachment
        :param action_result: Object of ActionResult() class
        :return: status (success/failure) and (response obtained after adding attachment or None)
        """

        # If attachment is to be added, then details will be provided in 'entry' field
        files = []
        data_params = None
        if "entry" in attachment_data:
            for key, value in attachment_data.items():
                if key == "entry":
                    tup = (key, (None, json.dumps(value).encode(), 'text/json'))
                else:
                    tup = (key, (value[0], value[1]))
                files.append(tup)
        else:
            data_params = json.dumps(attachment_data)

        # Create incident using given input parameters
        response_status, response_data = self._make_rest_call_abstract(consts.BMCREMEDY_COMMENT_ENDPOINT, action_result,
                                                                       data=data_params, method="post",
                                                                       files=files)
        if phantom.is_fail(response_status):
            return action_result.get_status(), None

        return phantom.APP_SUCCESS, response_data

    def _get_url(self, action_result, incident_number):
        """ Helper function returns the url for the set status and update ticket action.

        :param incident_number: ID of incident
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message) and url to be used
        """

        params = {'q': "'Incident Number'=\"{}\"".format(incident_number)}

        response_status, response_data = self._make_rest_call_abstract(consts.BMCREMEDY_GET_TICKET, action_result,
                                                                       params=params, method='get')

        if phantom.is_fail(response_status):
            return phantom.APP_ERROR, None

        # If incident is not found
        if not response_data.get("entries"):
            return phantom.APP_SUCCESS, None

        try:
            url = response_data["entries"][0].get('_links', {}).get('self', [])[0].get('href', None)
            if url:
                url = re.findall("(?:/api).*", url)[0]

        except Exception as e:
            message = self._get_error_message_from_exception(e)
            self.error_print(consts.BMCREMEDY_ERROR_FETCHING_URL.format(error=message))
            return phantom.APP_ERROR, None

        return phantom.APP_SUCCESS, url

    def _bmc_int_auth_refresh(self, action_result):

        self.debug_print("Refreshing access token using refresh token...")

        config = self.get_config()
        client_id, client_secret = config.get('client_id'), config.get('client_secret')
        oauth_token = self._state.get('oauth_token')

        if not (oauth_token and oauth_token.get("refresh_token")):
            self._reset_the_state()
            action_result.set_status(phantom.APP_ERROR, "Unable to get refresh token. Please run Test Connectivity again")
            return None, "Unable to get refresh token. Please run Test Connectivity again"

        if client_id != self._state.get('client_id', ''):
            self._reset_the_state()
            action_result.set_status(phantom.APP_ERROR, "Client ID has been changed. Please run Test Connectivity again")
            return None, "Client ID has been changed. Please run Test Connectivity again"

        refresh_token = oauth_token['refresh_token']

        base_url = self._base_url.replace(self._base_url[len(self._base_url) - 4:], config.get("ports").split(",")[1].strip())
        request_url = f'{base_url}/rsso/oauth2/token'
        body = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'refresh_token': refresh_token,
            'client_secret': client_secret
        }
        try:
            r = requests.post(request_url, data=body, timeout=60)
        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, "Error refreshing token: {}".format(str(e)))
            return None, "Error refreshing token: {}".format(str(e))

        try:
            oauth_token = r.json()
            if "error" in oauth_token:
                if oauth_token["error"] in consts.BMC_ASSET_PARAM_CHECK_LIST_ERRORS:
                    self._reset_the_state()
                action_result.set_status(phantom.APP_ERROR,
                    f"Error occur while refreshing access token using refresh token. \
                        Please run test connectivity first. Error message - {oauth_token['error_description']}")
                return None, oauth_token["error_description"]
        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, "Error retrieving access token using refresh token token. Exception - {}".format(str(e)))
            return None, "Error retrieving OAuth Token. Exception - {}".format(str(e))

        self._state['oauth_token'] = oauth_token
        return phantom.APP_SUCCESS, "Success fully refreshed access token"

    def _make_rest_call_abstract(self, endpoint, action_result, data=None, params=None, method="post",
                                 accept_headers=None, files=None):
        """ This method generates a new token if it is not available or if the existing token has expired
        and makes the call using _make_rest_call method.

        :param endpoint: REST endpoint
        :param action_result: object of ActionResult class
        :param data: request body
        :param params: request params
        :param method: GET/POST/PUT/DELETE (Default will be POST)
        :param accept_headers: requests headers
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message) and API response
        """

        # Use this object for _make_rest_call
        # Final status of action_result will be determined after retry, in case the token is expired
        intermediate_action_result = ActionResult()
        response_data = None

        headers = {}
        # Prepare request headers
        if self.auth_type == consts.BMCREMEDY_OAUTH:
            headers = {"Authorization": "Bearer {}".format(self._state.get('oauth_token', {}).get('access_token'))}
        else:
            headers = {"Authorization": "AR-JWT {}".format(self._state.get('token'))}

        if not files and self.auth_type != consts.BMCREMEDY_OAUTH:
            headers['Content-Type'] = 'application/json'

        # Updating headers if Content-Type is 'multipart/formdata'
        if accept_headers:
            headers.update(accept_headers)

        # Make call
        rest_ret_code, response_data, response = self._make_rest_call(endpoint, intermediate_action_result, headers=headers,
                                                       params=params, data=data, method=method, files=files)

        # If token is invalid in case of API call, generate new token and retry
        if str(consts.BMCREMEDY_REST_RESP_UNAUTHORIZED) in str(intermediate_action_result.get_message()):
            self.debug_print(f"Token is invalid. Generating new token and retrying... ---> {str(intermediate_action_result.get_message())}")
            oauth_token = self._state.get('oauth_token', {})
            is_oauth_token = oauth_token and oauth_token.get("access_token") and oauth_token.get("refresh_token")
            if self.auth_type == consts.BMCREMEDY_OAUTH and is_oauth_token:
                if self._state.get("oauth_token", {}).get("refresh_token", None):
                    ret_code, _ = self._bmc_int_auth_refresh(action_result)
                    if phantom.is_fail(ret_code):
                        return action_result.get_status(), response_data
            elif self.auth_type == consts.BMCREMEDY_BASIC:
                ret_code, response_data = self._generate_api_token(action_result)
                if phantom.is_fail(ret_code):
                    return action_result.get_status(), response_data

            if self.auth_type == consts.BMCREMEDY_OAUTH:
                headers = {"Authorization": "Bearer {}".format(self._state.get('oauth_token', {}).get('access_token'))}
            else:
                # Update headers with new token
                headers["Authorization"] = "AR-JWT {}".format(self._state.get('token'))

            # Retry the REST call with new token generated
            rest_ret_code, response_data, response = self._make_rest_call(endpoint, intermediate_action_result, headers=headers,
                                                           params=params, data=data, method=method)

        # Assigning intermediate action_result to action_result, since no further invocation required
        if phantom.is_fail(rest_ret_code):
            action_result.set_status(rest_ret_code, intermediate_action_result.get_message())
            return action_result.get_status(), response_data

        return phantom.APP_SUCCESS, response_data

    def _make_rest_call(self, endpoint, action_result, headers=None, params=None, data=None, method="post", files=None):
        """ Function that makes the REST call to the device. It's a generic function that can be called from various
        action handlers.

        :param endpoint: REST endpoint that needs to appended to the service address
        :param action_result: object of ActionResult class
        :param headers: request headers
        :param params: request parameters
        :param data: request body
        :param method: GET/POST/PUT/DELETE (Default will be POST)
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS(along with appropriate message),
        response obtained by making an API call
        """

        response_data = None
        response = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            self.error_print(consts.BMCREMEDY_ERROR_API_UNSUPPORTED_METHOD.format(method=method))
            # Set the action_result status to error, the handler function will most probably return as is
            return RetVal3(action_result.set_status(phantom.APP_ERROR), response_data, response)
        except Exception as e:
            error_message = "{}. {}".format(consts.BMCREMEDY_EXCEPTION_OCCURRED, self._get_error_message_from_exception(e))
            self.error_print(error_message)
            # Set the action_result status to error, the handler function will most probably return as is
            return RetVal3(action_result.set_status(phantom.APP_ERROR, error_message), response_data, response)

        try:
            if files:
                response = request_func('{}{}'.format(self._base_url, endpoint), headers=headers, files=files,
                                    verify=self._verify_server_cert, timeout=consts.BMCREMEDY_DEFAULT_TIMEOUT)
            else:
                response = request_func('{}{}'.format(self._base_url, endpoint), headers=headers, data=data, params=params,
                                        verify=self._verify_server_cert, timeout=consts.BMCREMEDY_DEFAULT_TIMEOUT)

        except requests.exceptions.ProxyError as e:
            error = self._get_error_message_from_exception(e)
            action_result_error_message = "Proxy connection failed:  {}".format(error)
            return RetVal3(action_result.set_status(phantom.APP_ERROR, action_result_error_message), response_data, response)

        except requests.exceptions.ConnectionError as e:
            self._get_error_message_from_exception(e)
            error_msg = "Error connecting to server. Connection refused from server for {}".format(
                '{}{}'.format(self._base_url, endpoint))
            return RetVal3(action_result.set_status(phantom.APP_ERROR, error_msg), response_data, response)
        except Exception as error:
            error_message = self._get_error_message_from_exception(error)
            self.error_print(consts.BMCREMEDY_REST_CALL_ERROR.format(error=error_message))
            # Set the action_result status to error, the handler function will most probably return as is
            action_result_error_message = "{}. {}".format(consts.BMCREMEDY_ERROR_SERVER_CONNECTIVITY, error_message)
            return RetVal3(action_result.set_status(phantom.APP_ERROR, action_result_error_message), response_data, response)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in response.headers.get('content-type', ''):
            response_message = self._parse_html_response(response)
            return RetVal3(action_result.set_status(phantom.APP_ERROR, response_message), response_data, response)

        if response.status_code in consts.ERROR_RESPONSE_DICT:
            self.debug_print(consts.BMCREMEDY_ERROR_FROM_SERVER.format(status=response.status_code,
                                                                     detail=consts.ERROR_RESPONSE_DICT[response.status_code]))

            response_data = {"content": response.content, "headers": response.headers}

            response_message = ""
            custom_error_message = ""
            if response_data and response_data.get('content'):
                try:
                    content_dict = json.loads(response_data.get("content"))[0]
                    if consts.BMCREMEDY_BLANK_PARAM_ERROR_SUBSTRING in content_dict.get('messageAppendedText'):
                        custom_error_message = consts.BMCREMEDY_CUSTOM_ERROR_MESSAGE

                    message_text = content_dict.get('messageText')
                    message_appended_text = content_dict.get('messageAppendedText')
                    if custom_error_message:
                        message_appended_text = "{}{}".format(custom_error_message, message_appended_text)
                    response_message = 'Message Text: {}. Message Appended Text: {}'.format(
                        message_text, message_appended_text
                    )
                except Exception:
                    response_message = consts.BMCREMEDY_ERROR_JSON_PARSE.format(raw_text=response.text)
                    self.debug_print(response_message)

            # Set the action_result status to error, the handler function will most probably return as is
            action_result_error_msg = "{}. {}".format(
                consts.BMCREMEDY_ERROR_FROM_SERVER.format(
                    status=response.status_code,
                    detail=consts.ERROR_RESPONSE_DICT[response.status_code]
                ),
                response_message
            )
            return RetVal3(action_result.set_status(phantom.APP_ERROR, action_result_error_msg), response_data, response)

        # Try parsing response, even in the case of an HTTP error the data might contain a json of details 'message'
        try:
            content_type = response.headers.get('content-type')
            if content_type and content_type.find('json') != -1:
                response_data = response.json()
            else:
                response_data = {"content": response.content, "headers": response.headers}
        except Exception:
            # response.text is guaranteed to be NON None, it will be empty, but not None
            msg_string = consts.BMCREMEDY_ERROR_JSON_PARSE.format(raw_text=response.text)
            self.debug_print(msg_string)
            # Set the action_result status to error, the handler function will most probably return as is
            return RetVal3(action_result.set_status(phantom.APP_ERROR, msg_string), response_data, response)

        if response.status_code in consts.SUCCESS_RESPONSE_CODES:
            return RetVal3(action_result.set_status(phantom.APP_SUCCESS), response_data, response)

        # See if an error message is present
        message = response_data.get('message', consts.BMCREMEDY_REST_RESP_OTHER_ERROR_MESSAGE)
        error_message = consts.BMCREMEDY_ERROR_FROM_SERVER.format(status=response.status_code, detail=message)
        self.debug_print(error_message)

        # Set the action_result status to error, the handler function will most probably return as is
        return RetVal3(action_result.set_status(phantom.APP_ERROR, error_message), response_data, response)

    def _reset_the_state(self):
        self.debug_print("Resetting the state file")
        self._state = {"app_version": self.get_app_json().get("app_version")}

    def _make_rest_calls_to_phantom(self, action_result, url):

        # Ignored the verify semgrep check as the following is a call to the phantom's REST API on the instance itself
        r = requests.get(url, verify=False)  # nosemgrep
        if not r:
            message = 'Status Code: {0}'.format(r.status_code)
            if r.text:
                message = "{} Error from Server: {}".format(message, r.text.replace('{', '{{').replace('}', '}}'))
            return action_result.set_status(phantom.APP_ERROR, "Error retrieving system info, {0}".format(message)), None

        try:
            resp_json = r.json()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error processing response JSON", e), None

        return phantom.APP_SUCCESS, resp_json

    def _get_phantom_base_url_ews(self, action_result):

        ret_val, resp_json = self._make_rest_calls_to_phantom(action_result, '{}rest/system_info'.format(self.get_phantom_base_url()))

        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        phantom_base_url = resp_json.get('base_url')
        if not phantom_base_url:
            return action_result.set_status(
                phantom.APP_ERROR, "Phantom Base URL is not configured, please configure it in System Settings"), None

        phantom_base_url = phantom_base_url.strip("/")

        return phantom.APP_SUCCESS, phantom_base_url

    def _get_asset_name(self, action_result):

        ret_val, resp_json = self._make_rest_calls_to_phantom(
            action_result, '{}rest/asset/{}'.format(self.get_phantom_base_url(), self.get_asset_id()))

        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        asset_name = resp_json.get('name')
        if not asset_name:
            return action_result.set_status(phantom.APP_ERROR, "Error retrieving asset name"), None

        return phantom.APP_SUCCESS, asset_name

    def _get_url_to_app_rest(self, action_result=None):
        if not action_result:
            action_result = ActionResult()
        # get the phantom ip to redirect to
        ret_val, phantom_base_url = self._get_phantom_base_url_ews(action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status(), action_result.get_message()
        # get the asset name
        ret_val, asset_name = self._get_asset_name(action_result)
        if phantom.is_fail(ret_val):
            return action_result.get_status(), action_result.get_message()
        self.save_progress('Using Phantom base URL as: {0}'.format(phantom_base_url))
        app_json = self.get_app_json()
        app_name = app_json['name']
        app_dir_name = _get_dir_name_from_app_name(app_name)
        url_to_app_rest = "{0}/rest/handler/{1}_{2}/{3}".format(phantom_base_url, app_dir_name, app_json['appid'], asset_name)
        return phantom.APP_SUCCESS, url_to_app_rest

    def _bmc_int_auth_initial(self, client_id, client_secret):

        state = self.rsh.load_state()
        asset_id = self.get_asset_id()

        ret_val, message = self._get_url_to_app_rest()
        if phantom.is_fail(ret_val):
            return None, message

        app_rest_url = message

        request_url = '{}/rsso/oauth2'.format(self._base_url)

        proxy = {}
        if 'HTTP_PROXY' in os.environ:
            proxy['http'] = os.environ.get('HTTP_PROXY')

        if 'HTTPS_PROXY' in os.environ:
            proxy['https'] = os.environ.get('HTTPS_PROXY')

        state['proxy'] = proxy
        state['client_id'] = client_id
        state['redirect_url'] = app_rest_url
        state['request_url'] = request_url
        state['client_secret'] = client_secret

        self.rsh.save_state(state)
        self.save_progress("Redirect URI: {}".format(app_rest_url))
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': app_rest_url,
            'state': asset_id
        }
        url = requests.Request('GET', '{}/authorize'.format(request_url), params=params).prepare().url
        url = '{}&'.format(url)

        self.save_progress("To continue, open this link in a new tab in your browser")
        self.save_progress(url)
        for i in range(0, 60):
            self.save_progress("." * i)
            time.sleep(5)
            state = self.rsh.load_state()
            oauth_token = state.get('oauth_token')
            if oauth_token:
                break
            elif state.get('error'):
                self._reset_the_state()
                return None, "Error retrieving OAuth token connector"
        else:
            return None, "Timed out waiting for login"

        self._state['oauth_token'] = oauth_token
        self._state['client_id'] = client_id

        # NOTE: This state is in the app directory, it is
        #  different from the app state (i.e. self._state)

        self.rsh.delete_state()

        return oauth_token['access_token'], ""

    def _set_bmc_int_auth(self, config):

        client_id = config.get(consts.BMCREMEDY_CONFIG_CLIENT_ID)
        client_secret = config.get(consts.BMCREMEDY_CONFIG_CLIENT_SECRET)

        if not client_id:
            return None, "ERROR: {0} is a required parameter for BMC Authentication.\
                 please specify one.".format(consts.BMCREMEDY_CONFIG_CLIENT_ID)

        if not client_secret:
            return None, "ERROR: {0} is a required parameter for BMC Authentication.\
                 please specify one.".format(consts.BMCREMEDY_CONFIG_CLIENT_SECRET)

        self.debug_print("Try to generate token from authorization code")
        return self._bmc_int_auth_initial(client_id, client_secret)

    def _set_auth_method(self, action_result):
        "Method for setting authentication"
        config = self.get_config()
        if self.auth_type == consts.BMCREMEDY_BASIC:
            self.save_progress("Using Basic auth")
            auth_token, message = self._generate_api_token(action_result)
        elif self.auth_type == consts.BMCREMEDY_OAUTH:
            self.save_progress("Using BMC SSO (interactive)")
            auth_token, message = self._set_bmc_int_auth(config)
        else:
            message = "Please specify authentication method"
        if not auth_token:
            return phantom.APP_ERROR, message
        return phantom.APP_SUCCESS, message

    def _test_asset_connectivity(self, param):
        """ This function tests the connectivity of an asset with given credentials.

        :param param: dictionary of input parameters
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message)
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress(consts.BMCREMEDY_TEST_CONNECTIVITY_MESSAGE)
        self.save_progress("Configured URL: {}".format(self._base_url))

        response_status, message = self._set_auth_method(action_result)
        if phantom.is_fail(response_status):
            self.save_progress(consts.BMCREMEDY_TEST_CONNECTIVITY_FAIL)
            return action_result.set_status(phantom.APP_ERROR, message)

        self.save_progress(consts.BMCREMEDY_TEST_CONNECTIVITY_PASS)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _create_ticket(self, param):
        """ This function is used to create an incident.

        :param param: dictionary of input parameters
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message)
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        attachment_data = dict()
        add_attachment_details_param = dict()

        # List of recommended parameters that will be checked if user provided in corresponding input parameter
        incident_details_params = ["First_Name", "Last_Name", "Description", "Reported Source", "Service_Type",
                                   "Status", "Urgency", "Impact", "Status_Reason"]

        # Get optional parameters
        work_log_type = param.get(consts.BMCREMEDY_COMMENT_ACTIVITY_TYPE)
        fields_param = param.get(consts.BMCREMEDY_JSON_FIELDS, '{}')

        try:
            fields_param = json.loads(fields_param)
            if isinstance(fields_param, list):
                return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_FIELDS_PARAM_ERROR_MESSAGE)
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            self.error_print(consts.BMCREMEDY_JSON_LOADS_ERROR.format(error_message))
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_JSON_LOADS_ERROR.format(error_message))

        attachment_list = param.get(consts.BMCREMEDY_JSON_VAULT_ID, '')

        if attachment_list:
            # Segregating attachment related fields from 'fields_param', and creating a dictionary that will contain
            # attachment related information
            vault_details_status, add_attachment_details_param, attachment_data = \
                self._provide_attachment_details(attachment_list, action_result)

            # Something went wrong while executing request
            if phantom.is_fail(vault_details_status):
                return action_result.get_status()

        if work_log_type:
            add_attachment_details_param["Work Log Type"] = work_log_type

        # Getting parameters that are related to adding attachment
        # fields_param may contain extra information apart from details of adding attachment. So getting information
        # about attachments and storing it in a separate dictionary, and removing corresponding details from
        # fields_param, so that fields_param can be used for creating incident.
        for add_attachment_param in consts.ADD_ATTACHMENT_PARAMS_LIST:
            if add_attachment_param in fields_param:
                add_attachment_details_param[add_attachment_param] = fields_param[add_attachment_param]
                fields_param.pop(add_attachment_param)

        # Adding all parameters in 'fields' parameter from corresponding optional parameters, only if not available
        # in 'fields'.
        for create_ticket_param in incident_details_params:
            config_param = create_ticket_param.replace(" ", "_").lower()
            if create_ticket_param not in fields_param and param.get(config_param):
                fields_param[str(create_ticket_param)] = str(param.get(config_param))

        data = json.dumps({"values": fields_param})

        # Create incident using given input parameters
        response_status, response_data = self._make_rest_call_abstract(consts.BMCREMEDY_CREATE_TICKET, action_result,
                                                                       data=data, method="post")

        # Something went wrong while executing request
        if phantom.is_fail(response_status):
            return action_result.get_status()

        if not response_data.get("headers", {}).get("Location"):
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_LOCATION_NOT_FOUND)

        # Fetch url to get details of newly created incident
        get_incident_data = re.findall("(?:/api).*", response_data.get("headers", {}).get("Location"))[0]

        # Get details of newly created incident
        response_status, incident_response_data = self._make_rest_call_abstract(get_incident_data, action_result,
                                                                                method="get")

        if phantom.is_fail(response_status):
            return action_result.get_status()

        try:
            if not incident_response_data.get("values", {}).get("Incident Number"):
                return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_INCIDENT_NUMBER_NOT_FOUND)

            summary_data["incident_id"] = incident_response_data.get("values", {})["Incident Number"]

        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            self.error_print("Error while summarizing data: {}".format(error_message))
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_SUMMARY_ERROR.format(
                action_name="create_ticket"))

        add_attachment_details_param["Incident Number"] = incident_response_data["values"]["Incident Number"]

        # Adding attachment to newly created incident
        if attachment_list:
            attachment_data["entry"] = {"values": add_attachment_details_param}
        else:
            attachment_data["values"] = add_attachment_details_param

        # Invoking attachment API if relevant fields are present
        if len(add_attachment_details_param.keys()) > 1:
            add_attachment_status, add_attachment_response_data = self._add_attachment(attachment_data, action_result)

            if phantom.is_fail(add_attachment_status):
                return action_result.get_status()

        action_result.add_data(incident_response_data)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _update_ticket(self, param):
        """ This function is used to update an existing incident.

        :param param: includes ID of incident to update
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message)
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        attachment_data = dict()
        add_attachment_details_param = dict()

        # Getting optional parameters
        work_log_type = param.get(consts.BMCREMEDY_COMMENT_ACTIVITY_TYPE)

        try:
            fields_param = json.loads(param.get(consts.BMCREMEDY_JSON_FIELDS, '{}'))
            if isinstance(fields_param, list):
                return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_FIELDS_PARAM_ERROR_MESSAGE)
        except Exception as e:
            message = self._get_error_message_from_exception(e)
            self.error_print(consts.BMCREMEDY_JSON_LOADS_ERROR.format(message))
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_JSON_LOADS_ERROR.format(e))

        incident_number = fields_param.get("Incident Number", param[consts.BMCREMEDY_INCIDENT_NUMBER])

        attachment_list = param.get(consts.BMCREMEDY_JSON_VAULT_ID, '')

        if attachment_list:
            # Segregating attachment related fields from 'fields_param', and creating a dictionary that will contain
            # attachment related information
            vault_details_status, add_attachment_details_param, attachment_data = \
                self._provide_attachment_details(attachment_list, action_result)

            # Something went wrong while executing request
            if phantom.is_fail(vault_details_status):
                return action_result.get_status()

        if work_log_type:
            add_attachment_details_param["Work Log Type"] = work_log_type

        # Getting update link for incident
        return_status, update_link = self._get_url(action_result, incident_number)

        if phantom.is_fail(return_status):
            self.debug_print(consts.BMCREMEDY_URL_NOT_FOUND)
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_URL_NOT_FOUND)

        if not update_link:
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_INCIDENT_NUMBER_NOT_FOUND)

        # Getting parameters that are related to adding attachment
        # fields_param may contain extra information apart from details of adding attachment. So getting information
        # about attachments and removing corresponding details from fields_param
        for add_attachment_param in consts.ADD_ATTACHMENT_PARAMS_LIST:
            if add_attachment_param in fields_param:
                add_attachment_details_param[add_attachment_param] = fields_param[add_attachment_param]
                fields_param.pop(add_attachment_param)

        if fields_param:
            data = json.dumps({"values": fields_param})

            # Updating incident based on field parameters given by user
            response_status, response_data = self._make_rest_call_abstract(update_link, action_result, data=data,
                                                                           method="put")

            if phantom.is_fail(response_status):
                return action_result.get_status()

        add_attachment_details_param["Incident Number"] = incident_number

        # Adding attachment to the incident
        if attachment_list:
            attachment_data["entry"] = {"values": add_attachment_details_param}
        else:
            attachment_data["values"] = add_attachment_details_param

        # Invoking attachment API if relevant fields are present
        if len(add_attachment_details_param.keys()) > 1:
            add_attachment_status, add_attachment_response_data = self._add_attachment(attachment_data, action_result)

            if phantom.is_fail(add_attachment_status):
                return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, consts.BMCREMEDY_UPDATE_SUCCESSFUL_MESSAGE)

    def _get_ticket(self, param):
        """ Get information for the incident ID provided.

        :param param: includes ID of incident
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message)
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        # Getting mandatory parameter
        incident_id = param[consts.BMCREMEDY_INCIDENT_NUMBER]

        action_params = {'q': "'Incident Number'=\"{}\"".format(incident_id)}

        response_status, ticket_details = self._make_rest_call_abstract(consts.BMCREMEDY_GET_TICKET, action_result,
                                                                        params=action_params, method='get')

        # Something went wrong while executing request
        if phantom.is_fail(response_status):
            return action_result.get_status()

        response_status, ticket_comment_details = self._make_rest_call_abstract(consts.BMCREMEDY_COMMENT_ENDPOINT,
                                                                                action_result, params=action_params,
                                                                                method='get')

        if phantom.is_fail(response_status):
            self.debug_print(consts.BMCREMEDY_GET_COMMENT_ERROR.format(id=incident_id))
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_GET_COMMENT_ERROR.format(
                id=incident_id))

        # Adding comments of incident in ticket_details
        ticket_details.update({"work_details": ticket_comment_details})
        action_result.add_data(ticket_details)
        summary_data['ticket_availability'] = True if ticket_details.get('entries') else False

        return action_result.set_status(phantom.APP_SUCCESS)

    def _paginator(self, action_result, params, endpoint, key, offset, max_results):
        """
        Fetch all the results using pagination logic.

        :param action_result: object of ActionResult class
        :param params: params to be passed while calling the API
        :param endpoint: REST endpoint that needs to appended to the service address
        :param key: response key that needs to fetched
        :param offset: starting index of the results to be fetched
        :param max_results: maximum number of results to be fetched
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS, successfully fetched results or None in case of failure
        """
        items_list = list()

        params['offset'] = offset
        params['limit'] = consts.BMCREMEDY_DEFAULT_PAGE_LIMIT

        while True:
            ret_val, items = self._make_rest_call_abstract(endpoint, action_result, params=params, method='get')

            if phantom.is_fail(ret_val):
                return action_result.get_status(), None

            items_list.extend(items.get(key, []))

            # Max results fetched. Hence, exit the paginator.
            if max_results and len(items_list) >= max_results:
                return phantom.APP_SUCCESS, items_list[:max_results]

            # 1. Items fetched is less than the default page limit, which means there is no more data to be processed
            # 2. Next page link is not available in the response, which means there is no more data to be fetched from the server
            if (len(items.get(key, [])) < consts.BMCREMEDY_DEFAULT_PAGE_LIMIT) or (not items.get('_links', {}).get('next')):
                break

            params['offset'] += consts.BMCREMEDY_DEFAULT_PAGE_LIMIT

        return phantom.APP_SUCCESS, items_list

    def _list_tickets(self, param):
        """ Get list of incidents.

        :param param: includes limit: maximum number of incidents to return, query: additional parameters to query
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        # Getting optional parameters
        limit = param.get(consts.BMCREMEDY_JSON_LIMIT)
        query = param.get(consts.BMCREMEDY_JSON_QUERY)
        offset = param.get(consts.BMCREMEDY_JSON_OFFSET, consts.BMCREMEDY_DEFAULT_OFFSET)

        # Prepare request parameters
        # All incidents will be sorted in descending order based on their Last Modified date
        action_params = {"sort": "Last Modified Date.desc"}

        # Validate if 'limit' is positive integer
        ret_val, limit = self._validate_integer(action_result, limit, 'limit', allow_zero=True)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        action_params['limit'] = limit

        if query:
            action_params['q'] = query

        # Integer validation for 'offset' parameter
        ret_val, offset = self._validate_integer(action_result, offset, 'offset', allow_zero=True)
        if phantom.is_fail(ret_val):
            return action_result.get_status()
        action_params['offset'] = offset

        # make rest call
        response_status, response_data = self._paginator(
            action_result, action_params, consts.BMCREMEDY_LIST_TICKETS,
            'entries', offset, limit
        )

        # Something went wrong while executing request
        if phantom.is_fail(response_status):
            return action_result.get_status()

        for data in response_data:
            action_result.add_data(data)

        summary_data['total_tickets'] = len(response_data)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _set_status(self, param):
        """ This function modifies status of incident.

        :param param: dictionary of input parameters
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message)
        """

        action_result = self.add_action_result(ActionResult(dict(param)))

        fields_param = {}

        # getting mandatory parameter
        incident_number = param[consts.BMCREMEDY_INCIDENT_NUMBER]

        fields_param['Status'] = param[consts.BMCREMEDY_JSON_STATUS]

        # Getting optional parameter
        if param.get("assignee_login_id"):
            fields_param["Assignee Login ID"] = param.get("assignee_login_id")

        if param.get("status_reason"):
            fields_param["Status_Reason"] = param.get("status_reason")

        optional_parameter_list = ["assigned_support_company", "assigned_support_organization", "assigned_group",
                                   "assignee", "resolution"]

        for parameter in optional_parameter_list:
            field_name = parameter.replace("_", " ").title()

            if param.get(parameter):
                fields_param[field_name] = param.get(parameter)

        fields_param = {"values": fields_param}

        # Getting update link for incident
        return_status, url = self._get_url(action_result, incident_number)

        if phantom.is_fail(return_status):
            self.debug_print(consts.BMCREMEDY_URL_NOT_FOUND)
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_URL_NOT_FOUND)

        if not url:
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_INCIDENT_NUMBER_NOT_FOUND)

        response_status, response_data = self._make_rest_call_abstract(str(url), action_result,
                                                                       data=json.dumps(fields_param), method='put')

        if phantom.is_fail(response_status):
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, consts.BMCREMEDY_SET_STATUS_MESSAGE)

    def _add_comment(self, param):
        """ This function is used to add comment/work log to an incident.

        :param param: includes ID of incident to add comment
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR (along with appropriate message)
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        add_attachment_details_param = dict()
        attachment_data = dict()
        incident_number = param[consts.BMCREMEDY_INCIDENT_NUMBER]

        # List of optional parameters
        optional_parameters = {"description": "Description", "comment": "Detailed Description",
                               "view_access": "View Access", "secure_work_log": "Secure Work Log",
                               "worklog_submitter": "Work Log Submitter"}

        # Adding mandatory parameters
        add_attachment_details_param.update({
            "Incident Number": incident_number,
            "Work Log Type": param[consts.BMCREMEDY_COMMENT_ACTIVITY_TYPE]
        })

        # Getting update link for incident
        return_status, url = self._get_url(action_result, incident_number)

        if phantom.is_fail(return_status):
            self.debug_print(consts.BMCREMEDY_URL_NOT_FOUND)
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_URL_NOT_FOUND)

        if not url:
            return action_result.set_status(phantom.APP_ERROR, consts.BMCREMEDY_INCIDENT_NUMBER_NOT_FOUND)

        # Adding optional parameters in 'fields'
        for key_param, api_key in optional_parameters.items():
            if param.get(key_param) and api_key not in add_attachment_details_param:
                add_attachment_details_param[str(api_key)] = str(param.get(key_param))

        attachment_data["values"] = add_attachment_details_param

        add_attachment_status, add_attachment_response_data = self._add_attachment(attachment_data, action_result)

        if phantom.is_fail(add_attachment_status):
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, consts.BMCREMEDY_ADD_COMMENT_MESSAGE)

    def handle_action(self, param):
        """ This function gets current action identifier and calls member function of it's own to handle the action.

        :param param: dictionary which contains information about the actions to be executed
        :return: status phantom.APP_SUCCESS/phantom.APP_ERROR
        """

        # Dictionary mapping each action with its corresponding actions
        action_mapping = {
            'test_asset_connectivity': self._test_asset_connectivity,
            'create_ticket': self._create_ticket,
            'get_ticket': self._get_ticket,
            'list_tickets': self._list_tickets,
            'update_ticket': self._update_ticket,
            'set_status': self._set_status,
            'add_comment': self._add_comment
        }

        action = self.get_action_identifier()
        action_execution_status = phantom.APP_SUCCESS

        if self._is_client_id_changed or self.is_oauth_token_exist:
            if self.get_action_identifier() != phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY:
                self.save_progress("Please run the test connectivity first...")
                return self.set_status(phantom.APP_ERROR, "Please run the test connectivity first...")

        if action in action_mapping.keys():
            action_function = action_mapping[action]
            action_execution_status = action_function(param)

        return action_execution_status

    def finalize(self):
        """ This function gets called once all the param dictionary elements are looped over and no more handle_action
        calls are left to be made. It gives the AppConnector a chance to loop through all the results that were
        accumulated by multiple handle_action function calls and create any summary if required. Another usage is
        cleanup, disconnect from remote devices etc.
        """

        # save state
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import sys

    import pudb

    pudb.set_trace()
    if len(sys.argv) < 2:
        print('No test json specified as input')
        sys.exit(0)
    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))
        connector = BmcremedyConnector()
        connector.print_progress_message = True
        return_value = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(return_value), indent=4))
    sys.exit(0)
