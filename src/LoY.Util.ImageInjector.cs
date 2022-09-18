using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.Effects;
using Experience.ScriptEvent;


namespace LoYUtil
{

/* 外部からのイメージの追加をできるようにする
 * ver0.0.1現在ダンジョン突入時の看板(IngressEffect)しか対応していない
 */
class ImageInjector
{
    public static readonly ScriptFlagId FlagId = (ScriptFlagId)1905;
    static List<EffectData> EffectDataList = null;
    static List<IngressEffectData> IngressEffectDataList = null;
    //ゲーム内ではID:131まで定義
    static EffectDataTable ExEffectDataTable = null;
    //ゲーム内ではID:18まで定義
    static IngressEffectDataTable ExIngressEffectDataTable = null;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "ImageInjector", false,
                "イメージを追加できるようにする"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][ImageInjector]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][ImageInjector]enable");
            LoYUtilPlugin.ev_load += load;
            LoYUtilPlugin.ev_load_later += load_later;
            LoYUtilPlugin.ev_reload += reload;

            LoYUtilPlugin.mgr.add_flag(FlagId, true);

            var org = Util.get_method(typeof(EffectDataTable), "get_Default");
            var hook = typeof(ImageInjector).GetMethod("EffectDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(IngressEffectDataTable), "get_Default");
            hook = typeof(ImageInjector).GetMethod("IngressEffectDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(IngressEffectPlayer), "Play");
            hook = typeof(ImageInjector).GetMethod("ExPlay");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    /* 改造したテーブルを返す */
    public static bool EffectDataTableDefault(ref EffectDataTable __result)
    {
        if(ExEffectDataTable == null)
            return true;
        __result = ExEffectDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool IngressEffectDataTableDefault(ref IngressEffectDataTable __result)
    {
        if(ExIngressEffectDataTable == null)
            return true;
        __result = ExIngressEffectDataTable;
        return false;
    }

    /* ダンジョン突入時に表示される看板を外部ファイルから読み込む
     * キャッシュを無視して直でファイルから読み込む脳筋実装
     */
    public static bool ExPlay(EffectPlayDescription desc, ref IEmissiveEffect __result, EffectUpdater ___updater, EffectCanvasPool ___canvasPool)
    {
        if(!IngressEffectPlayer.IsValidId(desc.Id))
            return true;
        string fname = IngressEffectDataTable.GetData(desc.Id).FileName;
        //MODフォルダ以外からのロードは無視する
        if(!fname.StartsWith("BepInEx"))
            return true;
        IngressEffect effect = new IngressEffect(___canvasPool, desc);
        ___updater.Add(effect);
        Texture tx = read_image(fname);
        effect.OnLoaded(tx);
        __result = effect;
        return false;
    }

    public static void load()
    {
        TableBuilder.build_list_by_json(ref EffectDataList, "*.EffectData.json");
        TableBuilder.build_list_by_json(ref IngressEffectDataList, "*.IngressEffectData.json");
    }

    public static void load_later()
    {
        TableBuilder.build_table(ref ExEffectDataTable, EffectDataList);
        TableBuilder.build_table(ref ExIngressEffectDataTable, IngressEffectDataList);
    }

    public static void reload()
    {
        if(ExEffectDataTable == null)
            return;
        Console.Write("[ImageInjector] reloading...");
        load();
        load_later();
    }

    public static Texture read_image(string fname)
    {
        byte[] buf = File.ReadAllBytes(fname);
        //サイズはLoadImageが勝手に直してくれるんで適当で良い
        Texture2D tx = new Texture2D(2, 2);
        tx.LoadImage(buf);
        return tx;
    }
}

}