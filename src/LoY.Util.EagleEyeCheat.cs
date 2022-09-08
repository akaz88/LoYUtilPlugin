using System;
using System.Reflection;
using System.Reflection.Emit;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;

using Experience;
using Experience.UIs;
using Experience.Battle;
using Experience.Characters;


namespace LoYUtil
{

/* スキル「鷹の眼」でHPとLvを数字で表示する */
class EagleEyeCheat
{
    private static NumbersPlayerHpMp cur = null;
    private static NumbersPlayerHpMp max = null;
    private static UIText text = null;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "EagleEyeCheat", false,
                "スキル「鷹の眼」でHPとLvを数字で表示する"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][EagleEyeCheat]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][EagleEyeCheat]enable");

            //メインのHP表示処理
            var org_main = Util.get_method(typeof(BattleEnemyParametersWindow), "SetupParametersByEnemy");
            var hook = typeof(EagleEyeCheat).GetMethod("ShowEnemyHPNumber");
            hm.Patch(org_main, postfix: new HarmonyMethod(hook));

            //クリアしておかないと無効なキャンバスに描画しようとしてエラーを吐くのでその予防
            var org_clear = typeof(BattleStats).GetConstructor(new Type[]{});
            hook = typeof(EagleEyeCheat).GetMethod("ClearUI");
            hm.Patch(org_clear, postfix: new HarmonyMethod(hook));
        }
    }

    public static void ShowEnemyHPNumber(BattleEnemyParametersWindow __instance, EnemyCombatant enemy, bool isShowHp, bool isShowLevel, UICanvas ___canvasParameters, UIText ___textLevel)
    {
        if(!isShowHp)
            return;
        if(enemy.Hp.Max > Enemy.MaxHpLimit.Upper)
            Console.Write("[ShowEnemyHPNumber]Enemy.Hp.Max > {0}({1})", Enemy.MaxHpLimit.Upper, enemy.Hp.Max);

        if(cur == null)
        {
            //表示する場所は敵パラメーターウィンドウのHPゲージ部分
            text = new UIText(___canvasParameters, UITextId.BattleEnemyParametersEnemyName);
            text.SetTextString("/");
            text.SetColor(FontColorId.White);
                //もうちょいいい感じの色とかサイズとか知りたい

            NumbersBaseImageTexture.InitializeParam NumbersInitializeParam = new NumbersBaseImageTexture.InitializeParam(NumbersBaseImageTexture.HigherDigitSpaceType.Pack, NumbersBaseImageTexture.SignType.None, UIUtility.GetDigitMax(Enemy.MaxHpLimit.Upper));
            cur = new NumbersPlayerHpMp(___canvasParameters, ref NumbersInitializeParam);
            max = new NumbersPlayerHpMp(___canvasParameters, ref NumbersInitializeParam);

            Util.invoke(__instance, "AddChild", new object[]{text});
            Util.invoke(__instance, "AddChild", new object[]{cur});
            Util.invoke(__instance, "AddChild", new object[]{max});
        }

        //HPゲージ上に重ねて表示する
        //敵のHPが高すぎるとはみ出る危険はあるが、社長再戦時も大丈夫だったのでヨシ！
        //      -> オーバーアルダーLv125Hp99999で問題なかったんで多分大丈夫
        UIPositionData pos = UIPositionDataTable.GetData(UIPositionId.BattleEnemyParametersHpBar);
        float base_x = pos.PositionX + 10;
        cur.SetNumbers(enemy.Hp.Value);
        max.SetNumbers(enemy.Hp.Max);
        float text_x = cur.GetSizeX();
        float max_x = text_x + text.GetSizeX();
        cur.SetPosition(base_x, pos.PositionY);
        text.SetPosition(base_x + text_x, pos.PositionY);
        max.SetPosition(base_x + max_x, pos.PositionY);

        //ついでにボスであってもレベルも表示する
        ___textLevel.SetTextString(EmbeddedText.BATTLE_ENEMY_PARAMETER_LEVEL_SHOWN, new object[] {enemy.Level});
    }

    /* 戦闘終了時にcurをNULLにするだけ､このクラスの処理にはノータッチ */
    public static void ClearUI()
    {
        cur = null;
    }
}

}
