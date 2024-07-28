# Python で砂時計のプログラム

## 実行方法

`python run.py`

### オプションで仮想環境の構築

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

仮想環境を終了する場合 `deactivate`

## プレビュー

[a]を押して回転できます（+90°）。

[q]または`control`+`c`で終了できます。

```shell
frame:   110 ball:   3 angle:   45° GRID_SIZE:  8
                                    Alerm!
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
[a]で回転, [q]または`control + c`で終了
```
