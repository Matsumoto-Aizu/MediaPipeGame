# https://acordecode.com/%E3%80%90python%E3%80%91mediapipe%E3%81%A7%E6%89%8B%E3%82%92%E6%A4%9C%E5%87%BA%E3%81%97%E3%81%A6%E5%86%86%E3%82%BF%E3%83%83%E3%83%81%E3%82%B2%E3%83%BC%E3%83%A0%E3%82%92%E4%BD%9C%E3%82%8B%E6%96%B9/
import cv2
import mediapipe as mp
import random
import time

# MediaPipeのHand Trackingインスタンスを作成
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 画面の幅と高さ
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# ポイントと制限時間の初期化
points = 0
time_limit = 60
start_time = time.time()
game_started = False

appear_timelimit_normal_mogura = 2
appear_timelimit_angry_mogura = 5

#モグラの画像を読み込み
normal_mogura_img_ori = cv2.imread("../asset/normal_mogura.png",-1)
angry_mogura_img_ori = cv2.imread("../asset/angry_mogura.png",-1)

def set_mogura_size_and_position(mogura_img):
    
    mogura_random_size = random.randint(80, 150)
    mogura_img = cv2.resize(mogura_img,(mogura_random_size,mogura_random_size))
    mogura_image_height,mogura_image_width = mogura_img.shape[:2]

    x = random.randint(0, WINDOW_WIDTH-mogura_image_width)
    y = random.randint(0, WINDOW_HEIGHT-mogura_image_height)
    mogura_position = (x,y)

    return mogura_img,mogura_position

# https://blanktar.jp/blog/2015/02/python-opencv-overlay
def appear_mogura(frame,mogura_img,mogura_position):

    x,y = mogura_position[0],mogura_position[1]
    mogura_image_height,mogura_image_width = mogura_img.shape[:2]
    
    mask = mogura_img[:,:,3]
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
    mask = mask / 255  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。

    mogura_img = mogura_img[:,:,:3]  

    frame[y:mogura_image_height+y:, x:mogura_image_width+x] = frame[y:mogura_image_height+y:, x:mogura_image_width+x] * (1 - mask)  # 透過率に応じて元の画像を暗くする。
    frame[y:mogura_image_height+y:, x:mogura_image_width+x] = frame[y:mogura_image_height+y:, x:mogura_image_width+x] + mogura_img * mask  # 貼り付ける方の画像に透過率をかけて加算。


# Webカメラの初期化
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 画像を水平方向に反転してミラー表示
        frame = cv2.flip(frame, 1)

        # ゲームが開始していない場合はスタート画面を表示
        if not game_started:
            cv2.putText(frame, "Press Enter to Start", (150, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Mole Whacking Game", (110, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 2)
            
            cv2.imshow('Mediapipe Game', frame)

            # キー入力を待機してゲームを開始
            key = cv2.waitKey(1)
            if key == 13:  # Enterキー
                game_started = True
                start_time = time.time()
                # モグラの初期位置とサイズを設定
                normal_mogura_img,normal_mogura_position=set_mogura_size_and_position(normal_mogura_img_ori)
                angry_mogura_img,angry_mogura_position=set_mogura_size_and_position(angry_mogura_img_ori)

                normal_mogura_size = normal_mogura_img.shape[0]
                angry_mogura_size = angry_mogura_img.shape[0]
                
                appear_mogura(frame,normal_mogura_img,normal_mogura_position)
                appear_mogura(frame,angry_mogura_img,angry_mogura_position)

                appear_time_normal_mogura = time.time()
                appear_time_angry_mogura = time.time()

            if key == 27:  # Escキー
                break
            continue

        # 入力画像をMediaPipeに渡して手の位置を検出
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        # 手の位置が検出された場合
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 手の位置を描画
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(0, 0,0), thickness=2, circle_radius=2)
                )

                # 人差し指の先端座標(INDEX_FINGER_TIP)を取得
                cx = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * WINDOW_WIDTH)
                cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * WINDOW_HEIGHT)

                # モグラの中央座標との距離を計算
                normal_mogura_dist = ((cx - (normal_mogura_position[0]+normal_mogura_size//2)) ** 2 + (cy - (normal_mogura_position[1]+normal_mogura_size//2)) ** 2) ** 0.5
                angry_mogura_dist = ((cx - (angry_mogura_position[0]+angry_mogura_size//2)) ** 2 + (cy - (angry_mogura_position[1]+angry_mogura_size//2)) ** 2) ** 0.5

                # ノーマルモグラは1点
                if normal_mogura_dist < 20:
                    cv2.putText(frame,f"+1",(normal_mogura_position[0],normal_mogura_position[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
                    points+=1
                    normal_mogura_img,normal_mogura_position=set_mogura_size_and_position(normal_mogura_img_ori)
                    normal_mogura_size = normal_mogura_img.shape[0]
                    appear_time_normal_mogura = time.time()
                    
                # アングリーモグラは2点加算され、サイズが50以下になると消滅
                if angry_mogura_dist < 20:
                    cv2.putText(frame,f"+2",(angry_mogura_position[0],angry_mogura_position[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                    points+=2
                    angry_mogura_size-=10
                    angry_mogura_img = cv2.resize(angry_mogura_img,(angry_mogura_size,angry_mogura_size))   
                    if angry_mogura_size <= 50:
                        angry_mogura_img,angry_mogura_position=set_mogura_size_and_position(angry_mogura_img_ori)
                        angry_mogura_size = angry_mogura_img.shape[0]
                        appear_time_angry_mogura = time.time()
                        
        # ノーマルモグラは2秒以上退治されなかったら逃げてしまう
        if time.time()-appear_time_normal_mogura >= appear_timelimit_normal_mogura:
            cv2.putText(frame,f"Miss",(normal_mogura_position[0],normal_mogura_position[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
            normal_mogura_img,normal_mogura_position=set_mogura_size_and_position(normal_mogura_img_ori)
            normal_mogura_size = normal_mogura_img.shape[0]
            appear_time_normal_mogura = time.time()
            

        # アングリーモグラは5秒以上退治されなかったら逃げてしまう
        if time.time()-appear_time_angry_mogura >= appear_timelimit_angry_mogura:
            cv2.putText(frame,f"Miss",(angry_mogura_position[0],angry_mogura_position[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)       
            angry_mogura_img,angry_mogura_position=set_mogura_size_and_position(angry_mogura_img_ori)
            angry_mogura_size = angry_mogura_img.shape[0]
            appear_time_angry_mogura = time.time()
            
        appear_mogura(frame,normal_mogura_img,normal_mogura_position)
        appear_mogura(frame,angry_mogura_img,angry_mogura_position)

        # ポイントと残り時間を表示
        elapsed_time = time.time() - start_time
        remaining_time = max(time_limit - int(elapsed_time), 0)
        cv2.putText(frame, f"Time: {remaining_time}", (490, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Points: {points}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 制限時間を超えた場合は結果表示画面を表示
        if elapsed_time >= time_limit:
            cv2.putText(frame, "Nice Game", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            cv2.putText(frame, f"Points: {points}", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Mediapipe Game', frame)

            # キー入力を待機して終了
            key = cv2.waitKey(2)
            if key == 27:  # Escキー
                break

            # ゲームをリセット
            points = 0
            start_time = time.time()
            game_started = False

        cv2.imshow('Mediapipe Game', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()