import os

class JsonSearch():
    # 파일 검색 (폴더명 혹은 전체탐색 시 .)
    # 현재 경로 확인 필수
    def search(self, dirname, ext = '.json'):
        filenames = os.listdir(dirname)
        fl = []
        for filename in filenames:
            if ext in filename:
                fl.append(os.path.join(dirname, filename))
        
        self.file_list = fl
        return self.file_list
