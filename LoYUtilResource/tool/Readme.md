# Modding tools

スクリプトのコンパイル/逆コンパイルやxlsxファイルで記述された各種データのコンバータが含まれます。<br>
これらのツールはPython3で書かれており、[PLY](https://github.com/dabeaz/ply)と[OpenPyXL](https://openpyxl.readthedocs.io)を使用しています。<br>
使用する際はpip install ply openpyxlしてから使ってください。<br>
手抜きなのでオプションの順番等に制限がある他、既知のバグが有ります。<br>
なお、ゲーム本体で使用されているデータはUndernauts Labyrinth of Yomi\Labyrinth of Yomi_Data\StreamingAssets\aa\Windows\StandaloneWindows64内の各アセットバンドル内にあります。<br>
[AssetStudio](https://github.com/Perfare/AssetStudio)等のツールで展開して各ツールにかけることでデータ作成の際の参考にできます。

## CommandReverseCompiler.py
逆コンパイラです。<br>
scriptdata_assets_all.bundleから抽出したScriptDataContainer.bytesを逆コンパイルしたり、CommandCompiler.pyでコンパイルしたスクリプトを逆コンパイルできます。<br>
```CommandReverseCompiler.py <in> <out> [-f/--force] [--key=SCRIPT_NAME] [--no-print]```
<pre>
    <in>
        入力ファイルとしてコンパイルされたスクリプトを取る
    <out>
        出力ファイル
        "stdout"を指定するとファイルには出力せずに標準出力のみに出力するが、-fオプションと--no-printオプションは無視される
    -f/--force
        非必須オプション
        出力ファイルが存在していても上書き保存する
    --key=SCRIPT_NAME
        非必須オプション
        ScriptDataContainer.bytesを逆コンパイルする際に「S_タイトル」等の指定したスクリプト名=SCRIPT_NAMEのみを逆コンパイルする
    --no-print
        非必須オプション
        逆コンパイルされたスクリプトを標準出力に出力しない<br>
</pre>

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




