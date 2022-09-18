using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.Items;
using Experience.ScriptEvent;


namespace LoYUtil
{

/* スクリプトにユーザー定義のコマンドを追加する */
public class ExternalCommand
{
    public delegate ResultCode ExCommand(object self, ScriptCommand command);
    public static Dictionary<string, ExCommand> excommand = null;
    public static readonly ScriptFlagId FlagId = (ScriptFlagId)1906;
    //拡張コマンドは常にコマンドIDが301となる
    public static readonly ScriptCommandId excmd_id = (ScriptCommandId)301;
    public static readonly string ResouceID = "ExternalCommand.excommand";

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "ExternalCommand", false,
                "イメージを追加できるようにする"
            );

        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][ExternalCommand]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][ExternalCommand]enable");
            excommand = new Dictionary<string, ExCommand>();
            excommand["test"] = test;
            excommand["nop"] = nop;

            LoYUtilPlugin.mgr.add_flag(FlagId, true);
            LoYUtilPlugin.mgr.add_data(ResouceID, excommand);
            GoldenHourglass.register_excommand();

            var org = Util.get_method(typeof(IScriptCommandBinderExtensions), "Execute");
            var hook = typeof(ExternalCommand).GetMethod("Execute");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    /* コマンドIDがexcmd_idなら該当するコマンドを実行する */
    public static bool Execute(IScriptCommandBinder self, ScriptCommand command, ref ResultCode __result)
    {
        if(command.CommandId != excmd_id)
            return true;
        string func_name = command.GetParameter<string>(0);
        if(!excommand.ContainsKey(func_name))
            return true;
        //パラメータから関数名を省いて呼び出し先へと渡す
        ScriptCommandParameterData[] p = new ScriptCommandParameterData[command.ParameterCount - 1];
        for(int i = 1; i < command.ParameterCount; ++i)
            p[i - 1] = command.Parameters[i];
        ScriptCommand cmd = new ScriptCommand(command.LineNumber, command.CommandId, p);
        __result = excommand[func_name]((object)self, cmd);
        return false;
    }

    /* 引数を一つ取り、引数をコンソールに出力するだけのテスト用コマンド */
    public static ResultCode test(object self, ScriptCommand command)
    {
        Console.Write("external command test.");
        Console.Write("argument: {0}.", command.GetParameter<string>(0));
        return ResultCode.Next;
    }

    /* 何もしないコマンド */
    public static ResultCode nop(object self, ScriptCommand command)
    {
        return ResultCode.Next;
    }
}

}