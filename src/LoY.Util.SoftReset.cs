using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.Characters;
using Experience.City;
using Experience.Dungeons;
using Experience.Facilities;
using Experience.SaveLoad;
using Experience.Scenes;
using Experience.SceneManagement;
using Experience.ScriptEvent;

namespace LoYUtil
{

/* L2ボタン押しながらSelectキーでソフトリセット
 * 一応ゲーム中ならいつでもタイトルに戻れるようにはなったが、システムの都合上演出が変
 * これはシーンのスタックを一つずつ終わらせながら遡っていくからのようだ
 */
class SoftReset
{
    public static bool is_loading = false;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "SoftReset", false,
                "L2ボタンを押しながらSelectキーでソフトリセット"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][SoftReset]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][SoftReset]enable");
            LoYUtilPlugin.ev_update += update;
        }
    }

    public static IEnumerator update()
    {
        //ソフトリセット：L2を押しながらSelectでタイトルに戻る
        if(SingletonMonoBehaviour<Gamepad>.Instance != null && !is_loading && Gamepad.GetKeyState(GamepadKey.L2).Holding && Gamepad.GetKeyState(GamepadKey.Select).Pressed)
        {
            is_loading = true;
            yield return reset();
            is_loading = false;
        }
    }

    static IEnumerator reset()
    {
        //UIs.InputSystemInterruptRoor::StartBackToTitleMain
        //Console.Write("SoftReset");

        //セーブ中なら終わるまで待つ
        var slcntl = SingletonMonoBehaviour<SaveLoadController>.Instance;
        if(slcntl.IsAutoSaving())
            yield return new WaitWhile(() => slcntl.IsAutoSaving());
        slcntl.SetIsEnableAutoSave(false);

        //camera reset
        //in dungeon
        if(DungeonScene.IsInstanced && Party.Current.Location.IsInDungeon())
            SingletonMonoBehaviour<ScriptEngine>.Instance.Screen.GetCameraController().ResetOnScriptEnd();
        var camera2d = SingletonMonoBehaviour<ResidentScreen2D>.Instance.GetCamera2DPostEffect();
        camera2d.ResetFocus();

        AudioSystem.Music.Stop();
        AudioSystem.Sound.Stop();
        ScriptEngine se = SingletonMonoBehaviour<ScriptEngine>.Instance;
        if(se != null)
            se.ForceFinishScript();
        QuestController.AbortCoroutines();
        Database.Session.SessionInfo.ClearPlayingUserId();

        yield return SceneManager.ExitScene();
        SceneNavigator.Navigate(Navigation.Title, null);
        yield return new WaitWhile(() => SceneManager.IsNavigating);

        slcntl.SetIsEnableAutoSave(true);
        //Console.Write("done");
    }
}

}