import pandas as pd
from SNS import FileSearch
from konlpy.tag import Okt
from SNS import WordPre

# 텍스트 전처리 (해시태그 추출해서 파일로 저장)
fl = FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/AA')
fl.extend(FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/AB'))
fl.extend(FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/AC'))
fl.extend(FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/NO4/AA'))
fl.extend(FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/NO4/AB'))
fl.extend(FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/NO1/AA'))
fl.extend(FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/NO1/AB'))
fl.extend(FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/NO3'))
wp = WordPre.Pre()
okt = Okt()

target_path = '/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/prepost/'
count = 0
complete = True
MAX_File = len(fl)
for f in fl:
    count+=1
    try:
        temp = pd.read_json(f)[['insta_id', 'content']].dropna()
    except:
        print(f)
    # print(temp['content'])
    try:
        temp['hashtag'] = wp.search('(?<=\#)[^# ]+', [wp.del_escape(c) for c in temp['content']])
    except:
        print(f)
        complete = False
        break
    temp.to_csv(target_path+'{}.txt'.format(count), sep='\t')
    print('해시태그 추출 {:2f}% 진행 중'.format(count/MAX_File))
    
if complete:
    # 학습을 위한 데이터 insta_id, hashtag, target
    print('파일 합치기 진행 中')
    fl = FileSearch.JsonSearch().search('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/prepost', '.txt')
    MAX_File = len(fl)
    result_df = pd.DataFrame()
    count = 0
    id_df = pd.read_json('/home/lab10/JJC/sns_project/Insta/Insta_Data/insta_id_raw.json').set_index('insta_id')
    for f in fl:
        count += 1
        temp = pd.read_csv(f, sep='\t')[['insta_id', 'hashtag']].set_index('insta_id')
        temp['target'] = id_df['target']
        result_df = pd.concat([result_df, temp.dropna()])
        print('파일 합치기 {:2f}% 진행 중'.format(count/MAX_File))
    


    result_df.to_csv('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/post_data.txt', sep='\t')

# 파일 추가 필요 시

# temp = pd.read_json('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/insta_post/insta_post_2nd.json')[['insta_id', 'content']].dropna()
# temp['hashtag'] = wp.search('(?<=\#)[^# ]+', [wp.del_escape(c) for c in temp['content']])
# temp['insta_id'] = list(map(int, temp['insta_id']))
# temp['insta_id'] = list(map(str, temp['insta_id']))
# result_df = pd.read_csv('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/post_data.txt', sep='\t')
# result_df = pd.concat([result_df, temp])
# temp.to_csv('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/post_data.txt', sep='\t')