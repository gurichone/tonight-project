# check_strからstartとendに挟まれた部分をを抽出する関数
def extract_info(check_str, start, end):
    flag = False
    num = 0
    check_end = ''
    ans = ''

    for s in check_str:
        # endまでの文字列をansにいれる
        if flag == True:
            if s == end[num]:
                check_end += s
                num += 1
                if check_end == end:
                    break
            else:
                ans += check_end + s
                # endと不一致になるごとにnumとcheck_endを初期化
                num = 0
                check_end = ''
            continue
        # startと一致する部分を探す
        if start[num] == s:
            num += 1
            if num == len(start):
                num = 0
                flag = True
        else:
            num = 0

    if flag:
        return ans
    else:
        return 'not found'