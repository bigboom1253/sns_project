import json
import os

class JsonMaker():

    # Large Folder Index
    f_li = 65
    # Small Folder Index
    f_si = 65

    # File Name (Number)
    fn = 1

    # 호출 수
    count = 0

    last_path = ''

    # File Path 통합용 (Post, Follower, Follow) 별로 구분하기
    def __init__(self, file_path = './Insta_Data/'):
        self.file_path = file_path

    def create_folder(self):
        fol_dir = self.file_path + chr(self.f_li) + chr(self.f_si)
        try:
            if not os.path.exists(fol_dir):
                os.makedirs(fol_dir)
        except OSError:
            print('Error: Creating Directory' + fol_dir)
        self.last_path = fol_dir + '/'

    # file path, name 통합
    def write_file(self, data):
        self.file = open(self.last_path + str(self.fn) + '.json', 'a')
        self.file.write('[\n' + json.dumps(data))
        self.count += 1

    def add_data(self, data):
        self.file.write(',\n' + json.dumps(data))
        self.count += 1
        if self.count==10000:
            self.close_file()
            self.count = 0
            self.fn += 1
            if self.fn == 101:
                self.fn = 1
                self.f_si += 1
                if self.f_si == 91:
                    self.f_li += 1
                    self.f_si = 65
                self.create_folder()
            self.write_file({})


    def close_file(self):
        self.file.write('\n]')
        self.file.close()
