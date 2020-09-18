# [SNS User Profiling 프로젝트] 관심사 예측



> 관련참고

> 1. Twitter User Profiling 논문 분석

> https://drive.google.com/file/d/10nOya5gDsnjoDfzgar4S3IUy3w4_Mmd0/view?usp=sharing

> 1. 최종 분석 결과

> https://drive.google.com/file/d/1sTRl8DDt7VgiQdrO9pAsHlOkT7Mgvstz/view?usp=sharing



### 프로젝트 내려받기

```
git clone 'https://github.com/svstar94/sns_project.git'
```



## 0. 패키지 다운로드

### 0.1 requirements.txt

```
pip install -r requirements.txt
```

### 0.2 PyKoSpacing 패키지 사용을 위해 깃 설치 필요

https://git-scm.com/downloads



## 1. Instagram_crawling

### 1.1 Insta 디렉토리로 이동

```
cd sns_project/Insta
```

### 1.2 scrapy 크롤러 동작 명령어

```
scrapy crawl insta_tag -a HASTAG='검색할 해시태그'
scrapy crawl insta_post -a INSTA_ID='검색할 인스타 아이디'
scrapy crawl insta_follow -a INSTA_ID='검색할 인스타 아이디'
scrapy crawl insta_follower -a INSTA_ID='검색할 인스타 아이디'
```

※ 인스타 아이디는 인스타그램 닉네임이 아닌 인스타그램 DB에 있는 Index 번호임



## 2. Target User Profiling

### 2.1 sns_project 디렉토리로 이동

```
cd sns_project
```

### 2.2 타겟 유저 관심사 예측 명령어

```
& ../anaconda3/python.exe ../sns_project/Insta/INSTA_PROFILING.py TARGET_ID
```



## 3. 사용 패키지 정보

### 3.1 PyKoSpacing

전처리 시 띄어쓰기 문제를 해결

https://github.com/haven-jeon/PyKoSpacing

### 3.2 SoyNLP

비지도 학습법을 통해 단어 추출, 토큰화, 벡터화

https://github.com/lovit/soynlp

### 3.3 Support Vector Machine (LibSVM)

sklearn SVM도 LibSVM 기반임. 선형, 비선형, SVM 멀티 클래스 분류

https://www.csie.ntu.edu.tw/~cjlin/libsvm/



