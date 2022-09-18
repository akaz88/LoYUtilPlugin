using System;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.Battle;
using Experience.Characters;
using Experience.ScriptEvent;


namespace LoYUtil
{

/* 難易度宣託
 * 「ChooseDifficulty」はデモンゲイズGEでの英語表記に依る
 *
 * 本来の難易度設定はExperience.Game.Difficultyで設定されているが、
 * 本作にはNormalしか定義がない
 * 元々はExperience.Battle.EncounterGenerator::GetLevelScaling()にて
 * 敵やアイテムのレベルを調整するものだったようだ
 * Experience.Dungeons.DungeonTreasure::GenerateRandomItems()では
 * GetModifiedPlanModify()しているが､falseで呼び出しているので事実上無関係？
 * デフォルト値はdatabase_assets_all.bundle/DifficultyDataTable参照
 *
 * 難易度Normal時のパラメータ(全イベントクリア後平均レベル57時)
 *      planDivider : 5
 *      planModify  : 3
 *      modifiedPlanModify = SessionFlagAccessorMisc.GetModifiedPlanModify(true)
 *                  : 0x17
 *      GetLevelScaling() : 43
 */
class ChooseDifficulty
{
    private static int difficulty;
    //ぬるい(Easy), あったかい(Normal), あつい(Hard), まるこげ(VeryHard)
    public static readonly ScriptFlagId FlagId = (ScriptFlagId)1900;
    //2bitで四通りの難易度、スクリプト内では必ずこのIDに合わせること
    public static readonly ScriptFlagId DifficultyHigh = (ScriptFlagId)1500;
    public static readonly ScriptFlagId DifficultyLow = (ScriptFlagId)1501;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<string> d = cfg.Bind(
                "Const", "Difficulty",
                "あったかい",
                "難易度：ぬるい, あったかい(Normal), あつい, まるこげ"
            );
        difficulty = Difficulty[d.Value];
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "ChooseDifficulty", false,
                "難易度宣託"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][ChooseDifficulty]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][ChooseDifficulty]enable");
            LoYUtilPlugin.mgr.add_flag(FlagId, true);
            int f = difficulty - 9;
            bool high = f >> 1 == 1;
            bool low = (f & 1) == 1;
            LoYUtilPlugin.mgr.add_flag(DifficultyHigh, high);
            LoYUtilPlugin.mgr.add_flag(DifficultyLow, low);

            var org = Util.get_method(typeof(EncounterGenerator), "GetLevelScaling");
            var hook = typeof(ChooseDifficulty).GetMethod("EnemyLvMultiplier");
            hm.Patch(org, postfix: new HarmonyMethod(hook));

            /*
            org = Util.get_method(typeof(DropItemGenerator), "GenerateEnemyDropItems");
            hook = typeof(ChooseDifficulty).GetMethod("ItemLvMultiplier");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
            */
        }
    }

    /* 敵レベルを難易度に従って上げる
     * 本来の敵レベルのベース計算式は
     *  パーティ平均レベル/planDivider+modifiedPlanModify+スキル補正値（魔物の口笛等）
     */
    public static void EnemyLvMultiplier(ref int __result)
    {
        update_difficulty();
        //黄金の砂時計使用後は敵のレベルをパーティの平均レベル*3/5上げる
        //終盤になるとかばうが失敗すると侍が即死しがちでハゲるんで要修正か
        if(SessionFlagAccessorScripts.IsOnScriptFlag(GoldenHourglass.GoldenHourglassUsed))
        {
            Party party = Party.Current;
            int n = 0;
            for(int i = 0; i < party.MemberCount; ++i)
                n += party.GetCharacterByOrder(i).Level;
            __result += (int)System.Math.Round(n * 3.0 / party.MemberCount / 5.0);
            //Console.Write($"[EnemyLvMultiplier]{__result}/{n/party.MemberCount}");
        }
        __result = (int)System.Math.Round(__result * difficulty / 10.0);
    }

    /*
    //戦闘場所に応じたアイテムのレベル, ドロップレベルのキャップ, 課長のレベル, 倒した敵のレベル, 倒した敵のID, dropRateAddValue(0固定？), (あれば)確定入手アイテムリストからドロップアイテムを生成する
    //ドロップレベルのキャップはDropItemGenerator::CalcTreasureLevel()で計算される
    //キャップの決定に関与するドロップ計算除数はSectorData.dropDivisorに記述される
    //確定入手アイテムリストはスクリプトからしか設定できない？
    //EnemyLvMultiplier()で敵レベルをいじってるのでいじる必要はなさげ
    public static void ItemLvMultiplier(int treasureLevel, int itemLevelCap, int playerLevel, int enemyLevel, int enemyId, int dropRateAddValue)
    {
        //99鉱区キャンプ出入り口に設定した魔物の花で検証
        //課長レベル57、敵レベル46
        //14, 3, 57, 46, 3, 0
        UnityEngine.Debug.LogFormat("{0}, {1}, {2}, {3}, {4}, {5}", treasureLevel, itemLevelCap, playerLevel, enemyLevel, enemyId, dropRateAddValue);
    }
    */

    /* 難易度宣託の結果を反映させる
     * 敵レベルを算出するたびに呼ばれるのは格好悪いので要修正か
     */
    public static void update_difficulty()
    {
        if(!LoYUtilPlugin.mgr.is_enable)
            return;
        bool high, low;
        //フラグストレージから読み出す
        if(Database.Session.Flags.ScriptFlag.ContainsKey(DifficultyHigh))
        {
            //Console.Write("[update_difficulty]from session storage");
            high = SessionFlagAccessorScripts.IsOnScriptFlag(DifficultyHigh);
            low = SessionFlagAccessorScripts.IsOnScriptFlag(DifficultyLow);
        }
        //ResourceManagerのフラグストレージから読み出す
        else
        {
            //Console.Write("[update_difficulty]from resource manager");
            high = LoYUtilPlugin.mgr.get_flag(DifficultyHigh);
            low = LoYUtilPlugin.mgr.get_flag(DifficultyLow);
        }
        int result = (Convert.ToInt32(high) << 1) + Convert.ToInt32(low);
        //Console.Write($"[update_difficulty]{result}/{high}, {low}");
        switch(result)
        {
            case 0:
                difficulty = Difficulty["ぬるい"];
                break;
            case 1:
                difficulty = Difficulty["あったかい"];
                break;
            case 2:
                difficulty = Difficulty["あつい"];
                break;
            case 3:
                difficulty = Difficulty["まるこげ"];
                break;
            default:
                Console.Write($"[ChooseDifficulty][update_difficulty]Error: difficulty is {result}.");
                break;
        }
    }

    public static Dictionary<string, int> Difficulty = new Dictionary<string, int>()
        {
            {"ぬるい", 9},
            {"あったかい", 10},
            {"あつい", 11},
            {"まるこげ", 12}
        };
}

}