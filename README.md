## venv(virtual environment)
- グローバルな環境でpip installをすると、グローバル用の場所にパッケージがインストールされてしまう。
- プロジェクトごとに異なるバージョンの同一パッケージを利用したい場合などにvenvの真価が発揮される
- python3 -m venv myenv とすると、以下のようなディレクトリが作られる
```
myenv/
├── bin/                  # Windowsでは Scripts/
│   ├── python            # システムのpythonへのsymlink（またはコピー）
│   ├── python3           # 同上
│   ├── pip
│   └── activate          # シェルスクリプト
├── lib/
│   └── python3.x/
│       └── site-packages/  # ← ここに隔離してインストールされる
└── pyvenv.cfg            # 設定ファイル（これが最重要）
```
- myenv/bin/activateスクリプトを実行すると、一時的に環境変数PATHを書き換える
- PATHの先頭に`/path/to/myenv/bin`を追加することで、優先的にmyenv以下のpythonのsymlinkが使われるようになる

### パッケージの隔離ができるのはなぜか？
Pythonインタプリタは起動時に「自分がどこにインストールされているか（sys.prefix）」を、実行された python バイナリの位置から逆算します。具体的には、バイナリと同じ階層やその親に pyvenv.cfg があるかをチェックします。

- myenv/bin/python を実行すると、すぐ上の myenv/ に pyvenv.cfg を発見する
- すると sys.prefix を myenv に設定し、site-packages の探索先を myenv/lib/python3.x/site-packages/ に切り替える
- 結果として pip install も import もこのディレクトリを見るようになる