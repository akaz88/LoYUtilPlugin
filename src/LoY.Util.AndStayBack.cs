using System;
using System.Reflection;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.Dungeons;


namespace LoYUtil
{

/* 前を向いたまま移動できるようにする */
class AndStayBack
{
    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "AndStayBack", false,
                "右スティックで過去作同様に前を向いたまま移動できるようにする\n" +
                "カメラモードにはR2で入ること"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][AndStayBack]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][AndStayBack]enable");
            var org = Util.get_method(typeof(InputActionEvaluator), "RegisterKeyMap");
            var hook = typeof(AndStayBack).GetMethod("RemoveRStickCamera");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            //internalクラスはAssemly.GetTypeしなければならない
            //コンストラクタはGetConstructor()で取得する
            var org2 = Assembly.GetAssembly(typeof(DungeonInput)).GetType("Experience.Dungeons.MovementKeyTranslator").GetConstructor(new Type[]{typeof(MovementActionKeyMap)});
            hook = typeof(AndStayBack).GetMethod("AddRStickMove");
            hm.Patch(org2, prefix: new HarmonyMethod(hook));
        }
    }

    /* 右スティック入力でカメラモードに入るのを防ぎ、R2でカメラモードに入るようにする */
    public static void RemoveRStickCamera(InputActionEvaluator __instance, ref InputActionKeyMap keyMap)
    {
        keyMap.Remove(GamepadKey.RStickUp);
        keyMap.Remove(GamepadKey.RStickDown);
        keyMap.Remove(GamepadKey.RStickLeft);
        keyMap.Remove(GamepadKey.RStickRight);
        keyMap.Add(GamepadKey.R2, InputAction.StartCameraMode, InputActionKeyMap.KeyState.Pressed);
    }

    /* 右スティック下入力で移動できるようにする */
    public static void AddRStickMove(ref MovementActionKeyMap keyMap)
    {
        keyMap.Add(GamepadKey.RStickUp, MovementAction.Move, MovementWay.Forward);
        keyMap.Add(GamepadKey.RStickDown, MovementAction.Move, MovementWay.Back);
        keyMap.Add(GamepadKey.RStickLeft, MovementAction.Move, MovementWay.Left);
        keyMap.Add(GamepadKey.RStickRight, MovementAction.Move, MovementWay.Right);
    }
}

}