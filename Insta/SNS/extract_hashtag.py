import pandas as pd
import json
import re

class extract_hashtag () :
    def __init__(self):
        return
    
    def _read_json(self, file_path):
        f = pd.read_json('{}'.format(file_path))
        
        return list(f['content'])
    
    def _separate_contents(self, df_file) :
        hash_ls = [] # 해쉬테그만
        hash_remove_content = [] # 해쉬제거 text
        for i in range(len(df_file)):        
            tmp = []
            if re.findall('\#[\w가-힣a-zA-Z0-9]*', str(df_file[i])):
                hash_ls.append(re.findall('\#[\w가-힣a-zA-Z0-9]*', str(df_file[i])))
            else :
                hash_ls.append('')
            
            tmp = re.sub('\#[\w가-힣a-zA-Z0-9]*',"",str(df_file[i])) 
            tmp = re.sub("\n"," ",tmp)
            tmp = re.sub("\@[\w가-힣a-zA-Z0-9]*","",tmp)
            # tmp = re.sub("\n","",tmp) 여기 "\n"자리에 이모지제거 형식 넣으면됩니다!
            hash_remove_content.append(tmp)
        
        return hash_ls, hash_remove_content
    
    def _hash_remove(self, hash_ls) :
        hash_remove_ls = []
        for i in hash_ls:
            tmp = []
            for j in  i:
                tmp.append(re.sub("#","",j))
            hash_remove_ls.append(tmp)
        
        return hash_remove_ls
    
    def call_hash_and_content(self, file_path) :
        f = self._read_json(file_path)
        hashtag, content = self._separate_contents(f)
        hashtag = self._hash_remove(hashtag)
        
        return hashtag, content