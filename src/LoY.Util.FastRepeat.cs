using System;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.Battle.TurnBasedBattle;
using Experience.UIs;


namespace LoYUtil
{

/* オートバトルに高速戦闘の選択肢を追加する */
class FastRepeat
{
    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "FastRepeat", false,
                "オートバトルで高速戦闘を選べるようにする"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][FastRepeat]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][FastRepeat]enable");

            var org = Util.get_method(typeof(InputBattleCommandConfirmWindowList), "GetSelectionIdTable");
            var hook = Util.get_method(typeof(FastRepeat), "GetSelectionIdTablePlusFastRepeat");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputBattleCommandRoot), "SelectAutoBattleDecide");
            hook = Util.get_method(typeof(FastRepeat), "SelectAutoBattleDecidePlusFastRepeat");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputBattleCommandRoot), "StartSelectAutoBattle");
            hook = Util.get_method(typeof(FastRepeat), "SetSelectionFastRepeat");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    /* オートバトルに高速戦闘の選択肢を追加する */
    public static bool GetSelectionIdTablePlusFastRepeat(InputBattleCommandConfirmWindowList.Mode mode, ref BattleDefines.BattleCommandConfirmSelectionId[] __result)
    {
        if(mode != InputBattleCommandConfirmWindowList.Mode.SelectAutoBattle)
            return true;
        __result =  new BattleDefines.BattleCommandConfirmSelectionId[]
            {
                BattleDefines.BattleCommandConfirmSelectionId.ActionDecideFast,
                BattleDefines.BattleCommandConfirmSelectionId.SelectAutoBattleRepeat,
                BattleDefines.BattleCommandConfirmSelectionId.SelectAutoBattleNormalAttack,
                BattleDefines.BattleCommandConfirmSelectionId.SelectAutoBattleCancel
            };
        return false;
    }

    /* オートバトルでの高速戦闘を有効にする */
    public static bool SelectAutoBattleDecidePlusFastRepeat(InputBattleCommandRoot __instance, BattleCommandConfirmWindowListSelectionParam selectionParam, bool isDecideByActionKey)
    {
        if(selectionParam.GetSelectionId() != BattleDefines.BattleCommandConfirmSelectionId.ActionDecideFast)
            return true;
        Util.invoke(__instance, "ConfirmAllCommandsCommandRepeat", new object[]{true});
        return false;
    }

    /* デフォルトで高速戦闘にカーソルを置く */
    public static bool SetSelectionFastRepeat(InputBattleCommandRoot __instance, InputBattleCommandTop ___inputCommand, InputBattleCommandConfirmWindowList ___inputCommandConfirmWindow, TurnBasedBattleData ___refBattleData)
    {
        //Console.Write("SetSelection");
        ___inputCommand.StartDisappear(false, false);
        ___inputCommandConfirmWindow.SetupBeforeInput(InputBattleCommandConfirmWindowList.Mode.SelectAutoBattle, ___refBattleData.PlayerCombatParty.Id);
        ___inputCommandConfirmWindow.SetSelection(BattleDefines.BattleCommandConfirmSelectionId.ActionDecideFast, false);
        ___inputCommandConfirmWindow.StartInputAsChild(__instance, true, true, false);
        return false;
    }
}

}