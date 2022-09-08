using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;

using Experience;
using Experience.Characters;
using Experience.Dungeons;
using Experience.Inventories;
using Experience.Items;
using Experience.Notifications;
using Experience.ScriptEvent;


namespace LoYUtil
{

/* ExternalCommandが有効な際、追加コマンドGoldenHourGlassを追加する
 * 読んで字のごとく黄金の砂時計を使用した際にゲームの進行状況等をリセットするコマンド
 */
class GoldenHourglass
{
    public static readonly string command_name = "GoldenHourglass";
    public static readonly ScriptFlagId GoldenHourglassUsed = (ScriptFlagId)1502;
    static readonly int GATE_FLOWER_ID = 721;
    static ScriptFlagId[] ignore_flag = new ScriptFlagId[]{
        ScriptFlagId.TUTORIAL_BATTLE_SWITCHBOOST, ScriptFlagId.DUNGEON_MAKING_DEBUT, ScriptFlagId.TUTORIAL_BATTLE_TREASURETRAP, ScriptFlagId.TUT_LHUNT, ScriptFlagId.TUT_KEYWORD, ScriptFlagId.TUT_WARPSTONE, ScriptFlagId.TUT_ETALK2, ScriptFlagId.TUT_DIFFICULTY, ScriptFlagId.TUT_CAREERUP, ScriptFlagId.TUT_MAINQUEST, ScriptFlagId.TUT_DMAKING, ScriptFlagId.TUT_ETALK, ScriptFlagId.TUT_FLENEMY
    };
    static ScriptFlagId[] flag_force_on = new ScriptFlagId[]{
        ScriptFlagId.ALWAYS
    };
    static DungeonId[] ignore_dungeon = new DungeonId[]{
        DungeonId.Tresure, DungeonId.Tresure2, DungeonId.Tresure3
    };

    public static void register_excommand()
    {
        Console.Write("[LoYUtilPlugin][GoldenHourglass]register external command : GoldenHourglass.");
        LoYUtilPlugin.mgr.add_excommand(command_name, GoldenHourglassCommand);
    }

    /* 追加コマンド: GoldenHourglass
     * ゲームを初期化する
     * 以下は初期化されるもの
     * ・フラグ
     *     ・難易度宣託、黄金の砂時計使用フラグ、各種チュートリアル履歴等は残す
     *     ・MODで設定されたフラグのうち、フラグIDが2000以上のものは消す
     *     ・チュートリアルのうち一部はシナリオ進行上見る必要があるが、こちらはスクリプトで対応
     * ・イベントアイテム
     *     ・オオトビラの花は残す
     * ・ダンジョンの鍵開け等の状況
     * ・宝の夢以外に設置した黄泉の花
     *     ・黄泉の花は換金する
     *     ・宝の夢は再設置があまりにめんどうなので残す
     * ・グローバル変数
     * ・サブクエストを含む進行状況
     * ・融合炉での強化最大値
     */
    public static ResultCode GoldenHourglassCommand(object self, ScriptCommand command)
    {
        Console.Write("GoldenHourglass used.");
        FlagContainer flags = Database.Session.Flags;
        clear_flags();
        sell_flowers();
        delete_keyitems();
        flags.EventMapSymbol.Clear();
        flags.DungeonEntranceAvailableFlag.Clear();
        flags.ControlledDoor.Clear();
        flags.SecretDoor.Clear();
        flags.EnemySymbol.Clear();
        flags.ErasedEnemy.Clear();
        flags.Treasure.Clear();
        flags.TreasureTemporary.Clear();
        flags.BreakableObject.Clear();
        flags.RandomObject.Clear();
        flags.QuestRecord.Clear();
        flags.ProgressNo = ScriptConsts.ProgressNumberInitial;
        flags.PlayerAttributeGrowthCap = Player.AttributeGrowthCapInitial;
        flags.ItemEnhanceCap = 3;
        flags.ItemLevelCapModify = 0;
        flags.PlanModifyModify = 0;
        flags.Difficulty = 0;
        SessionFlagAccessorScripts.ClearEventEndFlag();
        SessionFlagAccessorScripts.ClearGlobalWork();
        //ここでオンにしておかないとダンジョンに出られなくなって詰む
        SessionFlagAccessorDungeon.SetAvailableEntrance(DungeonEntranceId.Tunnel, true);
        //これをしないとセーブデータに反映されない
        NotificationCenter.Post<NewGame>();
        return ResultCode.Next;
    }

    /* フラグをクリアする
     * 一部のフラグは無視され、また強制的にオンとなる
     */
    static void clear_flags()
    {
        FlagContainer flagContainer = Database.Session.Flags;
        Dictionary<ScriptFlagId, bool> d = new Dictionary<ScriptFlagId, bool>();
        foreach(var id in flagContainer.ScriptFlag.GetKeys(false))
            if((1060 <= (int)id && (int)id <= 1999) || ignore_flag.Contains(id))
                d[id] = flagContainer.ScriptFlag.IsOn(id);
        flagContainer.ScriptFlag.Clear();
        foreach(var p in d)
            flagContainer.ScriptFlag.Set(p.Key, p.Value);
        foreach(var id in flag_force_on)
            flagContainer.ScriptFlag.Set(id, true);
    }

    /* マップ上に設置したオブジェクトを全て売っぱらう
     * 宝の夢は再設置がめんどくさすぎてハゲるので無視
     * オオトビラは回収する
     */
    static void sell_flowers()
    {
        int pid = Database.Session.Parties.CurrentPartyId;
        Item gate_flower = Item.Generate(GATE_FLOWER_ID);
        Dictionary<InstantObjectType, int> count = new Dictionary<InstantObjectType, int>();
        List<InstantObject> l = new List<InstantObject>();
        foreach(var obj in InstantObjectManager.InstantObjects)
        {
            if(ignore_dungeon.Contains(obj.Sector.Dungeon.Id))
                continue;
            //InstantObjectManager.Remove(obj);
            l.Add(obj);
            //オオトビラの花はインベントリに戻す
            if(obj.Type == InstantObjectType.Gate)
            {
                //所持限界に達してなかったらインベントリに追加
                if(SessionInventoriesAccessorItemsParty.CalcCanAddStackCount(pid, GATE_FLOWER_ID) > 0)
                    SessionInventoriesAccessorItemsParty.AddItem(pid, gate_flower);
                continue;
            }
            //処分した花の種類と数を記録
            if(count.ContainsKey(obj.Type))
                count[obj.Type] += 1;
            else
                count[obj.Type] = 1;
        }
        foreach(var obj in l)
            InstantObjectManager.Remove(obj);
        InstantObjectManager.ClearUsedFlags();
        InstantObjectManager.SetDirty();
        //換金
        int payback = 0;
        foreach(var p in count)
            payback += DungeonInstantResourceDataTable.GetData((int)p.Key).CreateCostResourcePoint * p.Value;
        Database.Session.DungeonMakingResources.AddResourcePoint(payback);
    }

    /* オオトビラの花を除くキーアイテム全てを処分する */
    static void delete_keyitems()
    {
        List<Item> l = new List<Item>();
        foreach(var item in SessionInventoriesAccessorItemsParty.GetItemAllCurrentParty(InventoryTypePartyItem.KeyItems))
            if(item.Id != GATE_FLOWER_ID)
                l.Add(item);
        foreach(var item in l)
            SessionInventoriesAccessorItemsParty.RemoveItemCurrentParty(item);
    }
}

}