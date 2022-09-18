using System;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.ScriptEvent;



namespace LoYUtil
{

/* デバッグ出力を見つけたらここに足していく */
class ExpDebugPrint
{
    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "ExpDebugPrint", false,
                "デバッグ用と思しきメッセージをコンソールに出力する\n"+
                "MOD開発の際のデバッグ向け\n"+
                "要BepInEx/config/BepInEx.cfgのLogging.Console"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][ExpDebugPrint]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][ExpDebugPrint]enable");
            var org =Util.get_method(typeof(ScriptExpressionDecoder), "DecodeLogError");
            var hook = typeof(ExpDebugPrint).GetMethod("SEDDecodeLogError");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    /* ScriptEvent.ScriptExpressionDecoder.DecodeLogError() */
    public static void SEDDecodeLogError(string scriptName, ScriptCommand command, int commandParameterIndex, string message, params object[] args)
    {
        //string m = (string)Util.get_method(typeof(ScriptExpressionDecoder), "GetLogBaseString").Invoke(null, new object[]{scriptName, command});
        string m = (string)Util.invoke(typeof(ScriptExpressionDecoder), "GetLogBaseString", new object[]{scriptName, command});
        if(args.Length != 0)
            Console.Write("[Script][{0}][{1}]{2}@{3}", m, commandParameterIndex, message, String.Join(", ", args));
        else
            Console.Write("[Script][{0}][{1}]{2}", m, commandParameterIndex, message);
    }
}

}