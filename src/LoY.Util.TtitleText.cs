using System;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.UIs;


namespace LoYUtil
{

/* タイトル画面でシステムをセーブする前にMODをロードした旨を表示するウィンドウを出す */
class TitleTextIndicator
{
    private static string messageString;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<string> message = cfg.Bind(
                "Const", "TitleTextIndicatorDesc",
                "LoYUtilPluginのロードに成功",
                "タイトル画面でMODがロードされたときに表示する文章"
            );
        messageString = message.Value;
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "TitleTextIndicator", false,
                "タイトル画面でMODがロードされたかを表示する\n" +
                "確認用なので基本的にfalse推奨"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][TitleTextIndicator]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][TitleTextIndicator]enable");
            var org = typeof(InputTitleRoot).GetMethod("CreateCopyrightImage", BindingFlags.NonPublic | BindingFlags.Instance);
            var hook = typeof(TitleTextIndicator).GetMethod("Prefix");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    public static void Prefix(InputTitleRoot __instance)
    {
        //InputTitleRoot.StartNewGameMessageSelectSlot()から転用
        InputCommonWindowRoot commonWindow = SingletonMonoBehaviour<ResidentUIs>.Instance.GetCommonWindow();
        InputCommonWindowRoot.MessageWindowParam messageWindowParam = new InputCommonWindowRoot.MessageWindowParam();
        messageWindowParam.SetMessageString(messageString);
        commonWindow.SetupBeforeInput(messageWindowParam, true);
        commonWindow.StartInputAsChild(__instance, true, false, false);
    }
}

}

