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

/* L2ボタン押しながらSelectキーでソフトリセット(予定) */
class SoftReset
{
    public static bool is_loading = false;
    /*static StorageResultCode st_result;
    static int slot_no;
    static Navigation navigation;
    static FacilityId fac_id;*/

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
        var slcntl = SingletonMonoBehaviour<SaveLoadController>.Instance;
        if(slcntl.IsAutoSaving())
            yield return new WaitWhile(() => slcntl.IsAutoSaving());
        slcntl.SetIsEnableAutoSave(false);

        //in dungeon
        if(DungeonScene.IsInstanced && Party.Current.Location.IsInDungeon())
        {
            SingletonMonoBehaviour<ScriptEngine>.Instance.Screen.GetCameraController().ResetOnScriptEnd();
            /*
            Vector3Tween v3 = new Vector3Tween();
            v3.From = DungeonScene.Player.Camera.CameraWorldOffset;
            v3.To = Vector3.Zero;
            v3.Duration = 0.0;
            v3.IsLooping = false;
            v3.Begin();
            DungeonScene.Player.Camera.CameraWorldOffset = v3.Value;
            */
        }
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

    static IEnumerator __old__reset()
    {
        Console.Write("SoftReset");
        var inst = SingletonMonoBehaviour<SaveLoadController>.Instance;
        int slot = (int)Util.get_value(inst, "loadingSlotNumber");
        if(slot == SaveLoadController.SaveSlotNumberInvalid)
        {
            Console.Write("break");
            is_loading = false;
            yield break;
        }

        Console.Write("exitting...");
        yield return SceneManager.ExitScene();

        Console.Write("loading...");
        inst.LoadSessionData(
            slot, 0,
            new SaveLoadController.LoadSessionDataFinishCallback(
                change_scene
            )
        );
        yield return new WaitWhile(() => is_loading);
        yield return new WaitWhile(() => SceneManager.IsNavigating);
        Console.Write("done.");
    }

    static void change_scene(StorageResultCode result, int no, Navigation nav, FacilityId fid)
    {
        Console.Write($"change_scene: {result}, {no}, {nav}, {fid}");
        if(nav == Navigation.ChangeCity)
        {
            CityEnteringParameter cep = new CityEnteringParameter();
            cep.SetFacilityIdInitial(fid);
            cep.SetByLoadSaveData(true);
            SceneNavigator.Navigate(nav, cep);
        }
        else
            SceneNavigator.Navigate(nav, null);
        is_loading = false;
    }
}

}