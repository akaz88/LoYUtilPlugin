using System;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.UIs;
using Experience.Battle;
using Experience.Battle.TurnBasedBattle;
using Experience.Characters;


namespace LoYUtil
{

/* 戦闘中LRでキャラクターを選択する */
class LRSelect
{
    public static void enable(Harmony hm, ConfigFile cfg)
    {
        //return;
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "LRSelect", false,
                "戦闘中LRで剣街風にキャラクターを選択できるようにする\n" +
                "元のRキーで表示変更をする機能はセレクトキーに移設する"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][LRSelect]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][LRSelect]enable");
            var org = Util.get_method(typeof(InputBattleCommandRoot), "InputPlayerAccuracyEvasionPanel");
            var hook = typeof(LRSelect).GetMethod("InputHookLR");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    public static bool InputHookLR(InputBattleCommandRoot __instance, InputState ___inputStateCurrent, ref bool __result, ref int ___commandSelectingPlayerOrder, ref TurnBasedBattleData ___refBattleData)
    {
        __result = false;
        InputState inputState = ___inputStateCurrent;
        if(!(inputState == InputState.CommandTop || inputState == InputState.PlayerSelect || inputState - InputState.ConfirmCommand <= 2))
            return false;

        //Rキーの機能をSelectキーに移設
        if (Gamepad.GetKeyDown(GamepadKey.Select))
        {
            Util.invoke(__instance, "SwitchCockpitIsDetailed");
            __result = true;
        }
        //LRでキャラ選択移動
        //InputBattleCommandRoot::CommandTopCancel()よりわりと改変
        else if(Gamepad.GetKeyDown(GamepadKey.R1) && inputState == InputState.CommandTop)
        {
            bool isChangeSelectionIndex = true;
            int i = ___commandSelectingPlayerOrder + 1;
            while(i != ___commandSelectingPlayerOrder)
            {
                if(i >= Player.PartyMemberCountUpper)
                    i = 0;
                PlayerCombatant playerByOrder = ___refBattleData.PlayerCombatParty.GetCharacterByOrder(0, i);
                if (playerByOrder != null && playerByOrder.CanInputAction())
                {
                    AudioSystem.Sound.Play(SoundId.Select.ResourceId(), 1f);
                    break;
                }
                ++i;
            }
            if(i == ___commandSelectingPlayerOrder)
            {
                AudioSystem.Sound.Play(SoundId.Cancel.ResourceId(), 1f);
                isChangeSelectionIndex = false;
            }
            Util.invoke(__instance, new Type[]{typeof(int), typeof(bool)}, "StartCommandTop", new object[]{i, isChangeSelectionIndex});
            __result = true;
        }
        else if(Gamepad.GetKeyDown(GamepadKey.L1) && inputState == InputState.CommandTop)
        {
            bool isChangeSelectionIndex = true;
            int i = ___commandSelectingPlayerOrder - 1;
            while(i != ___commandSelectingPlayerOrder)
            {
                if(i < 0)
                    i = Player.PartyMemberCountUpper;
                PlayerCombatant playerByOrder = ___refBattleData.PlayerCombatParty.GetCharacterByOrder(0, i);
                if (playerByOrder != null && playerByOrder.CanInputAction())
                {
                    AudioSystem.Sound.Play(SoundId.Select.ResourceId(), 1f);
                    break;
                }
                --i;
            }
            if(i == ___commandSelectingPlayerOrder)
            {
                AudioSystem.Sound.Play(SoundId.Cancel.ResourceId(), 1f);
                isChangeSelectionIndex = false;
            }
            Util.invoke(__instance, new Type[]{typeof(int), typeof(bool)}, "StartCommandTop", new object[]{i, isChangeSelectionIndex});
            __result = true;
        }
        return false;
    }

    //InputBattleCommandRoot.InputStateはprivateのため参照が面倒
    public enum InputState
    {
        None,
        CommandTop,
        SkillList,
        SkillListHighCast,
        ItemList,
        PlayerSelect,
        EnemySelect,
        PartyBattleStyleSelect,
        ConfirmCommand,
        SelectAutoBattle,
        ConfirmEscape,
        EscapeTrying,
        EscapeByItem,
        BeforeBattleStart,
        BeforeBattleStartDisappearPartyBattleStylePanel,
        Tutorial
    }
}

}