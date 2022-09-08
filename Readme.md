# 黄泉ヲ裂ク華 Utility Plug-In MOD

Steam版黄泉ヲ裂ク華に以下の機能を追加します。
- 起動時の企業ロゴ画面短縮
- タイトル画面にMODの読み込みに成功したかを表示するテキストボックスを出す（読み込み確認用）
- スキル「鷹の眼」でHPを数字で表示、ボスであってもLvを表示する
- ダンジョンでの操作で右スティックをカメラ切り替えから振り向きなしの移動に変更し、カメラモードへの切り替えはR2キーに変更
- 戦闘中にLRでキャラ選択
- キャンプでの花力抽出，アルゲン抽出，倉庫出し入れ，アイテム所持数オーバーでの廃棄画面で複数のアイテムを同時選択して一括入力できるようにする
- 難易度宣託
- 戦闘時のオートバトルに高速戦闘の選択肢を追加
- ゲーム中のスクリプトを書き換え/新規に追加できるようにする
- 敵キャラクターの追加/変更をできるようにする（v0.0.1現在グラフィックの追加は未対応）
- アイテムの追加/変更をできるようにする
- ダンジョンの追加/変更をできるようにする
- スクリプトで使用されるエフェクトの追加/変更をできるようにする
- スクリプトにコマンドを追加できるようにする
また、上記機能を利用して以下を追加してあります。
- テントで飯場管理官を襲う
- 飯場管理官との会話から難易度宣託
- 99行区採掘層入口に本来のものとは微妙に違う気のする敵を追加
- デモンゲイズの神々のエデン風のダンジョン「狂王のエデン」を追加、クリア報酬に黄金の砂時計
これらに関してはLoYUtilResource内の各フォルダにReadme.txtがあるので参照してください。

全体的にデバッグが不十分なため、バグを見つけたら教えてください。


## 注意事項

本MODは無保証です。<br>
本MODの使用により生じたあらゆる得失に対し作者は一切の責任を負いません。<br>

セーブデータに破損・非互換を生じる恐れがあります。<br>
必ず%HOMEPATH%\AppData\LocalLow\Aksys Games\Undernauts_ Labyrinth of Yomi内のセーブデータはバックアップを取った上で導入・使用してください。


## インストール

本MODはBepInEx(https://github.com/BepInEx/BepInEx)を使用しています。<br>
githubのReleaseから64bit版BepInEx最新版(※開発環境ではBepInEx_x64_5.4.19.0.zipを使用)をダウンロードし、黄泉ヲ裂ク華のルートフォルダ(例：C:\Program Files (x86)\Steam\steamapps\common\Undernauts Labyrinth of Yomi\)にそのまま展開します。<br>
Labyrinth of Yomi.exeとwinhttp.dllが同じフォルダに存在するように展開すればOKです。<br>
ここに本MODのBepInExフォルダをそのまま上書きします。<br>
例えばC:\Program Files (x86)\Steam\steamapps\common\Undernauts Labyrinth of Yomi\BepInEx\plugins\LoY.Util.Plugin.dllというような階層になっていればOK。

設定はBepInEx\config\LoY.Util.Plugin.cfgをテキストエディタで開いて行います。<br>
MODにより自動生成もされる一方、自分で関係ないことを書いても勝手に消えるので注意。<br>
なおデフォルトではTitleTextIndicator以外すべての機能がオンになっていますが、自動生成された場合はすべての機能はオフの状態で生成されます。


## 設定ファイル

以下にLoY.Util.Plugin.cfgで使用される設定を記します。<br>
型はC#のそれに準じており、[Enable]の各項目はtrueで機能オン、falseで機能オフとなります。

### Enable
#### BootScreenFix
起動時の企業ロゴ画面短縮とそれに伴い表示される画像を五枚から三枚へ削減（海賊版注意喚起とUnityロゴを削除）<br>
裏で各種初期化を行っているため、それほど大きな時間短縮はできない<br>
型：bool<br>
既定値：false
#### TitleTextIndicator
タイトル画面でMODがロードされたかを表示する<br>
MODのロードに成功しているかを確認するためだけの目的で存在している機能のため、必要なくばfalse推奨<br>
型：bool<br>
既定値：false
#### EagleEyeCheat
スキル「鷹の眼」で表示されるHPバーに敵の現在HP/最大HPをオーバーレイ表示する<br>
ボスのようにLvが表示されない相手であっても鷹の眼が有効ならLv表示を強制する<br>
型：bool<br>
既定値：false
#### AndStayBack
ダンジョンでの移動の際に右スティック過去作同様に振り向かずに移動できるようにする<br>
カメラモードに入りたい場合はR2ボタンを押すとカメラモードに入るようになる<br>
型：bool<br>
既定値：false
#### LRSelect
戦闘中LRでキャラクターを選択できるようにする<br>
先頭のキャラでLを押すと最後尾のキャラに、最後尾のキャラでRを押すと先頭のキャラに移動する<br>
LRで移動した後も行動未決定のキャラから行動選択ができ、全キャラ行動選択が完了すると通常戦闘/高速戦闘を選ぶウィンドウが出てターン開始となる<br>
なお、本来のRボタンの機能であるパーティのステータス表示の変更機能はSelectボタンに移設される<br>
型：bool<br>
既定値：false
#### MultiItemSelect
キャンプでの花力抽出，アルゲン抽出，倉庫でのアイテムの出し入れ，アイテム所持数オーバーでの廃棄画面で複数のアイテムを同時選択して一括処理できるようにする<br>
Yボタンでアイテムを選択、L2ボタンで一括処理<br>
スタック可能なアイテムはYボタンで選択した際に全量が選択される<br>
このため、例えば56個中26個だけ売りたい、といった要求には答えることができない<br>
また、Yボタンでの選択中にAボタンで通常通りに売ることはできるが、数量選択や確認画面でキャンセルをすると選択状態もすべて消えるので注意<br>
選択したアイテムはアイテム名先頭(アイコンとアイテム名の間)に「✓」（Unicode:U+2713）が入る<br>
型：bool<br>
既定値：false
#### ChooseDifficulty
敵Lvの調整による難易度宣託<br>
ぬるい(Easy), あったかい(Normal), あつい(Hard), まるこげ(VeryHard)の四段階から選択可能で、敵Lvの調整はそれぞれ0.9倍，1.0，1.1倍，1.2倍となる<br>
難易度は設定ファイルから指定できるほか、ScriptInjectorを利用して飯場管理官との会話からでも変更でき、そちらが優先される<br>
なお、黄金の砂時計使用後は敵Lvがさらに上昇する<br>
型：bool<br>
既定値：false
#### FastRepeat
戦闘時のオートバトルに高速戦闘の選択肢を追加する<br>
型：bool<br>
既定値：false
#### ScriptInjector
スクリプトの追加/置き換え，任意の行へのスクリプトの挿入，任意の行のスクリプトの置換をできるようにする<br>
スクリプト内で定義した拡張フラグはセーブデータに反映されるため、セーブデータに非互換の生じる恐れがある<br>
仕様は大変混沌としているので、「スクリプト仕様」の項を参照されたし<br>
型：bool<br>
既定値：false
#### ExpDebugPrint
ゲーム本来の機能として実装されているデバッグ出力と思しき文字列をログ/コンソールに出力する<br>
リリース用に削除されたのかほぼ残っておらず、また普通に遊ぶ分には全く不要な機能<br>
型：bool<br>
既定値：false
#### EnemyInjector
敵データの追加/変更をできるようにする<br>
データはxlsxファイルをコンバーターにかけて生成するか、json形式で記述する<br>
敵グラフィックの追加にはv0.0.1現在対応していないが、デフォルトの敵グラフィックとキャラクターの立ち絵は使用できる<br>
型：bool<br>
既定値：false
#### ItemInjector
アイテムデータの追加/変更をできるようにする<br>
データはxlsxファイルをコンバーターにかけて生成するか、json形式で記述する<br>
型：bool<br>
既定値：false
#### DungeonInjector
ダンジョンを追加/変更をできるようにする<br>
データはxlsxファイルをコンバーターにかけて生成するか、json形式で記述する<br>
ダンジョンデータはダンジョンの定義とセクターの定義とマップの定義の三種類のファイルに分かれている<br>
型：bool<br>
既定値：false
#### ImageInjector
エフェクトのグラフィックを追加/変更できるようにする<br>
データはxlsxファイルをコンバーターにかけて生成するか、json形式で記述する<br>
v0.0.1現在未完で、ダンジョン侵入時の看板の追加くらいしかできない<br>
型：bool<br>
既定値：false
#### ExternalCommand
スクリプトで使用できるコマンドを新規に追加する<br>
コマンドは_excmd:"追加コマンド名":"パラメータ":...という形式で記述する<br>
型：bool<br>
既定値：false
#### ResourceManager
本MODでの機能の仲介(フラグ変数の提供等)を行う<br>
特別な理由がなければ有効にしておくべきである<br>
型：bool<br>
既定値：false

### Const
#### TitleTextIndicatorDesc
タイトル画面でMODがロードされたときに表示する文章<br>
TitleTextIndicatorが有効でなければ表示されない<br>
型：string<br>
既定値：LoYUtilPluginのロードに成功
#### Difficulty
難易度宣託の難易度<br>
ScriptInjectorでの難易度選択を導入していれば飯場管理官の会話でも難易度は変更可能だが、その際は飯場管理官の会話で選択した難易度が優先される<br>
型：string<br>
既定値：まるこげ
#### ShowScriptSource
スクリプトが実行される際にスクリプト名とソースをログ/コンソール出力する<br>
スクリプト開発の際のデバッグ目的以外には不要<br>
型：bool<br>
既定値：false


## ツール

LoYUtilResource\tool\にあり、スクリプトのコンパイル/逆コンパイルやxlsxファイルで記述された各種データのコンバータが含まれます。<br>
これらのツールはPython3で書かれており、[PLY](https://github.com/dabeaz/ply)と[OpenPyXL](https://openpyxl.readthedocs.io)を使用しています。<br>
使用する際はpip install ply openpyxlしてから使ってください。<br>
手抜きなのでオプションの順番等に制限があります。<br>
ゲームで使用されるデータはUndernauts Labyrinth of Yomi\Labyrinth of Yomi_Data\StreamingAssets\aa\Windows\StandaloneWindows64内の各アセットバンドル内にあります。<br>
[AssetStudio](https://github.com/Perfare/AssetStudio)等のツールで展開して各ツールにかけることでデータ作成の際の参考にできます。

### CommandReverseCompiler.py
逆コンパイラです。<br>
scriptdata_assets_all.bundleから抽出したScriptDataContainer.bytesを逆コンパイルしたり、CommandCompiler.pyでコンパイルしたスクリプトを逆コンパイルできます。<br>
```CommandReverseCompiler.py <in> <out> [-f/--force] [--key=SCRIPT_NAME] [--no-print]```
#### \<in\>
入力ファイルとしてコンパイルされたスクリプトを取る
#### \<out\>
出力ファイル
"stdout"を指定するとファイルには出力せずに標準出力のみに出力するが、-fオプションと--no-printオプションは無視される
#### -f/--force
非必須オプション<br>
出力ファイルが存在していても上書き保存する
#### --key=SCRIPT_NAME
非必須オプション<br>
ScriptDataContainer.bytesを逆コンパイルする際に「S_タイトル」等の指定したスクリプト名=SCRIPT_NAMEのみを逆コンパイルする
#### --no-print
非必須オプション<br>
逆コンパイルされたスクリプトを標準出力に出力しない<br>

例：ScriptDataContainer.bytesを全文行番号付きで逆コンパイルにかける<br>
```CommandReverseCompiler.py ScriptDataContainer.bytes o.txt --no-print```

### CommandCompiler.py
コンパイラです。<br>
CommandReverseCompiler.pyで逆コンパイルしたスクリプトをコンパイルしたり、自分で書いたスクリプトをコンパイルできます。<br>
```CommandCompiler.py <in> <out> [--ex-flagpth=flagpath]```
#### \<in\>
入力ファイルとして逆コンパイルされたスクリプトを取る
#### \<out\>
出力ファイル<br>
"stdout"を指定するとファイルには出力せずに標準出力のみに出力するが、-fオプションは無視される
#### --ex-flagpth=flagpath
非必須オプション<br>
ユーザーの定義した拡張フラグを読み書きするための設定ファイルを指定する<br>
特別な理由のない限りはBepInEx\LoYUtilResource\exflags.eflを指定すべきである<br>
指定しない場合既存のフラグIDとの衝突が発生し、スクリプトが予期しない動作をする可能性がある<br>

例：..\HanBattle\HanBattle.Script.txtを拡張フラグを出力するよう指定してコンパイルする<br>
```CommandCompiler.py ..\HanBattle\HanBattle.Script.txt ..\HanBattle\compiled\ --ex-flagpath=..\exflags.efl```

### compare.py
コンパイラと逆コンパイラ用のテストスクリプトです。<br>
通常使用することはありません。

### commandlist.py
各種定義の書かれたスクリプトです。<br>
通常使用することはありませんが、コマンド定義やフラグID等があるためスクリプトの作成等の際に参考にできます。

### DataTableBuilder.py
ExcelのxlsxファイルからEnemyInjector等で読み込むjsonファイルへ変換するツールです。<br>
また、database_assets_all.bundle内の**DataTableファイルをxlsxファイルへ変換することもできます。<br>
なおxlsxファイルへ変換する際、各データにつきワークシートを作成するためItemDataTableなどの要素数が多いデータテーブルを変換したxlsxファイルは相応に重くなります。<br>
xlsxファイルの例はLoYUtilResource\Eden of the mad overlordを参照してください。<br>
```DataTableBuilder.py <in> <out> [JapaneseTextData.json] [tid file] [mod dir] [-f/--force]```
#### \<in\>
xlsxファイル->jsonファイル : xlsxファイル<br>
jsonファイル->xlsxファイル : database_assets_all.bundleから抽出した**DataTableファイル
#### \<out\>
xlsxファイル->jsonファイル : 複数のjsonファイルが生成されるため、フォルダを指定する<br>
jsonファイル->xlsxファイル : xslsxファイル
#### JapaneseTextData.json
非必須オプション<br>
jsonファイル->xlsxファイル時限定で、textdata_assets_all.bundleから抽出したJapaneseTextData.jsonファイルを指定する<br>
これにより"name": {"id": "EXAMPLE_NAME_0001"}形式のデータ構造を持つテーブルならワークシートにこの名称が使用される
#### tid file
非必須オプション<br>
jsonファイル->xlsxファイル時限定で、MODのtidファイルを指定する<br>
これにより"name": {"id": "EXAMPLE_NAME_0001"}形式のデータ構造を持つテーブルならワークシートにこの名称が使用される
#### mod dir
非必須オプション<br>
jsonファイル->xlsxファイル時限定で、MODフォルダを指定する<br>
自動で指定フォルダ以下からtidファイルを検索して使用する<br>
これにより"name": {"id": "EXAMPLE_NAME_0001"}形式のデータ構造を持つテーブルならワークシートにこの名称が使用される
#### force
非必須オプション<br>
jsonファイル->xlsxファイル時限定で、出力ファイルがすでに存在しても強制的に上書きする<br>

例：SectorDataTable.jsonをワークシート名補間のためにtextdata_assets_all.bundleのJapaneseTextData.jsonとMODフォルダ(..\)を参照しつつxlsxファイルに変換する<br>
```DataTableBuilder.py SectorDataTable.json o.xlsx JapaneseTextData.json ..\```<br>
例：..\Eden of the mad overlord\EdenMiscData.xlsxをjsonファイルに変換して..\Eden of the mad overlord\compiledフォルダに展開する<br>
```DataTableBuilder.py "..\Eden of the mad overlord\EdenMiscData.xlsx" "..\Eden of the mad overlord\compiled"```

### DngmapConv.py
ExcelのxlsxファイルからDungeonInjectorで使用するjsonファイルを生成します。<br>
また、dungeonmaps_assets_all.bundleから抽出したdngmapファイルをxlsxファイルへ変換することもできますが、マップに若干のバグは見られるため参考程度にしてください。<br>
```DngmapConv.py <in> <out> -t=decode/encode [-f/--force]```
#### \<in\>
xlsxファイル->jsonファイル : xlsxファイル<br>
jsonファイル->xlsxファイル : dungeonmaps_assets_all.bundleから抽出した*.dngmap.jsonファイル
#### \<out\>
xlsxファイル->jsonファイル : jsonファイル(DungeonInjectorは*.dngmap.json形式のファイル名のファイルを読む)<br>
jsonファイル->xlsxファイル : xlsxファイル
#### -t=decode/encode
jsonファイルをxlsxファイルに変換する際にはencodeを、xlsxファイルをjsonファイルに変換する際にはdecodeを指定する
#### -f/--force
非必須オプション<br>
jsonファイル->xlsxファイル時限定で、出力ファイルがすでに存在しても強制的に上書きする<br>

例：..\Eden of the mad overlord\Eden.xlsxを..\Eden of the mad overlord\compiled\Eden.dngmap.jsonに変換する<br>
```DngmapConv.py "..\Eden of the mad overlord\Eden.xlsx" "..\Eden of the mad overlord\compiled\Eden.dngmap.json" -t=decode```

### CompileAll.py
MODフォルダ内のスクリプトやxlsxファイルをCommandCompiler.py、DataTableBuilder.py、DngmapConv.pyを使用して一括変換します。<br>
生成したファイルはcompiledフォルダを作成してその中に保存されますが、compiledフォルダはCompileAll.pyを実行する毎に削除されるため、compiledフォルダ内には自動生成されたファイル以外は決して置かないでください。<br>
なお、いちいちコマンドラインを開くのも面倒なのでCompileAll.pyを実行するCompileAll.batも用意してあります。<br>
デフォルトではCompileAll.pyを実行したフォルダ以下の**.Script.txt、**.xslxファイルを検索して変換にかけますが、対象フォルダを限定することもできます。<br>
```CompileAll.py [target dir]```
#### target dir
非必須オプション<br>
変換対象となるフォルダを限定する<br>
このオプションを使用しない場合、作業フォルダ以下全てのフォルダが変換の対象となる<br>

例：HanBattleフォルダ以下のファイルのみを変換対象とする<br>
```CompileAll.py HanBattle```

## スクリプト仕様

コンパイラに入力するスクリプトの仕様について記述します。<br>
<工事中>

## データファイル仕様

<工事中>

## マップファイル仕様

<工事中>

## TODO

- 難易度宣託の敵Lv倍率調整(二周目終盤は無理ゲー感ある)
- デバッグログ出力っぽい関数を見つけたら片っ端からExpDebugPrintに追加していく
- S_住居テントのように一行に複数のコマンドが入ったスクリプトにスマートにコマンドを注入する方法を考える
- 敵画像などを外部から挿入する方法を調査する（アニメーション周りがかなりめんどくさそう）
- DungeonInjectorでマップの出口を設定できない(そのため、花石で代用している)


## change log

0.0.1
- 公開


## 開発環境

- Windows10 Pro 64bit
- BepInEx x64_5.4.19
- mono-6.12.0.107-x64付属のコンパイラ
- Python 3.9.6 AMD64 on win32
- LibreOffice_7.3.3_Win_x64
