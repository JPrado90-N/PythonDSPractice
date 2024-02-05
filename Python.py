import os
import json
import urllib.request
import urllib.response
import http.client
from urllib.error import URLError,URLError

class StateModel:
	def __init__(self, disabled, o_Key, o_SecurityId, code, 
			  description, o_Code, o_Description):
		self.disabled = disabled
		self.o_Key = o_Key
		self.o_SecurityId = o_SecurityId
		self.code = code
		self.description = description
		self.o_Code = o_Code
		self.o_Description = o_Description

	def __init__(self):
		self.code = "";
		self.description = "";
		self.disabled = False;
		self.o_Code = "";
		self.o_Description = "";
		self.o_Key = 0;
		self.o_SecurityId = 0;

#Example use of Advanced REST Web API interactions using Python.
class WebApiRequests:

    # setting up user credential and URL root (URL must be a full PATH )
    def __init__(self):
        self.retrieveUserCredentionals()
        self.retrieveHttpURL()

    def retrieveUserCredentionals(self):
        self._webApiUser = input("Please input CIS UserId: ")
        self._webApiPassword = input("Please input CIS password: ")
	
    def retrieveHttpURL(self):
        self._webApiRootUrl = input("Please input root path of REST Web API: ")  + "/data/state"

    """
    python connection needs secure certificate to access URLs.
    this will create a trust manager that does not validate certificate chains
    use it then server does not have secure certificate
    """
    def SSLCertificateOff(self):
        import ssl
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context

    """ 
    stateModel - the model for which string response should be generated
    returns all not null value field from the model, in a format 'property=value&property2=value2...'
    """
    @staticmethod
    def getStateModelInfo(self, stateModel):
        pythonJsonStateModel = {}
        pythonJsonStateModel["disabled"] = stateModel.disabled
        pythonJsonStateModel["o_Key"] = stateModel.o_Key
        pythonJsonStateModel["o_SecurityId"] = stateModel.o_SecurityId
        if(stateModel.code != ''):
            pythonJsonStateModel["code"] = stateModel.code
        if(stateModel.description != ''):
            pythonJsonStateModel["description"] = stateModel.description
        if(stateModel.o_Code != ''):
            pythonJsonStateModel["o_Code"] = stateModel.o_Code
        if(stateModel.o_Description != ''):
            pythonJsonStateModel["o_Description"] = stateModel.o_Description
        return pythonJsonStateModel

    """ 
    === HTTPS GET List 
    // This request will retrieve a list of states, using GET request.
    // The result should be success
    """
    def getHttpList(self):
        try:
            currentUrl = self._webApiRootUrl # current URL will change to the next page URL, when all data for the current page will be printed
            currentUrl += "?page=2"
            currentUrl += "&pagesize=5"
            currentUrl += "&where=code%20like%20'%N%'%20and%20O_Key%20gt%205"
            currentUrl += "&order=-description"
            currentUrl += "&fields=*"

            jsonObject = urllib.request.urlopen(currentUrl).read() # retrieve data from the connection
            loaded_json = json.loads(jsonObject) # load object into JSON format
            print("Successfully retrieved list of states: ", end="")
            print("Page=", end="")
            print(loaded_json["currentPage"], end=", ")
            print("PageSize=", end="")
            print(loaded_json["pageSize"], end=", ")
            print("TotalPages=", end="")
            print(loaded_json["totalPages"], end=", ")
            print("TotalItems=", end="")
            print(loaded_json["totalItems"])

            if (loaded_json.get('_embedded') and loaded_json["_embedded"] != ''): # if loaded json contains parameter '_embedded', load further parameters and display
                states = loaded_json['_embedded']['state']
                for currentState in states:
                    print(currentState['code'], end='\t')
                    print(currentState['description'], end='\t')
                    print(currentState['o_Key'])
        except URLError as e:
            print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")

    """
    === HTTPS GET One
    This request will retrieve one state (NY) using GET method.
    Retrieve a single resource
    The result should be success
    """
    def getHttpOne(self):
        try:
            searchingState = input("Please insert value: ") # value for searching
            found = False
            currentUrl = self._webApiRootUrl # current URL will change to the next page URL, when all data for the current page will be printed
            while True:
                jsonObject = urllib.request.urlopen(currentUrl).read() # retrieve data from the connection
                loaded_json = json.loads(jsonObject) # load object into JSON format
                if (loaded_json.get('_embedded') and loaded_json["_embedded"] != ''): # if loaded json contains parameter '_embedded', load further parameters and display
                    states = loaded_json['_embedded']['state']
                    for currentState in states:
                        if(currentState['code'] == searchingState):
                            print("Successfully retrieved one resource from State Control: ", end="\t")
                            print(currentState['code'], end='\t')
                            print(currentState['description'], end='\t')
                            print(currentState['o_Key'])
                            found = True
                            break
                if loaded_json['totalPages'] == loaded_json['currentPage']:
                    break
                currentUrl = json.loads(jsonObject)['_links']['next']['href']
            if(not found):
                print("Property " + searchingState + " was not found")
        except URLError as e:
            print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")

    """
    === HTTPS POST
    This request will add new object to the server.
    Add a new resource
    If the result will fail, the most common problem is that resource probably already exist on the server. Consider using delete against the resource and try again
    The Result should be success
    """
    def postHttp(self):
        stateModel = StateModel()
        stateModel.code = input("Insert state: ")
        stateModel.description = input("Insert description: ")
        localRoot = self._webApiRootUrl + '/'
        body = WebApiRequests.getStateModelInfo(self, stateModel)
        req = urllib.request.Request(localRoot)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8') # should be converted to bytes
        try:
            response = urllib.request.urlopen(req, jsondataasbytes)
            print("Successfully created new property at location: " + localRoot + stateModel.code)
        except URLError as e:
            jsonObject = e.read()
            if e.msg == "Validation failed":
                loaded_json = json.loads(jsonObject) # load object into JSON format

                print("Request failed with code: Validation failed")
                for res in loaded_json:
                    if res["field"]:
                        print("field: " + res["field"])
                    else:
                        print("field: None")
                    if res["field"]:
                        print("message: " + res["message"])
                    else:
                        print("message: None")
                    if res["value"]:
                        print("value: " + res["value"])
                    else:
                        print("value: None")
                    if res["optionDetail"]:
                        print("optionDetail: " + res["optionDetail"])
                    else:
                        print("optionDetail: None")
                print()
            else:
                print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")
 
    """        
    === HTTP Delete
    This request will delete particular resource on the server
    Should be success
    """
    def deleteHttp(self):
        deletingParam = self._webApiRootUrl + '/' + input("Please insert parameter for deleting: ")
        try:
            req = urllib.request.Request(
                    deletingParam,
                    method='DELETE'
            )
            response = urllib.request.urlopen(req)
            strResponse = response.read().decode('utf8')
            jsonResponse = json.loads(strResponse)
            print("Successfully deleted state " +  jsonResponse['code'])
        except URLError as e:
            print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")

    """
    === HTTPS PUT
    Edit the existing resource using PUT
    (PUT typically requires a GET followed by a PUT, because PUT requires the entire object to be sent, since missing properties are defaulted to "empty" values- not what you normally want)
    The result should be success
    Edit the existing resource using PUT
    (PUT typically requires a GET followed by a PUT, because PUT requires the entire object to be sent, since missing properties are defaulted to "empty" values- not what you normally want)
    The result should be success
    """
    def putHttp(self):
        stateModel = StateModel()
        stateModel.code = input("Please insert code: ")
        stateModel.description = input("Please insert description: ")
        localRoot = self._webApiRootUrl + "/" + stateModel.code
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        try:
            data = WebApiRequests.getStateModelInfo(self, stateModel)
            str = json.dumps(data).encode()
            req = urllib.request.Request(localRoot, data=str, headers=headers, method='PUT')
            urllib.request.urlopen(req)
            print("Successfully update state " + stateModel.code)
        except URLError as e:
            jsonObject = e.read()
            if e.msg == "Validation failed":
                loaded_json = json.loads(jsonObject) # load object into JSON format

                print("Request failed with code: Validation failed")
                for res in loaded_json:
                    if res["field"]:
                        print("field: " + res["field"])
                    else:
                        print("field: None")
                    if res["field"]:
                        print("message: " + res["message"])
                    else:
                        print("message: None")
                    if res["value"]:
                        print("value: " + res["value"])
                    else:
                        print("value: None")
                    if res["optionDetail"]:
                        print("optionDetail: " + res["optionDetail"])
                    else:
                        print("optionDetail: None")
                print()
            else:
                print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")
            
    """
    === HTTPS PATCH
    Edit the existing resource using PATCH, which allows selective operations on fields.
    Refer to https://en.wikipedia.org/wiki/JSON_Patch for details on the patch document format and supported directives.
    The request body should be in a particular format, E.G. "[{ "op": "replace", "path": "/description", "value": "ARKANSAS" }]"
    op - method on the resource, path - the field on the resource for update, value - resource which should be updated
    The result should be success
    """
    def patchHttp(self):
        code = input("Please insert code: ")
        description = input("Please insert description: ")
        updatingProperty = input("Please insert property you want to update: ")
        localFullPath = self._webApiRootUrl + "/" + code
        headers = {'Content-Type': 'application/json'}
        try:
            req = urllib.request.Request(localFullPath, method="POST", headers=headers)
            req.get_method = lambda: 'PATCH'
            updatingString = [{'op': 'replace', 'path': '/' + updatingProperty, 'value': description}]
            req.data = updatingString
            values = json.dumps(updatingString).encode()
            resp = urllib.request.urlopen(req, data=values)
            print("Successfully updated state " + code + " " + updatingProperty + " via PATCH")
        except URLError as e:
            jsonObject = e.read()
            if e.msg == "Validation failed":
                loaded_json = json.loads(jsonObject) # load object into JSON format

                print("Request failed with code: Validation failed")
                for res in loaded_json:
                    if res["field"]:
                        print("field: " + res["field"])
                    else:
                        print("field: None")
                    if res["field"]:
                        print("message: " + res["message"])
                    else:
                        print("message: None")
                    if res["value"]:
                        print("value: " + res["value"])
                    else:
                        print("value: None")
                    if res["optionDetail"]:
                        print("optionDetail: " + res["optionDetail"])
                    else:
                        print("optionDetail: None")
                print()
            else:
                print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")

    """
    Adds user credentials to requests
    """
    def authorizeUser(self):
        try:
            p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            p.add_password(None, self._webApiRootUrl, self._webApiUser, self._webApiPassword)
            auth_handler = urllib.request.HTTPBasicAuthHandler(p)
            opener = urllib.request.build_opener(auth_handler)
            urllib.request.install_opener(opener)
        except: 
            print("Unable to authorize user")

    """
    === HTTPS VALIDATE for add
    This request, using post method, will ensure that business rules, existing on a server, work properly.
    Code inside StateModel represents US state, which should contain 2 letters. If we will try to set more then that, it should fail.
    The result of this request should be a failure
    """
    def validateAdd(self):
        stateModel = StateModel()
        stateModel.code = "ZZQ"
        stateModel.description = "State of Mind"
        localRoot = self._webApiRootUrl + '/'
        body = WebApiRequests.getStateModelInfo(self, stateModel)
        req = urllib.request.Request(localRoot)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8') # should be converted to bytes
        try:
            urllib.request.urlopen(req, jsondataasbytes)
            print("Successfully created new property at location: " + localRoot + stateModel.code)
        except URLError as e:
            jsonObject = e.read()
            if e.msg == "Validation failed":
                loaded_json = json.loads(jsonObject) # load object into JSON format

                print("Request failed with code: Validation failed")
                for res in loaded_json:
                    if res["field"]:
                        print("field: " + res["field"])
                    else:
                        print("field: None")
                    if res["field"]:
                        print("message: " + res["message"])
                    else:
                        print("message: None")
                    if res["value"]:
                        print("value: " + res["value"])
                    else:
                        print("value: None")
                    if res["optionDetail"]:
                        print("optionDetail: " + res["optionDetail"])
                    else:
                        print("optionDetail: None")
                print()
            else:
                print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")

    """
    === HTTPS VALIDATE for update
    This is similar to the previous one request, will fail due to incorrect business rule (description is too long)
    Validate a given resource update model for changes
    The result should be a failure
    """
    def validateUpdate(self):
        stateModel = StateModel()
        stateModel.code = "TT"
        stateModel.description = "This is very long description, which should fail validation"
        localRoot = self._webApiRootUrl + '/'
        body = WebApiRequests.getStateModelInfo(self, stateModel)
        req = urllib.request.Request(localRoot)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8') # should be converted to bytes
        try:
            urllib.request.urlopen(req, jsondataasbytes)
            print("Successfully created new property at location: " + localRoot + stateModel.code)
        except URLError as e:
            jsonObject = e.read()
            if e.msg == "Validation failed":
                loaded_json = json.loads(jsonObject) # load object into JSON format

                print("Request failed with code: Validation failed")
                for res in loaded_json:
                    if res["field"]:
                        print("field: " + res["field"])
                    else:
                        print("field: None")
                    if res["field"]:
                        print("message: " + res["message"])
                    else:
                        print("message: None")
                    if res["value"]:
                        print("value: " + res["value"])
                    else:
                        print("value: None")
                    if res["optionDetail"]:
                        print("optionDetail: " + res["optionDetail"])
                    else:
                        print("optionDetail: None")
                print()
            else:
                print(e)
        except HTTPError as e:
            print(e)
        except:
            print("Unable to process post request. Please check inserted credentials, URL and property for existence")

    # run all existing methods
    def runAll(self):
        print("Getting list")
        webApiRequest.getHttpList()
        print("")
        print("Getting one")
        webApiRequest.getHttpOne()
        print("")
        print("Post")
        webApiRequest.postHttp()
        print("")
        print("Put")
        webApiRequest.putHttp()
        print("")
        print("Patch")
        webApiRequest.patchHttp()
        print('does not available')
        print("")
        print("Delete")
        webApiRequest.deleteHttp()

# Main program. Creates Requests model, authorize user and prompts for selection
webApiRequest = WebApiRequests()
webApiRequest.SSLCertificateOff() # turn off secure certificate validation
webApiRequest.authorizeUser()
selection = -1
while selection != 0:
    print("\nPlease input operation number:")
    print("0 - EXIT");
    print("1 - run GET list request");
    print("2 - run GET one request");
    print("3 - run add validation for state 'ZZX' (should cause a failure)");
    print("4 - run update validation for long description (should cause a failure)");
    print("5 - run POST request");
    print("6 - run PUT request");
    print("7 - run PATCH request");
    print("8 - run DELETE request");
    print("9 - run all operations for testing (GET list, GET one, Validations, POST, PUT, PATCH, DELETE)");
    print("10 - update URL");
    print("11 - update user name and password");
    print()

    selection = input("Selection: ")
    if selection == '0':
        os._exit(0)
    elif selection == '1':
        webApiRequest.getHttpList()
    elif selection == '2':
        webApiRequest.getHttpOne()
    elif selection == '3':
        webApiRequest.validateAdd()
    elif selection == '4':
        webApiRequest.validateUpdate()
    elif selection == '5':
        webApiRequest.postHttp()
    elif selection == '6':
        webApiRequest.putHttp()
    elif selection == '7':
        webApiRequest.patchHttp()
    elif selection == '8':
        webApiRequest.deleteHttp()
    elif selection == '9':
        webApiRequest.runAll()
    elif selection == '10':
        webApiRequest.retrieveHttpURL()
        webApiRequest.authorizeUser()
        print("URL updated")
    elif selection == '11':
        webApiRequest.retrieveUserCredentionals()
        webApiRequest.authorizeUser()
        print("User credentials updated")
    else:
        print("Unable to process selection")