import os
import sip
import random
from Data import Watch_Data
from PyQt5.QtWidgets import QListWidgetItem, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import QDir

class Utils:
    def __init__(self):
        self.File_data = Watch_Data()


    def scan_files(self, movie_container):
        self.File_data.scan_functions()
        
        data = self.File_data.get_parent_files()
        self.update_main_container(movie_container, data)


    def change_main_dir(self, main_window, stack):
        folder_path = QFileDialog.getExistingDirectory(main_window,"Choose New Main Folder", QDir.homePath() + "/Videos")

        if folder_path:
            self.File_data.json_data["parent_path"] = folder_path.replace('/', '\\')
            self.File_data.save_JSON_data(self.File_data.json_data)
            stack.setCurrentIndex(0)

        return folder_path


    def play_random(self, movie_container, load_film, window):
        movie_count = movie_container.count()
        movies_title = [str(movie_container.item(i).text()) for i in range(movie_count) 
                        if self.File_data.is_movie(self.get_widget_text(movie_container.item(i)))] #contains only movie/videos
        
        if movies_title:
            random_index = random.randint(0, len(movies_title)-1)
            chosen_movie = movies_title[random_index]
            self.play_movie(chosen_movie, load_film, window)

            if window.ui.Stack.currentIndex != 1: 
                window.ui.Stack.setCurrentIndex(1)

        else:
            self.show_error_msgbox(window, 'No Videos Found!', 'Make sure to open a folder with a video file.')


    def get_widget_text(self, widget):
        return str(widget.text())


    def play_movie(self, chosen_movie, load_film, window):
        load_film(f'{self.File_data.json_data["all_movies"][chosen_movie]}')
        window.setWindowTitle('Movie Explorer - ' + chosen_movie)


    def show_error_msgbox(self, parent, title, content):
        msg = QMessageBox()
        msg.critical(parent, title, content)
    

    def get_path_btns(self, path_frame):
        path = self.File_data.json_data["parent_path"]
        btns = path_frame.findChildren(QPushButton)

        for i in range(1,len(btns)):
            path += '\\' + self.get_widget_text(btns[i])   

        return [btns, path]


    def update_main_container(self,movie_container, data):
        movie_container.clear()

        if type(data) == dict:
            data = sorted(data.keys())
        elif type(data) == list:
             data.sort()

        for fi in data:
            item = QListWidgetItem(f'{fi}')
            movie_container.addItem(item)


    def get_folder_data(self, path):
        movie_data = self.File_data.json_data["movie_data"]
        temp_data = movie_data.copy()

        for key in temp_data:
            if path not in movie_data or path in key:  #If the current_open folder is not on movie data but the key of movie data contains the path
                movie_data[path] = {}   #To prevent having a key error
                self.File_data.save_JSON_data(self.File_data.json_data)

        data = movie_data[path]     # This will be represent as key. Ex. C:\\User\...\movie where movie is the current open folder

        for folder in os.listdir(path):     # Iterate all the files in the current_open folder - ex. movie  -   path == movie
            current_path = os.path.join(path, folder)      #current_path == absolute path on each file in the current_open folder - ex. movie

            if os.path.isdir(current_path): #   check if the path is folder then:
                valid_path_files = []     #This arr will be act as one of the condition

                for f in os.listdir(current_path):      #iterate through all the files in the sub_folder of current_open folder. Ex. Folder inside the movie folder - Lion King
                    sub_folder_file_path = os.path.join(current_path, f)    #absolute path of the file in the sub_foldder of current_open folder
                    if self.File_data.is_movie(f):        
                        valid_path_files.append(f)
                        continue
                    
                    if sub_folder_file_path in movie_data:  #if this path exist exactly on movie data or the folder contains movie then: 
                        valid_path_files.append(f)
                    
                    for key in movie_data:      #iterate through all the key in movie_data
                        if os.path.isdir(key):  
                            if sub_folder_file_path in key:     #if the key contains the path even though it's not fully identical then:
                                valid_path_files.append(f)


                if len(os.listdir(path)) > 20 and len(valid_path_files) == 1:   #This block will only execute if the sub_folder of current_open_folder contains only one movie and does not have a folder which contains a move in it.
                    temp_path = f'{os.path.join(current_path, valid_path_files[0])}'    #Absolute path of the movie
                    data[self.File_data.get_movie_name(valid_path_files[0])] = temp_path    #append to the data


                else:   #This block will execute if there are multiple movie in sub_folder of the current_open folder and does not have a folder which contains movie
                    if current_path in movie_data:  #If the absolute path of sub_folder in current_open_folder in movie data then: 
                        data[folder] = current_path     #append to the data which has a key if its folder name and value of its absolute path
                    
                    for key in movie_data: 
                        if os.path.isdir(key):
                            if current_path in key: #check every key if it's contain  absolute path of the subfolder in current_open_folder 
                                data[folder] = current_path

            elif self.File_data.is_movie(current_path):
                data[self.File_data.get_movie_name(folder)] = current_path

        self.File_data.save_JSON_data(self.File_data.json_data)

        return data


    def del_path_folder_btns(self, widgets):
        for btn in widgets:
            sip.delete(btn)


    def create_path_folder_btns(self, win_ui, path):
        self.del_path_folder_btns(win_ui.path_frame.findChildren(QPushButton) + win_ui.path_frame.findChildren(QLabel))

        path_folder = path.split('\\')
        btns_title = path_folder[path_folder.index(self.File_data.main_folder):]

        for title in btns_title:
            win_ui.path_frame_hlayout.addWidget(QLabel('>>'))
            btn = QPushButton(title)
            win_ui.path_frame_hlayout.addWidget(btn)
            btn.clicked.connect(lambda checked, text=title : self.display_folder_files(win_ui, path, text))    


    def display_folder_files(self, win_ui, path, title):
        path_element = path.split('\\')

        if title == self.File_data.main_folder:
            data = self.File_data.get_parent_files()
            self.update_main_container(win_ui.movie_container, data)
            self.create_path_folder_btns(win_ui, self.File_data.path)

        else:
            new_path = '\\'.join(path_element[:path_element.index(title)+1])
            data = self.get_folder_data(new_path) 

            self.update_main_container(win_ui.movie_container, data)
            self.create_path_folder_btns(win_ui, new_path)

    





##### HIDE CONTROL LAYOUT ####
'''''
    Main idea: After the players open, call the function that handle the controls state:
        if the control is shown then:
            call a function that have a timer:
                if the timer is equal to 0 or after 5 sec then hide

        on mouse move:
            if control is hidden:
                show it
            else: 
                do nothing

            after mouse move:    
                call a function that have a timer
'''''