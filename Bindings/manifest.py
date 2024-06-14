import json

controllers = ["oculus_touch", "knuckles"]
boolActions = ["Jump","SwitchGrenades","Interact","SwitchWeapons","Melee","Flashlight","Grenade","Fire","MenuForward","MenuBack","Crouch","Zoom","Reload", "Recentre"]
vec1Actions = []
vec2Actions = ["Look", "Move"]

bindings = {
    "Jump" : { "h" : "right", "b" : "joystick|north"},
    "SwitchGrenades" : {"h" : "left", "b" : "grip"},
    "SwitchWeapons" : {"h" : "right", "b" : "grip"},
    #"Interact" : {"h" : "left", "b" : "y"}, #Moved to right hand
    "Melee" : {"h" : "left", "b" : "x"},
    #"Flashlight" : {"h" : "right", "b" : "a"}, #Handled by gesture
    #"Reload" : {"h" : "right", "b" : "b"}, #Handled by interact
    "Grenade" : {"h" : "right", "b" : "a"},
    "Interact" : {"h" : "right", "b" : "b"},
    #"Grenade" : {"h" : "left", "b" : "trigger"}, #Moved to right hand
    "Fire" : {"h" : "right", "b" : "trigger"},
    "Crouch" : {"h" : "right", "b" : "joystick|south"},
    "Look" : {"h" : "right", "b" : "joystick"},
    "Move" : {"h" : "left", "b" : "joystick"},
    "Zoom" : {"h" : "right", "b" : "thumbrest"},
    "Recentre" : {"h" : "left", "b" : "thumbrest"},
}

manifest = {
    "default_bindings" : [],
    "actions" : [],
    "action_sets" : [
        {
            "name" : "/actions/default",
            "usage" : "leftright"
        }
    ]
}

for c in controllers:
    manifest["default_bindings"].append({"controller_type" : c, "binding_url" : c + ".json"})

for b in boolActions:
    manifest["actions"].append({"name" : "/actions/default/in/" + b, "requirement" : "suggested", "type" : "boolean"})

for v in vec1Actions:
    manifest["actions"].append({"name" : "/actions/default/in/" + v, "requirement" : "suggested", "type" : "vector1"})
    
for v in vec2Actions:
    manifest["actions"].append({"name" : "/actions/default/in/" + v, "requirement" : "suggested", "type" : "vector2"})

try:
    with open("actions.json", "w") as f:
        f.write(json.dumps(manifest, indent=4))
except:
    print ("failed to create manifest")
else:
    print ("successfully created manifest")

#todo: merge thumbstick dpad actions
for c in controllers:
    controller = {
        "bindings" : {
            "/actions/default" : {
                "haptics" : [],
                "poses" : [],
                "sources" : [],
                "skeleton" : []
            }
        },
        "controller_type" : c,
        "description" : "Autogenerated bindings for " + c,
        "app_key" : "system.generated.halo.exe",
        "name" : c
    }
    
    for binding in bindings:
        b = bindings[binding]
        
        parameters = {}
        
        mode = "button"
        
        inputs = b["b"].split("|")
        
        inputtype = "click"
        
        if inputs[0] == "joystick":
            if controllers == "knuckles":
                inputs[0] = "thumbstick"
        
            if len(inputs) > 1:
                mode = "dpad"
                parameters["sub_mode"] = "touch"
                inputtype = inputs[1]
                
                needsMerge = False
                
                for entry in controller["bindings"]["/actions/default"]["sources"]:
                    if entry["mode"] == mode and entry["path"] == "/user/hand/" + b["h"] + "/input/" + inputs[0]:
                        needsMerge = True
                        break
                
                if needsMerge:
                    entry["inputs"][inputtype] = {"output" : "/actions/default/in/" + binding}
                    continue
            else:
                mode = "joystick"
                inputtype = "position"
        elif inputs[0] == "grip":
            parameters["click_activate_threshold"] = 0.8
            parameters["click_deactivate_threshold"] = 0.7
        elif inputs[0] == "x":
            if controllers == "knuckles":
                inputs[0] = "a"
        elif inputs[0] == "y":
            if controllers == "knuckles":
                inputs[0] = "b"
        elif inputs[0] == "thumbrest":
            if controllers == "knuckles":
                inputs[0] = "trackpad"
        
        input = {}
        input[inputtype] = {"output" : "/actions/default/in/" + binding}
        
        controller["bindings"]["/actions/default"]["sources"].append({"inputs" : input, "mode" : mode, "path" : "/user/hand/" + b["h"] + "/input/" + inputs[0], "parameters" : parameters})
    
    try:
        with open(c+".json", "w") as f:
            f.write(json.dumps(controller, indent=4))
    except:
        print ("failed to create " + c + ".json")
    else:
        print ("successfully created " + c + ".json")
        


































