#スクリプトコンパイラ/逆コンパイラ用の定義

#スクリプトで使用するコマンド
#0から300まで定義されているが、実際にゲーム内で使用されているのは257種でしかない
#逆コンパイル時にスクリプト内での引数使用例を拾っているのでコメントとして入れておく
#引数が複数種類のものは条件式か可変長引数と思われるが、詳細不明
#Experience.ScriptEvent.ScriptCommandId
command = {
    0: "_exit_script",
        #引数なし
    1: "_call_script",
        #String
    2: "_change_script",
        #String
    3: "_function",
        #未使用
    4: "_call_function",
        #未使用
    5: "_unload_all",
        #未使用
    6: "_if",
        #条件式
        #例：_if:!:ScriptFlag:flag(S28_00_00)
        #ExpressionValueType:ExpressionArgument
        #ExpressionInt:ExpressionOperator:ExpressionInt
        #ExpressionValueType:ExpressionOperator:ExpressionInt:ExpressionOperator:ExpressionValueType:ExpressionOperator:ExpressionInt
        #など
    7: "_elif",
        #未使用
        #_ifと同様であると思われる
    8: "_else",
        #引数なし
    9: "_endif",
        #引数なし
    10: "_set_lwork",
        #Int:ExpressionInt
        #Int:ExpressionValueType:ExpressionArgument
        #Int:ExpressionValueType:ExpressionArgument:ExpressionOperator:ExpressionInt
        #Int:ExpressionValueType:ExpressionOperator:ExpressionInt
        #Int:ExpressionValueType:ExpressionArgument:ExpressionArgument
        #Int:ExpressionValueType
        #Int:ExpressionInt:ExpressionOperator:ExpressionValueType:ExpressionArgument
        #Int:ExpressionInt:ExpressionOperator:ExpressionInt:ExpressionOperator:ExpressionInt
    11: "_set_gwork",
        #Int:ExpressionInt
        #Int:ExpressionValueType:ExpressionArgument
        #Int:ExpressionValueType
        #Int:ExpressionValueType:ExpressionArgument:ExpressionOperator:ExpressionInt
        #Int:ExpressionInt:ExpressionOperator:ExpressionValueType:ExpressionArgument
        #Int:ExpressionValueType:ExpressionArgument:ExpressionOperator:ExpressionValueType:ExpressionArgument
    12: "_wait_seconds",
        #Float
    13: "_wait_frames",
        #未使用
    14: "_wait_key",
        #引数なし
    15: "_wait_load_all",
        #引数なし
    16: "_wait_install_game",
        #引数なし
    17: "_set_scenario_title_text",
        #TextId
    18: "_clear_scenario_title",
        #引数なし
    19: "_set_scenario_message_speed",
        #Float
    20: "_set_scenario_message_duration",
        #Float
    21: "_message_scenario",
        #ScenarioWindowPositionType:TextId:Align
    22: "_message_scenario_line_align_left",
        #ScenarioWindowPositionType:TextId:Align
    23: "_message_scenario_narration",
        #ScenarioWindowPositionType:TextId:Align
    24: "_message_scenario_narration_line_align_left",
        #ScenarioWindowPositionType:TextId:Align
    25: "_hide_scenario",
        #引数なし
    26: "_message_common_window",
        #TextId
    27: "_hide_common_window",
        #引数なし
    28: "_message_radio",
        #Int
    29: "_wait_radio",
        #引数なし
    30: "_hide_radio",
        #引数なし
    31: "_start_selection",
        #引数なし
    32: "_set_selection_message",
        #Int:TextId
    33: "_show_selection",
        #引数なし
    34: "_show_selection_dev",
        #引数なし
    35: "_show_selection_yes_no",
        #引数なし
    36: "_show_selection_yes_no_dev",
        #引数なし
    37: "_decided_selection",
        #Int
    38: "_canceled_selection",
        #引数なし
    39: "_end_selection",
        #引数なし
    40: "_restart_selection",
        #引数なし
    41: "_back_selection",
        #Int
    42: "_start_riddle",
        #引数なし
    43: "_set_riddle_keyboard_default_text",
        #TextId
    44: "_set_riddle_keyboard_description",
        #TextId
    45: "_add_riddle_answer_text",
        #TextId
    46: "_clear_riddle_answer_text",
        #未使用
    47: "_show_riddle",
        #引数なし
    48: "_add_tutorial_text",
        #TextId
    49: "_show_tutorial",
        #引数なし
    50: "_set_flag_on",
        #ScriptFlagId
    51: "_set_flag_off",
        #ScriptFlagId
    52: "_set_event_wakeup_on",
        #String
    53: "_set_event_wakeup_off",
        #String
    54: "_set_event_icon",
        #String:MapSymbolType
    55: "_reset_event_icon",
        #String
    56: "_set_progress",
        #ExpressionInt
    57: "_set_money",
        #ExpressionInt
    58: "_add_money",
        #ExpressionInt
        #ExpressionInt:ExpressionOperator:ExpressionValueType:ExpressionArgument
        #ExpressionValueType:ExpressionArgument
    59: "_set_dungeon_making_resource",
        #ExpressionInt
    60: "_add_dungeon_making_resource",
        #未使用
    61: "_set_class_change_resource",
        #BaseClassId:ExpressionInt
    62: "_add_class_change_resource",
        #BaseClassId:ExpressionInt
    63: "_add_class_change_resource_all",
        #ExpressionInt
    64: "_set_class_careerup_resource",
        #未使用
    65: "_add_class_careerup_resource",
        #未使用
    66: "_set_item_enhance_cap",
        #ExpressionInt
    67: "_add_item_enhance_cap",
        #ExpressionInt
    68: "_set_item_level_cap_modify",
        #ExpressionInt
    69: "_add_item_level_cap_modify",
        #ExpressionInt
    70: "_set_enemy_level_modify_modify",
        #ExpressionInt
    71: "_add_enemy_level_modify_modify",
        #ExpressionInt
    72: "_set_enemy_journal_force_on",
        #EnemyData
    73: "_set_door_open",
        #未使用
    74: "_set_door_close",
        #未使用
    75: "_set_dungeon_entrance_on",
        #DungeonEntranceId
    76: "_set_dungeon_entrance_off",
        #DungeonEntranceId
    77: "_set_sector_luminance_level",
        #SectorData:LuminanceLevel
    78: "_reset_sector_luminance_level",
        #未使用
        #SectorData
    79: "_unlock_achievement",
        #AchievementData
    80: "_set_has_seen_prologue",
        #引数なし
    81: "_set_has_cleared_extra_scenario",
        #未使用
    82: "_set_has_notified_install_extra_scenario",
        #引数なし
    83: "_set_has_seen_title",
        #引数なし
    84: "_set_has_game_cleared_system_savedata",
        #引数なし
    85: "_set_game_clear",
        #引数なし
    86: "_add_item",
        #ItemInventoryType:Bool:ItemData:ExpressionValueType:ExpressionArgument
        #ItemInventoryType:Bool:ItemData:ExpressionInt
    87: "_add_item_lwork",
        #ItemInventoryType:Bool:Int:ExpressionValueType:ExpressionArgument
    88: "_add_item_gwork",
        #ItemInventoryType:Bool:Int:ExpressionInt
    89: "_add_item_confirmed",
        #未使用
    90: "_remove_item",
        #ItemInventoryType:ItemData:ExpressionInt
        #ItemInventoryType:ItemData:ExpressionValueType:ExpressionArgument
    91: "_remove_item_lwork",
        #未使用
    92: "_remove_item_gwork",
        #ItemInventoryType:Int:ExpressionInt
    93: "_start_item_list",
        #BelongingsInventoryType
    94: "_start_hero_making",
        #引数なし
    95: "_change_hp_percentage",
        #Int:Int:Bool
    96: "_change_mp_percentage",
        #Int:Int:Bool
    97: "_change_hp",
        #Int:Int:Bool
    98: "_change_mp",
        #Int:Int:Bool
    99: "_cure_ailment_all",
        #未使用
    100: "_change_party_hp_percentage",
        #Int:Bool
    101: "_change_party_mp_percentage",
        #Int:Bool
    102: "_change_party_hp",
        #Int:Bool
    103: "_change_party_mp",
        #Int:Bool
    104: "_cure_party_ailment_all",
        #引数なし
    105: "_leave_party",
        #パーティを課長一人にするコマンド
        #引数なし
    106: "_load_npc_bust",
        #NpcBustData
    107: "_wait_load_npc_bust",
        #未使用
    108: "_wait_load_npc_bust_all",
        #引数なし
    109: "_unload_npc_bust",
        #NpcBustData
    110: "_unload_npc_bust_all",
        #引数なし
    111: "_show_npc_bust",
        #NpcBustData:NpcFacialExpressionId:NpcBustPositionId:ImageShowType
    112: "_wait_show_npc_bust",
        #NpcBustData
    113: "_wait_show_npc_bust_all",
        #引数なし
    114: "_hide_npc_bust",
        #NpcBustData:ImageHideType
    115: "_hide_npc_bust_all",
        #ImageHideType
    116: "_wait_hide_npc_bust",
        #NpcBustData
    117: "_wait_hide_npc_bust_all",
        #引数なし
    118: "_change_face_npc_bust",
        #NpcBustData:NpcFacialExpressionId:Bool
        #表情変更コマンドだが、少し遅い
        #_hide_npc_bust -> _show_npc_bustなら一瞬で切り替えられる
    119: "_wait_change_face_npc_bust",
        #NpcBustData
    120: "_move_npc_bust",
        #未使用
    121: "_wait_move_npc_bust",
        #未使用
    122: "_wait_move_npc_bust_all",
        #未使用
    123: "_set_water_surface_effect_on",
        #引数なし
    124: "_set_water_surface_effect_off",
        #引数なし
    125: "_load_enemy_line",
        #Int:EnemyData:EnemyData:EnemyData
        #Int:EnemyData
        #Int:EnemyData:EnemyData
        #Int:EnemyData:EnemyData:EnemyData:EnemyData
    126: "_wait_load_enemy_line",
        #未使用
    127: "_wait_load_enemy_all",
        #引数なし
    128: "_unload_enemy_line",
        #Int
    129: "_unload_enemy_all",
        #引数なし
    130: "_wait_unload_enemy",
        #未使用
    131: "_set_enemy_position_offset",
        #Int:Int:Float:Float
    132: "_show_enemy",
        #Int:Int:EnemyAppearType:Bool:Bool
    133: "_show_enemy_line",
        #Int:EnemyAppearType:Bool:Bool
    134: "_wait_show_enemy",
        #Int:Int
    135: "_wait_show_enemy_line",
        #Int
    136: "_wait_show_enemy_all",
        #引数なし
    137: "_hide_enemy",
        #Int:Int:EnemyDisappearType
    138: "_hide_enemy_line",
        #Int:EnemyDisappearType
    139: "_hide_enemy_all",
        #EnemyDisappearType
    140: "_wait_hide_enemy",
        #Int:Int
    141: "_wait_hide_enemy_line",
        #Int
    142: "_wait_hide_enemy_all",
        #引数なし
    143: "_pause_enemy_on",
        #未使用
    144: "_pause_enemy_off",
        #未使用
    145: "_pause_enemy_line_on",
        #Int
    146: "_pause_enemy_line_off",
        #Int
    147: "_pause_enemy_all_on",
        #未使用
    148: "_pause_enemy_all_off",
        #未使用
    149: "_load_back_enemy",
        #EnemyGraphicData
    150: "_wait_load_back_enemy",
        #引数なし
    151: "_unload_back_enemy",
        #引数なし
    152: "_show_back_enemy",
        #EnemyAppearType
    153: "_wait_show_back_enemy",
        #引数なし
    154: "_hide_back_enemy",
        #EnemyDisappearType
    155: "_wait_hide_back_enemy",
        #引数なし
    156: "_load_background",
        #BackgroundData
    157: "_wait_load_background",
        #BackgroundData
    158: "_wait_load_background_all",
        #引数なし
    159: "_unload_background",
        #BackgroundData
    160: "_unload_background_all",
        #引数なし
    161: "_show_background",
        #BackgroundData:Float
    162: "_wait_show_background",
        #BackgroundData
    163: "_wait_show_background_all",
        #引数なし
    164: "_hide_background",
        #BackgroundData:Float
    165: "_hide_background_all",
        #Float
    166: "_wait_hide_background",
        #BackgroundData
    167: "_wait_hide_background_all",
        #引数なし
    168: "_load_image",
        #EventImageData
    169: "_wait_load_image",
        #未使用
    170: "_wait_load_image_all",
        #引数なし
    171: "_unload_image",
        #EventImageData
    172: "_unload_image_all",
        #引数なし
    173: "_show_image",
        #EventImageData:Float:Float:ImageShowType
    174: "_wait_show_image",
        #EventImageData
    175: "_wait_show_image_all",
        #引数なし
    176: "_hide_image",
        #EventImageData:ImageHideType
    177: "_hide_image_all",
        #ImageHideType
    178: "_wait_hide_image",
        #EventImageData
    179: "_wait_hide_image_all",
        #引数なし
    180: "_move_image",
        #EventImageData:Float:Float:Float
    181: "_wait_move_image",
        #EventImageData
    182: "_wait_move_image_all",
        #未使用
    183: "_load_cev",
        #CevData
    184: "_wait_load_cev",
        #未使用
    185: "_wait_load_cev_all",
        #引数なし
    186: "_unload_cev",
        #CevData
    187: "_unload_cev_all",
        #引数なし
    188: "_show_cev",
        #CevData:Float:Float:ImageShowType
    189: "_show_cev_position_id",
        #CevData:CevPositionId:ImageShowType
    190: "_wait_show_cev",
        #CevData
    191: "_wait_show_cev_all",
        #引数なし
    192: "_hide_cev",
        #CevData:ImageHideType
    193: "_hide_cev_all",
        #ImageHideType
    194: "_wait_hide_cev",
        #CevData
    195: "_wait_hide_cev_all",
        #引数なし
    196: "_move_cev",
        #CevData:Float:Float:Float
    197: "_move_cev_position_id",
        #未使用
    198: "_wait_move_cev",
        #CevData
    199: "_wait_move_cev_all",
        #未使用
    200: "_set_cev_facility_unload_off",
        #未使用
    201: "_load_effect",
        #EffectData
    202: "_wait_load_effect",
        #EffectData
    203: "_wait_load_effect_all",
        #未使用
    204: "_unload_effect",
        #EffectData
    205: "_unload_effect_all",
        #引数なし
    206: "_play_effect",
        #EffectData:GraphicsSortOrderId:Float:Float:Bool
    207: "_play_effect_enemy",
        #EffectData:GraphicsSortOrderId:Int:Int:Bool
    208: "_wait_play_effect",
        #EffectData
    209: "_wait_play_effect_all",
        #未使用
    210: "_pause_effect",
        #未使用
    211: "_resume_effect",
        #未使用
    212: "_stop_effect",
        #EffectData
    213: "_stop_effect_all",
        #未使用
    214: "_play_dungeon_ambient_effect",
        #引数なし
    215: "_stop_dungeon_ambient_effect",
        #引数なし
    216: "_set_effect_skip_on",
        #EffectData
    217: "_play_bgm",
        #MusicResourceData:Float
    218: "_play_dungeon_bgm",
        #Float
    219: "_stop_bgm",
        #Float(duration)
    220: "_wait_stop_bgm",
        #引数なし
    221: "_play_sound",
        #SoundResourceData
    222: "_play_dungeon_ambient",
        #引数なし
    223: "_wait_play_sound",
        #SoundResourceData
    224: "_wait_play_sound_all",
        #引数なし
    225: "_wait_play_se_all",
        #未使用
    226: "_wait_play_ambient_all",
        #引数なし
    227: "_wait_play_voice_all",
        #引数なし
    228: "_stop_sound",
        #SoundResourceData:Float(Duration)
    229: "_stop_sound_all",
        #未使用
    230: "_stop_se_all",
        #Float
    231: "_stop_ambient_all",
        #Float
    232: "_stop_voice_all",
        #Float
    233: "_play_video",
        #VideoResourceData
    234: "_wait_play_video",
        #引数なし
    235: "_stop_video",
        #Float
    236: "_setup_battle_dungeon_random",
        #引数なし
    237: "_setup_battle_dungeon_confirmed",
        #ConfirmedEncounterData
    238: "_setup_battle_city",
        #CityEncounterData
    239: "_set_battle_background",
        #BackgroundData
    240: "_set_battle_background_default",
        #未使用
    241: "_set_battle_bgm",
        #MusicResourceData
    242: "_set_battle_result_bgm",
        #MusicResourceData
    243: "_set_battle_result_bgm_default",
        #引数なし
    244: "_set_battle_result_bgm_none",
        #引数なし
    245: "_set_battle_result_bgm_not_change",
        #引数なし
    246: "_set_battle_encounter_se_on",
        #引数なし
    247: "_set_battle_encounter_se_off",
        #未使用
    248: "_set_battle_encounter_effect",
        #TransitionType
    249: "_set_battle_confirmed_drop",
        #ConfirmedDropData
    250: "_set_battle_light_level",
        #LuminanceLevel
    251: "_set_battle_annihilate",
        #AfterAnnihilatedType
    252: "_set_battle_gameover_on",
        #引数なし
    253: "_set_battle_gameover_off",
        #引数なし
    254: "_set_battle_treasurebox_on",
        #引数なし
    255: "_set_battle_treasurebox_off",
        #引数なし
    256: "_set_battle_treasurebox_trap_on",
        #引数なし
    257: "_set_battle_treasurebox_trap_off",
        #引数なし
    258: "_set_battle_escape_player_on",
        #引数なし
    259: "_set_battle_escape_player_off",
        #引数なし
    260: "_set_battle_escape_enemy_on",
        #未使用
    261: "_set_battle_escape_enemy_off",
        #引数なし
    262: "_set_battle_restore_last_battle_condition_on",
        #引数なし
    263: "_set_battle_restore_last_battle_condition_off",
        #引数なし
    264: "_start_battle",
        #引数なし
    265: "_move_event",
        #引数なし
    266: "_move_gameover",
        #未使用
    267: "_move_city",
        #FacilityId
        #Enum: 0:全景, 1:基地テント, 2:融合炉, 3:倉庫テント, 4:住居テント, 5:迷宮ゲート
    268: "_cancel_enter_dungeon",
        #未使用
    269: "_move_dungeon",
        #SectorData:Int:Int:DirectionType
    270: "_move_in_dungeon",
        #SectorData:Int:Int:DirectionType
    271: "_move_party",
        #DirectionType
    272: "_turn_party",
        #DirectionType
    273: "_quest_arise",
        #QuestData
    274: "_quest_end",
        #QuestData:Bool
    275: "_move_camera",
        #Float:Float:Float:Float
    276: "_reset_move_camera",
        #Float
    277: "_wait_move_camera",
        #引数なし
    278: "_change_camera_height",
        #Float:Float:Bool
    279: "_change_camera_height_enemy",
        #EnemyData:Int:Float:Bool
    280: "_wait_change_camera_height",
        #引数なし
    281: "_focus_camera",
        #Int:Int:Float:Float
    282: "_reset_focus_camera",
        #Float
    283: "_wait_focus_camera",
        #引数なし
    284: "_shake_camera",
        #Float:Float:Float
    285: "_shake_camera_loop",
        #Float:Float
    286: "_wait_shake_camera",
        #引数なし
    287: "_stop_shake_camera",
        #Float
    288: "_blur_on",
        #Float:Float
    289: "_blur_off",
        #Bool
    290: "_set_screen_color",
        #String:Float:Float
    291: "_reset_screen_color",
        #Float
    292: "_wait_set_screen_color",
        #引数なし
    293: "_show_scenario_back_mask",
        #引数なし
    294: "_wait_show_scenario_back_mask",
        #引数なし
    295: "_hide_scenario_back_mask",
        #引数なし
    296: "_wait_hide_scenario_back_mask",
        #引数なし
    297: "_fade_out",
        #String:Float(duration):GraphicsSortOrderId:Int
    298: "_fade_in",
        #Float(duration):Int(fadeSlotNumber:0～3)
    299: "_wait_fade",
        #引数なし
    300: "_show_epilogue_character_list",
        #TextId:Float
    301: "_excmd",
        #LoYUtilMod.ExternalCommandで追加したユーザー定義コマンド
        #_excmd:"FunctionName":param1:param2:...
        #実際の呼び出しにはFunctionNameで定義した関数に
        #object(ScriptCommandBinder)とScriptCommandを引数に呼ぶ
        #ここでScriptCommandは"FunctionName"を取り除いて引数に積んである
}


#Experience.ScriptEvent.ParameterDefines.ParameterType
parameter_t = {
    0: "String",
    1: "Bool",
    2: "Int",
    3: "Float",
    4: "Expression",
        #未使用のため詳細不明
    5: "OperatorType",
        #未使用のため詳細不明
    6: "TextId",
    7: "Align",
    8: "ScriptFlagId",
    9: "ImageShowType",
        #0: 瞬時, 1:フェード通常
    10: "ImageHideType",
        #0: 瞬時, 1:フェード通常
    11: "BackgroundData",
    12: "NpcBustData",
    13: "NpcFacialExpressionId",
        #0～15まででそれぞれ通常, 笑み, 驚き, 怒り, 嘲り, 苦痛, 呆け, ごまかし, 大笑, 泣き, 疑念, 真剣, 蔑み, 興奮, 出血笑み, 出血驚き
        #キャラによっては存在しない表情もあるため、NpcBustDataTableを参照したほうが良い
    14: "NpcBustPositionId",
        #0固定
    15: "EventImageData",
    16: "CevData",
        #立ち絵ID
        #0:None, 1:久世戸, 2:久世戸with触手, 3:ルキ最終形態, 4:ルキ初期型, 5:ルキver2, 6:ルキ(頭蓋骨), 7:ルキの車椅子だけ, 8:社長(帽子あり), 9:社長(帽子なし), 10:飯場, 11:灰十字, 12:荒堀
    17: "CevPositionId",
        #立ち絵表示位置
        #0:Center, 1:Left, 2:Right, 3:C_Left, 4:C_Right
    18: "EnemyData",
    19: "EnemyGraphicData",
    20: "EnemyAppearType",
    21: "EnemyDisappearType",
    22: "MusicResourceData",
    23: "SoundResourceData",
    24: "VideoResourceData",
    25: "EffectData",
    26: "FacilityId",
    27: "ItemData",
    28: "DungeonId",
    29: "SectorData",
    30: "DungeonEntranceId",
    31: "MapSymbolType",
    32: "QuestData",
    33: "QuestState",
    34: "ConfirmedEncounterData",
    35: "CityEncounterData",
    36: "ConfirmedDropData",
    37: "ItemInventoryType",
    38: "DirectionType",
    39: "GraphicsSortOrderId",
    40: "ScenarioWindowPositionType",
    41: "LuminanceLevel",
    42: "TransitionType",
    43: "BaseClassId",
    44: "AchievementData",
    45: "AfterAnnihilatedType",
    46: "BelongingsInventoryType",
    47: "AdditionalContentsId",
    48: "ExpressionInvalid",
        #未使用のため詳細不明
    49: "ExpressionOperator",
        #比較演算用比較演算子？下記operator参照
    50: "ExpressionValueType",
        #比較用関数？下記expval_t参照
    51: "ExpressionArgument",
        #ExpressionValueType用の引数っぽい
    52: "ExpressionInt",
        #比較
}


#C#のTypeCode
#事実上使わない
raw_t = {
    0: "Empty",
    1: "Object",
    2: "DBNull",
    3: "Boolean",
    4: "Char",
    5: "SByte",
    6: "Byte",
    7: "Int16",
    8: "UInt16",
    9: "Int32",
    10: "UInt32",
    11: "Int64",
    12: "UInt64",
    13: "Single",
    14: "Double",
    15: "Decimal",
    16: "DateTime",
    #失われたTypeCode17についてはStackOverflowに記述を発見
    #https://stackoverflow.com/questions/7329834/what-happened-to-system-typecode-of-value-17
    18: "String",
}


#Experience.ScriptEvent.OperatorType
operator = {
    0: "!",
    1: "*",
    2: "/",
    3: "%",
    4: "+",
    5: "-",
    6: "<",
    7: "<=",
    8: ">",
    9: ">=",
    10: "!=",
    11: "=",
    12: "&",
    13: "|"
}


#Experience.ScriptEvent.ScriptExpressionDecoder.GetValue()に実際の処理が書かれている
#引数としてExpressionArgumentを取る関数
#参考:Experience.ScriptEvent.ExpressionDefines
#Experience.ScriptEvent.ExpressionValueType
expval_t = {
    0: "None",
            #何もせず0を返す
    1: "RandomMax",
            #引数を最大値としたゼロ以上の整数を返す
            #引数：int
    2: "RandomDice",
            #count回、絶対値side個の面を持つダイスを振り、結果にmodifierを加算する
            #count==0ならダイスは振らず、side<0の場合は結果はマイナスとなる
            #いずれにせよ最終的にmodifierは加算される
            #引数：int(count), int(side), int(modifier)
    3: "GlobalWork",
            #GlobalWork（グローバル変数？）を返す
            #GlobalWorkのサイズはScriptEvent.ScriptConsts参照
            #引数：int(GlobalWorkIndex)
    4: "LocalWork",
            #LocalWork（ローカル変数？）を返す
            #LocalWorkのサイズはScriptEvent.ScriptConsts参照
            #引数：int(LocalWorkIndex)
    5: "EventWakeUp",
            #イベント終了フラグの反転したもの=イベント未了フラグを返すっぽい
            #引数：string（eventName？）
    6: "ScriptFlag",
            #フラグ(flags)がオンかオフかを返す
            #引数：Experience.ScriptEvent.ScriptFlagId
    7: "Progress",
            #ゲームの進行状況IDを返す
            #以下はスクリプト内で_set_progressされたIDとその時にセットされたフラグ
            #01:【導入】プロローグを見た(S01_00_00)
            #02:【導入】飯場に最初の報告をした(S01_01_05)
            #03:【導入】飯場に第二キャンプの報告をした(S02_01_02)
            #04:【導入】ゲートを開くのに失敗した(S03_00_01)
            #05:【処刑人】カサンドラのアドバイスを聞いた(S05_02_00)
            #06:()
            #07:【処刑人】1個目の遺物を捧げた（ハシゴ）(ARTIFACT01)
            #08:()
            #09:【処刑人】2個目の遺物を捧げた（牢のカギ）(ARTIFACT02)
            #10:【処刑人】久世戸ラジオ2回目を聞いた(S09_01_00)
            #11:【処刑人】飯場からの救援要請を聞いた(S16_00_00)
            #12:【処刑人】襲撃を撃退した(S16_02_00)
            #13:【処刑人】3個目の遺物を捧げた（森のカギ）(ARTIFACT03)
            #14:()
            #15:【処刑人】4個目の遺物を捧げた（イヤシ）(ARTIFACT04)
            #16:()
            #17:【処刑人】5個目の遺物を捧げた（マモノケシ）(ARTIFACT05)
            #18:【処刑人】赤ルキから採血した(S21_03_00)
            #19:【処刑人】ルキを正気に戻した(S22_01_00)
            #20:()
            #21:【処刑人】6個目の遺物を捧げた（城のカギ）(ARTIFACT06)
            #22:()
            #23:【処刑人】7個目の遺物を捧げた（カケハシ）(ARTIFACT07)
            #24:()
            #25:【処刑人】8個目の遺物を捧げた（マモノ）(ARTIFACT08)
            #26:【処刑人】9個目の遺物を捧げた（黄泉）(ARTIFACT09)
            #27:()
            #28:【処刑人】黄泉ヲ裂ク華を使って脱出した(S26_00_01)
            #29:()
            #30:【折返し】頭蓋骨で融合炉が復活した(S28_02_00)
            #31:邦人子宮に入った(DUNENTER_10)
            #32:０行区西に入った(DUNENTER_11)
            #33:()
            #34:異人子宮に入った(DUNENTER_12)
            #35:()
            #36:【少女復活】カサンドラを虚無空間で助けた(S34_00_01)
            #37:ルキが復活した(LUKI_REVIVAL)
            #38:拡張版が適用されていない状態で久世戸を倒した(DLC_ENDING_NOTAPP)
            #39:【少女復活】ラスボスと戦った（負けた時含む）(S38_01_00)
            #40:エンディング（クレジット）を見た(ENDING)
            #41:【クリア後】住居テントで灰十字の伝言を聞いた(S41_00_00)
            #42:()
            #43:ルキの森に入った(DUNENTER_17)
            #44:【クリア後】灰十字を保護した(S43_00_00)
            #45:狂王の城に入った(DUNENTER_18)
            #46:()
            #47:【クリア後】飯場にキワミの花のことを報告した(S45_01_02)
            #48:()
            #49:エンディング２（裏ボス撃破）を見た(ENDING2)
    8: "QuestStateId",
            #クエストの進行状況IDを返す
            #引数：Experience.Quests.QuestState
    9: "QuestState",
            #指定したクエストの進行状況IDを返す
            #上記QuestStateIdと合わせて以下のように使用する
            #_if:QuestState:[ID]:=:QuestStateId:[State]
            #引数：int(クエストID?)
    10: "PartyMemberCount",
            #パーティの人数を返す
    11: "PartyAnihilated",
            #パーティが全滅したかどうかを返す
    12: "PlayerLevel",
            #パーティのn番目のキャラクターのレベルを返す
            #引数：int(n)
    13: "PlayerLevelMax",
            #パーティメンバーの中での最大レベルを返す
    14: "PlayerLevelAverage",
            #パーティの平均レベルを返す
    15: "IsPlayerLeaderHpMax",
            #課長のHPが全快かどうかを返す
    16: "ItemId",
            #アイテムIDを返す
            #引数：int(アイテムID)
    17: "ItemCount",
            #指定アイテムの個数を返す
            #引数：Experience.ScriptEvent.ItemInventoryType, int(アイテムID)
    18: "IsItemRecorded",
            #アイテムが図鑑に登録されているかを返す
            #引数：int(アイテムID)
    19: "IsItemAcquired",
            #IsItemRecordedと全く同じ処理
            #引数：int(アイテムID)
    20: "IsItemListDecided",
            #アイテムが選択されたかどうかを返す
    21: "ItemListDecidedItemId",
            #選択されたアイテムIDを返す
    22: "IsItemListDecidedDiscardable",
            #選択されたアイテムが破棄可能かを返す
    23: "BagEmptyCount",
            #バッグインベントリの空き容量を返す
    24: "StorageEmptyCount",
            #倉庫インベントリの空き容量を返す
    25: "DungeonId",
            #ダンジョンIDを返す
            #引数：Experience.Dungeons.DungeonId
    26: "DungeonIdCurrent",
            #現在地点のダンジョンIDを返す
    27: "SectorId",
            #セクターIDを返す
            #引数：int
    28: "SectorIdCurrent",
            #現在地点のセクターIDを返す
    29: "BlockPositionX",
            #現在地点のX座標を返す
    30: "BlockPositionY",
            #現在地点のY座標を返す
    31: "IsInBlock",
            #指定した座標にいるかどうかを返す
            #引数：int(X), int(Y)
    32: "IsDoorOpened",
            #ドアの開閉フラグを返す
            #引数：int(セクターID), int(ドアのインデックス番号)
    33: "Money",
            #パーティの所持金を返す
    34: "DungeonMakingResource",
            #パーティの所持花力を返す
    35: "BaseClassChangeResource",
            #おそらく現在は破棄された仕様であると思われる、クラス変更ポイント？を返す
            #Experience.Characters.ClassIdなどなかなか趣深い物がある
            #聖備工とかいい名前だと思うんだが、氣爆工とは？？？
    36: "ClassCareerUpResource",
            #同じく現在は破棄された仕様であると思われる、キャリアアップポイント？を返す
            #当初は上級職はスペシャリスト/ジェネラリストだったようだ
    37: "ItemEnhanceCap",
            #アイテム強化最大レベルを返す
            #Experience.Items.Itemで最大0～99と定義されている
    38: "ItemLevelCapModify",
            #ドロップアイテムレベルの最大値に関する係数？
            #Experience.ScriptEvent.ScriptConstsで最大-9999～9999と定義されている
    39: "PlanModifyModify",
            #謎係数
            #ランダムエンカウントの敵レベルの決定に関与していることが判明している
            #Experience.ScriptEvent.ScriptConstsで最大-9999～9999と定義されている
    40: "EventRiddleDecidedCorrectAnswer",
            #謎解きに対して正しい答えを選択したか
    41: "EventRiddleCanceled",
            #謎解きで答えを選択せずにキャンセルしたか
    42: "IsLastBattleEscaped",
            #直前の戦闘で逃げたかどうか
    43: "IsLastBattleAnnihilated",
            #直前の戦闘に敗北したかどうか
    44: "IsInCityMapByAnnihilated",
            #キャンプにいる理由が全滅したためかどうか
    45: "HasSeenPrologue",
            #プロローグを観たことがあるかどうか？
    46: "HasClearedExtraScenario",
            #やりこみDLCをクリアしたかどうか？
    47: "HasNotifiedInstallExtraScenario",
            #やりこみDLCインストールの表示を観たことがあるかどうか？
    48: "HasSeenTitle",
            #タイトル画面を観たことがあるかどうか
    49: "HasGameCleared",
            #ベースゲームをクリアしたことがあるかどうか
    50: "IsFinishedInstallGame",
            #ゲームのインストールが完了したかどうか？
    51: "IsInstalledAdditionalContents",
            #DLC(追加シナリオ、ポートレート)を導入しているかどうか
            #引数：Experience.Game.AdditionalContentsId
            #0:なし, 1:やりこみDLC, 2:ポートレート学園, 3:ポートレート死印
}


#Experience.ScriptEvent.ScriptFlagId
flags = {
    0: "DUMMY",    #ダミーフラグ。エラーがあった時などはこのフラグが参照される
    1: "NEVER",    #常にFALSE（テーブル用、変更禁止）
    2: "ALWAYS",    #常にTRUE（テーブル用、変更禁止）
    3: "GAMEOVER_ON",    #全滅時に必ずゲームオーバーになる（キカンの花は使えない）
    4: "MUST_DOPING_ON",    #マストドーピングを使用可能であるか
    5: "FACILITY_COMMAND_BUY",    #購入
    6: "FACILITY_COMMAND_SELL",    #売却
    7: "FACILITY_COMMAND_ITEM_ENHANCE",    #アイテム強化
    8: "FACILITY_COMMAND_DUNGEON_MAKING",    #ダンジョンメイキング用アイテム
    9: "DUNGEON_UNLOCK_TUNNEL",    #ダンジョンメイキング用アイテム
    10: "DUNGEON_UNLOCK_CASTLE",    #ダンジョンメイキング用アイテム
    11: "DUNGEON_UNLOCK_FOREST",    #ダンジョンメイキング用アイテム
    12: "DUNGEON_UNLOCK_SHIRINE",    #ダンジョンメイキング用アイテム
    13: "DUNGEON_INSTANT_RESOURCE_LADDER",    #ダンジョンメイキング用アイテム
    14: "DUNGEON_INSTANT_RESOURCE_BRIDGE",    #ダンジョンメイキング用アイテム
    15: "DUNGEON_INSTANT_RESOURCE_GATE",    #ダンジョンメイキング用アイテム
    16: "DUNGEON_INSTANT_RESOURCE_RECOVERY",    #ダンジョンメイキング用アイテム
    17: "DUNGEON_INSTANT_RESOURCE_ENEMY",    #ダンジョンメイキング用アイテム
    18: "DUNGEON_INSTANT_RESOURCE_BANISH",    #ダンジョンメイキング用アイテム
    19: "DUNGEON_INSTANT_RESOURCE_SWITCH_001",    #ダンジョンメイキング用アイテム
    20: "DUNGEON_INSTANT_RESOURCE_SWITCH_002",    #ダンジョンメイキング用アイテム
    21: "DUNGEON_INSTANT_RESOURCE_SWITCH_003",    #ダンジョンメイキング用アイテム
    22: "DUNGEON_INSTANT_RESOURCE_SWITCH_004",    #ダンジョンメイキング用アイテム
    23: "TEST_HERO_CREATED",    #ダンジョンメイキング用アイテム
    24: "TEST_SHOP_FIRST_DONE",    #ダンジョンメイキング用アイテム
    25: "TEST_COMPANY_FIRST_DONE",    #ダンジョンメイキング用アイテム
    26: "DUNGEON_INSTANT_RESOURCE_RESERVE",    #ダンジョンメイキング用リザーブ
    27: "TEST_0001",    #ダンジョンメイキング用リザーブ
    28: "TEST_0002",    #ダンジョンメイキング用リザーブ
    29: "TEST_0003",    #ダンジョンメイキング用リザーブ
    30: "TEST_0004",    #ダンジョンメイキング用リザーブ
    31: "TEST_0005",    #ダンジョンメイキング用リザーブ
    32: "TEST_0006",    #ダンジョンメイキング用リザーブ
    33: "TEST_0007",    #ダンジョンメイキング用リザーブ
    34: "TEST_0008",    #ダンジョンメイキング用リザーブ
    35: "TEST_0009",    #ダンジョンメイキング用リザーブ
    36: "TEST_0010",    #ダンジョンメイキング用リザーブ
    37: "TEST_0011",    #ダンジョンメイキング用リザーブ
    38: "TEST_QUEST_LOG_0001_01",    #ダンジョンメイキング用リザーブ
    39: "TEST_QUEST_LOG_0001_02",    #ダンジョンメイキング用リザーブ
    40: "TEST_QUEST_LOG_0001_03",    #ダンジョンメイキング用リザーブ
    41: "TEST_QUEST_LOG_0001_04",    #ダンジョンメイキング用リザーブ
    42: "TEST_QUEST_LOG_0001_05",    #ダンジョンメイキング用リザーブ
    43: "TEST_QUEST_LOG_0001_06",    #ダンジョンメイキング用リザーブ
    44: "TEST_QUEST_LOG_0001_07",    #ダンジョンメイキング用リザーブ
    45: "TEST_QUEST_LOG_0001_08",    #ダンジョンメイキング用リザーブ
    46: "TEST_QUEST_LOG_0001_09",    #ダンジョンメイキング用リザーブ
    47: "TEST_QUEST_LOG_0001_10",    #ダンジョンメイキング用リザーブ
    48: "TEST_QUEST_LOG_0002_01",    #ダンジョンメイキング用リザーブ
    49: "TEST_QUEST_LOG_0002_02",    #ダンジョンメイキング用リザーブ
    50: "TEST_QUEST_LOG_0002_03",    #ダンジョンメイキング用リザーブ
    51: "TEST_QUEST_LOG_0003_07",    #ダンジョンメイキング用リザーブ
    52: "TEST_QUEST_LOG_0003_08",    #ダンジョンメイキング用リザーブ
    53: "TEST_QUEST_LOG_0003_09",    #ダンジョンメイキング用リザーブ
    54: "DEBUG_ON",    #ONだとデバッグ用イベント発生
    55: "HIDENPC_BASE",    #ONだと基地テントのNPCを非表示にする
    56: "HIDENPC_REACTOR",    #ONだと融合炉のNPCを非表示にする
    57: "HIDENPC_LIVING",    #ONだと住居テントのNPCを非表示にする
    58: "HIDENPC_STORAGE",    #ONだと倉庫テントのNPCを非表示にする
    59: "HIDENPC_ENTRANCE",    #ONだと迷宮ゲートのNPCを非表示にする
    60: "HIDENPC_CAMP",    #ONだと全景のNPCを非表示にする
    61: "RANDOM_ENCOUNTER_OFF",    #フラグが立っている間はランダムエンカウントが発生しなくなる
    62: "RAGE_EVENTENEMY",    #ONの間、ランダムエンカウントで赤ルキが襲撃してくる
    63: "ENEMY_DISABLE_PLAN_MODIFY",    #エネミーのLVに企画補正を適用しなくする
    64: "FACILITY_COMMAND_PLAYER_SELECT",    #登録
    65: "FACILITY_COMMAND_PLAYER_MAKING",    #編成
    66: "FACILITY_COMMAND_PLAYER_CLASSCHANGE",    #転職
    67: "FACILITY_COMMAND_PLAYER_CAREERUP",    #昇進
    68: "FACILITY_COMMAND_ITEM",    #物資
    69: "TUTORIAL_BATTLE_SWITCHBOOST",    #スイッチブーストのチュートリアル戦闘用フラグ
    70: "DUNGEON_MAKING_DEBUT",    #ダンジョンメイキングをしたことがある
    71: "TUTORIAL_BATTLE_TREASURETRAP",    #宝箱の罠のチュートリアル用フラグ
    72: "FLOWER_NORETURN",    #キカンの花＆オオトビラの花が使えなくなるフラグ
    73: "GAMEOVER_ON2",    #全滅時に必ずゲームオーバーになる（キカンの花は使える）
    74: "DLC_STORY_ENTRY",    #拡張版のシナリオ入り口を表示する。
    75: "DLC_BEFORE_APP",    #拡張版を適用する前にゲームを開始した。
    76: "SYS_RE22",    #システム系リザーブ22
    77: "SYS_RE23",    #システム系リザーブ23
    78: "SYS_RE24",    #システム系リザーブ24
    79: "SYS_RE25",    #システム系リザーブ25
    80: "SYS_RE26",    #システム系リザーブ26
    81: "SYS_RE27",    #システム系リザーブ27
    82: "SYS_RE28",    #システム系リザーブ28
    83: "SYS_RE29",    #システム系リザーブ29
    84: "SYS_RE30",    #システム系リザーブ30
    85: "SYS_RE31",    #システム系リザーブ31
    86: "SYS_RE32",    #システム系リザーブ32
    87: "SYS_RE33",    #システム系リザーブ33
    88: "SYS_RE34",    #システム系リザーブ34
    89: "SYS_RE35",    #システム系リザーブ35
    90: "SYS_RE36",    #システム系リザーブ36
    91: "SYS_RE37",    #システム系リザーブ37
    92: "SYS_RE38",    #システム系リザーブ38
    93: "SYS_RE39",    #システム系リザーブ39
    94: "SYS_RE40",    #システム系リザーブ40
    95: "SYS_RE41",    #システム系リザーブ41
    96: "SYS_RE42",    #システム系リザーブ42
    97: "SYS_RE43",    #システム系リザーブ43
    98: "SYS_RE44",    #システム系リザーブ44
    99: "SYS_RE45",    #システム系リザーブ45
    100: "SYS_RE46",    #システム系リザーブ46
    101: "SYS_RE47",    #システム系リザーブ47
    102: "SYS_RE48",    #システム系リザーブ48
    103: "SYS_RE49",    #システム系リザーブ49
    104: "SYS_RE50",    #システム系リザーブ50
    105: "LIGHTHUNT_01",    #MAP01のライトハント終了
    106: "LIGHTHUNT_02",    #MAP02のライトハント終了
    107: "LIGHTHUNT_03",    #MAP03のライトハント終了
    108: "LIGHTHUNT_04",    #MAP04のライトハント終了
    109: "LIGHTHUNT_05",    #MAP05のライトハント終了
    110: "LIGHTHUNT_06",    #MAP06のライトハント終了
    111: "LIGHTHUNT_07",    #MAP07のライトハント終了
    112: "LIGHTHUNT_08",    #MAP08のライトハント終了
    113: "LIGHTHUNT_09",    #MAP09のライトハント終了
    114: "LIGHTHUNT_10",    #MAP10のライトハント終了
    115: "LIGHTHUNT_11",    #MAP11のライトハント終了
    116: "LIGHTHUNT_12",    #MAP12のライトハント終了
    117: "LIGHTHUNT_13",    #MAP13のライトハント終了
    118: "LIGHTHUNT_14",    #MAP14のライトハント終了
    119: "LIGHTHUNT_15",    #MAP15のライトハント終了
    120: "LIGHTHUNT_16",    #MAP16のライトハント終了
    121: "LIGHTHUNT_17",    #MAP17のライトハント終了
    122: "LIGHTHUNT_18",    #MAP18のライトハント終了
    123: "LIGHTHUNT_19",    #MAP19のライトハント終了
    124: "LIGHTHUNT_20",    #MAP20のライトハント終了
    125: "LIGHTHUNT_21",    #MAP21のライトハント終了
    126: "LIGHTHUNT_22",    #MAP22のライトハント終了
    127: "LIGHTHUNT_23",    #MAP23のライトハント終了
    128: "LIGHTHUNT_24",    #MAP24のライトハント終了
    129: "LIGHTHUNT_25",    #MAP25のライトハント終了
    130: "LIGHTHUNT_26",    #MAP26のライトハント終了
    131: "LIGHTHUNT_27",    #MAP27のライトハント終了
    132: "LIGHTHUNT_28",    #MAP28のライトハント終了
    133: "LIGHTHUNT_29",    #MAP29のライトハント終了
    134: "LIGHTHUNT_30",    #MAP30のライトハント終了
    135: "LIGHTHUNT_31",    #MAP31のライトハント終了
    136: "LIGHTHUNT_32",    #MAP32のライトハント終了
    137: "LIGHTHUNT_33",    #MAP33のライトハント終了
    138: "LIGHTHUNT_34",    #MAP34のライトハント終了
    139: "LIGHTHUNT_35",    #MAP35のライトハント終了
    140: "LIGHTHUNT_36",    #MAP36のライトハント終了
    141: "LIGHTHUNT_37",    #MAP37のライトハント終了
    142: "LIGHTHUNT_38",    #MAP38のライトハント終了
    143: "LIGHTHUNT_39",    #MAP39のライトハント終了
    144: "LIGHTHUNT_40",    #MAP40のライトハント終了
    145: "LIGHTHUNT_41",    #MAP41のライトハント終了
    146: "LIGHTHUNT_42",    #MAP42のライトハント終了
    147: "LIGHTHUNT_43",    #MAP43のライトハント終了
    148: "LIGHTHUNT_44",    #MAP44のライトハント終了
    149: "LIGHTHUNT_45",    #MAP45のライトハント終了
    150: "LIGHTHUNT_46",    #MAP46のライトハント終了
    151: "LIGHTHUNT_47",    #MAP47のライトハント終了
    152: "LIGHTHUNT_48",    #MAP48のライトハント終了
    153: "LIGHTHUNT_49",    #MAP49のライトハント終了
    154: "LIGHTHUNT_50",    #MAP50のライトハント終了
    155: "LIGHTHUNT_51",    #MAP51のライトハント終了
    156: "LIGHTHUNT_52",    #MAP52のライトハント終了
    157: "LIGHTHUNT_53",    #MAP53のライトハント終了
    158: "LIGHTHUNT_54",    #MAP54のライトハント終了
    159: "LIGHTHUNT_55",    #MAP55のライトハント終了
    160: "LIGHTHUNT_56",    #MAP56のライトハント終了
    161: "LIGHTHUNT_57",    #MAP57のライトハント終了
    162: "LIGHTHUNT_58",    #MAP58のライトハント終了
    163: "LIGHTHUNT_59",    #MAP59のライトハント終了
    164: "LIGHTHUNT_60",    #MAP60のライトハント終了
    165: "LIGHTHUNT_61",    #MAP61のライトハント終了
    166: "LIGHTHUNT_62",    #MAP62のライトハント終了
    167: "LIGHTHUNT_63",    #MAP63のライトハント終了
    168: "LIGHTHUNT_64",    #MAP64のライトハント終了
    169: "LIGHTHUNT_65",    #MAP65のライトハント終了
    170: "LIGHTHUNT_66",    #MAP66のライトハント終了
    171: "LIGHTHUNT_67",    #MAP67のライトハント終了
    172: "LIGHTHUNT_68",    #MAP68のライトハント終了
    173: "LIGHTHUNT_69",    #MAP69のライトハント終了
    174: "LIGHTHUNT_70",    #MAP70のライトハント終了
    175: "LIGHTHUNT_71",    #MAP71のライトハント終了
    176: "LIGHTHUNT_72",    #MAP72のライトハント終了
    177: "LIGHTHUNT_73",    #MAP73のライトハント終了
    178: "LIGHTHUNT_74",    #MAP74のライトハント終了
    179: "LIGHTHUNT_75",    #MAP75のライトハント終了
    180: "LIGHTHUNT_76",    #MAP76のライトハント終了
    181: "LIGHTHUNT_77",    #MAP77のライトハント終了
    182: "LIGHTHUNT_78",    #MAP78のライトハント終了
    183: "LIGHTHUNT_79",    #MAP79のライトハント終了
    184: "LIGHTHUNT_80",    #MAP80のライトハント終了
    185: "LIGHTHUNT_81",    #MAP81のライトハント終了
    186: "LIGHTHUNT_82",    #MAP82のライトハント終了
    187: "LIGHTHUNT_83",    #MAP83のライトハント終了
    188: "LIGHTHUNT_84",    #MAP84のライトハント終了
    189: "LIGHTHUNT_85",    #MAP85のライトハント終了
    190: "LIGHTHUNT_86",    #MAP86のライトハント終了
    191: "LIGHTHUNT_87",    #MAP87のライトハント終了
    192: "LIGHTHUNT_88",    #MAP88のライトハント終了
    193: "LIGHTHUNT_89",    #MAP89のライトハント終了
    194: "LIGHTHUNT_90",    #MAP90のライトハント終了
    195: "LIGHTHUNT_91",    #MAP91のライトハント終了
    196: "LIGHTHUNT_92",    #MAP92のライトハント終了
    197: "LIGHTHUNT_93",    #MAP93のライトハント終了
    198: "LIGHTHUNT_94",    #MAP94のライトハント終了
    199: "LIGHTHUNT_95",    #MAP95のライトハント終了
    200: "LIGHTHUNT_96",    #MAP96のライトハント終了
    201: "LIGHTHUNT_97",    #MAP97のライトハント終了
    202: "LIGHTHUNT_98",    #MAP98のライトハント終了
    203: "LIGHTHUNT_99",    #MAP99のライトハント終了
    204: "TUT_LHUNT",    #ライトハントのチュートリアルを見た
    205: "TUT_KEYWORD",    #用語集のチュートリアルを見た
    206: "TUT_FULLMAP",    #全体マップのチュートリアルを見た
    207: "TUT_WARPSTONE",    #花石のチュートリアルを見た
    208: "TUT_ETALK2",    #魔物NPC討伐チュートリアルを見た
    209: "TUT_DIFFICULTY",    #攻略難度のチュートリアルを見た
    210: "TUT_CAREERUP",    #キャリアアップのチュートリアルを見た
    211: "TUT_MAINQUEST",    #作戦業務のチュートリアルを見た
    212: "TUT_DMAKING",    #ダンジョンメイキングのチュートリアルを見た
    213: "TUT_RADIO",    #ラジオのチュートリアルを見た
    214: "TUT_ETALK",    #魔物会話のチュートリアルを見た
    215: "TUT_FLENEMY",    #マモノの花のチュートリアルを見た
    216: "STAY_HANBA_BASE",    #【会話用】飯場が基地テントにいる
    217: "STAY_HANBA_REACTOR",    #【会話用】飯場が融合炉にいる
    218: "STAY_HANBA_LIVING",    #【会話用】飯場が住居テントにいる
    219: "STAY_HANBA_STORAGE",    #【会話用】飯場が倉庫テントにいる
    220: "STAY_LUKI_BASE",    #【会話用】ルキが基地テントにいる
    221: "STAY_LUKI_REACTOR",    #【会話用】ルキが融合炉にいる
    222: "STAY_LUKI_LIVING",    #【会話用】ルキが住居テントにいる
    223: "STAY_LUKI_STORAGE",    #【会話用】ルキが倉庫テントにいる
    224: "STAY_CASSANDRA_LIVING",    #【会話用】カサンドラが住居テントにいる
    225: "STAY_DEATHRETURN",    #全滅して拠点へ戻ったことがある
    226: "STAY_HAIJUZI_REACTOR",    #【会話用】灰十字が融合炉にいる
    227: "STAY_HAIJUZI_STORAGE",    #【会話用】灰十字が倉庫テントにいる
    228: "DLC_ENTRY_TUT",    #拡張版の入り口の説明を受ける
    229: "ADD_LIMITITEM",    #拠点の全景で装備制限アイテムをもらった。
    230: "TOWN_RE13",    #拠点系リザーブ13
    231: "TOWN_RE14",    #拠点系リザーブ14
    232: "TOWN_RE15",    #拠点系リザーブ15
    233: "TOWN_RE16",    #拠点系リザーブ16
    234: "TOWN_RE17",    #拠点系リザーブ17
    235: "TOWN_RE18",    #拠点系リザーブ18
    236: "TOWN_RE19",    #拠点系リザーブ19
    237: "TOWN_RE20",    #拠点系リザーブ20
    238: "ARTIFACT_HAVE",    #【全体】遺物を1つ以上持っている
    239: "MAKE_YOMIHANA",    #【全体】黄泉ヲ裂ク華が作れる（現状未使用）
    240: "WARP_WAKEUP",    #【全体】花石を覚醒させる手段を得た
    241: "WARP_WAKEUP2",    #【全体】クリア後の花石を覚醒させる手段を得た
    242: "LUKI_REVIVAL",    #ルキが復活した
    243: "CAS_CATEAR",    #カサンドラの猫耳が見えるようになった
    244: "ENDING",    #エンディング（クレジット）を見た
    245: "ENDING2",    #エンディング２（裏ボス撃破）を見た
    246: "MAINALL_RE007",    #メインシナリオ（全体）リザーブ0007
    247: "MAINALL_RE008",    #メインシナリオ（全体）リザーブ0008
    248: "MAINALL_RE009",    #メインシナリオ（全体）リザーブ0009
    249: "S01_00_00",    #【導入】プロローグを見た
    250: "S01_00_01",    #【導入】黄泉で覚醒めた
    251: "S01_00_02",    #【導入】赤ルキを目撃した
    252: "S01_01_00",    #【導入】初めてキャンプに戻った
    253: "S01_01_01",    #【導入】基地テントで飯場と話した
    254: "S01_01_02",    #【導入】融合炉に初めて移動した
    255: "S01_01_03",    #【導入】住居テントに初めて移動した
    256: "S01_01_04",    #【導入】チノワゲートに初めて移動した
    257: "S02_01_00",    #【導入】第二キャンプに入った
    258: "S02_01_01",    #【導入】ルキを保護した
    259: "S02_02_00",    #【導入】ルキを連れてキャンプに帰還した
    260: "S03_00_00",    #【導入】ルキが融合炉を復活させた
    261: "S03_00_01",    #【導入】ゲートを開くのに失敗した
    262: "S03_01_00",    #【導入】飯場と飯を食った
    263: "S05_00_00",    #【処刑人】ルキに加護をもらった
    264: "S05_01_00",    #【処刑人】1個目の遺物を飯場に見せた
    265: "ARTIFACT01",    #【処刑人】1個目の遺物を捧げた（ハシゴ）
    266: "S01_01_05",    #【導入】飯場に最初の報告をした
    267: "S02_01_02",    #【導入】飯場に第二キャンプの報告をした
    268: "S02_02_01",    #【導入】融合炉前で放心しているルキを見た
    269: "ARTIFACT02",    #【処刑人】2個目の遺物を捧げた（牢のカギ）
    270: "ARTIFACT03",    #【処刑人】3個目の遺物を捧げた（森のカギ）
    271: "ARTIFACT04",    #【処刑人】4個目の遺物を捧げた（イヤシ）
    272: "ARTIFACT05",    #【処刑人】5個目の遺物を捧げた（マモノケシ）
    273: "ARTIFACT06",    #【処刑人】6個目の遺物を捧げた（城のカギ）
    274: "ARTIFACT07",    #【処刑人】7個目の遺物を捧げた（カケハシ）
    275: "ARTIFACT08",    #【処刑人】8個目の遺物を捧げた（マモノ）
    276: "ARTIFACT09",    #【処刑人】9個目の遺物を捧げた（黄泉）
    277: "LUKIBODY01",    #※未使用
    278: "HAN_RANK",    #飯場に探行士の等級の話をした
    279: "HAN_CARD",    #飯場に名刺を見せた
    280: "LUKI_CARD",    #ルキに名刺を見せた
    281: "CAS_CARD",    #カサンドラに名刺を見せた
    282: "S05_05_00",    #【処刑人】全景でヨミヌー前座イベントを見た
    283: "S07_02_00",    #【処刑人】久世戸ラジオ1回目を聞いた
    284: "S07_03_00",    #【処刑人】2個目の遺物を飯場に見せた
    285: "S09_00_00",    #【処刑人】カサンドラに９９行区の噂を聞いた
    286: "S05_05_01",    #【処刑人】飯場とのヨミヌー会話の流れで写真の話が出た
    287: "S09_00_02",    #【処刑人】※未使用※
    288: "S09_01_00",    #【処刑人】久世戸ラジオ2回目を聞いた
    289: "S09_02_00",    #【処刑人】赤ルキに初めて会った
    290: "ARTI_LUST",    #色欲の遺物を捧げた
    291: "ARTI_BLIND",    #盲目の遺物を捧げた
    292: "ARTI_GLUTTON",    #大食の遺物を捧げた
    293: "ARTI_ENVY",    #嫉妬の遺物を捧げた
    294: "ARTI_GRIEF",    #悲嘆の遺物を捧げた
    295: "ARTI_GREED",    #金欲の遺物を捧げた
    296: "ARTI_PRIDE",    #傲慢の遺物を捧げた
    297: "ARTI_SLOTH",    #怠惰の遺物を捧げた
    298: "ARTI_WRATH",    #憤怒の遺物を捧げた
    299: "S11_00_00",    #【処刑人】※未使用※
    300: "S11_00_01",    #【処刑人】※未使用※
    301: "S11_00_02",    #【処刑人】※未使用※
    302: "S11_00_03",    #【処刑人】飯場に家族の話を聞いた
    303: "S11_01_00",    #【処刑人】久世戸ラジオ3回目を聞いた
    304: "MAINEV_RE040",    #メインシナリオリザーブ0040
    305: "S13_01_00",    #【処刑人】久世戸ラジオ4回目を聞いた
    306: "S15_00_00",    #【処刑人】カサンドラに一杯誘われた
    307: "S15_00_01",    #【処刑人】カサンドラと飲み明かす約束をした
    308: "S15_00_02",    #【処刑人】飯場から目標の話を聞いた
    309: "S15_01_00",    #【処刑人】※未使用※
    310: "S16_00_00",    #【処刑人】飯場からの救援要請を聞いた
    311: "S16_01_00",    #【処刑人】襲撃中、全景でカサンドラの話を聞いた
    312: "S16_01_01",    #【処刑人】襲撃中、住居テントへ入った
    313: "S16_01_02",    #【処刑人】襲撃中、融合炉へ入った
    314: "S16_01_03",    #【処刑人】襲撃中、基地テントへ入った（敵倒した）
    315: "S16_01_04",    #【処刑人】襲撃中、倉庫テントへ入った（敵倒した）
    316: "S16_01_05",    #【処刑人】襲撃中、ルキが死ななかった
    317: "S16_02_00",    #【処刑人】襲撃を撃退した
    318: "S17_00_00",    #【処刑人】襲撃後の飯場会話が終わった
    319: "S19_00_00",    #【処刑人】カサンドラから融合炉復活の話を聞いた
    320: "S21_00_00",    #【処刑人】ルキが発狂した
    321: "S21_01_00",    #【処刑人】飯場にルキの発狂の話をした
    322: "S21_02_00",    #【処刑人】灰十字にルキの発狂の話をした
    323: "S21_02_01",    #【処刑人】灰十字に赤ルキをおびきよせてもらった
    324: "S21_03_00",    #【処刑人】赤ルキから採血した
    325: "S22_00_00",    #【処刑人】灰十字に血清をもらった
    326: "S22_01_00",    #【処刑人】ルキを正気に戻した
    327: "S25_00_00",    #【処刑人】飯場と脱出後の話をした
    328: "S23_02_00",    #【処刑人】カサンドラに黄泉公社の陰謀の話をきいた
    329: "S25_01_00",    #【処刑人】ルキと脱出後の話をした
    330: "S25_01_01",    #【処刑人】ルキを引き取ると言った
    331: "S25_02_00",    #【処刑人】黄泉ヲ裂ク華を手に入れた
    332: "S26_00_00",    #【処刑人】飯場に黄泉ヲ裂ク華のことを話した
    333: "S26_00_01",    #【処刑人】黄泉ヲ裂ク華を使って脱出した
    334: "S05_02_00",    #【処刑人】カサンドラのアドバイスを聞いた
    335: "S05_03_00",    #【処刑人】飯場への報告を誘導するテキストを見た
    336: "S02_00_00",    #【導入】カサンドラと初遭遇した
    337: "S02_01_03",    #【導入】カサンドラに第二キャンプの報告をした
    338: "S05_02_01",    #【導入】最初の処刑人攻略中にカサンドラと1回話した
    339: "S05_04_00",    #【導入】カサンドラに写真を見せた
    340: "S21_04_00",    #【処刑人】久世戸ラジオ6回目を聞いた
    341: "S23_01_00",    #【処刑人】久世戸ラジオ7回目を聞いた
    342: "S25_03_00",    #【処刑人】久世戸ラジオ8回目を聞いた
    343: "S25_04_00",    #【処刑人】第２キャンプで融合炉の真実を見た
    344: "S25_04_01",    #【処刑人】第２キャンプで融合炉の真実を見て帰還した
    345: "S21_05_00",    #【処刑人】飯場からカサンドラの評価を聞いた
    346: "S26_00_02",    #【処刑人】黄泉ヲ裂ク華で脱出前にカサンドラと話した
    347: "MAINEV_RE094",    #メインシナリオリザーブ0094
    348: "MAINEV_RE095",    #メインシナリオリザーブ0095
    349: "MAINEV_RE096",    #メインシナリオリザーブ0096
    350: "MAINEV_RE097",    #メインシナリオリザーブ0097
    351: "MAINEV_RE098",    #メインシナリオリザーブ0098
    352: "S28_01_02",    #【折返し】廃キャンプ東でゲート帰還をキャンセルした
    353: "S28_00_00",    #【折返し】黄泉に逆戻りした
    354: "S28_00_01",    #【折返し】廃キャンプへ着く前に敗北した
    355: "S28_01_00",    #【折返し】廃キャンプ東で灰十字と遭遇した
    356: "S28_01_01",    #【折返し】廃キャンプ東から９９行区へ帰還した
    357: "S28_02_00",    #【折返し】頭蓋骨で融合炉が復活した
    358: "S28_02_01",    #【折返し】融合炉前で灰十字の話を聞いた
    359: "S28_00_02",    #【折返し】０行区東で荒堀と会った
    360: "S30_00_00",    #【少女復活】邦人子宮へのゲートが開けた
    361: "S32_00_00",    #【少女復活】クローンルキと遭遇した
    362: "S32_01_00",    #【少女復活】赤ルキ日記回収
    363: "S32_01_01",    #【少女復活】廃キャンプ西のゲートを見た
    364: "S32_01_02",    #【少女復活】※未使用※
    365: "S32_02_00",    #【少女復活】クローンルキと戦った（敗北含む）
    366: "S32_03_00",    #【少女復活】異人子宮へのゲートが開けた
    367: "S32_04_00",    #【少女復活】赤ルキの居場所が分かった
    368: "S34_00_00",    #【少女復活】石化カサンドラを見た
    369: "S34_00_01",    #【少女復活】カサンドラを虚無空間で助けた
    370: "S34_00_02",    #【少女復活】灰十字に高純度アルゲンを渡した
    371: "S34_01_00",    #【少女復活】赤ルキと1回会って勝利した
    372: "S34_01_01",    #【少女復活】赤ルキと2回会った
    373: "S34_01_02",    #【少女復活】赤ルキと3回会った（赤ルキ死んだ）
    374: "S34_01_03",    #【少女復活】灰十字にクローンの死体を渡した
    375: "S37_00_00",    #【少女復活】倉庫でルキの泣き言を聞いた
    376: "S37_00_01",    #【少女復活】倉庫で血の儀式の話を聞いた
    377: "S37_00_02",    #【少女復活】倉庫で血の儀式を受けた
    378: "S38_00_00",    #【少女復活】黄泉大ピンチラジオを聞いた
    379: "S38_00_01",    #【少女復活】ラスダン前に飯場と話した
    380: "S38_00_02",    #【少女復活】ラスダン前にカサンドラと話した（抗魅了薬）
    381: "S38_00_03",    #【少女復活】ラスダン前に灰十字と話した
    382: "S38_01_00",    #【少女復活】ラスボスと戦った（負けた時含む）
    383: "S38_01_01",    #【少女復活】ラスボスに勝った
    384: "S34_02_01",    #【少女復活】カサンドラ救出後に飯場と話した
    385: "S34_02_02",    #【少女復活】カサンドラ救出後にカサンドラと話した
    386: "S37_01_00",    #【少女復活】血の儀式前にカサンドラの話を聞いた
    387: "S38_02_00",    #【少女復活】ラスダン前に住居テントへいった
    388: "S38_02_01",    #【少女復活】ラスダン前に倉庫テントへいった
    389: "S38_02_02",    #【少女復活】ラスダン前に融合炉へいった
    390: "S38_03_00",    #【少女復活】ルキを愛していると宣言した
    391: "S34_01_06",    #【少女復活】赤ルキを森で倒した
    392: "S34_01_04",    #【少女復活】赤ルキを塔で倒した
    393: "S34_01_05",    #【少女復活】赤ルキを瓦礫で倒した
    394: "MAINEV_RE130",    #メインシナリオリザーブ0130
    395: "MAINEV_RE131",    #メインシナリオリザーブ0131
    396: "MAINEV_RE132",    #メインシナリオリザーブ0132
    397: "MAINEV_RE133",    #メインシナリオリザーブ0133
    398: "MAINEV_RE134",    #メインシナリオリザーブ0134
    399: "MAINEV_RE135",    #メインシナリオリザーブ0135
    400: "MAINEV_RE136",    #メインシナリオリザーブ0136
    401: "S41_00_00",    #【クリア後】住居テントで灰十字の伝言を聞いた
    402: "S41_01_00",    #【クリア後】記憶ボスを1体倒して灰十字のアドバイス聞いた
    403: "S41_01_01",    #【クリア後】記憶ボスを全部倒して灰十字のヘルプ聞いた
    404: "S41_02_00",    #【クリア後】カサンドラのツテを聞いた
    405: "S43_00_00",    #【クリア後】灰十字を保護した
    406: "S43_01_00",    #【クリア後】ルキの森入ってからルキの話を聞いた
    407: "S43_01_01",    #【クリア後】灰十字助けてから飯場の話を聞いた
    408: "S43_01_02",    #【クリア後】灰十字助けてからカサンドラの話を聞いた
    409: "S45_00_00",    #【クリア後】狂王の城進入時の久世戸ラジオを聞いた
    410: "S45_03_00",    #【クリア後】カサンドラに狂王の城をした
    411: "S45_02_01",    #【クリア後】荒堀に会ってからルキと話した
    412: "S45_02_02",    #【クリア後】荒堀に会ってから飯場と話した
    413: "S45_02_03",    #【クリア後】荒堀に会ってからカサンドラと話した
    414: "S45_02_04",    #【クリア後】荒堀に会ってから灰十字と話した
    415: "S45_01_00",    #【クリア後】灰十字から特異アルゲンの話を聞いた
    416: "S45_01_01",    #【クリア後】キワミの花を手に入れた
    417: "S45_01_02",    #【クリア後】飯場にキワミの花のことを報告した
    418: "S45_01_03",    #【クリア後】飯場にキワミの花のことを報告後に灰十字と話した
    419: "S47_00_00",    #【クリア後】キワミの花を使って一度外へ出た
    420: "S47_01_00",    #【クリア後】駅前の黄泉族を倒した（＝裏ボスと戦った）
    421: "S47_02_00",    #【クリア後】オーバーソルを倒した
    422: "S47_02_01",    #【クリア後】オーバーヘルを倒した
    423: "S47_02_02",    #【クリア後】裏ボスを倒した
    424: "S49_00_00",    #【クリア後】カサンドラに昇進試験の話にされた
    425: "S49_00_01",    #【クリア後】昇進試験で移動中（移動済んだらOFFにする）
    426: "S49_00_02",    #【クリア後】カサンドラと戦った
    427: "S49_00_03",    #【クリア後】カサンドラに勝った
    428: "S49_01_00",    #【クリア後】ルキのシメの会話を聞いた
    429: "S49_02_00",    #【クリア後】昇進試験前に飯場に話した
    430: "S49_02_01",    #【クリア後】昇進試験終わってから飯場に話した
    431: "S49_02_02",    #【クリア後】昇進試験終わってからカサンドラに話した
    432: "S40_00_00",    #【クリア後】クリア後の導入イベントを見た
    433: "S47_00_01",    #【クリア後】駅前の黄泉族と戦った
    434: "S49_00_04",    #【クリア後】試験後にカサンドラと戻ってきた
    435: "S49_00_05",    #【クリア後】カサンドラに負けた直後（済んだらOFFにする）
    436: "S49_02_03",    #【クリア後】昇進試験終わってから灰十字に話した
    437: "S49_03_00",    #【クリア後】ルキに高純度アルゲンを渡した
    438: "S41_02_01",    #【クリア後】カサンドラがラジオをやめた理由を聞いた
    439: "S43_02_00",    #【クリア後】クローン討伐時の久世戸の挑発1を聞いた（まだまだ）
    440: "S43_02_01",    #【クリア後】クローン討伐時の久世戸の挑発2を聞いた（半分）
    441: "S43_02_02",    #【クリア後】クローン討伐時の久世戸の挑発3を聞いた（もう少し）
    442: "S49_04_00",    #【クリア後】カサンドラ戦でクローンを見た
    443: "S49_04_01",    #【クリア後】カサンドラ再戦後に一緒に帰る（済んだらOFFにする）
    444: "MAINEV_RE180",    #メインシナリオリザーブ0180
    445: "DLC_ENDING_NOTAPP",    #拡張版が適用されていない状態で久世戸を倒した
    446: "MAINEV_RE182",    #メインシナリオリザーブ0182
    447: "MAINEV_RE183",    #メインシナリオリザーブ0183
    448: "MAINEV_RE184",    #メインシナリオリザーブ0184
    449: "MAINEV_RE185",    #メインシナリオリザーブ0185
    450: "MAINEV_RE186",    #メインシナリオリザーブ0186
    451: "MAINEV_RE187",    #メインシナリオリザーブ0187
    452: "MAINEV_RE188",    #メインシナリオリザーブ0188
    453: "MAINEV_RE189",    #メインシナリオリザーブ0189
    454: "MAINEV_RE190",    #メインシナリオリザーブ0190
    455: "DUNNAME_FIRST",    #迷宮名表示を一度見た
    456: "WARPSTONE01",    #MAP03（色欲）の花石が覚醒
    457: "WARPSTONE02",    #MAP07（盲目）の花石が覚醒
    458: "WARPSTONE03",    #MAP05（大食）の花石が覚醒
    459: "WARPSTONE04",    #MAP10（嫉妬）の花石が覚醒
    460: "WARPSTONE05",    #MAP18（金欲）の花石が覚醒
    461: "WARPSTONE06",    #MAP22（悲嘆）の花石が覚醒
    462: "WARPSTONE07",    #MAPXX（傲慢）の花石が覚醒
    463: "WARPSTONE08",    #MAPXX（怠惰）の花石が覚醒
    464: "WARPSTONE09",    #MAPXX（憤怒）の花石が覚醒
    465: "RAGE_FIRST",    #赤ルキ襲撃の各段階の初回フラグ（段階進行時にOFF）
    466: "WARPSTONE10",    #MAP42邦人子宮への花石が覚醒
    467: "WARPSTONE11",    #MAPXX０行区西への花石が覚醒
    468: "WARPSTONE12",    #MAP43異人子宮への花石が覚醒
    469: "WARPSTONE13",    #MAP47虚無空間（ルキの森）への花石が覚醒
    470: "WARPSTONE14",    #MAP51黄泉子宮への花石が覚醒
    471: "WARPSTONE15",    #MAP53ラスボス戦への花石が覚醒
    472: "STONE_FIRST2",    #活性化した花石を見たことがある
    473: "STONE_FIRST",    #花石をはじめてみた
    474: "WARPSTONE16",    #MAP63狂王の城への花石が覚醒
    475: "EX1_WORD2",    #【色欲】話題「看守長」入手
    476: "EX1_WORD3",    #【色欲】話題「看守長の起こし方」入手
    477: "EX1_WORD4",    #【色欲】話題「看守長の好み」入手
    478: "EX1_WORD5",    #【色欲】話題「人間の巣」入手
    479: "EX1_NPC1_TALK",    #【色欲】E0030 NPC1と話した
    480: "EX1_NPC1_WIN",    #【色欲】E0030 NPC1を一度倒した（深紅ワンピースを入手）
    481: "EX1_NPC1_DEAD",    #【色欲】※未使用※
    482: "EX1_NPC2_TALK",    #【色欲】E0031 NPC2と話した
    483: "EX1_NPC2_WIN",    #【色欲】E0031 NPC2を一度倒した
    484: "EX1_NPC2_GETID",    #【色欲】E0031 NPC2から学生証をもらった
    485: "EX1_NPC2_PAY",    #【色欲】E0031 NPC2にAGを払った
    486: "EX1_NPC3_TALK",    #【色欲】E0032 NPC3と話した
    487: "EX1_NPC3_WIN",    #【色欲】E0032 NPC3を一度倒した
    488: "EX1_NPC3_DEAD",    #【色欲】※未使用※
    489: "EX1_BOSS_ITEM1",    #【色欲】E0033 穴にワンピースを投げた（正解1）
    490: "EX1_BOSS_ITEM2",    #【色欲】E0033 穴に学生証を投げた（正解2）
    491: "EX1_BOSS_ITEM3",    #【色欲】E0033 穴に頭皮を投げた（正解3）
    492: "EX1_BOSS_BATTLE",    #【色欲】E0033 ボスと戦闘した（敗北含む）
    493: "EX1_BOSS_WIN",    #【色欲】E0033 ボスに勝利して遺物も拾った
    494: "EX1_GET_HEAD",    #【色欲】M010 引き千切られた頭皮を入手
    495: "EX1_GET_ARM",    #【色欲】※未設定※
    496: "EX1_GET_FOOT",    #【色欲】※未設定※
    497: "EX1_BOSS_NOPICK",    #【色欲】E0033 ボスは倒したが遺物拾ってない
    498: "EX1_NPC1_LIKE",    #【色欲】E0030 NPC1に好みの話を聞いた
    499: "DUNEV_RE002",    #迷宮イベントリザーブ0002
    500: "EX2_WORD2",    #【盲目】話題「竜の戦車」入手
    501: "EX2_WORD3",    #【盲目】話題「ブレス攻撃」入手
    502: "EX2_WORD4",    #【盲目】話題「停止呪文」入手
    503: "EX2_WORD5",    #【盲目】※未設定※
    504: "EX2_NPC1_TALK",    #【盲目】E0070 NPC1と話した
    505: "EX2_NPC1_WIN",    #【盲目】E0070 NPC1を一度倒した
    506: "EX2_NPC1_DEAD",    #【盲目】※未使用※
    507: "EX2_NPC1_BREATH",    #【盲目】E0070 NPC1からブレスの話を聞いた
    508: "EX2_HIT_BREATH",    #【盲目】E0071 処刑人のブレスを受けた
    509: "EX2_GET_PAPER1",    #【盲目】E0084 死体からちぎれた羊皮紙入手。
    510: "EX2_DRA_BATTLE",    #【盲目】機械竜と1度戦った
    511: "EX2_DRA1_DEAD",    #【盲目】E0076 機械竜１号が停止した
    512: "EX2_DRA2_DEAD",    #【盲目】E0080 機械竜２号が停止した
    513: "EX2_DRA3_DEAD",    #【盲目】E0081 機械竜３号が停止した
    514: "EX2_BOSS_BATTLE",    #【盲目】E0075 ボスと戦闘した（敗北含む）
    515: "EX2_BOSS_WIN",    #【盲目】E0075 ボスに勝利して遺物も拾った
    516: "EX2_BOSS_NOPICK",    #【盲目】E0075 ボスは倒したが遺物拾ってない
    517: "EX2_NPC1_DRAGON",    #【盲目】E0070 NPC1から竜戦車の話を聞いた
    518: "EX2_NPC1_SCROLL",    #【盲目】E0070 NPC1から羊皮紙の話を聞いた
    519: "EX3_WORD2",    #【大食】話題「矯正監」入手
    520: "EX3_WORD3",    #【大食】話題「脱獄者」入手
    521: "EX3_WORD4",    #【大食】話題「統一神」入手
    522: "EX3_WORD5",    #【大食】※未設定※
    523: "EX3_NPC1_TALK",    #【大食】E0050 NPC1と話した
    524: "EX3_NPC1_WIN",    #【大食】E0050 NPC1を一度倒した
    525: "EX3_NPC1_DEAD",    #【大食】※未使用※
    526: "EX3_NPC2_TALK",    #【大食】E0052 NPC2と話した
    527: "EX3_NPC2_WIN",    #【大食】E0052 NPC2を一度倒した
    528: "EX3_NPC2_DEAD",    #【大食】※未使用※
    529: "EX3_NPC2_PAY",    #【大食】E0052 NPC2にAGを払った
    530: "EX3_NPC3_TALK",    #【大食】E0053 NPC3と話した
    531: "EX3_NPC3_WIN",    #【大食】E0053 NPC3を一度倒した
    532: "EX3_NPC3_DEAD",    #【大食】E0053 NPC3が死亡中
    533: "EX3_NPC3_ERASE",    #【大食】E0053 NPC3から脳みそ奪った
    534: "EX3_NPC4_TALK",    #【大食】E0061 NPC4と話した
    535: "EX3_NPC4_WIN",    #【大食】E0061 NPC4を一度倒した
    536: "EX3_NPC4_DEAD",    #【大食】E0061 NPC4が死亡中
    537: "EX3_NPC4_ERASE",    #【大食】E0061 NPC4から脳みそ奪った
    538: "EX3_NPC5_TALK",    #【大食】E0062 NPC5と話した
    539: "EX3_NPC5_WIN",    #【大食】E0062 NPC5を一度倒した
    540: "EX3_NPC5_DEAD",    #【大食】※未使用※
    541: "EX3_BOSS_TALK",    #【大食】E0055 ボスと話した
    542: "EX3_BOSS_PIT",    #【大食】E0055 ボスに廃棄層に落とされた
    543: "EX3_BOSS_QUEST",    #【大食】E0055 ボスに脳みそ集めを頼まれた
    544: "EX3_BOSS_BRAINS",    #【大食】E0055 ボスに小さな脳みそ渡した
    545: "EX3_BOSS_BRAINL",    #【大食】E0055 ボスに大きな脳みそ渡した
    546: "EX3_BOSS_BATTLE",    #【大食】E0055 ボスと戦闘した（敗北含む）
    547: "EX3_BOSS_WIN",    #【大食】E0055 ボスに勝利して遺物も拾った
    548: "EX3_BOSS_NOPICK",    #【大食】E0055 ボスは倒したが遺物拾ってない
    549: "DUNEV_RE019",    #迷宮イベントリザーブ0019
    550: "DUNEV_RE020",    #迷宮イベントリザーブ0020
    551: "EX4_WORD2",    #【嫉妬】話題「マーフィン公爵」入手
    552: "EX4_WORD3",    #【嫉妬】話題「七聖人」入手
    553: "EX4_WORD4",    #【嫉妬】話題「七つの称号」入手
    554: "EX4_WORD5",    #【嫉妬】話題「大聖堂」入手
    555: "EX4_NPC1_TALK",    #【嫉妬】E0102 NPC1と話した
    556: "EX4_NPC1_WIN",    #【嫉妬】E0102 NPC1を一度倒した
    557: "EX4_NPC1_DEAD",    #【嫉妬】※未使用※
    558: "EX4_BOSS_BEFORE",    #【嫉妬】E1504 加護6個終了で次はマーフィン戦
    559: "EX4_BOSS_BATTLE",    #【嫉妬】E1504 ボスと戦闘した（敗北含む）
    560: "EX4_BOSS_NOSTONE",    #【嫉妬】E1504 マーフィンを倒したがまだ遺物発見してない
    561: "EX4_BOSS_WIN",    #【嫉妬】E1504 ボスに勝利して遺物も拾った
    562: "EX4_BOSS_NOPICK",    #【嫉妬】E1504 ボスは倒したが遺物拾ってない
    563: "EX4_GRAVE1_BLESS",    #【嫉妬】E0121 学びの聖人の加護を受けた
    564: "EX4_GRAVE2_BLESS",    #【嫉妬】E0123 癒しの聖人の加護を受けた
    565: "EX4_GRAVE3_BLESS",    #【嫉妬】E0131 忠義の聖人の加護を受けた
    566: "EX4_GRAVE4_BLESS",    #【嫉妬】E0133 大海の聖人の加護を受けた
    567: "EX4_GRAVE5_BLESS",    #【嫉妬】E0135 戦いの聖人の加護を受けた
    568: "EX4_GRAVE6_BLESS",    #【嫉妬】E0141 大地の聖人の加護を受けた
    569: "EX4_GRAVE7_BLESS",    #【嫉妬】E0144 大空の聖人の加護を受けた
    570: "EX4_NPC1_SEVEN",    #【嫉妬】E0102 NPC1に7つの称号を聞いた
    571: "EX4_GRAVE_FIRST",    #【嫉妬】E1503 初めて加護を受けた
    572: "DUNEV_RE026",    #迷宮イベントリザーブ0026
    573: "DUNEV_RE027",    #迷宮イベントリザーブ0027
    574: "EX567_FIRSTENTER",    #【嫉妬・金欲・悲嘆】初めて花石で他迷宮へ入った
    575: "EX5_WORD2",    #【金欲】話題「錬金王」入手
    576: "EX5_WORD3",    #【金欲】話題「不死身」入手
    577: "EX5_WORD4",    #【金欲】話題「統一神」入手
    578: "EX5_WORD5",    #【金欲】話題「神の子」入手
    579: "EX5_FOUNTAIN",    #【金欲】E0150 泉イベントを見た
    580: "EX5_FOUNT_AG",    #【金欲】E0150 泉にAG投げ込んだ
    581: "EX5_FOUNT_MEDAL",    #【金欲】E0150 泉からメダルを入手した
    582: "EX5_BOSS_TALK",    #【金欲】E180 ボスと接触した
    583: "EX5_BOSS_ITEM2",    #【金欲】※未使用
    584: "EX5_BOSS_ITEM3",    #【金欲】※未使用
    585: "EX5_BOSS_AWAKE",    #【金欲】E0180 ボスを覚醒させた
    586: "EX5_BOSS_BATTLE",    #【金欲】E0180 ボスと戦闘した（敗北含む）
    587: "EX5_BOSS_WIN",    #【金欲】E0180 ボスに勝利して遺物も拾った
    588: "EX5_BOSS_NOPICK",    #【金欲】E0180 ボスは倒したが遺物拾ってない
    589: "EX5_NPC1_TALK",    #【金欲】E0182 追加NPCと話した
    590: "EX5_NPC1_WIN",    #【金欲】E0182 追加NPCを一度倒した
    591: "EX5_NPC1_TALK2",    #【金欲】※未使用※
    592: "EX5_NPC1_BOOK",    #【金欲】E0182 追加NPCに書物をもらった
    593: "DUNEV_RE033",    #迷宮イベントリザーブ0033
    594: "EX6_WORD2",    #【悲嘆】話題「機械の兵士」入手
    595: "EX6_WORD3",    #【悲嘆】話題「転移装置」入手
    596: "EX6_WORD4",    #【悲嘆】※未使用
    597: "EX6_WORD5",    #【悲嘆】※未使用
    598: "EX6_NPC1_TALK",    #【悲嘆】E0193 NPC1と話した
    599: "EX6_NPC1_WIN",    #【悲嘆】E0193 NPC1を一度倒した
    600: "EX6_NPC1_DEAD",    #【悲嘆】※未使用※
    601: "EX6_NPC2_TALK",    #【悲嘆】E0194 NPC2と話した
    602: "EX6_NPC2_WIN",    #【悲嘆】E0194 NPC2を一度倒した
    603: "EX6_NPC2_DEAD",    #【悲嘆】※未使用※
    604: "EX6_NPC3_TALK",    #【悲嘆】E0200 NPC3と話した
    605: "EX6_NPC3_WIN",    #【悲嘆】E0200 NPC3を一度倒した
    606: "EX6_NPC3_DEAD",    #【悲嘆】※未使用※
    607: "EX6_NPC4_TALK",    #【悲嘆】E0210 NPC4と話した
    608: "EX6_NPC4_WIN",    #【悲嘆】E0210 NPC4を一度倒した
    609: "EX6_NPC4_DEAD",    #【悲嘆】※未使用※
    610: "EX6_NPC5_TALK",    #【悲嘆】E0220 NPC5と話した
    611: "EX6_NPC5_WIN",    #【悲嘆】E0220 NPC5を一度倒した
    612: "EX6_BOSS_WORD1",    #【悲嘆】E0221 ボスに指令書のことをきいた
    613: "EX6_BOSS_TALK",    #【悲嘆】E0221 ボスと話した
    614: "EX6_BOSS_AWAKE",    #【悲嘆】E0221 ボスが自分たちの事を理解した
    615: "EX6_BOSS_BATTLE",    #【悲嘆】E0221 ボスと戦闘した（敗北含む）
    616: "EX6_BOSS_WIN",    #【悲嘆】E0221 ボスに勝利して遺物も拾った
    617: "EX6_BOSS_NOPICK",    #【悲嘆】E0221 ボスは倒したが遺物拾ってない
    618: "EX6_LITHOGRAPH",    #【悲嘆】S226 埋もれた石版を見た
    619: "EX6_BOSS_FINISH",    #【悲嘆】E0221 ボスに終焉の話をした
    620: "EX6_NPC6_TALK",    #【悲嘆】E0202 追加NPCと話した
    621: "EX6_NPC6_WIN",    #【悲嘆】E0202 追加NPCを一度倒した
    622: "EX6_NPC6_BOOK",    #【悲嘆】E0202 追加NPCに綱領をもらった
    623: "EX6_GET_PAPER",    #【悲嘆】E0224 指令書を拾った
    624: "EX7_WORD2",    #【傲慢】話題「統一神」入手
    625: "EX7_WORD3",    #【傲慢】話題「教皇」入手
    626: "EX7_WORD4",    #【傲慢】話題「鬼子」入手
    627: "EX7_WORD5",    #【傲慢】話題「信仰の証明」入手
    628: "EX7_NPC1_TALK",    #【傲慢】E0240 NPC1と話した
    629: "EX7_NPC1_WIN",    #【傲慢】E0240 NPC1を一度倒した
    630: "EX7_NPC1_DEAD",    #【傲慢】※未使用※
    631: "EX7_NPC1_PAY",    #【傲慢】E0240 NPC1にＡＧを払った
    632: "EX7_NPC2_TALK",    #【傲慢】E0241 NPC2と話した
    633: "EX7_NPC2_WIN",    #【傲慢】E0241 NPC2を一度倒した
    634: "EX7_NPC2_BATTLE",    #【傲慢】E0241 NPC2と戦闘した（敗北含む）
    635: "EX7_NPC2_DEAD",    #【傲慢】※未使用※
    636: "EX7_NPC3_TALK",    #【傲慢】E0260 NPC3と話した
    637: "EX7_NPC3_WIN",    #【傲慢】E0260 NPC3を一度倒した
    638: "EX7_NPC3_DEAD",    #【傲慢】※未使用※
    639: "EX7_NPC3_PAY",    #【傲慢】E0260 NPC3にＡＧを払った
    640: "EX7_NPC4_TALK",    #【傲慢】E0261 NPC4と話した
    641: "EX7_NPC4_WIN",    #【傲慢】E0261 NPC4を一度倒した
    642: "EX7_NPC4_DEAD",    #【傲慢】※未使用※
    643: "EX7_NPC4_BATTLE",    #【傲慢】E0261 NPC4と戦闘した（敗北含む）
    644: "EX7_NPC5_TALK",    #【傲慢】E0280 NPC5と話した
    645: "EX7_NPC5_WIN",    #【傲慢】E0280 NPC5を一度倒した
    646: "EX7_NPC5_DEAD",    #【傲慢】※未使用※
    647: "EX7_WARP",    #【傲慢】E0230 入り口のワープを行った
    648: "EX7_BOSS_BATTLE",    #【傲慢】EXXXX ボスと戦闘した（敗北含む）
    649: "EX7_BOSS_WIN",    #【傲慢】EXXXX ボスに勝利して遺物も拾った
    650: "EX7_BOSS_NOPICK",    #【傲慢】EXXXX ボスは倒したが遺物拾ってない
    651: "EX7_NPC6_TALK",    #【傲慢】E0252 追加NPC6と話した
    652: "EX7_NPC6_WIN",    #【傲慢】E0252 追加NPC6を一度倒した
    653: "EX7_NPC6_BOOK",    #【傲慢】E0252 追加NPC6に書物をもらった
    654: "EX7_NPC6_ITEM",    #【傲慢】E0252 追加NPC6に聖印をもらった
    655: "EX7_STATUE_A",    #【傲慢】E0270 統一のアルダー像を見た
    656: "EX7_STATUE_G",    #【傲慢】E0271 善のアルダー像を見た
    657: "EX8_WORD2",    #【怠惰】話題「赤キノコ頭の狩場」入手
    658: "EX8_WORD3",    #【怠惰】話題「緑キノコ頭の牧場」入手
    659: "EX8_WORD4",    #【怠惰】話題「青キノコ頭の賢者」入手
    660: "EX8_WORD5",    #【怠惰】話題「狂王の訪問」入手
    661: "EX8_HUNT_TONBO",    #【怠惰】E0335 トンボリュウを狩った
    662: "EX8_RIDDLE_OK",    #【怠惰】E0350 NPC3のリドルに全問正解した
    663: "DUNEV_EX8_RE2",    #【怠惰】リザーブ
    664: "EX8_NPC1_TALK",    #【怠惰】E0330 NPC1と話した
    665: "EX8_NPC1_BATTLE",    #【怠惰】E0330 NPC1と戦闘した（敗北含む）
    666: "EX8_NPC1_WIN",    #【怠惰】E0330 NPC1を一度倒した
    667: "EX8_NPC1_DEAD",    #【怠惰】※未使用※
    668: "EX8_NPC2_TALK",    #【怠惰】E0340 NPC2と話した
    669: "EX8_NPC2_BATTLE",    #【怠惰】E0340 NPC2と戦闘した（敗北含む）
    670: "EX8_NPC2_WIN",    #【怠惰】E0340 NPC2を一度倒した
    671: "EX8_NPC2_DEAD",    #【怠惰】※未使用※
    672: "EX8_NPC3_TALK",    #【怠惰】E0350 NPC3と話した
    673: "EX8_NPC3_BATTLE",    #【怠惰】E0350 NPC3と戦闘した（敗北含む）
    674: "EX8_NPC3_WIN",    #【怠惰】E0350 NPC3を一度倒した
    675: "EX8_NPC3_DEAD",    #【怠惰】※未使用※
    676: "EX8_BOSS_BATTLE",    #【怠惰】EXXXX ボスと戦闘した（敗北含む）
    677: "EX8_BOSS_WIN",    #【怠惰】EXXXX ボスに勝利して遺物も拾った
    678: "EX8_BOSS_NOPICK",    #【怠惰】EXXXX ボスは倒したが遺物拾ってない
    679: "EX8_WARPAFTER",    #【怠惰】EXXXX ボスを襲ってワープさせられた直後（直後でなければOFF）
    680: "EX8_NPC1_HUNT",    #【怠惰】E0330 NPC1から獲物の話を聞いた
    681: "EX8_NPC2_FOOD",    #【怠惰】E0340 NPC2から牧場の話を聞いた
    682: "EX8_NPC3_KNOW",    #【怠惰】E0350 NPC3から知識収集の話を聞いた
    683: "DUNEV_RE049",    #迷宮イベントリザーブ0049
    684: "EX9_WORD2",    #【憤怒】話題「同盟軍」入手
    685: "EX9_WORD3",    #【憤怒】話題「内部闘争」入手
    686: "EX9_WORD4",    #【憤怒】※未設定※
    687: "EX9_WORD5",    #【憤怒】※未設定※
    688: "EX9_NPC1_TALK",    #【憤怒】E0391 NPC1と話した
    689: "EX9_NPC4_ITEM",    #【憤怒】E0393 NPC4から勲章を入手した
    690: "EX9_NPC1_LETTER",    #【憤怒】E0391 NPC1に密書もらった
    691: "EX9_NPC2_TALK",    #【憤怒】E0402 NPC2と話した
    692: "EX9_NPC2_DELIVERY",    #【憤怒】E0402 NPC2に密書見せた
    693: "EX9_NPC3_TALK",    #【憤怒】E0412 NPC3と話した
    694: "EX9_NPC3_DELIVERY",    #【憤怒】E0412 NPC3に密書見せた
    695: "EX9_BOSS_BATTLE",    #【憤怒】E0391 ボスと戦闘した（敗北含む）
    696: "EX9_BOSS_WIN",    #【憤怒】E0391 ボスに勝利して遺物も拾った
    697: "EX9_BOSS_NOPICK",    #【憤怒】E0391 ボスは倒したが遺物拾ってない
    698: "EX9_WARPAFTER",    #【憤怒】E0391 NPC1を襲ってワープさせられた直後（直後でなければOFF）
    699: "EX9_ALL_DELIVERY",    #【憤怒】NPC2とNPC3に密書見せた
    700: "EX9_NPC4_TALK",    #【憤怒】E0393 NPC4と話した
    701: "EX9_NPC4_WIN",    #【憤怒】E0393 NPC4を一度倒した
    702: "HAI_DUN1_TALK",    #灰十字と隠し穴で話した
    703: "HAI_DUN2_TALK",    #灰十字と錬金の塔で話した
    704: "HAI_DUN3_TALK",    #灰十字と臥竜の森で話した
    705: "HAI_FRIENDY",    #灰十字が友好的になった
    706: "HAI_WARPAFTER",    #灰十字にボスにワープさせられた直後に話した
    707: "HAI_HINT_TUNNEL",    #灰十字に99行区の話を聞いた
    708: "HAI_HINT_TOWER",    #灰十字に錬金の塔の話を聞いた
    709: "HAI_HINT_FOREST",    #灰十字に臥竜の森の話を聞いた
    710: "HAI_CARD",    #灰十字に名刺を見せた
    711: "HAI_HINT_ARTIFACT",    #灰十字に遺物の話を聞いた
    712: "HAI_POINT2",    #灰十字が錬金の塔へ移動した
    713: "HAI_POINT3",    #灰十字が臥竜の森へ移動した
    714: "HAI_MOVEBASE",    #灰十字が迷宮から拠点へ移動した
    715: "HAI_TALK1",    #灰十字が非友好のときに一度話した
    716: "HAI_MAMONO_NOBUY",    #灰十字がマモノの花を売らなくなった
    717: "DUNEV_RE077",    #迷宮イベントリザーブ0077
    718: "DUNEV_RE078",    #迷宮イベントリザーブ0078
    719: "ARA_DUN1_TALK",    #荒堀と死星の森と出会った
    720: "ARA_DUN2_TALK",    #荒堀と死星の森で話した
    721: "ARA_DUN3_TALK",    #荒堀と死星同盟砦で話した
    722: "ARA_FRIENDY",    #荒堀が友好的になった
    723: "ARA_WARPAFTER",    #荒堀にボスに落とされた直後に話した
    724: "ARA_HINT_FOREST",    #荒堀に死星の森の話を聞いた
    725: "ARA_HINT_FORT",    #荒堀に死星同盟砦の話を聞いた
    726: "ARA_CARD",    #荒堀に名刺を見せた
    727: "ARA_POINT3",    #荒堀が死星同盟砦へ移動した
    728: "ARA_RADIO",    #荒堀に過去の試練の話を聞いた
    729: "ARA_DUN4_TALK",    #荒堀と０行区で話した
    730: "ARA_HINT_CLONE",    #荒堀にクローンの話を聞いた
    731: "ARA_PLAYMUSIC",    #荒堀に音楽再生機を一度見せた
    732: "DUNENTER_01",    #色欲エリアに入った
    733: "DUNENTER_02",    #盲目エリアに入った
    734: "DUNENTER_03",    #大食エリアに入った
    735: "DUNENTER_04",    #嫉妬エリアに入った
    736: "DUNENTER_05",    #金欲エリアに入った
    737: "DUNENTER_06",    #悲嘆エリアに入った
    738: "DUNENTER_07",    #傲慢エリアに入った
    739: "DUNENTER_08",    #怠惰エリアに入った
    740: "DUNENTER_09",    #憤怒エリアに入った
    741: "DUNENTER_10",    #邦人子宮に入った
    742: "DUNENTER_11",    #０行区西に入った
    743: "DUNENTER_12",    #異人子宮に入った
    744: "DUNENTER_13",    #黄泉子宮に入った
    745: "DUNENTER_14",    #教皇の記憶に入った
    746: "DUNENTER_15",    #臥竜の記憶に入った
    747: "DUNENTER_16",    #死星の記憶に入った
    748: "DUNENTER_17",    #ルキの森に入った
    749: "DUNENTER_18",    #狂王の城に入った
    750: "DUNEV_RE097",    #迷宮イベントリザーブ0097
    751: "DUNEV_RE098",    #迷宮イベントリザーブ0098
    752: "DUNEV_RE099",    #迷宮イベントリザーブ0099
    753: "DUNEV_RE100",    #迷宮イベントリザーブ0100
    754: "HOUSHRINE_MAGICPILLAR",    #【邦人子宮】魔法柱イベントを見た
    755: "HOUSHRINE_ARAHORIKO_ALL",    #【邦人子宮】荒堀クローンたちを全員倒した
    756: "HOUSHRINE_ARAHORI_MEET",    #【邦人子宮】荒堀のクローンに出会った
    757: "HOUSHRINE_TOUCH",    #【邦人子宮】魔法柱に1度触った
    758: "DUNEV_RE120",    #迷宮イベントリザーブ0120
    759: "DUNEV_RE121",    #迷宮イベントリザーブ0121
    760: "DUNEV_RE122",    #迷宮イベントリザーブ0122
    761: "DUNEV_RE123",    #迷宮イベントリザーブ0123
    762: "DUNEV_RE124",    #迷宮イベントリザーブ0124
    763: "DUNEV_RE125",    #迷宮イベントリザーブ0125
    764: "DUNEV_RE126",    #迷宮イベントリザーブ0126
    765: "DUNEV_RE127",    #迷宮イベントリザーブ0127
    766: "DUNEV_RE128",    #迷宮イベントリザーブ0128
    767: "DUNEV_RE129",    #迷宮イベントリザーブ0129
    768: "ARA_GIVEME",    #荒堀に手土産を要求された
    769: "ARA_BEFOREBOSS",    #荒堀とラスボス前に一度話した
    770: "DUNEV_RE132",    #迷宮イベントリザーブ0132
    771: "DUNEV_RE133",    #迷宮イベントリザーブ0133
    772: "DUNEV_RE134",    #迷宮イベントリザーブ0134
    773: "DUNEV_RE135",    #迷宮イベントリザーブ0135
    774: "DUNEV_RE136",    #迷宮イベントリザーブ0136
    775: "DUNEV_RE137",    #迷宮イベントリザーブ0137
    776: "IJINSHRINE_MAGICPILLAR",    #【異人子宮】魔法柱イベントを見た
    777: "IJINSHRINE_CASSANDRAKO_ALL",    #【異人子宮】カサンドラクローンたちを全員倒した
    778: "IJINSHRINE_CASSANDRA_MEET",    #【異人子宮】でカサンドラのクローンに出会った
    779: "DUNEV_RE141",    #迷宮イベントリザーブ0141
    780: "DUNEV_RE142",    #迷宮イベントリザーブ0142
    781: "DUNEV_RE143",    #迷宮イベントリザーブ0143
    782: "DUNEV_RE144",    #迷宮イベントリザーブ0144
    783: "DUNEV_RE145",    #迷宮イベントリザーブ0145
    784: "DUNEV_RE146",    #迷宮イベントリザーブ0146
    785: "DUNEV_RE147",    #迷宮イベントリザーブ0147
    786: "DUNEV_RE148",    #迷宮イベントリザーブ0148
    787: "DUNEV_RE149",    #迷宮イベントリザーブ0149
    788: "DUNEV_RE150",    #迷宮イベントリザーブ0150
    789: "DUNEV_RE151",    #迷宮イベントリザーブ0151
    790: "DUNEV_RE152",    #迷宮イベントリザーブ0152
    791: "DUNEV_RE153",    #迷宮イベントリザーブ0153
    792: "DUNEV_RE154",    #迷宮イベントリザーブ0154
    793: "DUNEV_RE155",    #迷宮イベントリザーブ0155
    794: "DUNEV_RE156",    #迷宮イベントリザーブ0156
    795: "DUNEV_RE157",    #迷宮イベントリザーブ0157
    796: "DUNEV_RE158",    #迷宮イベントリザーブ0158
    797: "DUNEV_RE159",    #迷宮イベントリザーブ0159
    798: "YOMI_WORD2",    #【黄泉子宮】話題「資質の試練」入手
    799: "YOMI_WORD3",    #【黄泉子宮】話題「狂王」入手
    800: "YOMI_WORD4",    #【黄泉子宮】※未設定※
    801: "YOMI_WORD5",    #【黄泉子宮】※未設定※
    802: "YOMI_NPC1_TALK",    #【黄泉子宮】E0510 NPC1と話した
    803: "YOMI_NPC1_CLEAR",    #【黄泉子宮】E0510 NPC1の試練をクリア
    804: "YOMI_NPC2_TALK",    #【黄泉子宮】E0511 NPC2と話した
    805: "YOMI_NPC2_MISS",    #【黄泉子宮】E0511 NPC2の試練に失敗
    806: "YOMI_NPC2_CLEAR",    #【黄泉子宮】E0511 NPC2の試練をクリア
    807: "YOMI_NPC3_TALK",    #【黄泉子宮】E0520 NPC3と話した
    808: "YOMI_NPC3_MISS",    #【黄泉子宮】E0520 NPC3の試練に失敗
    809: "YOMI_NPC3_CLEAR",    #【黄泉子宮】E0520 NPC3の試練をクリア
    810: "YOMI_NPC4_TALK",    #【黄泉子宮】E0500 NPC4と話した
    811: "YOMI_NPC4_MISS",    #【黄泉子宮】E0500 NPC4の試練に失敗
    812: "YOMI_NPC4_CLEAR",    #【黄泉子宮】E0500 NPC4の試練をクリア
    813: "YOMI_NPC5_TALK",    #【黄泉子宮】E0530 NPC5と話した
    814: "YOMI_NPC5_CLEAR",    #【黄泉子宮】E0530 NPC5の試練をクリア
    815: "YOMISHRINE_KUZEDOKO_ALL",    #【黄泉子宮】久世戸クローンたちを全員倒した
    816: "YOMI_NPC1_MEET",    #【黄泉子宮】E0510 NPC1と会った
    817: "YOMI_NPC2_MEET",    #【黄泉子宮】E0511 NPC2と会った
    818: "YOMI_NPC3_MEET",    #【黄泉子宮】E0520 NPC3と会った
    819: "YOMI_NPC4_MEET",    #【黄泉子宮】E0500 NPC4と会った
    820: "YOMI_NPC5_MEET",    #【黄泉子宮】E0530 NPC5と会った
    821: "YOMI_NPC_MEET",    #【黄泉子宮】いずれかのクローン久世戸と会った
    822: "DUNEV_RE184",    #迷宮イベントリザーブ0184
    823: "DUNEV_RE185",    #迷宮イベントリザーブ0185
    824: "DR_NPC1_TALK",    #【宝の夢】E0152 宝の夢の門番（錬金の塔）と話した
    825: "DR_NPC1_WIN",    #【宝の夢】E0152 宝の夢の門番（錬金の塔）を一度倒した
    826: "DR_DUN1_ENTER",    #【宝の夢】宝の夢（錬金の塔）に入った
    827: "DR_DUN1_BOSS",    #【宝の夢】宝の夢（錬金の塔）のボスを倒した
    828: "DR_NPC2_TALK",    #【宝の夢】E0292 宝の夢の門番（大聖堂）と話した
    829: "DR_NPC2_WIN",    #【宝の夢】E0292 宝の夢の門番（大聖堂）を一度倒した
    830: "DR_DUN2_ENTER",    #【宝の夢】宝の夢（大聖堂）に入った
    831: "DR_DUN2_BOSS",    #【宝の夢】宝の夢（大聖堂）のボスを倒した
    832: "DR_NPC3_TALK",    #【宝の夢】E0431 宝の夢の門番（0行区）と話した
    833: "DR_NPC3_WIN",    #【宝の夢】E0431 宝の夢の門番（0行区）を一度倒した
    834: "DR_DUN3_ENTER",    #【宝の夢】宝の夢（0行区）に入った
    835: "DR_DUN3_BOSS",    #【宝の夢】宝の夢（0行区）のボスを倒した
    836: "DR_NPCSOME_TALK",    #いずれかの宝の夢の門番に話したことがある
    837: "DR_FLOWER_GET",    #門番と話して黄泉の花をもらった（ON OFFで繰り返し使用）
    838: "DR_FIRSTWARP",    #一度でも宝の夢にワープしたことがある
    839: "DUNEV_RE112",    #迷宮イベントリザーブ0112
    840: "DUNEV_RE113",    #迷宮イベントリザーブ0113
    841: "DUNEV_RE114",    #迷宮イベントリザーブ0114
    842: "DUNEV_RE115",    #迷宮イベントリザーブ0115
    843: "ZERO_GUARD_WIN",    #【０行区】廃キャンプ西の前連戦に勝利した
    844: "DUNEV_RE187",    #迷宮イベントリザーブ0187
    845: "DUNEV_RE188",    #迷宮イベントリザーブ0188
    846: "DUNEV_RE189",    #迷宮イベントリザーブ0189
    847: "DUNEV_RE190",    #迷宮イベントリザーブ0190
    848: "MEM1_BOSS_BATTLE",    #【教皇】E0544 ルミナリスと戦闘した（敗北含む）
    849: "MEM1_BOSS_WIN",    #【教皇】E0544 ルミナリスに勝利した
    850: "DUNEV_RE193",    #迷宮イベントリザーブ0193
    851: "MEM2_BOSS_WIN",    #【臥竜】E055X ボス全員に勝利した
    852: "MEM2_NPC1_BATTLE",    #【臥竜】E0551 長男と戦闘した（敗北含む）
    853: "MEM2_NPC1_WIN",    #【臥竜】E0551 長男に勝利した
    854: "MEM2_NPC2_BATTLE",    #【臥竜】E0552 次男と戦闘した（敗北含む）
    855: "MEM2_NPC2_WIN",    #【臥竜】E0552 次男に勝利した
    856: "MEM2_NPC3_BATTLE",    #【臥竜】E0553 三男と戦闘した（敗北含む）
    857: "MEM2_NPC3_WIN",    #【臥竜】E0553 三男に勝利した
    858: "MEM3_BOSS_WIN",    #【死星】E058X ボス全員に勝利した
    859: "MEM3_NPC1_BATTLE",    #【死星】E0580 中立と戦闘した（敗北含む）
    860: "MEM3_NPC1_WIN",    #【死星】E0580 中立に勝利した
    861: "MEM3_NPC2_BATTLE",    #【死星】E0581 善と戦闘した（敗北含む）
    862: "MEM3_NPC2_WIN",    #【死星】E0581 善に勝利した
    863: "MEM3_NPC3_BATTLE",    #【死星】E0582 悪と戦闘した（敗北含む）
    864: "MEM3_NPC3_WIN",    #【死星】E05872 悪に勝利した
    865: "FOREST_LUKI_ALL",    #【ルキの森】クローンルキを全滅させた
    866: "FOREST_LUKI_TALK",    #【ルキの森】クローンルキと接触した
    867: "FOREST_LUKI_WIN",    #【ルキの森】クローンルキに一度勝った
    868: "FOREST_LUKI_HAI",    #【ルキの森】灰十字のいるルキ戦独白飛ばし用
    869: "DUNEV_RE212",    #迷宮イベントリザーブ0212
    870: "CASTLE_RIDDLE",    #【狂王の城】リドルに正解した
    871: "CASTLE_BOSS_ALL",    #【狂王の城】ボス（罪人）を全滅させた
    872: "CASTLE_ARA_TALK",    #【狂王の城】荒堀と話した
    873: "CASTLE_ARA_BAT",    #【狂王の城】荒堀に挑んだ
    874: "CASTLE_ARA_WIN",    #【狂王の城】荒堀に勝利した
    875: "DUNEV_RE218",    #迷宮イベントリザーブ0218
    876: "DUNEV_RE219",    #迷宮イベントリザーブ0219
    877: "DUNEV_RE220",    #迷宮イベントリザーブ0220
    878: "DUNEV_RE221",    #迷宮イベントリザーブ0221
    879: "DUNEV_RE222",    #迷宮イベントリザーブ0222
    880: "EX7_STATUE_N",    #【傲慢】E0272 中立のアルダー像を見た
    881: "EX7_STATUE_E",    #【傲慢】E0273 悪のアルダー像を見た
    882: "LANGUAGE_YOMI",    #黄泉語の説明を見た
    883: "DUNEV_RE226",    #迷宮イベントリザーブ0226
    884: "DUNEV_RE227",    #迷宮イベントリザーブ0227
    885: "DUNEV_RE228",    #迷宮イベントリザーブ0228
    886: "DUNEV_RE229",    #迷宮イベントリザーブ0229
    887: "DUNEV_RE230",    #迷宮イベントリザーブ0230
    888: "DUNEV_RE231",    #迷宮イベントリザーブ0231
    889: "DUNEV_RE232",    #迷宮イベントリザーブ0232
    890: "DUNEV_RE233",    #迷宮イベントリザーブ0233
    891: "DUNEV_RE234",    #迷宮イベントリザーブ0234
    892: "DUNEV_RE235",    #迷宮イベントリザーブ0235
    893: "DUNEV_RE236",    #迷宮イベントリザーブ0236
    894: "DUNEV_RE237",    #迷宮イベントリザーブ0237
    895: "DUNEV_RE238",    #迷宮イベントリザーブ0238
    896: "DUNEV_RE239",    #迷宮イベントリザーブ0239
    897: "DUNEV_RE240",    #迷宮イベントリザーブ0240
    898: "DUNEV_RE241",    #迷宮イベントリザーブ0241
    899: "DUNEV_RE242",    #迷宮イベントリザーブ0242
    900: "DUNEV_RE243",    #迷宮イベントリザーブ0243
    901: "DUNEV_RE244",    #迷宮イベントリザーブ0244
    902: "DUNEV_RE245",    #迷宮イベントリザーブ0245
    903: "DUNEV_RE246",    #迷宮イベントリザーブ0246
    904: "DUNEV_RE247",    #迷宮イベントリザーブ0247
    905: "DUNEV_RE248",    #迷宮イベントリザーブ0248
    906: "DUNEV_RE249",    #迷宮イベントリザーブ0249
    907: "DUNEV_RE250",    #迷宮イベントリザーブ0250
    908: "DUNEV_RE251",    #迷宮イベントリザーブ0251
    909: "DUNEV_RE252",    #迷宮イベントリザーブ0252
    910: "DUNEV_RE253",    #迷宮イベントリザーブ0253
    911: "DUNEV_RE254",    #迷宮イベントリザーブ0254
    912: "DUNEV_RE255",    #迷宮イベントリザーブ0255
    913: "DUNEV_RE256",    #迷宮イベントリザーブ0256
    914: "DUNEV_RE257",    #迷宮イベントリザーブ0257
    915: "DUNEV_RE258",    #迷宮イベントリザーブ0258
    916: "DUNEV_RE259",    #迷宮イベントリザーブ0259
    917: "DUNEV_RE260",    #迷宮イベントリザーブ0260
    918: "DUNEV_RE261",    #迷宮イベントリザーブ0261
    919: "DUNEV_RE262",    #迷宮イベントリザーブ0262
    920: "DUNEV_RE263",    #迷宮イベントリザーブ0263
    921: "DUNEV_RE264",    #迷宮イベントリザーブ0264
    922: "DUNEV_RE265",    #迷宮イベントリザーブ0265
    923: "DUNEV_RE266",    #迷宮イベントリザーブ0266
    924: "DUNEV_RE267",    #迷宮イベントリザーブ0267
    925: "DUNEV_RE268",    #迷宮イベントリザーブ0268
    926: "DUNEV_RE269",    #迷宮イベントリザーブ0269
    927: "DUNEV_RE270",    #迷宮イベントリザーブ0270
    928: "DUNEV_RE271",    #迷宮イベントリザーブ0271
    929: "DUNEV_RE272",    #迷宮イベントリザーブ0272
    930: "DUNEV_RE273",    #迷宮イベントリザーブ0273
    931: "DUNEV_RE274",    #迷宮イベントリザーブ0274
    932: "DUNEV_RE275",    #迷宮イベントリザーブ0275
    933: "DUNEV_RE276",    #迷宮イベントリザーブ0276
    934: "DUNEV_RE277",    #迷宮イベントリザーブ0277
    935: "DUNEV_RE278",    #迷宮イベントリザーブ0278
    936: "DUNEV_RE279",    #迷宮イベントリザーブ0279
    937: "DUNEV_RE280",    #迷宮イベントリザーブ0280
    938: "DUNEV_RE281",    #迷宮イベントリザーブ0281
    939: "DUNEV_RE282",    #迷宮イベントリザーブ0282
    940: "DUNEV_RE283",    #迷宮イベントリザーブ0283
    941: "DUNEV_RE284",    #迷宮イベントリザーブ0284
    942: "DUNEV_RE285",    #迷宮イベントリザーブ0285
    943: "DUNEV_RE286",    #迷宮イベントリザーブ0286
    944: "DUNEV_RE287",    #迷宮イベントリザーブ0287
    945: "DUNEV_RE288",    #迷宮イベントリザーブ0288
    946: "DUNEV_RE289",    #迷宮イベントリザーブ0289
    947: "DUNEV_RE290",    #迷宮イベントリザーブ0290
    948: "DUNEV_RE291",    #迷宮イベントリザーブ0291
    949: "DUNEV_RE292",    #迷宮イベントリザーブ0292
    950: "DUNEV_RE293",    #迷宮イベントリザーブ0293
    951: "DUNEV_RE294",    #迷宮イベントリザーブ0294
    952: "DUNEV_RE295",    #迷宮イベントリザーブ0295
    953: "DUNEV_RE296",    #迷宮イベントリザーブ0296
    954: "DUNEV_RE297",    #迷宮イベントリザーブ0297
    955: "DUNEV_RE298",    #迷宮イベントリザーブ0298
    956: "DUNEV_RE299",    #迷宮イベントリザーブ0299
    957: "DUNEV_RE300",    #迷宮イベントリザーブ0300
    958: "KEYWORD_001",    #用語001 管理官
    959: "KEYWORD_002",    #用語002 車椅子の少女
    960: "KEYWORD_003",    #用語003 社長
    961: "KEYWORD_004",    #用語004 機械人
    962: "KEYWORD_005",    #用語005 異形の巨漢
    963: "KEYWORD_006",    #用語006 黄泉公社総裁
    964: "KEYWORD_007",    #用語007 黄泉
    965: "KEYWORD_008",    #用語008 地下探行士
    966: "KEYWORD_009",    #用語009 アルゲン
    967: "KEYWORD_010",    #用語010 労働キャンプ
    968: "KEYWORD_011",    #用語011 融合炉
    969: "KEYWORD_012",    #用語012 黄泉族
    970: "KEYWORD_013",    #用語013 黄泉区
    971: "KEYWORD_014",    #用語014 黄泉技術
    972: "KEYWORD_015",    #用語015 黄泉公社
    973: "KEYWORD_016",    #用語016 カサンドラ社
    974: "KEYWORD_017",    #用語017 ラジオ
    975: "KEYWORD_018",    #用語018 神の子
    976: "KEYWORD_019",    #用語019 狂王
    977: "KEYWORD_020",    #用語020 統一神
    978: "KEYWORD_021",    #用語021 アルダー帝国
    979: "KEYWORD_022",    #用語022 死星同盟
    980: "KEYWORD_023",    #用語023 錬金技術
    981: "KEYWORD_024",    #用語024 ０行区
    982: "KEYWORD_025",    #用語025 融合炉の真実
    983: "KEYWORD_026",    #用語026 ４番の日記
    984: "KEYWORD_027",    #用語027 生命生成実験
    985: "KEYWORD_028",    #用語028 探行士の真実
    986: "KEYWORD_029",    #用語029 黄泉の真実
    987: "KEYWORD_030",    #用語030 総裁の計画
    988: "KEYWORD_031",    #用語031 ヨミえもん
    989: "KEYWORD_032",    #用語032 ウォーカーマン
    990: "KEYWORD_033",    #用語033 クローズアップ黄泉！
    991: "KEYWORD_034",    #用語034 黄泉カープ
    992: "KEYWORD_035",    #用語035 ジャイアントネズミ
    993: "KEYWORD_036",    #用語036 長島卓
    994: "KEYWORD_037",    #用語037 ３年Ｂ組黄泉先生
    995: "KEYWORD_038",    #用語038 ダブル黄泉ラジカセ
    996: "KEYWORD_039",    #用語039 チノワモータートレイン
    997: "KEYWORD_040",    #用語040 ロックＶＳジャイアント万場
    998: "KEYWORD_041",    #用語041 機動兵器ヨミダム
    999: "KEYWORD_042",    #用語042 週刊少年ノーツ
    1000: "KEYWORD_043",    #用語043 地下探行士１００人に聞きました
    1001: "KEYWORD_044",    #用語044 戦国アンダーノーツ
    1002: "KEYWORD_045",    #用語045 スーパーヨミビジョン
    1003: "KEYWORD_046",    #用語046 矢沢研二
    1004: "KEYWORD_047",    #用語047
    1005: "KEYWORD_048",    #用語048
    1006: "KEYWORD_049",    #用語049
    1007: "KEYWORD_050",    #用語050
    1008: "KEYWORD_051",    #用語051
    1009: "KEYWORD_052",    #用語052
    1010: "KEYWORD_053",    #用語053
    1011: "KEYWORD_054",    #用語054
    1012: "KEYWORD_055",    #用語055
    1013: "KEYWORD_056",    #用語056
    1014: "KEYWORD_057",    #用語057
    1015: "KEYWORD_058",    #用語058
    1016: "KEYWORD_059",    #用語059
    1017: "KEYWORD_060",    #用語060
    1018: "KEYWORD_061",    #用語061
    1019: "KEYWORD_062",    #用語062
    1020: "KEYWORD_063",    #用語063
    1021: "KEYWORD_064",    #用語064
    1022: "KEYWORD_065",    #用語065
    1023: "KEYWORD_066",    #用語066
    1024: "KEYWORD_067",    #用語067
    1025: "KEYWORD_068",    #用語068
    1026: "KEYWORD_069",    #用語069
    1027: "KEYWORD_070",    #用語070
    1028: "KEYWORD_071",    #用語071
    1029: "KEYWORD_072",    #用語072
    1030: "KEYWORD_073",    #用語073
    1031: "KEYWORD_074",    #用語074
    1032: "KEYWORD_075",    #用語075
    1033: "KEYWORD_076",    #用語076
    1034: "KEYWORD_077",    #用語077
    1035: "KEYWORD_078",    #用語078
    1036: "KEYWORD_079",    #用語079
    1037: "KEYWORD_080",    #用語080
    1038: "KEYWORD_081",    #用語081
    1039: "KEYWORD_082",    #用語082
    1040: "KEYWORD_083",    #用語083
    1041: "KEYWORD_084",    #用語084
    1042: "KEYWORD_085",    #用語085
    1043: "KEYWORD_086",    #用語086
    1044: "KEYWORD_087",    #用語087
    1045: "KEYWORD_088",    #用語088
    1046: "KEYWORD_089",    #用語089
    1047: "KEYWORD_090",    #用語090
    1048: "KEYWORD_091",    #用語091
    1049: "KEYWORD_092",    #用語092
    1050: "KEYWORD_093",    #用語093
    1051: "KEYWORD_094",    #用語094
    1052: "KEYWORD_095",    #用語095
    1053: "KEYWORD_096",    #用語096
    1054: "KEYWORD_097",    #用語097
    1055: "KEYWORD_098",    #用語098
    1056: "KEYWORD_099",    #用語099
    1057: "KEYWORD_100",    #用語100
    1058: "NOODLE_START",    #飯場がヨミヌーを集めている話を聞いた
    1059: "NOODLE_FIRST",    #飯場にヨミヌーを1回渡した
}


#ParameterTypeから適切なC#のTypeへ変換する
parameter_type = {
    "String": "String",
    "ExpressionValueType": "Int32",
    "ExpressionOperator": "Int32",
    "ExpressionInt": "Int32",
    "ExpressionArgument": "Int32",
    "ScriptFlagId": "Int32",
    "TextId": "String",
    "QuestData": "Int32",
    "SoundResourceData": "Int32",
    "Float": "Single",
    "Bool": "Boolean",
    "Int": "Int32",
    "GraphicsSortOrderId": "Int32",
    "DungeonEntranceId": "Int32",
    "MapSymbolType": "Int32",
    "EffectData": "Int32",
    "ScenarioWindowPositionType": "Int32",
    "Align": "Int32",
    "EnemyDisappearType": "Int32",
    "ImageHideType": "Int32",
    "EventImageData": "Int32",
    "ImageShowType": "Int32",
    "MusicResourceData": "Int32",
    "ConfirmedEncounterData": "Int32",
    "TransitionType": "Int32",
    "DirectionType": "Int32",
    "SectorData": "Int32",
    "LuminanceLevel": "Int32",
    "CevData": "Int32",
    "CevPositionId": "Int32",
    "ItemInventoryType": "Int32",
    "FacilityId": "Int32",
    "EnemyData": "Int32",
    "EnemyAppearType": "Int32",
    "NpcBustData": "Int32",
    "NpcFacialExpressionId": "Int32",
    "NpcBustPositionId": "Int32",
    "BelongingsInventoryType": "Int32",
    "ConfirmedDropData": "Int32",
    "AchievementData": "Int32",
    "ItemData": "Int32",
    "BackgroundData": "Int32",
    "AfterAnnihilatedType": "Int32",
    "CityEncounterData": "Int32",
    "EnemyGraphicData": "Int32",
    "VideoResourceData": "Int32",
    "BaseClassId": "Int32"
}


#expval_tのそれぞれの引数の長さリスト
#Experience.ScriptEvent.ScriptExpressionDecoderを読んだので正しいはず
#引数の型は正しいのか若干の疑問はある
expval_args = {
    0 : None, 1 : ["ExpressionArgument"], 2 : ["ExpressionArgument", "ExpressionArgument", "ExpressionArgument"], 3 : ["ExpressionArgument"], 4 : ["ExpressionArgument"], 5 : ["ExpressionArgument"], 6 : ["ExpressionArgument"], 7 : None, 8 : ["ExpressionArgument"], 9 : ["ExpressionArgument"], 10: None, 11: None, 12: ["ExpressionArgument"], 13: None, 14: None, 15: None, 16: ["ExpressionArgument"], 17: ["ExpressionArgument", "ExpressionArgument"], 18: ["ExpressionArgument"], 19: ["ExpressionArgument"], 20: None, 21: None, 22: None, 23: None, 24: None, 25: ["ExpressionArgument"], 26: None, 27: ["ExpressionArgument"], 28: None, 29: None, 30: None, 31: ["ExpressionArgument", "ExpressionArgument"], 32: ["ExpressionArgument", "ExpressionArgument"], 33: None, 34: None, 35: ["ExpressionArgument"], 36: None, 37: None, 38: None, 39: None, 40: None, 41: None, 42: None, 43: None, 44: None, 45: None, 46: None, 47: None, 48: None, 49: None, 50: None, 51: ["ExpressionArgument"]
}
"""expval_args = {
    0 : None, 1 : ["ExpressionInt"], 2 : ["ExpressionInt", "ExpressionInt", "ExpressionInt"], 3 : ["ExpressionInt"], 4 : ["ExpressionInt"], 5 : ["String"], 6 : ["ScriptFlagId"], 7 : None, 8 : ["QuestState"], 9 : ["ExpressionInt"], 10: None, 11: None, 12: ["ExpressionInt"], 13: None, 14: None, 15: None, 16: ["ExpressionInt"], 17: ["ItemInventoryType", "ExpressionInt"], 18: ["ExpressionInt"], 19: ["ExpressionInt"], 20: None, 21: None, 22: None, 23: None, 24: None, 25: ["DungeonId"], 26: None, 27: ["ExpressionInt"], 28: None, 29: None, 30: None, 31: ["ExpressionInt", "ExpressionInt"], 32: ["ExpressionInt", "ExpressionInt"], 33: None, 34: None, 35: None, 36: None, 37: None, 38: None, 39: None, 40: None, 41: None, 42: None, 43: None, 44: None, 45: None, 46: None, 47: None, 48: None, 49: None, 50: None, 51: ["AdditionalContentsId"]
}"""


#ScriptDataContainer.bytesを解析して得たコマンドの引数リスト
#そのうちコンパイラはこの情報を使ってコンパイルをするようにしてやりたい
command_args = {
    "_exit_script": [],
    "_call_script": ["String"],
    "_change_script": ["String"],
    "_if": ["ExpressionInt"],
    "_elif": ["ExpressionInt"],
    "_else": [],
    "_endif": [],
    "_set_lwork": ["Int", "ExpressionInt"],
    "_set_gwork": ["Int", "ExpressionInt"],
    "_wait_seconds": ["Float"],
    "_wait_key": [],
    "_wait_load_all": [],
    "_wait_install_game": [],
    "_set_scenario_title_text": ["TextId"],
    "_clear_scenario_title": [],
    "_set_scenario_message_speed": ["Float"],
    "_set_scenario_message_duration": ["Float"],
    "_message_scenario": ["ScenarioWindowPositionType", "TextId", "Align"],
    "_message_scenario_line_align_left": ["ScenarioWindowPositionType", "TextId", "Align"],
    "_message_scenario_narration": ["ScenarioWindowPositionType", "TextId", "Align"],
    "_message_scenario_narration_line_align_left": ["ScenarioWindowPositionType", "TextId", "Align"],
    "_hide_scenario": [],
    "_message_common_window": ["TextId"],
    "_hide_common_window": [],
    "_message_radio": ["Int"],
    "_wait_radio": [],
    "_hide_radio": [],
    "_start_selection": [],
    "_set_selection_message": ["Int", "TextId"],
    "_show_selection": [],
    "_show_selection_dev": [],
    "_show_selection_yes_no": [],
    "_show_selection_yes_no_dev": [],
    "_decided_selection": ["Int"],
    "_canceled_selection": [],
    "_end_selection": [],
    "_restart_selection": [],
    "_back_selection": ["Int"],
    "_start_riddle": [],
    "_set_riddle_keyboard_default_text": ["TextId"],
    "_set_riddle_keyboard_description": ["TextId"],
    "_add_riddle_answer_text": ["TextId"],
    "_show_riddle": [],
    "_add_tutorial_text": ["TextId"],
    "_show_tutorial": ["Bool", "Bool"],
    "_set_flag_on": ["ScriptFlagId"],
    "_set_flag_off": ["ScriptFlagId"],
    "_set_event_wakeup_on": ["String"],
    "_set_event_wakeup_off": ["String"],
    "_set_event_icon": ["String", "MapSymbolType"],
    "_reset_event_icon": ["String"],
    "_set_progress": ["ExpressionInt"],
    "_set_money": ["ExpressionInt"],
    "_add_money": ["ExpressionInt"],
    "_set_dungeon_making_resource": ["ExpressionInt"],
    "_set_class_change_resource": ["BaseClassId", "ExpressionInt"],
    "_add_class_change_resource": ["BaseClassId", "ExpressionInt"],
    "_add_class_change_resource_all": ["ExpressionInt"],
    "_set_item_enhance_cap": ["ExpressionInt"],
    "_add_item_enhance_cap": ["ExpressionInt"],
    "_set_item_level_cap_modify": ["ExpressionInt"],
    "_add_item_level_cap_modify": ["ExpressionInt"],
    "_set_enemy_level_modify_modify": ["ExpressionInt"],
    "_add_enemy_level_modify_modify": ["ExpressionInt"],
    "_set_enemy_journal_force_on": ["EnemyData"],
    "_set_dungeon_entrance_on": ["DungeonEntranceId"],
    "_set_dungeon_entrance_off": ["DungeonEntranceId"],
    "_set_sector_luminance_level": ["SectorData", "LuminanceLevel"],
    "_unlock_achievement": ["AchievementData"],
    "_set_has_seen_prologue": [],
    "_set_has_notified_install_extra_scenario": [],
    "_set_has_seen_title": [],
    "_set_has_game_cleared_system_savedata": [],
    "_set_game_clear": [],
    "_add_item": ["ItemInventoryType", "Bool", "ItemData", "ExpressionInt"],
    "_add_item_lwork": ["ItemInventoryType", "Bool", "Int", "ExpressionInt"],
    "_add_item_gwork": ["ItemInventoryType", "Bool", "Int", "ExpressionInt"],
    "_remove_item": ["ItemInventoryType", "ItemData", "ExpressionInt"],
    "_remove_item_gwork": ["ItemInventoryType", "Int", "ExpressionInt"],
    "_start_item_list": ["BelongingsInventoryType"],
    "_start_hero_making": [],
    "_change_hp_percentage": ["Int", "Int", "Bool"],
    "_change_mp_percentage": ["Int", "Int", "Bool"],
    "_change_hp": ["Int", "Int", "Bool"],
    "_change_mp": ["Int", "Int", "Bool"],
    "_change_party_hp_percentage": ["Int", "Bool"],
    "_change_party_mp_percentage": ["Int", "Bool"],
    "_change_party_hp": ["Int", "Bool"],
    "_change_party_mp": ["Int", "Bool"],
    "_cure_party_ailment_all": [],
    "_leave_party": [],
    "_load_npc_bust": ["NpcBustData"],
    "_wait_load_npc_bust_all": [],
    "_unload_npc_bust": ["NpcBustData"],
    "_unload_npc_bust_all": [],
    "_show_npc_bust": ["NpcBustData", "NpcFacialExpressionId", "NpcBustPositionId", "ImageShowType"],
    "_wait_show_npc_bust": ["NpcBustData"],
    "_wait_show_npc_bust_all": [],
    "_hide_npc_bust": ["NpcBustData", "ImageHideType"],
    "_hide_npc_bust_all": ["ImageHideType"],
    "_wait_hide_npc_bust": ["NpcBustData"],
    "_wait_hide_npc_bust_all": [],
    "_change_face_npc_bust": ["NpcBustData", "NpcFacialExpressionId", "Bool"],
    "_wait_change_face_npc_bust": ["NpcBustData"],
    "_set_water_surface_effect_on": [],
    "_set_water_surface_effect_off": [],
    "_load_enemy_line": None,
        #可変長引数のため定義できない
    "_wait_load_enemy_all": [],
    "_unload_enemy_line": ["Int"],
    "_unload_enemy_all": [],
    "_wait_unload_enemy": [],
    "_set_enemy_position_offset": ["Int", "Int", "Float", "Float"],
    "_show_enemy": ["Int", "Int", "EnemyAppearType", "Bool", "Bool"],
    "_show_enemy_line": ["Int", "EnemyAppearType", "Bool", "Bool"],
    "_wait_show_enemy": ["Int", "Int"],
    "_wait_show_enemy_line": ["Int"],
    "_wait_show_enemy_all": [],
    "_hide_enemy": ["Int", "Int", "EnemyDisappearType"],
    "_hide_enemy_line": ["Int", "EnemyDisappearType"],
    "_hide_enemy_all": ["EnemyDisappearType"],
    "_wait_hide_enemy": ["Int", "Int"],
    "_wait_hide_enemy_line": ["Int"],
    "_wait_hide_enemy_all": [],
    "_pause_enemy_line_on": ["Int"],
    "_pause_enemy_line_off": ["Int"],
    "_load_back_enemy": ["EnemyGraphicData"],
    "_wait_load_back_enemy": [],
    "_unload_back_enemy": [],
    "_show_back_enemy": ["EnemyAppearType"],
    "_wait_show_back_enemy": [],
    "_hide_back_enemy": ["EnemyDisappearType"],
    "_wait_hide_back_enemy": [],
    "_load_background": ["BackgroundData"],
    "_wait_load_background": ["BackgroundData"],
    "_wait_load_background_all": [],
    "_unload_background": ["BackgroundData"],
    "_unload_background_all": [],
    "_show_background": ["BackgroundData", "Float"],
    "_wait_show_background": ["BackgroundData"],
    "_wait_show_background_all": [],
    "_hide_background": ["BackgroundData", "Float"],
    "_hide_background_all": ["Float"],
    "_wait_hide_background": ["BackgroundData"],
    "_wait_hide_background_all": [],
    "_load_image": ["EventImageData"],
    "_wait_load_image_all": [],
    "_unload_image": ["EventImageData"],
    "_unload_image_all": [],
    "_show_image": ["EventImageData", "Float", "Float", "ImageShowType"],
    "_wait_show_image": ["EventImageData"],
    "_wait_show_image_all": [],
    "_hide_image": ["EventImageData", "ImageHideType"],
    "_hide_image_all": ["ImageHideType"],
    "_wait_hide_image": ["EventImageData"],
    "_wait_hide_image_all": [],
    "_move_image": ["EventImageData", "Float", "Float", "Float"],
    "_wait_move_image": ["EventImageData"],
    "_load_cev": ["CevData"],
    "_wait_load_cev_all": [],
    "_unload_cev": ["CevData"],
    "_unload_cev_all": [],
    "_show_cev": ["CevData", "Float", "Float", "ImageShowType"],
    "_show_cev_position_id": ["CevData", "CevPositionId", "ImageShowType"],
    "_wait_show_cev": ["CevData"],
    "_wait_show_cev_all": [],
    "_hide_cev": ["CevData", "ImageHideType"],
    "_hide_cev_all": ["ImageHideType"],
    "_wait_hide_cev": ["CevData"],
    "_wait_hide_cev_all": [],
    "_move_cev": ["CevData", "Float", "Float", "Float"],
    "_wait_move_cev": ["CevData"],
    "_load_effect": ["EffectData"],
    "_wait_load_effect": ["EffectData"],
    "_unload_effect": ["EffectData"],
    "_unload_effect_all": [],
    "_play_effect": ["EffectData", "GraphicsSortOrderId", "Float", "Float", "Bool"],
    "_play_effect_enemy": ["EffectData", "GraphicsSortOrderId", "Int", "Int", "Bool"],
    "_wait_play_effect": ["EffectData"],
    "_stop_effect": ["EffectData"],
    "_stop_effect_all": [],
    "_play_dungeon_ambient_effect": [],
    "_stop_dungeon_ambient_effect": [],
    "_set_effect_skip_on": ["EffectData"],
    "_play_bgm": ["MusicResourceData", "Float"],
    "_play_dungeon_bgm": ["Float"],
    "_stop_bgm": ["Float"],
    "_wait_stop_bgm": [],
    "_play_sound": ["SoundResourceData"],
    "_play_dungeon_ambient": [],
    "_wait_play_sound": ["SoundResourceData"],
    "_wait_play_sound_all": [],
    "_wait_play_ambient_all": [],
    "_wait_play_voice_all": [],
    "_stop_sound": ["SoundResourceData", "Float"],
    "_stop_sound_all": [],
    "_stop_se_all": ["Float"],
    "_stop_ambient_all": ["Float"],
    "_stop_voice_all": ["Float"],
    "_play_video": ["VideoResourceData"],
    "_wait_play_video": [],
    "_stop_video": ["Float"],
    "_setup_battle_dungeon_random": [],
    "_setup_battle_dungeon_confirmed": ["ConfirmedEncounterData"],
    "_setup_battle_city": ["CityEncounterData"],
    "_set_battle_background": ["BackgroundData"],
    "_set_battle_background_default": [],
    "_set_battle_bgm": ["MusicResourceData"],
    "_set_battle_result_bgm": ["MusicResourceData"],
    "_set_battle_result_bgm_default": [],
    "_set_battle_result_bgm_none": [],
    "_set_battle_result_bgm_not_change": [],
    "_set_battle_encounter_se_on": [],
    "_set_battle_encounter_effect": ["TransitionType"],
    "_set_battle_confirmed_drop": ["ConfirmedDropData"],
    "_set_battle_light_level": ["LuminanceLevel"],
    "_set_battle_annihilate": ["AfterAnnihilatedType"],
    "_set_battle_gameover_on": [],
    "_set_battle_gameover_off": [],
    "_set_battle_treasurebox_on": [],
    "_set_battle_treasurebox_off": [],
    "_set_battle_treasurebox_trap_on": [],
    "_set_battle_treasurebox_trap_off": [],
    "_set_battle_escape_player_on": [],
    "_set_battle_escape_player_off": [],
    "_set_battle_escape_enemy_off": [],
    "_set_battle_restore_last_battle_condition_on": [],
    "_set_battle_restore_last_battle_condition_off": [],
    "_start_battle": [],
    "_move_event": [],
    "_move_city": ["FacilityId"],
    "_move_dungeon": ["SectorData", "Int", "Int", "DirectionType"],
    "_move_in_dungeon": ["SectorData", "Int", "Int", "DirectionType"],
    "_move_party": ["DirectionType"],
    "_turn_party": ["DirectionType"],
    "_quest_arise": ["QuestData"],
    "_quest_end": ["QuestData", "Bool"],
    "_move_camera": ["Float", "Float", "Float", "Float"],
    "_reset_move_camera": ["Float"],
    "_wait_move_camera": [],
    "_change_camera_height": ["Float", "Float", "Bool"],
    "_change_camera_height_enemy": ["EnemyData", "Int", "Float", "Bool"],
    "_wait_change_camera_height": [],
    "_focus_camera": ["Int", "Int", "Float", "Float"],
    "_reset_focus_camera": ["Float"],
    "_wait_focus_camera": [],
    "_shake_camera": ["Float", "Float", "Float"],
    "_shake_camera_loop": ["Float", "Float"],
    "_wait_shake_camera": [],
    "_stop_shake_camera": ["Float"],
    "_blur_on": ["Float", "Float"],
    "_blur_off": ["Bool"],
    "_set_screen_color": ["String", "Float", "Float"],
    "_reset_screen_color": ["Float"],
    "_wait_set_screen_color": [],
    "_show_scenario_back_mask": [],
    "_wait_show_scenario_back_mask": [],
    "_hide_scenario_back_mask": [],
    "_wait_hide_scenario_back_mask": [],
    "_fade_out": ["String", "Float", "GraphicsSortOrderId", "Int"],
    "_fade_in": ["Float", "Int"],
    "_wait_fade": [],
    "_show_epilogue_character_list": ["TextId", "Float"],
}
