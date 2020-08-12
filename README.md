# [SNS User Profiling 프로젝트] sns_project

> 관련참고

> 1. 텍스트 마이닝을 활용한 금융통화위원회 의사록 분석

> https://www.bok.or.kr/portal/bbs/P0002454/view.do?nttId=10049321&menuNo=200431&pageIndex=2

> 1. 분석 요약

> https://drive.google.com/file/d/1w_tGNzVk3Q_RKzk-9VY-J6POkoUA3UXF/view?usp=sharing

> 1. 최종분석결과

> https://drive.google.com/file/d/1FS-0Fxcpf0toOQ9hmwha_-j2ShjOiDo-/view?usp=sharing

### 프로젝트 내려받기

```
git clone 'https://github.com/svstar94/sns_project.git'
```

## 0. 패키지 다운로드

### 0.1. requirements.txt

```
pip install -r requirements.txt
```

### 0.2. eKoNLPy 설치

```
pip install ./eKoNLPy-master/.
```

> 부가적인 설치 방법은 해당 링크 참조

> http://blog.naver.com/PostView.nhn?blogId=jjys9047&logNo=221586527508&parentCategoryNo=&categoryNo=45&viewDate=&isShowPopularPosts=false&from=postView

## 1. news_crawler

### crawling 디렉토리로 이동

```
cd crawling
```

### scrapy 크롤러 동작 명령어

```
scrapy crawl navernews                # csv 형식으로 저장(default)
scrapy crawl navernews -o test.json   # json 형식으로 저장
```