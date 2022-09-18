using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.Battle;
using Experience.Characters;
using Experience.GraphicParts;
using Experience.ScriptEvent;


namespace LoYUtil
{

/* モンスター等の追加
 * データテーブルをいじって敵データやエンカウントの追加を行っている
 * ついでにNPCの立ち絵(CEV)から敵グラッフィックデータを作成し、使えるようにしてある
 * InputEnemyLibraryRoot::StartEnemyLoadingを確認した際になぜかloadingEnemyGraphicIdが三桁に削られる問題を確認しているが、挙動に影響ない模様
 */
class EnemyInjector
{
    static List<CityEncounterData> CityEncounterDataList = null;
    static List<ConfirmedEncounterData> ConfirmedEncounterDataList = null;
    static List<EnemyData> EnemyDataList = null;
    static List<EnemyGraphicData> EnemyGraphicDataList = null;
    static List<GroupEncounterData> GroupEncounterDataList = null;
    static readonly int CEV_BASE = 221;
    static readonly int CEV_END = 233;
    //ゲーム内ではID:12まで定義
    static CityEncounterDataTable ExCityEncounterDataTable = null;
    //ゲーム内ではID:216まで定義
    static ConfirmedEncounterDataTable ExConfirmedEncounterDataTable = null;
    //ゲーム内ではID:505まで定義
    static EnemyDataTable ExEnemyDataTable = null;
    //ゲーム内ではID:220まで定義、CEVで233まで拡張
    static EnemyGraphicDataTable ExEnemyGraphicDataTable = null;
    //ゲーム内ではID:54まで定義
    static GroupEncounterDataTable ExGroupEncounterDataTable = null;
    public static readonly ScriptFlagId FlagId = (ScriptFlagId)1902;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "EnemyInjector", false,
                "モンスター等を追加できるようにする\n" +
                "詳細はReadme.txt参照のこと"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][EnemyInjector]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][EnemyInjector]enable");
            LoYUtilPlugin.ev_load += load;
            LoYUtilPlugin.ev_load_later += load_later;
            LoYUtilPlugin.ev_reload += reload;

            LoYUtilPlugin.mgr.add_flag(FlagId, true);

            var org = Util.get_method(typeof(CityEncounterDataTable), "get_Default");
            var hook = typeof(EnemyInjector).GetMethod("CityEncounterDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(ConfirmedEncounterDataTable), "get_Default");
            hook = typeof(EnemyInjector).GetMethod("ConfirmedEncounterDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(EnemyDataTable), "get_Default");
            hook = typeof(EnemyInjector).GetMethod("EnemyDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(EnemyGraphicDataTable), "get_Default");
            hook = typeof(EnemyInjector).GetMethod("EnemyGraphicDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(GroupEncounterDataTable), "get_Default");
            hook = typeof(EnemyInjector).GetMethod("GroupEncounterDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(EnemyGraphicUtility), "GetSpriteStudioFileNameAnimationPrefab");
            hook = Util.get_method(typeof(EnemyInjector), "ExSSFName");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(SpriteStudioController), "LoadStart");
            hook = Util.get_method(typeof(EnemyInjector), "BeforeSpriteAnimationLoadStart");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            //ExTextはResourceManagerのメソッド
            org = Util.get_method(typeof(EnemyData), "get_Name");
            hm.Patch(org, postfix: ResourceManager.extext);

            org = Util.get_method(typeof(EnemyData), "get_Description");
            hm.Patch(org, postfix: ResourceManager.extext);

            org = Util.get_method(typeof(EnemyData), "get_CallAllyOtherLineBeforeText");
            hm.Patch(org, postfix: ResourceManager.extext);
        }
    }

    /* 改造したテーブルを返す */
    public static bool CityEncounterDataTableDefault(ref CityEncounterDataTable __result)
    {
        if(ExCityEncounterDataTable == null)
            return true;
        __result = ExCityEncounterDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool ConfirmedEncounterDataTableDefault(ref ConfirmedEncounterDataTable __result)
    {
        if(ExConfirmedEncounterDataTable == null)
            return true;
        __result = ExConfirmedEncounterDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool EnemyDataTableDefault(ref EnemyDataTable __result)
    {
        if(ExEnemyDataTable == null)
            return true;
        __result = ExEnemyDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool EnemyGraphicDataTableDefault(ref EnemyGraphicDataTable __result)
    {
        if(ExEnemyGraphicDataTable == null)
            return true;
        __result = ExEnemyGraphicDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool GroupEncounterDataTableDefault(ref GroupEncounterDataTable __result)
    {
        if(ExGroupEncounterDataTable == null)
            return true;
        __result = ExGroupEncounterDataTable;
        return false;
    }

    /* CEVを基に作ったEnemyGraphicDataはアニメーションに一工夫必要 */
    public static bool ExSSFName(EnemyGraphicData enemyGraphicData, ref string __result)
    {
        if(CEV_BASE < enemyGraphicData.Id && enemyGraphicData.Id <= CEV_END)
        {
            //cev_100_1.01をcev_100に変換しなければならない
            string f = enemyGraphicData.FileName;
            if(f.Contains("."))
                f = f.Substring(0, f.Length - 5);
            __result = f;
            return false;
        }
        return true;
    }

    /* CEVを基に作ったEnemyGraphicDataはアニメーションに一工夫必要 */
    public static void BeforeSpriteAnimationLoadStart(ref string dataRootAddress, ref IEnumerable<string> animationFileNames)
    {
        if(dataRootAddress.Contains("cev_"))
        {
            string f = dataRootAddress.Split("/")[1];
            dataRootAddress = string.Format("{0}/{1}", GraphicPartsConsts.CevAddress, f);
        }
    }

    public static void reload()
    {
        if(CityEncounterDataList == null)
            return;
        Console.Write("[EnemyInjector] reloading...");
        load();
        load_later();
    }

    /* スクリプトから呼ばれるCityEncounterData, 固定エンカウントデータ,
     * 追加モンスターデータをロードする/しなおす
     */
    public static void load()
    {
        TableBuilder.build_list_by_json(ref CityEncounterDataList, "*.CityEncounterData.json");
        /* 敵の配置は二列/各列三種で最大8*2体まで
         * 大量に敵を配置しようとしても最大値はEnemyDataのScaleTypeに依存する
         */
        TableBuilder.build_list_by_json(ref ConfirmedEncounterDataList, "*.ConfirmedEncounterData.json");
        /* EnemyDataのscaleTypeは1ライン上に配置できる敵の最大数に関係している
         * 1ラインに最大8/scale valueまで配置でき、scale valueは下記の通り
         * 0: 8.0, 1: 4.0, 2: 2.5, 3: 2.0, 4: 1.5, 5: 1.0
         */
        TableBuilder.build_list_by_json(ref EnemyDataList, "*.EnemyData.json");
        TableBuilder.build_list_by_json(ref GroupEncounterDataList, "*.GroupEncounterData.json");
    }

    /* CEVのようにゲームの起動後でないとロードできない要素をロードする */
    public static void load_later()
    {
        //CEVのロード
        if(EnemyGraphicDataList == null)
            EnemyGraphicDataList = new List<EnemyGraphicData>();
        else
            EnemyGraphicDataList.Clear();
        foreach(var cev in CevDataTable.Default)
        {
            EnemyGraphicData ed = cev2enemygraphic(cev);
            Util.set_value(ed, "id", ed.Id + CEV_BASE - 1);
            EnemyGraphicDataList.Add(ed);
        }

        TableBuilder.build_table(ref ExCityEncounterDataTable, CityEncounterDataList);
        TableBuilder.build_table(ref ExConfirmedEncounterDataTable, ConfirmedEncounterDataList);
        TableBuilder.build_table(ref ExEnemyDataTable, EnemyDataList);
        TableBuilder.build_table(ref ExGroupEncounterDataTable, GroupEncounterDataList);
        TableBuilder.build_table(ref ExEnemyGraphicDataTable, EnemyGraphicDataList);
    }

    /* NPCのCevDataからEnemyGraphicDataを作成する */
    public static EnemyGraphicData cev2enemygraphic(CevData cd)
    {
        string json = JsonUtility.ToJson(cd).Replace("}", ", ");
        //荒堀のEnemyGraphicDataをベースに作成
        json += "\"bodyType\": 0, \"enemyEffectSizeId\": 1, \"positionOffsetX\": 0.0, \"positionRandomRangeX\": 0.0, \"positionOffsetY\": 0.0, \"positionRandomRangeY\": 0.0, \"distanceFromGroundOffset\": 0.0, \"effectPositionOffsetX\": 50.0, \"effectPositionOffsetY\": -380, \"cursorPositionOffsetX\": 40.0, \"cursorPositionOffsetY\": -500.0, \"libraryDescriptionInitialPositionOffsetX\": 0.0, \"libraryDescriptionInitialPositionOffsetY\": 170.0, \"libraryEnemyOnlyInitialPositionOffsetX\": 0.0, \"libraryEnemyOnlyInitialPositionOffsetY\": 170.0, \"emissionRate\": 1.75, \"emissionTweenId\": 2, \"emissionRateOnAction\": 2.5, \"effectEmissionRate\": 1.75, \"appearType\": 2, \"waterSurfaceWaveEffectScaleX\": 1.0, \"waterSurfaceWaveEffectScaleY\": 1.0, \"waterSurfaceWaveEffectPositionOffsetX\": 0.0, \"waterSurfaceWaveEffectPositionOffsetY\": 0.0, \"waterSurfaceLegMaskEffectScaleX\": 1.0, \"waterSurfaceLegMaskEffectScaleY\": 1.0, \"waterSurfaceLegMaskEffectPositionOffsetX\": 0.0, \"waterSurfaceLegMaskEffectPositionOffsetX\": 0.0, \"cameraHeightList\": [0.0, 0.0]}";
        //Console.Write(json);
        return JsonUtility.FromJson<EnemyGraphicData>(json);
    }
}

}