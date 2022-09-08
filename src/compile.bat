rem  BepInEx\src\となるフォルダ構成にして実行して下さい

@echo off
@setlocal enabledelayedexpansion

@set libs=-lib:..\core\,"..\..\Labyrinth of Yomi_Data\Managed\\"
@set dlls=-r:BepInEx.dll -r:0Harmony.dll -r:Assembly-CSharp.dll -r:Assembly-CSharp-firstpass.dll -r:UnityEngine.dll -r:UnityEngine.UI.dll -r:UnityEngine.CoreModule.dll -r:UnityEngine.ImageConversionModule.dll -r:UnityEngine.JSONSerializeModule.dll -r:UnityEngine.InputLegacyModule.dll -r:Unity.Addressables.dll
@set out="LoY.Util.Plugin.dll"
@set csc="C:\Program Files\Mono\bin\mono.exe" %MONO_OPTIONS% "C:\Program Files\Mono\lib\mono\4.5\mcs.exe"
@set miscopt=-nologo -errorendlocation -langversion:7
@set compile=%csc% %flags% %miscopt% %libs% %dlls%

@echo compiling plugin...
%compile% -t:library -out:%out% LoY.Util.*.cs
if not %ERRORLEVEL% == 0 exit /b
move /Y %out% ..\plugins\ >nul
@echo done
