from res.traverseSensitiveSources import get_sensitive_keywords


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


def check_api(temp_api):
    black_list = ["getServerName", "getThreadName", "setServerName", "setThreadName", "TextHeight", "TimeInSecond",
                  "TimeInMillisecond", "TimeInterval", "requestPasswordReset", "LocationProvider", "DisplayHeight",
                  "DisplayWidth", "LocationAttribute", "TimeIn", "getDeviceScreenWidthDip",
                  "getDeviceWidth", "createLocationRequest", "addBusinessEventWithCurrency", "emptyLocationData"]
    # black_list.append("")
    # black_list.append("")
    # black_list.append("")
    api = temp_api.lower()
    if api == 'getage' or api == 'setage':
        return True
    # if not (api.startswith("get") or api.startswith("set")):
    #     return False
    if "location" in api and not ("get" not in api and "set" not in api):
        return False
    if "click" in api and ("onclick" not in api and "clicked" not in api):
        return False
    start_words = ["waitfor", "doNotRead", "maybe", "to", "clear", "config", "setis", "setneed", "onreceive", "onreceive", "handle", "unset", "delete", "stop", "Notify", "trigger", "warn", "use"]
    end_words = ["TimeImmediately", "Callback", "Format", "num", "space", "Configeration", "source", "type", "purpose", "option", "report", "area", "Reset", "Surpport", "Configuration", "Mode", "Describe", "disabled", "Clickable", "Notify"]
    for word in start_words:
        if api.startswith(word.lower()):
            return False
    for word in end_words:
        if api.endswith(word.lower()):
            return False
    for word in black_list:
        if word.lower() in api:
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
