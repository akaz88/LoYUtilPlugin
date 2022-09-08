using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.UIs;

namespace LoYUtil
{

/* 軽微なバグの修正
 * ・エンディングの脱出者一覧
 */
[HarmonyPatch]
public class Bugfix
{
    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "Bugfix", true,
                "軽微なバグの修正"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][Bugfix]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][Bugfix]enable");
            LoYUtilPlugin.ev_load_later += rewrite_columns;
        }
    }

    /* 採掘課社員の欄を三列にすると三列目ははみ出すので二列に修正 */
    static void rewrite_columns()
    {
        Util.set_static_value(typeof(UI), "EpilogueCharacterListColumns", 2);
    }
}

}