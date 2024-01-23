import os
import sys
sys.path.append('/home/pi/togikai/togikai_function/')
import togikai_drive
import togikai_ultrasonic
import signal
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time
import numpy as np

# GPIOピン番号の指示方法
GPIO.setmode(GPIO.BOARD)

#超音波センサ初期設定
# Triger -- Fr:15, FrLH:13, RrLH:35, FrRH:32, RrRH:36
t_list=[15,23,27]
GPIO.setup(t_list,GPIO.OUT,initial=GPIO.LOW)
# Echo -- Fr:26, FrLH:24, RrLH:37, FrRH:31, RrRH:38
e_list=[14,24,17]
GPIO.setup(e_list,GPIO.IN)

#PWM制御の初期設定
##モータドライバ:PCA9685のPWMのアドレスを設定
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
##動作周波数を設定
pwm.set_pwm_freq(60)

#アライメント調整済みPWMパラメータ読み込み
PWM_PARAM = togikai_drive.ReadPWMPARAM(pwm)

#Gard 210523
#Steer Right
if PWM_PARAM[0][0] - PWM_PARAM[0][1] >= 100: #No change!
    PWM_PARAM[0][0] = PWM_PARAM[0][1] + 100  #No change!
    
#Steer Left
if PWM_PARAM[0][1] - PWM_PARAM[0][2] >= 100: #No change!
    PWM_PARAM[0][2] = PWM_PARAM[0][1] - 100  #No change!


#パラメータ
#前壁との最小距離
#Cshort = 30
Cshort = 5
#右左折判定基準
short = 70
#モーター出力
FORWARD_S = 70 #<=100
FORWARD_C = 70 #<=100
REVERSE = -60 #<=100
#Stear
LEFT = 90 #<=100
RIGHT = -90 #<=100
#データ記録用配列作成
d = np.zeros(4)
#操舵、駆動モーターの初期化
togikai_drive.Accel(PWM_PARAM,pwm,time,0)
togikai_drive.Steer(PWM_PARAM,pwm,time,0)

#一時停止（Enterを押すとプログラム実行開始）
print('Press any key to continue')
input()

#開始時間
start_time = time.time()

#ここから走行用プログラム
try:
    while True:
        #Frセンサ距離
        front_dis = togikai_ultrasonic.Mesure(GPIO,time,15,14)
        #FrLHセンサ距離
        right_dis = togikai_ultrasonic.Mesure(GPIO,time,23,24)
        #FrRHセンサ距離
        left_dis = togikai_ultrasonic.Mesure(GPIO,time,27,17)

        if front_dis >= Cshort:
            if right_dis <= short and left_dis >= short:
               togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_C)
               togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT) #original = "+"
               comment = "右旋回"
            elif right_dis > short and left_dis < short:
               togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_C)
               togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT) #original = "-"
               comment = "左旋回"
            elif right_dis < short and left_dis < short:
                if (right_dis - left_dis)>10:
                    togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_C)
                    togikai_drive.Steer(PWM_PARAM,pwm,time,LEFT) #original = "-"
                    comment = "左旋回"
                elif(left_dis - right_dis) > 10:
                    togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_C)
                    togikai_drive.Steer(PWM_PARAM,pwm,time,RIGHT) #original = "+"
                    comment = "右旋回"
                else:
                    togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                    togikai_drive.Steer(PWM_PARAM,pwm,time,0)
                    comment = "直進中"
            else:
                togikai_drive.Accel(PWM_PARAM,pwm,time,FORWARD_S)
                togikai_drive.Steer(PWM_PARAM,pwm,time,0)
                comment = "直進中"
        elif time.time()-start_time < 1:
            pass
        else:
            togikai_drive.Accel(PWM_PARAM,pwm,time,REVERSE)
            #togikai_drive.Accel(PWM_PARAM,pwm,time,0) #Stop if something is in front of you
            togikai_drive.Steer(PWM_PARAM,pwm,time,0)
            time.sleep(0.1)
            togikai_drive.Accel(PWM_PARAM,pwm,time,0)
            togikai_drive.Steer(PWM_PARAM,pwm,time,0)
            GPIO.cleanup()
            d = np.vstack([d,[time.time()-start_time, front_dis, left_dis, right_dis]])
            np.savetxt('/home/pi/code/record_data.csv', d, fmt='%.3e')
            print('Stop!')
            break
        #距離データを配列に記録
        d = np.vstack([d,[time.time()-start_time, front_dis, left_dis, right_dis]])
        #距離を表示
        print('Front:{0:.1f} , Left:{1:.1f} , Right:{2:.1f}}'.format(front_dis,left_dis,right_dis))
        time.sleep(0.05)

except KeyboardInterrupt:
    print('stop!')
    np.savetxt('/home/pi/code/record_data.csv', d, fmt='%.3e')
    togikai_drive.Accel(PWM_PARAM,pwm,time,0)
    togikai_drive.Steer(PWM_PARAM,pwm,time,0)
    GPIO.cleanup()
