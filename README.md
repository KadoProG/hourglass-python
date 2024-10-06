# Python で砂時計のプログラム

## 実行方法

### 事前準備

```shell
cp .env.example .env # 環境変数のコピー
pip install -r requirements.txt
python run.py
```

### node が入っている場合

```shell
yarn # install package
yarn dev
```

### オプションで仮想環境の構築

```shell
python -m venv venv
source venv/bin/activate
```

仮想環境を終了する場合 `deactivate`

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
