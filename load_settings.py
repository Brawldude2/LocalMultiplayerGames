from pygame.key import key_code

def load_player_controls(data,max_player_count):
    key_map = [0 for i in range(max_player_count*5)]
    for line in data:
        player_num,data = line.split(":")
        player_num = int(player_num[6:])
        keys = data.split(",")
        for key in keys:
            offset = (player_num-1)*5
            if key.startswith("up"):
                key_map[0+offset] = key_code(key[3])
            if key.startswith("down"):
                key_map[1+offset] = key_code(key[5])
            if key.startswith("left"):
                key_map[2+offset] = key_code(key[5])
            if key.startswith("right"):
                key_map[3+offset] = key_code(key[6])
            if key.startswith("mono"):
                key_map[4+offset] = key_code(key[5])
    return key_map
        
        

def load_input_mask(keyboard,max_player_count=4):
    with open("Settings/default_inputs.txt","r") as outfile:
        text = outfile.readlines()
    s_index = 0
    for i,line in enumerate(text):
        if "F_Keyboard" in line:
            s_index = i+1
            break
    return tuple(load_player_controls(text[s_index:s_index+max_player_count],max_player_count))





