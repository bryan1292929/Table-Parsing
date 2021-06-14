# Table-Parsing
- 공시 데이터 속 관계/정보 추출을 위한 코드
- src 폴더 내에 3개의 폴더가 있음 (model, process_data, re_util)
- 각 폴더는 관계추출을 위한 각 태스크에 적용되는 함수들을 담고 있음

1. model 폴더:
- 관계추출을 위한 Candidate Window 기반 QA모델을 평가하기 위한 함수들

1-1. baseline.py
- 규칙기반 baseline 모델의 평가를 위한 함수
- SQUAD 형식 평가셋을 dictionary 형태로 input
- Candidate Window에서 h_dict value가 가장 큰 것을 header로 guess (random shuffle 이후)

1-2. model.py
- Bert기반 모델의 평가를 위한 함수
- bert_accuracy(guess_list, answer_list, h_dict)라는 함수가 메인
  - guess_list: 모델이 각 QA별로 답이라 guess한 것들의 모음
    * 모델을 돌린 후 생성되는 predictions.json 파일이 input
  - answer_list: 각 QA에 해당하는 정답
    * test_set에 해당하는 SQUAD 형식의 json이 input
  
2. process_data 폴더:
- Bert 학습과 평가를 위한 데이터셋을 만들기 위한 함수들

2-1. extract 폴더:
- xml 파일 내의 TABLE element들을 총체적으로 사용하는 함수들

2-1-1. raw2Squad.py
- 폴더를 주었을 때 Squad 형식의 dictionary 및 json파일을 만듦
- 현재 context 생성 방법:
  * H + V or V + H
  * 토큰은 첫 5개, 마지막 2개
  * 공백은 '*'로 context에 추가
  * 길이가 10이 넘는 string은 10번째 char까지의 substring을 사용
  * 정답이 h_dict에 포함된 경우와 포함되지 않은 경우를 구분하기 위해서는 candidate_windows라는 함수의 answer_in_dict이라는 boolean을 이용. (line 96, 97)
    * 현재 예시 (line 97)는 정답이 h_dict에 포함됐을 때, 1/8의 확률로 QA를 데이터에 추가.
- json_from_folder(folder, name, h_dict)라는 함수가 메인
  - folder: 학습데이터 or 평가데이터를 담고 있는 폴더의 이름
  - name: 새롭게 만드는 json파일의 이름
- dict_from_json(name)이라는 함수는 위에서 만든 json 파일을 사전 형태로 변환해줌

2-1-2. traverse_data.py
- 폴더 내의 파일, 파일 내의 TABLE들을 탐색하기 위한 함수들

2-1-3. unmerge_table.py
- TABLE element가 주어졌을 때, unmerge된 text_matrix를 돌려줌
- unmerge(table)라는 함수가 메인

2-2. header_dictionary 폴더:

2-2-1. header.py
- THEAD와 관련된 것들을 다루는 함수들
- rowspan_guess(table), colspan_guess(table): vertically slice하는 index를 return
  * 둘이 일치할 때만 사용
- header_idx(table): TABLE의 몇번째 행까지가 THEAD인지 return.
  * THEAD가 없으면 header_idx = -1, 첫번째 행만 THEAD면 header_idx = 0, ...
- pickle_from_folder(folder, index_type, name): 주어진 폴더 내의 xml 파일들을 이용해 h_dict 생성
  - folder: 폴더명
  - index_type: True면 THEAD 마지막 행의 header만 선택, False면 THEAD 내의 모든 cell들을 이용
  - name: 생성되는 h_dict를 담는 pickle의 이름

3. re_util 폴더
- 데이터 전처리를 위한 함수들

3-1. re_util.py
- clean_matrix(text_matrix): 주어진 TABLE의 text_matrix 속 각 cell들을 전처리해서 새로운 matrix를 return
- clean(input_str): 주어진 문자열을 전처리해줌
  * 이 안에 들어가는 함수들을 변경해주면 데이터의 전처리가 달라짐
