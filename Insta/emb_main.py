import pandas as pd
import pickle


check =True

import requests
import json

def slackmessage(text = '업무자동화 너무 재미있어요. 슬랙 채널에 메시지 보내기 예제입니다.') :
  webhook_url = "https://hooks.slack.com/services/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" #이것만 넣으면 됨
  slack_data = {'text': text}

  response = requests.post(
      webhook_url, data=json.dumps(slack_data),
      headers={'Content-Type': 'application/json'}
  )

import time
import threading

check_point = 0

def thread_run(check_point):
    t = threading.Timer(3600, thread_run)
    if check_point == 0:
        slackmessage('모델 학습 시작')
        check_point = 1
    elif check_point == 1:
        slackmessage('학습 중..')
    elif check_point == 2:
        slackmessage('Spacing 학습 완료')
        check_point = 1
    elif check_point == 3:
        slackmessage('tokenizer 학습 완료')
        t.cancel()
        return
    elif check_point == 4:
        slackmessage('임베딩 시작')
        check_point = 1
    elif check_point == 5:
        slackmessage('임베딩 완료')
        t.cancel()
        return
    t.start()

thread_run(check_point)

# 재 실행 시 토크나이저, 데이터 불러옴
try:
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    with open("datas.pkl", "rb") as f:
        datas = pickle.load(f)
    check = False
except:
    print('학습된 데이터 없음')
    pass
      

# from pykospacing import spacing

if check:
    # 데이터 불러오기
    target_data = pd.read_csv('/home/lab10/JJC/sns_project/Insta/Insta_Data/final_post.txt', sep='\t')

    # Spacing 패키지 활용 의미단어 추출
    # print(list(target_data['hashtag'][:20]))
    # print()
    # print(spacing('왜안되는거야시발아'))
    # datas = [spacing(d) for d in ]
    # print(datas)
    

    # Spacing 학습된 데이터 저장
    # with open("datas.pkl", "wb") as f:
    #     pickle.dump(datas, f)
    # check_point = 2

    # # 카테고리 숫자화
    # cate = {'스포츠': 0, '카페': 1, '여행': 2, '패션': 3, '맛집': 4, '반려동물': 5, '게임': 6, '미디어감상': 7}
    # target_data['target'] = [cate[t] for t in target_data['target']]

    from soynlp.noun import LRNounExtractor_v2
    noun_extractor = LRNounExtractor_v2(verbose=True)
    nouns = noun_extractor.train_extract(target_data['hashtag'])

    from soynlp.word import WordExtractor

    word_extractor = WordExtractor(
        min_frequency=20, # example
        min_cohesion_forward=0.05,
        min_right_branching_entropy=0.0
    )

    word_extractor.train(target_data['hashtag'])
    words = word_extractor.extract()

    cohesion_score = {word:score.cohesion_forward for word, score in words.items()}

    noun_scores = {noun:score.score for noun, score in nouns.items()}
    combined_scores = {noun:score + cohesion_score.get(noun, 0)
        for noun, score in noun_scores.items()}
    combined_scores.update(
        {subword:cohesion for subword, cohesion in cohesion_score.items()
        if not (subword in combined_scores)}
    )

    from soynlp.tokenizer import LTokenizer

    tokenizer = LTokenizer(scores=combined_scores)

    # 메모리 과할당 방지 토크나이저 저장
    with open("tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)
    check_point = 3


else:
    check_point = 4
    from soynlp.vectorizer import BaseVectorizer

    vectorizer = BaseVectorizer(
        tokenizer=tokenizer,
        min_tf=0,
        max_tf=10000,
        min_df=0,
        max_df=1.0,
        stopwords=None,
        lowercase=True,
        verbose=True
    )

    # corpus.iter_sent = False
    final_data = vectorizer.fit_transform(datas)

    # 학습된 최종 벡터 데이터 저장
    with open("vector_data.pkl", "wb") as f:
        pickle.dump(final_data, f)

    check_point = 5

    # target_data.to_csv('/home/lab10/JJC/sns_project/Insta/Insta_Data/Target_Post/final_data.txt', sep='\t')