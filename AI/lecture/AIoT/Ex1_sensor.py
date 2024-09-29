repeat_idx = get_repeat_idx()  # 현재 반복 실행 횟수를 가져옵니다.
now_time = int(time.time())    # 현재 시간을 초 단위로 가져와서 정수형으로 저장합니다.

if repeat_idx == 0:
    save("flip", 0)            # 'flip' 상태를 0으로 초기화하여 저장합니다.
    send("flip", 0)            # 'flip' 상태 0을 서버나 다른 장치로 전송합니다.
    print("flip is set to", 0) 

    save("flipsaved", False)   # 'flipsaved' 상태를 False로 초기화하여 저장합니다.
    print("ismoved is set to", False) 

if repeat_idx < 100:
    if repeat_idx % 10 == 0:   # 반복 횟수가 10의 배수일 때마다 실행됩니다.
        send("timesync", now_time)  # 현재 시간을 'timesync' 이벤트로 전송합니다.
        print("TIMESYNC")      
    if repeat_idx == 99:       # 반복 횟수가 99에 도달했을 때 실행됩니다.
        print("READY")        
        send("timesync", -1)   # 'timesync' 이벤트로 -1을 전송하여 종료를 알립니다.

else:
    gx, gy, gz = get_gyro()    # 자이로스코프 센서로부터 X, Y, Z 축의 회전율 데이터를 가져옵니다.
    gs = math.sqrt(gx ** 2 + gy ** 2 + gz ** 2)  # 회전율 데이터를 이용해 회전 강도를 계산합니다.

    if gs > 10:                # 계산된 회전 강도가 임계값(10)을 초과하면 실행됩니다.
        save("ismoved", True)  # 'ismoved' 상태를 True로 저장하여 움직임이 있음을 기록합니다.
        if load("flipsaved") == False:  # 이전에 flip 상태가 저장되지 않았다면 실행됩니다.
            saved("fliptime", now_time) # 현재 시간을 'fliptime'으로 저장합니다.
            save("flipsaved", True)     # 'flipsaved' 상태를 True로 설정합니다.
        elif load("ismoved"):           # 움직임이 감지된 상태라면 실행됩니다.
            save("ismoved", False)      # 'ismoved' 상태를 False로 초기화합니다.
            save("flipsaved", False)    # 'flipsaved' 상태를 False로 초기화합니다.
            ry = get_rot()[1]           # 자이로스코프 센서로부터 Y축 회전 각도를 가져옵니다.
            if 165 < abs(ry):           # 회전 각도가 165도 이상이면 실행됩니다.
                if load("flip") == 0:   # 현재 'flip' 상태가 0이면 실행됩니다.
                    save("flip", 1)     # 'flip' 상태를 1로 설정합니다.
                    send("flip", 1)     # 'flip' 상태 1을 전송합니다.
                    send("fliptime", load("fliptime"))  # 저장된 flip 시간을 전송합니다.
                    print("flip is set to 1")  
            else:
                if load("flip") == 1:   # 현재 'flip' 상태가 1이면 실행됩니다.
                    save("flip", 0)     # 'flip' 상태를 0으로 설정합니다.
                    send("flip", 0)     # 'flip' 상태 0을 전송합니다.
                    send("fliptime", load("fliptime"))  # 저장된 flip 시간을 전송합니다.
                    print("flip is set to 0") 
        else:
            pass  # 'ismoved' 상태가 False일 경우 아무 작업도 하지 않습니다.
            
time.sleep(0.05)  # 50ms 간격으로 반복합니다.
