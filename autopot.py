from adb.client import Client as adbc
import numpy as np
import cv2
import argparse,time
import logging

parser = argparse.ArgumentParser(description=r'ROMobile AFK/Helper script. https://github.com/aizatrosli/ROMalas')
parser.add_argument("-a","--auto", help=r"Trigger auto-attack for all monsters every script start. Default value is 'false'.")
parser.add_argument("-m","--macro", help=r"Custom path for custom macro file. Default value is 'macro.txt'")
parser.add_argument("-v","--verbose", help=r"Toggle verbose output. Enable this will cause performance issues. Default value is 'false'.")
args = parser.parse_args()

AUTO_ATTACK = True if args.auto == "true" else False
VERBOSE = True if args.verbose == "true" else False
MACRO_PATH = args.macro if args.macro else "macro.txt"

bar_dict = {"xmin_bar": 42, "xmax_bar": 136, "ymin_h": 123, "ymax_h": 124, "ymin_m": 135, "ymax_m": 136}
poskey_dict= {"skill6":[0x4ca,0x28b],"skill5":[0x46c,0x28b],"skill4":[0x0a,0x28b],"skill3":[0x3aa,0x28b],"skill2":[0x348,0x28b],"skill1":[0x2e8,0x28b],"auto":[0x4ca,0x22b],"item5":[0x46c,0x22b],"item4":[0x40a,0x22b],"item3":[0x3aa,0x22b],"item2":[0x348,0x22b],"item1":[0x2e8,0x22b]}
posmap_dict={"map":[0x4ee,0x57],"world":[0x36f,0x23c],"minitopleft":[0x340,0xc8],"minibtmleft":[0x340,0x215],"minitopright":[0x4d5,0xc8],"minibtmright":[0x4d5,0x215]}
submenu_dict={"allmon":[0x3eb,0x11d]}

def connectadb():
    try:
        client = adbc(host="127.0.0.1", port=5037)
        device = client.device("127.0.0.1:62001")
        return device
    except Exception as e:
        print(str(e))

def convertarrhex(arrval):
    return str(int(arrval[0]))+" "+str(int(arrval[1]))

def getbarvalue(image, bar, dict):
    ymin = None
    ymax = None
    layer = None
    if bar == "health":
        ymin = bar_dict["ymin_h"]
        ymax = bar_dict["ymax_h"]
        layer = 1
    if bar == "mana":
        ymin = bar_dict["ymin_m"]
        ymax = bar_dict["ymax_m"]
        layer = 0
    getbar = image[ymin:ymax, dict["xmin_bar"]:dict["xmax_bar"]][:, :, layer][0]
    getbar[getbar > 110] = 255
    getbar[getbar < 110] = 0
    getbar = getbar.astype(bool)
    percentagebar = int(100 * (int(np.count_nonzero(getbar)) / getbar.size))

    return percentagebar

def getmacrotxt(filename):
    try:
        macrolist = []
        with open(filename,'r') as txt:
            for line in txt:
                if not line == '\n':
                    macrolist.append(line.replace('\n', "").split(","))
        return macrolist
    except Exception as e:
        print(str(e))

def setautoattack(device,status):
    try:
        if status:
            device.shell("input keyevent 4")
            time.sleep(0.5)
            device.shell("input keyevent 4")
            device.shell("input tap "+convertarrhex(poskey_dict["auto"]))
            time.sleep(0.5)
            device.shell("input tap " + convertarrhex(submenu_dict["allmon"]))
            print("INFO :AUTO-ATTACK Enabled")
        else:
            device.shell("input keyevent 4")
            time.sleep(0.5)
            device.shell("input keyevent 4")
            device.shell("input tap " + convertarrhex(poskey_dict["auto"]))
            print("INFO :AUTO-ATTACK Disabled")
    except Exception as e:
        print(str(e))

#key, delay(sec), health(percentage), mana(percentage)
def setmacrolist(device, macros, health, mana):
    try:
        for macro in macros:
            execute = False
            delay = int(macro[1]) if not macro[1] == "None" else 0
            if not macro[2] == "None" and not macro[3] == "None":
                if health < int(macro[2]) and mana < int(macro[3]):
                    time.sleep(delay)
                    device.shell("input tap " + convertarrhex(poskey_dict[str(macro[0])]))
                    execute = True
            elif not macro[2] == "None" and macro[3] == "None":
                if health < int(macro[2]):
                    time.sleep(delay)
                    device.shell("input tap " + convertarrhex(poskey_dict[str(macro[0])]))
                    execute = True
            elif macro[2] == "None" and not macro[3] == "None":
                if mana < int(macro[3]):
                    time.sleep(delay)
                    device.shell("input tap " + convertarrhex(poskey_dict[str(macro[0])]))
                    execute = True
            elif macro[2] == "None" and macro[3] == "None":
                time.sleep(delay)
                device.shell("input tap " + convertarrhex(poskey_dict[str(macro[0])]))
                execute = True
            else:
                time.sleep(delay)
                device.shell("input tap " + convertarrhex(poskey_dict[str(macro[0])]))
                execute = "True but check your macro please"
            print("Health : " + str(health) + " | Mana : " + str(mana) + " | Macro : " + str(macro) + " | Execute : " + str(execute))
    except Exception as e:
        print("ERROR: setmacrolist >>" +str(e))

def main():
    device = connectadb()
    if AUTO_ATTACK:
        setautoattack(device,True)
    macros = getmacrotxt(MACRO_PATH)
    try:
        while True:
            try:
                imgbytearr = device.screencap()
                screen = cv2.imdecode(np.fromstring(bytes(imgbytearr), np.uint8), cv2.IMREAD_COLOR)
                hval = getbarvalue(screen, "health", bar_dict)
                mval = getbarvalue(screen, "mana", bar_dict)
                if not macros is None:
                    setmacrolist(device,macros,hval,mval)
            except KeyboardInterrupt:
                if AUTO_ATTACK:
                    setautoattack(device, False)
                break
    except KeyboardInterrupt:
        if AUTO_ATTACK:
            setautoattack(device, False)
        pass

if __name__ == "__main__":
    main()
