import json

# カルテ本文の文字数をカウントしてcountキーとして辞書に新しく追加する
# 辞書を要素として格納している配列が引数に来ることが前提なのに、それが伝わらない書き方になっていると思うので、機能の分離も含めもっと良い書き方があるような気がします
def add_count(data):
    i = 0
    while i < len(data):
        data[i]['count'] = len((data[i]['text']).replace("\n",""))
        i += 1
    return(data)

# テキスト中の"。"から次の”）”までを見つけ、アノテーションとしてリストに格納して返す。
# アノテーションという呼び方は変えた方が良いのかもしれない
def create_annotation_list(string):
    result = []
    i = 0
    period = 0
    has_period = 1 #predでの))))のような箇所での挙動を修正するため。文頭にアノテーションがある場合を拾うため1
    has_brackets = 0 # (60日分)のような文言があると誤判断してしまうため
    while i < len(string):
        if (string[i] == "("):
            has_brackets = 1
        elif (string[i] == "。"):
            period = i
            has_period = 1
        elif (string[i] == ")" and has_brackets == 1):
            has_brackets = 0
        elif (string[i] == ")" and has_brackets == 0 and has_period == 1):
            result.append(string[period:i].replace("。",""))
            has_period = 0
        i += 1
    return(result)

# correctにあってtestにないものをリストで返す
def find_diff_list(correct_list,test_list):
    i = 0
    result = []
    while i < len(correct_list):
        j = 0
        while j < len(test_list):
            if (correct_list[i] == test_list[j]):
                break
            elif (correct_list[i] != test_list [j]):
                j += 1
                if (j == len(test_list)):
                    result.append(correct_list[i])
                continue
            j += 1
        i += 1
    return(result)

# diffキーを追加。一番不安な書き方をしている気が……
def add_diff(data):
    i = 0
    while i < len(data):
        data[i]['diff'] = find_diff_list(create_annotation_list(data[i]['label']),create_annotation_list(data[i]['pred']))
        i += 1
    return(data)


# ------------------main------------------

with open('data.json') as f:
    data = json.load(f)

result = add_diff(add_count(data))

# print(result)

with open('test.json','w') as f:
    json.dump(result,f,indent=4,ensure_ascii=False)