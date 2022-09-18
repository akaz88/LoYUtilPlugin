using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Collections;
using System.Collections.Generic;
using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.SaveLoad;

namespace LoYUtil
{

[BepInPlugin("LoY.Util.Plugin", "LoY Utility Plug-In", "0.0.0.1")]
public class LoYUtilPlugin : BaseUnityPlugin
{
    static string id = "LoY.Util.Plugin";
    static ConfigFile cfg;
    public static string rsrc_path;
    public static Manager mgr = null;
    public static event Action ev_load;
    public static event Action ev_load_later;
    public static event Action ev_reload;
    //キー入力等が必要な場合はここに追加する(例:SoftReset)
    public static event Func<IEnumerator> ev_update;
        //deligate cheat sheat
        //https://atmarkit.itmedia.co.jp/fdotnet/dotnettips/730dlgttype/dlgttype.html

    public void Awake()
    {
        Harmony hm = new Harmony(id);
        cfg = Config;
        rsrc_path = Path.Combine(Paths.BepInExRootPath, "LoYUtilResource");
        Console.Write("[LoYUtilPlugin]patching...");

        mgr = ResourceManager.enable(hm, cfg);
        BootScreenFix.enable(hm, cfg);
        TitleTextIndicator.enable(hm, cfg);
        EagleEyeCheat.enable(hm, cfg);
        //YAMinimapBorder.enable(hm, cfg);
            //どうにかする予定は特にない
        AndStayBack.enable(hm, cfg);
        LRSelect.enable(hm, cfg);
        MultiItemSelect.enable(hm, cfg);
        ChooseDifficulty.enable(hm, cfg);
        ScriptInjector.enable(hm, cfg);
        ExpDebugPrint.enable(hm, cfg);
        EnemyInjector.enable(hm, cfg);
        FastRepeat.enable(hm, cfg);
        ItemInjector.enable(hm, cfg);
        DungeonInjector.enable(hm, cfg);
        ImageInjector.enable(hm, cfg);
        ExternalCommand.enable(hm, cfg);
        SoftReset.enable(hm, cfg);
        Bugfix.enable(hm, cfg);

        //データのロードはゲームの初期化と同じタイミングで行うようにする
        var org = Util.get_method(typeof(GameInitializer), "SetReady");
        var hook = typeof(LoYUtilPlugin).GetMethod("load");
        hm.Patch(org, prefix: new HarmonyMethod(hook));
    }

    public void Update()
    {
        //F5キーでスクリプト等のリロード
        if(Input.GetKeyDown(KeyCode.F5))
            ev_reload();
        StartCoroutine(ev_update());
    }

    /* データのロードを行う場合はこちらに登録されたイベントから行う
     * GameInitializer.Phase.SystemInitialization
     *     ディスク上からデータを読み込む関数を登録しておいて、これを実行する
     *     また、本MOD外からのフラグ等の追加もここに登録しておくことが推奨される
     *     例:ItemInjector.load
     * GameInitializer.Phase.AssetLoading
     *     読み込んでおいたデータとゲーム内のデータを元にデータテーブルを作成する
     *     例:ItemInjector.load_later
     */
    public static void load(GameInitializer.Phase phase)
    {
        if(phase == GameInitializer.Phase.SystemInitialization)
            ev_load();
        else if(phase == GameInitializer.Phase.AssetLoading)
            ev_load_later();
    }
}

}