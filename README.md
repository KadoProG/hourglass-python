# Python で砂時計のプログラム

## 実行方法

### 事前準備

```shell
cp .env.example .env # 環境変数のコピー
pip install -r requirements.txt
python run.py # 通常モード
python run.py --fix # 固定モード
```

### node が入っている場合

```shell
yarn # install package
yarn dev # 通常モード
yarn dev --fix # 固定モード
```

### オプションで仮想環境の構築

```shell
python -m venv venv
source venv/bin/activate
```

仮想環境を終了する場合 `deactivate`

### env の項目

```shell
BOOT=
API_URL=
```

- **BOOT**：モードを選択
  - `macos`：mac 上で音を鳴らすことができる
  - `raspberrypi`：raspberrypi のブザーから音を鳴らすことができる
  - none(空白)：音を鳴らさない
- **API_URL**：アラーム時の API_URL を指定

## プレビュー

[a]を押して回転できます（+90°）。

[q]または`control`+`c`で終了できます。

```shell
frame:    50 angle:   45° GRID_SIZE:  8
    [pause]                         Alerm!
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 0
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 1
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 2
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 3
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 4
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 5
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 6
  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯                 7
                  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ 8
                  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ 9
                  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ 10
                  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ 11
                  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ 12
                  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ 13
                  ◯ ◯ ◯ ◯ ◯ ◯ ◯ ● 14
                  ◯ ◯ ◯ ◯ ◯ ◯ ● ● 15
  0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 ☆
 [a]start/stop  [r]rotate  [t]log  [q]exit
```
