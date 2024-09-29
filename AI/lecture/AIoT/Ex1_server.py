import time
import random

# 현재 시간을 초 단위로 정수형으로 저장합니다.
now_time = int(time.time())

# 'flip' 데이터를 센서로부터 받아옵니다. 데이터가 존재하면 첫 번째 값을 사용하고, 없으면 0으로 설정합니다.
flip = get_data("flip", 1)
if len(flip) > 0:
    flip = flip[0][1]
else:
    flip = 0

# 'fliptime' 데이터를 센서로부터 받아옵니다. 데이터가 존재하면 첫 번째 값을 사용하고, 없으면 0으로 설정합니다.
fliptime = get_data("fliptime", 1)
if len(fliptime) > 0:
    fliptime = fliptime[0][1]
else:
    fliptime = 0

# 'mintime' 데이터를 로드합니다. 데이터가 없으면 "NO DATA"로 표시하고, 있으면 소수점 둘째 자리까지만 남깁니다.
mintime = load("mintime")
mintime = "NO DATA" if mintime is None else f"{mintime:.2f} 초"
display("최고 반응 속도", mintime)

####### [ L O G I C ] #######

# 반복 인덱스가 0이면 초기 동기화 메시지를 표시하고, 서버 상태를 'TIMESYNC'로 설정합니다.
if get_repeat_idx() == 0:
    display("메시지", "시간 동기화 중입니다.")
    display("Tip", "센서 코드가 '실행 중'이 된 지 6초 뒤에도 넘어가지 않으면 서버/센서 코드를 모두 종료한 뒤 데이터 초기화 후 '서버 실행 중 > 센서 실행' 순으로 시작하세요.")
    save("servstate", "TIMESYNC")
    print("servstate", "TIMESYNC")

# 서버 상태가 'TIMESYNC'일 때
if load("servstate") == "TIMESYNC":
    tsdata = get_data("timesync", 9)
    if len(tsdata) >= 9:  # 동기화 데이터가 9개 이상 수신되었는지 확인하고
        ts = [tsreal[1] for tsreal in tsdata]  # 수신된 시간 데이터만 추출합니다.
        tscheck = [tsitem != -1 for tsitem in ts]  # 시간 데이터가 유효한지 확인합니다.
        tsdiffs = [tsreal - now_time + 0.5 * i for i, tsreal in enumerate(ts)]  # 각 시간 데이터에 대해 서버와의 시간 차이를 계산합니다.
        if all(tscheck):  # 모든 시간 데이터가 유효하면
            tsavgdiff = sum(tsdiffs) / 9  # 평균 시간 차이를 계산합니다.
            save("tsdiff", tsavgdiff)  # 계산된 평균 시간 차이를 저장합니다.
            print("tsdiff", tsavgdiff)

            save("servstate", "READY")  # 서버 상태를 'READY'로 변경합니다.
            print("servstate", "READY")

            save("timer", int(random.random() * 100 + 35))  # 타이머를 랜덤 값으로 초기화합니다.
else:
    servstate = load("servstate")  # 현재 서버 상태를 로드합니다.

    if servstate == "READY":  # 서버 상태가 'READY'인 경우
        if flip == 1:  # flip 상태가 1이면
            act_led("지시등", "black")  # 지시등을 검은색으로 설정합니다.
            display("메시지", "휴대폰을 화면이 보이도록 다시 뒤집으세요.")
            display("Tip", "")
            save("timer", int(random.random() * 100 + 35))  # 타이머를 랜덤 값으로 재설정합니다.
        elif load("timer") > 0:  # 타이머가 0보다 크면
            act_led("지시등", "red")  # 지시등을 빨간색으로 설정합니다.
            display("메시지", "흰색으로 바뀌는 순간 휴대폰을 뒤집으세요.")
            display("Tip", "")
            save("timer", load("timer") - 1)  # 타이머 값을 1 감소시킵니다.
        else:
            save("servstate", "FLIPREADY")  # 타이머가 0이 되면 서버 상태를 'FLIPREADY'로 변경합니다.
            print("servstate", "FLIPREADY")
            save("timer", -1)  # 타이머를 -1로 설정합니다.
    elif servstate == "FLIPREADY":  # 서버 상태가 'FLIPREADY'인 경우
        if flip == 1:  # flip 상태가 1이면
            bansok = max(now_time - fliptime - load("tsdiff"), 0)  # 현재 시간에서 fliptime과 tsdiff를 뺀 값을 계산하여 반응 속도를 구합니다.
            act_led("지시등", "black")  # 지시등을 검은색으로 설정합니다.
            display("메시지", f"반응 속도 : {bansok:.2f} 초")  # 계산된 반응 속도를 디스플레이합니다.
            display("Tip", "휴대폰을 원래대로 다시 뒤집으세요.")
            mintime = load("mintime")  # 기존에 저장된 최소 반응 속도를 로드합니다.
            if mintime is None:  # 기존 데이터가 없으면
                save("mintime", bansok)  # 현재 반응 속도를 저장합니다.
            elif mintime >= bansok:  # 새로운 반응 속도가 기존 기록보다 빠르면
                save("mintime", bansok)  # 새로운 기록으로 갱신합니다.
            save("timer", 50)  # 타이머를 50으로 설정합니다.
            save("servstate", "SUCCESS")  # 서버 상태를 'SUCCESS'로 변경합니다.
            print("servstate", "SUCCESS")
        elif load("timer") > 50:  # 타이머가 50을 초과하면
            save("servstate", "RESET")  # 서버 상태를 'RESET'으로 변경합니다.
            print("servstate", "FRESET")
        else:
            act_led("지시등", "white")  # 지시등을 흰색으로 설정합니다.
            display("메시지", "흰색으로 바뀌는 순간 휴대폰을 뒤집으세요.")
            display("Tip", "")
            save("timer", load("timer") + 1)  # 타이머 값을 1 증가시킵니다.
    elif servstate == "SUCCESS":  # 서버 상태가 'SUCCESS'인 경우
        if load("timer") > 0:  # 타이머가 0보다 크면
            save("timer", load("timer") - 1)  # 타이머 값을 1 감소시킵니다.
        else:
            save("servstate", "RESET")  # 타이머가 0이 되면 서버 상태를 'RESET'으로 변경합니다.
            print("servstate", "RESET")
    elif servstate == "RESET":  # 서버 상태가 'RESET'인 경우
        act_led("지시등", "black")  # 지시등을 검은색으로 설정합니다.
        display("메시지", "휴대폰을 원래대로 다시 뒤집으세요.")
        display("Tip", "")
        if flip == 0:  # flip 상태가 0이면
            save("timer", int(random.random() * 100 + 35))  # 타이머를 랜덤 값으로 설정합니다.
            save("servstate", "READY")  # 서버 상태를 'READY'로 변경합니다.
            print("servstate", "READY")
    else:
        pass  # 다른 모든 상태에 대해서는 아무 작업도 수행하지 않습니다.

# 50ms 간격으로 반복합니다.
time.sleep(0.1)
