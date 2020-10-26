from res.traverseSensitiveSources import get_sensitive_keywords


def check_api_by_class(temp_class_name, temp_api):
    class_name = temp_class_name.lower()
    tag = False
    if "identify" in class_name or "userproperty" in class_name or "identifies" in class_name or "userproperties" in class_name:
        tag = True
    api = temp_api.lower()
    if tag and (api == "add" or api == "set" or api == "setonce" or api == "append"):
        return True, ["GeneralUserProperty"]
    if api == "onevent" and "umeng" in class_name:
        return True, ["GeneralLogEvent"]
    if api == "logcustom" or api == "trackevent" or api == "logevent" or api == "logeventasync" or api == "logeventsync":
        return True, ["GeneralLogEvent"]
    if api == "setuserproperty" or api == "adduserproperty" or api == "setuserproperties" or api == "adduserpropertoes":
        return True, ["GeneralUserProperty"]
    sensitive_keywords = get_sensitive_keywords()
    is_sensitive = False
    privacy_item = ""
    for keywords in sensitive_keywords:
        is_sensitive = True
        for keyword in keywords:
            if keyword.lower() not in api:
                is_sensitive = False
        if is_sensitive:
            privacy_item = keywords
            break
    if is_sensitive:
        return True, privacy_item
    else:
        return False, privacy_item


def check_api_by_keywords(temp_api):
    api = temp_api.lower()
    if api == "logcustom" or api == "trackevent" or api == "logevent" or api == "onevent" or api == "logeventasync" or api == "logeventsync":
        return True, ["event"]
    if api == "setuserproperty" or api == "adduserproperty" or api == "setuserproperties" or api == "adduserpropertoes":
        return True, ["property"]
    sensitive_keywords = get_sensitive_keywords()
    is_sensitive = False
    privacy_item = ""
    for keywords in sensitive_keywords:
        is_sensitive = True
        for keyword in keywords:
            if keyword.lower() not in api:
                is_sensitive = False
        if is_sensitive:
            privacy_item = keywords
            break
    if is_sensitive:
        return True, privacy_item
    else:
        return False, privacy_item


def filter_api(temp_api):
    black_list = ["ClickLink", "PermissionGranted", "drawMyLocation", "ByLatitude", "DeviceBuildId",
                  "GoogleSearchInstallIdentifier", "DevicePayload", "DeviceType", "readLocationSelector",
                  "readId", "readIdentifiers", "PushAddress", "UAAddress", "ThreadID", "getServerName",
                  "getThreadName", "setServerName", "setThreadName", "TextHeight", "TimeInSecond",
                  "TimeInMillisecond", "TimeInterval", "requestPasswordReset", "LocationProvider",
                  "DisplayHeight", "DisplayWidth", "LocationAttribute", "TimeIn", "getDeviceScreenWidthDip",
                  "getDeviceWidth", "createLocationRequest", "addBusinessEventWithCurrency", "emptyLocationData",
                  "beginTransaction", "endTransaction", "LocationExists", "pollClicked", "showMyLocation",
                  "getBusCompany", "onLocationShareUrlSearched", "TicketPrice", "FirstRoadId", "SecondRoadId",
                  "onLocationShareUrlSearched", "PerKMPrice", "ZonePrice", "StartPrice", "startAssistantLocation",
                  "startLocation", "BasicPrice", "LocationUpdateMinDistance", "getLocationUpdateMinTime",
                  "LocationMapDrawingBounds", "LocationOverlay", "LocationRequiredZoom", "SocketAddress",
                  "LocationValidTime", "LocationService", "LocationDiscoveryActive", "LocationTimeOut",
                  "LocationUpdateTimeout", "LocationStyle", "LocationWhere", "DisToRealLocation", "MaxPrice",
                  "BasePrice"]
    api = temp_api.lower()
    if api == 'getage' or api == 'setage':
        return True
    # if not (api.startswith("get") or api.startswith("set")):
    #     return False
    if "location" in api and ("get" not in api and "set" not in api):
        return False
    if "click" in api and ("onclick" not in api and "clicked" not in api):
        return False
    start_words = ["setcanuse", "shoulduse", "open", "waitfor", "doNotRead", "maybe", "to", "clear", "config", "setis", "setneed",
                   "onreceive", "handle", "unset", "delete", "stop", "Notify", "trigger", "warn", "use",
                   "activate", "candraw", "delete"]
    end_words = ["OptedIn", "TimeImmediately", "Callback", "Format", "num", "space", "Configeration", "source", "type", "purpose",
                 "option", "report", "area", "Reset", "Surpport", "Configuration", "Mode", "Describe", "disabled",
                 "Clickable", "Notify", "Successful", "LocationIcon", "Detected", "OptOut"]
    for word in start_words:
        if api.startswith(word.lower()):
            return False
    for word in end_words:
        if api.endswith(word.lower()):
            return False
    for word in black_list:
        if word.lower() in api:
            return False
    if (api.startswith("get") or (api.startswith("set"))) and api.endswith("color"):
        return False
    if (api.startswith("get") or (api.startswith("set"))) and (api.endswith("resulttext") or api.endswith("resulttitle")):
        return False
    if api.startswith("from") or api.startswith("check") or api.startswith("disable"):
        return False
    if api.startswith("has") or api.startswith("search") or api.startswith("enable"):
        return False
    if api.startswith("calculate") or api.startswith("is") or api.startswith("remove"):
        return False
    if api.endswith("handler") or api.endswith("strategy") or api.endswith("support"):
        return False
    if api.endswith("enabled") or api.endswith("listener") or api.endswith("protocal"):
        return False
    return True
