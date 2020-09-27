


# CountlyConfig config = (new CountlyConfig(appC, COUNTLY_APP_KEY, COUNTLY_SERVER_URL));config.setDeviceId("YOUR_DEVICE_ID");Countly.sharedInstance().init(config);

def main(codes):
    lines = codes.split(";")
    for line in lines:
        print(line)
        tokens = line.split(".")
        if len(tokens) <= 1:
            continue
        else:
            caller_class = tokens[0]
            print("Caller Class=" + str(caller_class))
            for i in range(1, len(tokens)):
                print("API=" + str(tokens[i]))
        print("------------------")


if __name__ == '__main__':
    main("CountlyConfig config = (new CountlyConfig(appC, COUNTLY_APP_KEY, COUNTLY_SERVER_URL));config.setDeviceId(\"YOUR_DEVICE_ID\");Countly.sharedInstance().init(config);")