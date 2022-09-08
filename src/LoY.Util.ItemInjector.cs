using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.Items;
using Experience.Rewards;
using Experience.ScriptEvent;
using Experience.Statistics;
using Experience.UIs;


namespace LoYUtil
{

/* アイテムを追加する
 * ついでにランダムドロップテーブルにも追加できるようにする
 */
class ItemInjector
{
    static List<RandomDropData> RandomDropDataList = null;
    static List<ItemData> ItemDataList = null;
    //ゲーム内ではID:505まで定義
    static RandomDropDataTable ExRandomDropDataTable = null;
    //ゲーム内ではID:1005まで定義
    static ItemDataTable ExItemDataTable = null;
    public static readonly ScriptFlagId FlagId = (ScriptFlagId)1903;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "ItemInjector", false,
                "アイテムを追加できるようにする"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][ItemInjector]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][ItemInjector]enable");
            LoYUtilPlugin.ev_load += load;
            LoYUtilPlugin.ev_load_later += load_later;
            LoYUtilPlugin.ev_reload += reload;

            LoYUtilPlugin.mgr.add_flag(FlagId, true);

            var org = Util.get_method(typeof(ItemDataTable), "get_Default");
            var hook = Util.get_method(typeof(ItemInjector), "ItemDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(RandomDropDataTable), "get_Default");
            hook = Util.get_method(typeof(ItemInjector), "RandomDropDataTableDefault");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(ItemData), "get_Name");
            hm.Patch(org, postfix: ResourceManager.extext);

            org = Util.get_method(typeof(ItemData), "get_Description");
            hm.Patch(org, postfix: ResourceManager.extext);

            org = Util.get_method(typeof(ItemData), "GetDescription");
            hm.Patch(org, postfix: ResourceManager.extext);
        }
    }

    /* 改造したテーブルを返す */
    public static bool ItemDataTableDefault(ref ItemDataTable __result)
    {
        if(ExItemDataTable == null)
            return true;
        //Console.Write("ExItemDataTable");
        __result = ExItemDataTable;
        return false;
    }

    /* 改造したテーブルを返す */
    public static bool RandomDropDataTableDefault(ref RandomDropDataTable __result)
    {
        if(ExRandomDropDataTable == null)
            return true;
        //Console.Write("ExRandomDropDataTable");
        __result = ExRandomDropDataTable;
        return false;
    }

    public static void reload()
    {
        if(RandomDropDataList == null)
            return;
        Console.Write("[ItemInjector] reloading...");
        load();
        load_later();
    }

    public static void load()
    {
        //Console.Write("RandomDropData");
        TableBuilder.build_list_by_json(ref RandomDropDataList, "*.RandomDropData.json");
        //Console.Write("ItemData");
        TableBuilder.build_list_by_json(ref ItemDataList, "*.ItemData.json");
    }

    public static void load_later()
    {
        TableBuilder.build_table(ref ExRandomDropDataTable, RandomDropDataList);
        TableBuilder.build_table(ref ExItemDataTable, ItemDataList);
        overwrite_journal_sortedorder();
    }

    /* 追加したアイテムはSortedOrderに反映させてやらないと図鑑に出てこない */
    public static void overwrite_journal_sortedorder()
    {
        var j = ItemDataTable.Default.FilterByJournaling().OrderBySortNo().ToArray<ItemData>();
        Util.set_static_value(typeof(ItemJournal), "SortedOrder", j);
    }
}

}