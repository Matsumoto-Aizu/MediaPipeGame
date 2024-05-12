## Whack a Mole Game
### 概要
Googleが開発した機械学習ライブラリMediaPipeを活用し、「モグラたたき」を制作した。MediaPipeはWebカメラからリアルタイムで手の関節を推定し、座標データを取得できる。そのため、プレイヤーの人差し指の先端座標を使用し、画面上のモグラを迅速かつ正確な反応が求められるゲームを作成した。

### ゲームの流れ
#### ゲームが始まると、画面上に2種類のモグラが現れます。
#### プレイヤーは人差し指の先端を操作し、モグラを叩きます。
#### モグラは一定時間で姿を消し、別の場所に現れます。
#### 60秒以内に多くのモグラを叩こう！

### 登場するモグラは全2種
#### １．ノーマルモグラ
ヒットすると5点加算する。
出現して1秒後に逃げてしまう。
#### ２．アングリーモグラ
ヒットすると2点加算し、サイズが小さくなる。
一定のサイズになると消滅する。
出現して4秒後に逃げてしまう。

### ~/src/whack_a_mole.py
#### ソースコード
### ~/asset/*.png
#### normal_mogura.png：ノーマルモグラ
#### angry_mogura.png：アングリーモグラ
### ~/asset/*.mp3
#### hit.mp3:モグラのヒットした音 (決定ボタンを押す12 可愛い音),
#### escape.mp3:逃げられた音 (キャンセル３　ビュッ)
https://soundeffect-lab.info/sound/button/

### 実行環境
#### OS: Windows 11
#### Python バージョン：3.11.4
#### ライブラリ： MediaPipe (0.10.3) OpenCV (4.8.0) pygame(2.5.2)
### インストール方法
#### > pip install mediapipe
#### > pip install opencv-python
#### > pip install pygame

### 参考資料
#### 1.MediaPipe | Google for Developers
https://developers.google.com/mediapipe

#### 2.【Python】MediaPipeで手を検出して円タッチゲームを作る方法
https://acordecode.com/%E3%80%90python%E3%80%91mediapipe%E3%81%A7%E6%89%8B%E3%82%92%E6%A4%9C%E5%87%BA%E3%81%97%E3%81%A6%E5%86%86%E3%82%BF%E3%83%83%E3%83%81%E3%82%B2%E3%83%BC%E3%83%A0%E3%82%92%E4%BD%9C%E3%82%8B%E6%96%B9/

#### 3.python/OpenCVで透過pngをオーバレイする
https://blanktar.jp/blog/2015/02/python-opencv-overlay

#### 4.ボタン・システム音[1] | 効果音ラボ
https://soundeffect-lab.info/sound/button/
