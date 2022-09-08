using System;
using System.Reflection;
using System.Reflection.Emit;
using System.Collections;
using System.Collections.Generic;
using BepInEx.Configuration;
using HarmonyLib;

using Experience;
using Experience.UIs;
using Experience.Inventories;
using Experience.Items;


namespace LoYUtil
{

/* 花力抽出，AG抽出，倉庫出し入れで複数のアイテムを同時選択して一括入力できるようにする */
class MultiItemSelect
{
    public static List<SelectedItem> selected = new List<SelectedItem>();
    private static Type is_t = typeof(InputItemWindowWithTab).GetNestedType("InputState", BindingFlags.InvokeMethod | BindingFlags.NonPublic | BindingFlags.Instance);
    private static ShopType shop_type = ShopType.None;
    private static PartyMoneyPurchaseWindow moneyPurchaseWindow = null;
    private static PartyWalletPurchaseWindow walletPanel = null;

    public static void enable(Harmony hm, ConfigFile cfg)
    {
        //return;
        ConfigEntry<bool> enabled = cfg.Bind(
                "Enable", "MultiItemSelect", false,
                "花力抽出，AG抽出，倉庫出し入れで複数のアイテムを同時選択して一括入力できるようにする"
            );
        if(!enabled.Value)
            Console.Write("[LoYUtilPlugin][MultiItemSelect]disable");
        else
        {
            Console.Write("[LoYUtilPlugin][MultiItemSelect]enable");
            Type org_t = typeof(InputItemWindowWithTab);
            Type hook_t = typeof(MultiItemSelect);

            var org = Util.get_method(org_t, "Input");
            var hook = hook_t.GetMethod("InputHook");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(org_t, "SetInputState");
            hook = hook_t.GetMethod("SetInputStateHook");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            //org = Util.get_method(org_t, "UpdateInputState");
            //hook = hook_t.GetMethod("UpdateInputStateHook");
            //hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputItemSellRoot), "StartSelectInventory");
            hook = hook_t.GetMethod("ClearSelected");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputDungeonMakingResourceExtractRoot), "StartSelectInventory");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputCityStorageRoot), "InitializeInput");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputItemSellRoot), "SetupItemWindow");
            hook = hook_t.GetMethod("SetTypeSeller");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputDungeonMakingResourceExtractRoot), "SetupItemWindow");
            hook = hook_t.GetMethod("SetTypeExtractor");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputCityStorageRoot), "SetupSelectionParamListStorageTop");
            hook = hook_t.GetMethod("SetTypeStorage");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputItemDispose), "StartMessageBeginning");
            hook = hook_t.GetMethod("SetTypeDispose");
            hm.Patch(org, prefix: new HarmonyMethod(hook));

            org = Util.get_method(typeof(InputItemDispose), "UpdateSelectItem");
            hook = hook_t.GetMethod("ClearSelectedInDispose");
            hm.Patch(org, prefix: new HarmonyMethod(hook));
        }
    }

    /* 店タイプをアルゲン抽出に設定 */
    public static void SetTypeSeller(ref PartyMoneyPurchaseWindow ___moneyPurchaseWindow)
    {
        //Console.Write("Shop Type Seller");
        shop_type = ShopType.Seller;
        moneyPurchaseWindow = ___moneyPurchaseWindow;
        walletPanel = null;
        selected.Clear();
    }

    /* 店タイプを花力抽出に設定 */
    public static void SetTypeExtractor(ref PartyWalletPurchaseWindow ___walletPanel)
    {
        //Console.Write("Shop Type Extractor");
        shop_type = ShopType.Extractor;
        moneyPurchaseWindow = null;
        walletPanel = ___walletPanel;
        selected.Clear();
    }

    /* 店タイプを倉庫に設定 */
    public static void SetTypeStorage()
    {
        //Console.Write("Shop Type Storage");
        shop_type = ShopType.Storage;
        moneyPurchaseWindow = null;
        walletPanel = null;
        selected.Clear();
    }

    /* 店タイプを廃棄に設定 */
    public static void SetTypeDispose()
    {
        //Console.Write("Shop Type Dispose");
        shop_type = ShopType.Dispose;
        moneyPurchaseWindow = null;
        walletPanel = null;
        selected.Clear();
    }

    /* 誤爆回避 */
    public static void ClearSelected()
    {
        //Console.Write("Clear!");
        //Util.print_stack();
        shop_type = ShopType.None;
        selected.Clear();
    }

    /* アイテム廃棄の際のみここからClearSelectedを呼び、入力を終了させる */
    public static void ClearSelectedInDispose(InputItemDispose __instance)
    {
        int cap = SessionInventoriesAccessorItemsParty.GetInventoryCapacityCurrentParty(InventoryTypePartyItem.Bag);
        int cnt = SessionInventoriesAccessorItemsParty.GetItemCountCurrentParty(InventoryTypePartyItem.Bag);
        if(cnt > cap)
            return;
        //Console.Write("clear Dispose");
        ClearSelected();
        __instance.FinishInput();
    }

    /* アイテム選択画面への入力のフック
     * 店/倉庫だけでなく広範に渡り使用されるメソッドへのフックであることに注意
     */
    public static void InputHook(InputItemWindowWithTab __instance, ref bool __result, ref InputState ___inputState, ref ItemListDefines.SortInventoryType ___sortInventoryType, ref InputItemListWithTab ___inputItemListWithTab)
    {
        __result = false;
        if(___inputState != InputState.SelectItem || shop_type == ShopType.None)
            return;
        //Y/Spaceキーでアイテムを選択
        //if(Gamepad.GetKeyDown(GamepadKey.ActionRight) && ___inputState == InputState.SelectItem && shop_type != ShopType.None)
        if(Gamepad.GetKeyDown(GamepadKey.ActionRight))
        {
            //素直にMultiSelectを引数に積むと型チェックに引っかかってコケる
            var ms = Enum.ToObject(is_t, InputState.MultiSelect);
            Util.invoke(__instance, "SetInputState", new object[]{ms});
            __result = true;
        }
        //Select/Nキーで全アイテムを選択/解除
        else if(Gamepad.GetKeyDown(GamepadKey.Select))
        {
            __result = true;
            //すでに選択されていたら全解除
            if(selected.Count != 0)
            {
                switch_check(__instance);
                selected.Clear();
                return;
            }
            int selected_id = -1;
            foreach(var p in ___inputItemListWithTab.GetSelectionParamList(0))
            {
                ++selected_id;
                if(selected.Find(x => x.item_param == p) != null)
                    continue;
                SelectedItem t = new SelectedItem();
                t.id = selected_id;
                t.amount = p.GetItemCount();
                t.item = p.GetItem();
                t.item_param = p;
                //廃棄/売買不能アイテムは対象としない
                if(!t.item.IsDiscardable() || !t.item.IsSellable())
                    continue;
                selected.Add(t);
                switch_check(__instance, t);
            }
            SoundId.Select.Play();
            //foreach(var t in selected)
                //Console.Write($"{t.id}: {t.item.DisplayName.Text}");
        }
        //L2/Zキーでアイテムを売却/抽出/移動
        //else if(Gamepad.GetKeyDown(GamepadKey.L2) && ___inputState == InputState.SelectItem && selected.Count != 0 && shop_type != ShopType.None)
        else if(Gamepad.GetKeyDown(GamepadKey.L2) && selected.Count != 0)
        {
            //foreach(var t in selected)
                //Console.Write("{0} id:{1}, amount:{2}, price:{3}, fp:{4}", t.item.DisplayName, t.id, t.amount, t.item.GetSellingPrice() * t.amount, t.item.CalcDungeonMakingResourceExtractPoint() * t.amount);
            //チェックマークのクリアとアイテムの処理
            switch_check(__instance);
            if(shop_type == ShopType.Seller || shop_type == ShopType.Extractor || shop_type == ShopType.Dispose)
                execute_items(___sortInventoryType);
            else
                move_items(___sortInventoryType);

            //クラスの持ってるアイテムリストを更新
            List<ItemListSelectionParam> l = new List<ItemListSelectionParam>();
            foreach(var p in ___inputItemListWithTab.GetSelectionParamList(0))
            {
                SelectedItem t = selected.Find(delegate(SelectedItem s){return s.item_param == p;});
                if(t == null)
                    l.Add(p);
                else if(t.item_param.GetItemCount() != ItemListSelectionParam.ItemCountInvalid)
                        l.Add(t.item_param);
            }
            ___inputItemListWithTab.SetItemListSelectionParamList(l);

            __instance.UpdateSelectionParamList();
            //実際にアルゲン/花力が入るのはここ
            finalize();
            //カーソルをいちいち動かされるのは面倒
            //__instance.ResetListIndexSelected();
            selected.Clear();
            __result = true;
        }
    }

    public static bool SetInputStateHook(InputItemWindowWithTab __instance, InputState inputState, ref ItemListSelectionParam ___itemListSelectionParamCurrent)
    {
        if(inputState != InputState.MultiSelect)
            return true;

        int selected_id;
        SelectedItem t;

        selected_id = __instance.GetSelectionSelected();
        t = selected.Find(x => x.id == selected_id);
        //既に選択してあるアイテムをもう一度選択するとキャンセル
        if(t != null)
        {
            SoundId.Cancel.Play();
            selected.Remove(t);
            switch_check(__instance, t);
            return false;
        }
        SoundId.Select.Play();

        //強制的に全量選択
        t = new SelectedItem();
        t.id = selected_id;
        t.amount = ___itemListSelectionParamCurrent.GetItemCount();
        t.item = ___itemListSelectionParamCurrent.GetItem();
        t.item_param = __instance.GetSelectionParamSelected();
        //廃棄/売買不能アイテムは対象としない
        //Console.Write($"{t.id}: {t.item.IsDiscardable()}");
        if(!t.item.IsDiscardable() || !t.item.IsSellable())
            return false;
        selected.Add(t);
        switch_check(__instance, t);
        //Console.Write($"{t.id}: {t.item.DisplayName.Text}");
        return false;
    }

    /* 指定されたアイテムへのチェックの反転
     * s=nullで呼ばれた場合はチェックのつけられたアイテムすべてのチェックを外す
     */
    static void switch_check(InputItemWindowWithTab inst, SelectedItem s = null)
    {
        if(s != null)
        {
            if(s.item_param.GetTextStringMain().StartsWith("✓"))
                s.item_param.SetTextStringMain(s.item.DisplayName);
            else
                s.item_param.SetTextStringMain("✓" + s.item.DisplayName);
        }
        //nullで呼ばれたらすべてのチェックを外す
        else
            foreach(SelectedItem t in selected)
                t.item_param.SetTextStringMain(t.item.DisplayName);
        inst.UpdateSelectionParamList();
    }

    /* アイテムを売却/花力抽出
     * アイテムをデータ上減算するのみ
     */
    static void execute_items(ItemListDefines.SortInventoryType sortInventoryType)
    {
        foreach(SelectedItem t in selected)
        {
            //途中でアイテムの所持数などが変化してるかも
            //選択中でもAボタンで普通に売れるので
            if(!SessionInventoriesAccessorItemsParty.HasItemCurrentParty(t.item))
                continue;
            int current_amount = SessionInventoriesAccessorItemsParty.GetItemIdAllStackCountCurrentParty(t.item.Id);
            if(current_amount < t.amount)
                    t.amount = current_amount;

            if(sortInventoryType == ItemListDefines.SortInventoryType.Bag)
                SessionInventoriesAccessorItemsParty.DecreaseStackCountCurrentParty(t.item, t.amount);
            else if(sortInventoryType == ItemListDefines.SortInventoryType.Storage)
                SessionInventoriesAccessorItemsCommon.DecreaseStackCount(InventoryTypeCommonItem.Storage, t.item, t.amount);
            else
            {
                SoundId.Error.Play();
                Console.Write("[MultiItemSelect::execute_items]Inventory is not bag nor storage.");
                return;
            }

            if(shop_type != ShopType.Dispose)
                SessionInventoriesAccessorShop.AddItem(t.item.Id, t.amount);
            if(t.item_param.GetItemCount() == t.amount)
                Util.set_value(t.item_param, "itemCount", ItemListSelectionParam.ItemCountInvalid);
            else
                Util.set_value(t.item_param, "itemCount", t.item_param.GetItemCount() - t.amount);
        }
    }

    /* アイテムを倉庫に格納/倉庫から出す
     * アイテムをデータ上減算もする
     */
    static void move_items(ItemListDefines.SortInventoryType sortInventoryType)
    {
        foreach(SelectedItem t in selected)
        {
            if(sortInventoryType == ItemListDefines.SortInventoryType.Bag)
                SessionInventoriesAccessorItemsMisc.MoveItemPartyToCommonCurrentParty(InventoryTypePartyItem.Bag, InventoryTypeCommonItem.Storage, t.item, t.amount);
            else if(sortInventoryType == ItemListDefines.SortInventoryType.Storage)
                SessionInventoriesAccessorItemsMisc.MoveItemCommonToPartyCurrentParty(InventoryTypeCommonItem.Storage, InventoryTypePartyItem.Bag, t.item, t.amount);
            else
            {
                SoundId.Error.Play();
                UnityEngine.Debug.LogError("[MultiItemSelect::move_items()]Inventory is not bag nor storage.");
                return;
            }
            if(t.item_param.GetItemCount() == t.amount)
                Util.set_value(t.item_param, "itemCount", ItemListSelectionParam.ItemCountInvalid);
            else
                Util.set_value(t.item_param, "itemCount", t.item_param.GetItemCount() - t.amount);
        }
    }

    /* 最後に必要な処理いろいろ
     * アルゲン/花力の加算もここで行う
     */
    static void finalize()
    {
        int total_earn = 0;
        int current;
        if(shop_type == ShopType.Seller)
        {
            foreach(SelectedItem t in selected)
                total_earn += t.item.GetSellingPrice() * t.amount;
            SessionWalletAccessorPartyMoney.AddCurrentParty(total_earn);
            current = SessionWalletAccessorPartyMoney.GetAmountCurrentParty();
            moneyPurchaseWindow.SetMoney(PartyMoneyPurchaseWindow.MoneyType.Possession, current);
            SoundId.MoneyGain.Play();
        }
        else if(shop_type == ShopType.Extractor)
        {
            foreach(SelectedItem t in selected)
                total_earn += (int)t.item.CalcDungeonMakingResourceExtractPoint() * t.amount;
            Database.Session.DungeonMakingResources.AddResourcePoint(total_earn);
            current = Database.Session.DungeonMakingResources.GetResourcePoint();
            walletPanel.SetValue(PartyWalletPurchaseWindow.ValueType.Possession, current);
            SoundId.DungeonMakingResourceExtract.Play();
        }
        else if(shop_type == ShopType.Storage || shop_type == ShopType.Dispose)
        {
            SoundId.Submit.Play();
        }
        else
        {
            Console.Write("shop type is {0}.", shop_type);
        }
    }

    internal class SelectedItem
    {
        public int id, amount;
        public Item item;
        public ItemListSelectionParam item_param;
    }

    internal enum InputState
    {
        None,
        SelectItem,
        MessageSort,
        MultiSelect
    }

    internal enum ShopType
    {
        None,
        Seller,
        Extractor,
        Storage,
        Dispose
    }
}

}