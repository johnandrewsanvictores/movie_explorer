import json
import glob


class Watch_Data:
    def __init__(self):
        self.json_data = self.get_JSON_data()
        self.extensions = ["mp4", '3pg', 'avi', 'mov', 'mpeg', 'vob']
        self.path = self.json_data["parent_path"]
        self.main_folder = self.path.split('\\')[-1]

        if "movie_data" not in self.json_data or "sub_folder" not in self.json_data or "all_movies" not in self.json_data:
            self.scan_functions()

        
    def scan_functions(self):
        self.all_movies = self.get_all_movies(self.get_movie_data_value("parent_path"))
        self.save_all_movies()
        self.set_parent_files(self.get_movie_data_value("parent_path"))
        self.set_sub_files()

    
    def get_all_movies(self, path):
        return list(filter(lambda x: x.split('.')[-1].lower() in self.extensions, glob.glob(f"{path}\\**\\*", recursive=True)))

    def save_all_movies(self):
        self.path = self.json_data["parent_path"]
        self.main_folder = self.path.split('\\')[-1]
        
        temp = {}
        movie_key = list(map(lambda x: self.get_movie_name(x), self.all_movies))
        
        for key, value in zip(movie_key, self.all_movies):
            temp[key] = value

        self.json_data["all_movies"] = temp
        self.save_JSON_data(self.json_data)


    def get_parent_files(self):
        parent_movies = []
        for key in self.json_data["movie_data"]:
            if key.split('.')[-1].lower() in self.extensions:
                parent_movies.append(key)
        
        parent_files = parent_movies + self.json_data["sub_folder"]
        parent_files.sort()

        return parent_files

    def set_parent_files(self, path):
        self.json_data["movie_data"] = {}
        self.json_data["sub_folder"] = {} 

        self.subfiles, self.sub_folder = self.get_sub_movies(path, self.all_movies)
        parent_files = list(filter(lambda x: x not in self.subfiles, self.all_movies))
        temp = {}
        
        for key,value in zip(list(map(lambda x: self.get_movie_name(x), parent_files)), parent_files):
            temp[key] = value

        self.json_data["movie_data"] = temp
        self.json_data["sub_folder"] = self.sub_folder
        self.save_JSON_data(self.json_data)

    def set_sub_files(self):
        temp = {}
        temp_arr = []
        self.subfiles.sort()

        for i in range(1, len(self.subfiles)):
            current_file_path = ''.join(self.subfiles[i].split('\\')[:-1])
            previous_file_path = ''.join(self.subfiles[i-1].split('\\')[:-1])

            if i == 1:
                if ''.join(self.subfiles[0].split('\\')[:-1]) == ''.join(self.subfiles[1].split('\\')[:-1]):
                    temp_arr.append(self.subfiles[0])

            if current_file_path == previous_file_path:
                temp_arr.append(self.subfiles[i])

            if current_file_path != previous_file_path or i == len(self.subfiles)-1:
                for key,value in zip(list(map(lambda x: self.get_movie_name(x), temp_arr)), temp_arr):
                    temp[key] = value

                if self.subfiles[i-1].split('\\')[-1] not in self.sub_folder:
                    self.json_data["movie_data"] = self.merge_dic(self.json_data["movie_data"], {'\\'.join(self.subfiles[i-1].split('\\')[:-1]) : temp})
                
                self.save_JSON_data(self.json_data)

                temp = {}
                temp_arr = []
        

    def merge_dic(self,dic1, dic2):
        return {**dic1, **dic2}


    def get_sub_movies(self, parent, movie_array):
        parent_folder = parent.split('\\')[-1]
        sub_movies = []
        sub_folder = []

        for i in range(1,len(movie_array)-1):
            current_movie_folder = self.get_current_folder(movie_array[i], parent_folder)
            previous_movie_folder = self.get_current_folder(movie_array[i-1], parent_folder)
            next_movie_folder = self.get_current_folder(movie_array[i+1], parent_folder)

            if current_movie_folder == None or previous_movie_folder == None or next_movie_folder == None: continue

            if current_movie_folder == previous_movie_folder and current_movie_folder != parent_folder:         
                sub_movies.append(movie_array[i-1])
                sub_movies.append(movie_array[i])

                if current_movie_folder not in sub_folder:
                    sub_folder.append(current_movie_folder)
                    

            if current_movie_folder == next_movie_folder and current_movie_folder != parent_folder:
                if movie_array[i] not in sub_movies:
                    sub_movies.append(movie_array[i])

                sub_movies.append(movie_array[i+1])
                
                if current_movie_folder not in sub_folder:
                    sub_folder.append(current_movie_folder)

        return [sub_movies, sub_folder]


    def is_movie(self,f):
        return f.split('.')[-1].lower() in self.extensions


    def get_movie_name(self, full_movie_path):
        return full_movie_path.split('\\')[-1]     

    def get_current_folder(self,movie, parent):
        path_split = movie.split('\\')

        if parent not in path_split: return

        parent_index = path_split.index(parent)
        return movie.split('\\')[parent_index + 1]


    def get_JSON_data(self):
        with open('data.json', 'r') as f:
            data = json.load(f)  
        return data

    def get_movie_data_value(self, key):
        return self.get_JSON_data()[key]


    def save_JSON_data(self,data):
        with open("data.json", 'w') as f:
            json.dump(data, f, indent=2)

    def reset_JSON_data(self):
        self.get_JSON_data()["movie_data"] = {}
        self.get_JSON_data()["sub_folder"] = []
        self.get_JSON_data()["all_movies"] = {}
        self.save_JSON_data(self.get_JSON_data())
