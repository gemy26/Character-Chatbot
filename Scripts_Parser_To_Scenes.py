import json
import os
path = "./Scripts_txt"
dir_list = os.listdir(path)


def parse_file(file_name):
    file_path = path + '/' + file_name
    scenes = []
    with open(file_path, "r", encoding= "UTF-8") as file:
        # print("file opend succ")
        current_scene = ""
        for line in file:
            line = line.strip()
            if line.startswith(("ITN", "EXT")):
                if(current_scene != ""):
                    scenes.append(current_scene)
                    current_scene = ""
                current_scene = line 
            else:
                current_scene += line + "\n"           
        if current_scene != "":
            scenes.append(current_scene.strip())     

    return scenes                



def get_scenes(file_name):
    scenes = parse_file(file_name)
    print(len(scenes))
    with open(f"Scenes/{file_name[:-4]}.json", "w") as file:
        json.dump([{"scene": item} for item in scenes], file, indent=4)






for file in dir_list:
    get_scenes(file)
    


    