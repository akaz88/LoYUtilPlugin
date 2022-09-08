using System;
using System.Reflection;
using System.Collections;
using Steamworks;
using BepInEx.Configuration;
using HarmonyLib;
using UnityEngine;
using UnityEngine.UI;

using Experience;


namespace LoYUtil
{

/* 起動画面を少しだけ短縮する
 * BootScreenクラスをそのまますべて書き換えてしまうことに注意
 */
class BootScreenFix
{
    public static void enable(Harmony hm, ConfigFile cfg)
    {
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "BootScreenFix", false,
                "起動画面の短縮"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][BootScreenFix]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][BootScreenFix]enable");
            var org = Util.get_method(typeof(BootScreen), "Begin");
            var hook = typeof(BootScreenFix).GetMethod("Prefix");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    public static bool Prefix(BootScreen __instance, ref GameInitializer initializer, ref RawImage ___screen, ref Texture[] ___images, ref bool ___isBusy)
    {
        BSReplacer rpl = new BSReplacer();
        rpl.inst = __instance;
        rpl.screen = ___screen;
        rpl.images = ___images;
        //rpl.isBusy = ___isBusy;
        rpl.Awake();
        rpl.Begin(initializer);
        return false;
    }
}


class BSReplacer : BootScreen
{
    public BootScreen inst;
    //public bool isBusy;
        //不要
    private static readonly float ImageWaitTime = 3f;
    private static readonly float FinalWaitTime = 0.5f;
    private static readonly float FadeInDuration = 0.5f;
    private static readonly float FadeOutDuration = 0.5f;
    private Experience.Tweening.FloatTween fader;
    private GameInitializer initializer;
    private RealTimer timer;
    private enum Phase
    {
        Attention,
        AksysLogo,
        CompanyLogo,
        AutoSaving,
        UnityLogo
    }

    [SerializeField]
    public RawImage screen;

    [SerializeField]
    [ArrayElementLabel(typeof(BSReplacer.Phase))]
    public Texture[] images;

    //IsFinishedの値でExperience.GameController.Start()のループを制御している
    new public bool IsFinished
    {
        get
        {
            return this.inst.IsFinished;
        }
        private set
        {
            //setterは"set_変数名"という名前のメソッドとして隠蔽されている
            typeof(BootScreen).GetMethod("set_IsFinished", BindingFlags.NonPublic | BindingFlags.Instance).Invoke(this.inst, new object[]{value});
        }
    }

    public void Awake()
    {
        this.fader = new Experience.Tweening.FloatTween();
        this.fader.OnUpdate += this.OnFadeUpdate;
        this.timer = new RealTimer();
        if (SteamManager.Initialized)
            SteamFriends.GetPersonaName();
    }

    private void OnFadeUpdate(float x)
    {
        if (this.screen != null)
            this.screen.color = new Color(x, x, x);
    }

    private void BeginWaitTimer()
    {
        this.timer.Reset();
    }

    private void StartInitialize(GameInitializer.Phase phase)
    {
        if (this.initializer != null)
            this.initializer.SetReady(phase);
    }

    private IEnumerator WaitForInitialize(GameInitializer.Phase phase)
    {
        yield return new WaitUntil(() => this.initializer.IsDone(phase));
        yield break;
    }

    private IEnumerator FadeIn(float duration)
    {
        yield return this.fader.BeginRoutine(0f, 1f, duration, null);
        yield break;
    }

    private IEnumerator FadeOut(float duration)
    {
        yield return this.fader.BeginRoutine(1f, 0f, duration, null);
        yield break;
    }

    private void SetImage(BSReplacer.Phase phase)
    {
        if (this.images.IsValidIndex((int)phase))
            this.SetImage(this.images[(int)phase]);
        else
            this.SetImage(null);
    }

    private void SetImage(Texture texture)
    {
        screen.texture = texture;
    }

    private IEnumerator WaitTimer(float waitTime)
    {
        yield return new WaitWhile(() => this.timer.ElapsedTime < waitTime);
        yield break;
    }

    new public void Begin(GameInitializer initializer)
    {
        System.Globalization.CultureInfo.DefaultThreadCurrentCulture = System.Globalization.CultureInfo.InvariantCulture;
        this.IsFinished = false;
        this.inst.gameObject.SetActive(true);
        this.inst.StartCoroutine(this.BootRoutine(initializer));
    }

    /* 起動時の企業ロゴ等の表示を改造する
     *　ロゴ表示の裏で各種初期化を行っているのでそれほど短くできない
     * たぶん半分くらいにはなってる(気がする)
     * IEnumeratorはコンパイルすると隠蔽されてしまうのでフックするのはBeginの方
     */
    public IEnumerator BootRoutine(GameInitializer initializer)
    {
        //this.isBusy = true;
        this.initializer = initializer;
        UnityEngine.ThreadPriority loadingPriority = Application.backgroundLoadingPriority;
        Application.backgroundLoadingPriority = UnityEngine.ThreadPriority.High;
        float loadWaitedTime = BSReplacer.ImageWaitTime;

        //Experienceロゴ
        this.SetImage(BSReplacer.Phase.CompanyLogo);
        yield return new WaitForFrames(6);
        yield return this.FadeIn(BSReplacer.FadeInDuration);
        this.BeginWaitTimer();
        this.StartInitialize(GameInitializer.Phase.SystemInitialization);
        yield return this.WaitForInitialize(GameInitializer.Phase.SystemInitialization);
        if (this.timer.ElapsedTime > loadWaitedTime)
            loadWaitedTime = this.timer.ElapsedTime;
        yield return this.WaitTimer(BSReplacer.ImageWaitTime);
        yield return this.FadeOut(BSReplacer.FadeOutDuration);

        //Aksysロゴ
        this.SetImage(BSReplacer.Phase.AksysLogo);
        yield return this.FadeIn(BSReplacer.FadeInDuration);
        this.BeginWaitTimer();
        this.StartInitialize(GameInitializer.Phase.SystemLoading);
        yield return this.WaitForInitialize(GameInitializer.Phase.SystemLoading);
        this.StartInitialize(GameInitializer.Phase.AssetPreLoading);
        yield return this.WaitTimer(loadWaitedTime);
        yield return this.FadeOut(BSReplacer.FadeOutDuration);

        //オートセーブ注意画面
        this.SetImage(BSReplacer.Phase.AutoSaving);
        AudioSystem.Music.Play(MusicId.Title.ResourceId(), 1f);
            //AssetPreLoadingの初期化開始後でないと音は鳴らない
        yield return this.WaitForInitialize(GameInitializer.Phase.AssetPreLoading);
        yield return this.FadeIn(BSReplacer.FadeInDuration);
        this.BeginWaitTimer();
        this.StartInitialize(GameInitializer.Phase.AssetLoading);
        yield return this.WaitForInitialize(GameInitializer.Phase.AssetLoading);
        yield return this.WaitTimer(BSReplacer.FinalWaitTime);
        yield return this.FadeOut(BSReplacer.FadeOutDuration);

        Application.backgroundLoadingPriority = loadingPriority;
        this.IsFinished = true;
        //typeof(BootScreen).GetMethod("set_IsFinished", BindingFlags.NonPublic | BindingFlags.Instance).Invoke(this.inst, new object[]{true});
        //this.isBusy = false;
        //initializer = null;
        //this.SetImage(null);
        this.inst.gameObject.SetActive(false);
        yield break;
    }
}

}