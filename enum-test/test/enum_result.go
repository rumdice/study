package test

// COA_Table
type Common_Type int

const (
	Common_TypeASSET Common_Type = iota
	Common_TypeCHARACTER
	Common_TypeSTARGEM
	Common_TypeITEM
	Common_TypeCRAFTING
	Common_TypeSTORY
	Common_TypeAFFECTION
	Common_TypeCNT
)

var (
	Common_Type_name = map[int32]string{
		0: "ASSET",
		1: "CHARACTER",
		2: "STARGEM",
		3: "ITEM",
		4: "CRAFTING",
		5: "STORY",
		6: "AFFECTION",
		7: "CNT",
	}
	Common_Type_value = map[string]int32{
		"ASSET":     0,
		"CHARACTER": 1,
		"STARGEM":   2,
		"ITEM":      3,
		"CRAFTING":  4,
		"STORY":     5,
		"AFFECTION": 6,
		"CNT":       7,
	}
)

func (e Common_Type) String() string {
	return ""
}

func GetCommon_Type(s string) Common_Type {
	return -1
}

type Asset int

const (
	AssetGOLD Asset = iota
	AssetCRYSTAL
	AssetMINERAL
	AssetESSENCE
	AssetJEWEL
	AssetMEAT
	AssetHERB
	AssetSTARLIGHT
	AssetRARE_MINERAL
	AssetRARE_ESSENCE
	AssetRARE_JEWEL
	AssetRARE_MEAT
	AssetRARE_HERB
	AssetRARE_STARLIGHT
	AssetCNT
)

var (
	Asset_name = map[int32]string{
		0:  "GOLD",
		1:  "CRYSTAL",
		2:  "MINERAL",
		3:  "ESSENCE",
		4:  "JEWEL",
		5:  "MEAT",
		6:  "HERB",
		7:  "STARLIGHT",
		8:  "RARE_MINERAL",
		9:  "RARE_ESSENCE",
		10: "RARE_JEWEL",
		11: "RARE_MEAT",
		12: "RARE_HERB",
		13: "RARE_STARLIGHT",
		14: "CNT",
	}
	Asset_value = map[string]int32{
		"GOLD":           0,
		"CRYSTAL":        1,
		"MINERAL":        2,
		"ESSENCE":        3,
		"JEWEL":          4,
		"MEAT":           5,
		"HERB":           6,
		"STARLIGHT":      7,
		"RARE_MINERAL":   8,
		"RARE_ESSENCE":   9,
		"RARE_JEWEL":     10,
		"RARE_MEAT":      11,
		"RARE_HERB":      12,
		"RARE_STARLIGHT": 13,
		"CNT":            14,
	}
)

func (e Asset) String() string {
	return
}

func GetAsset(s string) Asset {
	return
}

type Asset_Grade int

const (
	Asset_GradeNORMAL Asset_Grade = iota
	Asset_GradeRARE
	Asset_GradeEPIC
	Asset_GradeLEGEND
	Asset_GradeMYTH
	Asset_GradeCNT
)

var (
	Asset_Grade_name = map[int32]string{
		0: "NORMAL",
		1: "RARE",
		2: "EPIC",
		3: "LEGEND",
		4: "MYTH",
		5: "CNT",
	}
	Asset_Grade_value = map[string]int32{
		"NORMAL": 0,
		"RARE":   1,
		"EPIC":   2,
		"LEGEND": 3,
		"MYTH":   4,
		"CNT":    5,
	}
)

func (e Asset_Grade) String() string {
	return
}

func GetAsset_Grade(s string) Asset_Grade {
	return
}

type Character_Species int

const (
	Character_SpeciesANGEL Character_Species = iota
	Character_SpeciesDEVIL
	Character_SpeciesDRAGON
	Character_SpeciesBEAST
	Character_SpeciesCNT
)

var (
	Character_Species_name = map[int32]string{
		0: "ANGEL",
		1: "DEVIL",
		2: "DRAGON",
		3: "BEAST",
		4: "CNT",
	}
	Character_Species_value = map[string]int32{
		"ANGEL":  0,
		"DEVIL":  1,
		"DRAGON": 2,
		"BEAST":  3,
		"CNT":    4,
	}
)

func (e Character_Species) String() string {
	return
}

func GetCharacter_Species(s string) Character_Species {
	return
}

type Character_Class int

const (
	Character_ClassWARRIOR Character_Class = iota
	Character_ClassRANGER
	Character_ClassASSASSIN
	Character_ClassKNIGHT
	Character_ClassWIZARD
	Character_ClassPRIEST
	Character_ClassBARD
	Character_ClassBATTLE_MAGE
	Character_ClassCNT
)

var (
	Character_Class_name = map[int32]string{
		0: "WARRIOR",
		1: "RANGER",
		2: "ASSASSIN",
		3: "KNIGHT",
		4: "WIZARD",
		5: "PRIEST",
		6: "BARD",
		7: "BATTLE_MAGE",
		8: "CNT",
	}
	Character_Class_value = map[string]int32{
		"WARRIOR":     0,
		"RANGER":      1,
		"ASSASSIN":    2,
		"KNIGHT":      3,
		"WIZARD":      4,
		"PRIEST":      5,
		"BARD":        6,
		"BATTLE_MAGE": 7,
		"CNT":         8,
	}
)

func (e Character_Class) String() string {
	return
}

func GetCharacter_Class(s string) Character_Class {
	return
}

type Character_Property int

const (
	Character_PropertyDARK Character_Property = iota
	Character_PropertyFIRE
	Character_PropertyWATER
	Character_PropertyFOREST
	Character_PropertyELECTRIC
	Character_PropertyEARTH
	Character_PropertyLIGHT
	Character_PropertyCNT
)

var (
	Character_Property_name = map[int32]string{
		0: "DARK",
		1: "FIRE",
		2: "WATER",
		3: "FOREST",
		4: "ELECTRIC",
		5: "EARTH",
		6: "LIGHT",
		7: "CNT",
	}
	Character_Property_value = map[string]int32{
		"DARK":     0,
		"FIRE":     1,
		"WATER":    2,
		"FOREST":   3,
		"ELECTRIC": 4,
		"EARTH":    5,
		"LIGHT":    6,
		"CNT":      7,
	}
)

func (e Character_Property) String() string {
	return
}

func GetCharacter_Property(s string) Character_Property {
	return
}

type Character_Grade int

const (
	Character_GradeNORMAL Character_Grade = iota
	Character_GradeRARE
	Character_GradeEPIC
	Character_GradeLEGEND
	Character_GradeMYTH
	Character_GradeCNT
)

var (
	Character_Grade_name = map[int32]string{
		0: "NORMAL",
		1: "RARE",
		2: "EPIC",
		3: "LEGEND",
		4: "MYTH",
		5: "CNT",
	}
	Character_Grade_value = map[string]int32{
		"NORMAL": 0,
		"RARE":   1,
		"EPIC":   2,
		"LEGEND": 3,
		"MYTH":   4,
		"CNT":    5,
	}
)

func (e Character_Grade) String() string {
	return
}

func GetCharacter_Grade(s string) Character_Grade {
	return
}

type Character_Skill int

const (
	Character_SkillCLASS Character_Skill = iota
	Character_SkillLEADER
	Character_SkillBASIC
	Character_SkillACTIVE
	Character_SkillULTIMATE
	Character_SkillPASSIVE
	Character_SkillCNT
)

var (
	Character_Skill_name = map[int32]string{
		0: "CLASS",
		1: "LEADER",
		2: "BASIC",
		3: "ACTIVE",
		4: "ULTIMATE",
		5: "PASSIVE",
		6: "CNT",
	}
	Character_Skill_value = map[string]int32{
		"CLASS":    0,
		"LEADER":   1,
		"BASIC":    2,
		"ACTIVE":   3,
		"ULTIMATE": 4,
		"PASSIVE":  5,
		"CNT":      6,
	}
)

func (e Character_Skill) String() string {
	return
}

func GetCharacter_Skill(s string) Character_Skill {
	return
}

type Character_Activity int

const (
	Character_ActivityNONE Character_Activity = iota
	Character_ActivityBATTLE
	Character_ActivityGUARD
	Character_ActivityCNT
)

var (
	Character_Activity_name = map[int32]string{
		0: "NONE",
		1: "BATTLE",
		2: "GUARD",
		3: "CNT",
	}
	Character_Activity_value = map[string]int32{
		"NONE":   0,
		"BATTLE": 1,
		"GUARD":  2,
		"CNT":    3,
	}
)

func (e Character_Activity) String() string {
	return
}

func GetCharacter_Activity(s string) Character_Activity {
	return
}

type Item int

const (
	ItemNONBATTLE Item = iota
	ItemBATTLE
	ItemCNT
)

var (
	Item_name = map[int32]string{
		0: "NONBATTLE",
		1: "BATTLE",
		2: "CNT",
	}
	Item_value = map[string]int32{
		"NONBATTLE": 0,
		"BATTLE":    1,
		"CNT":       2,
	}
)

func (e Item) String() string {
	return
}

func GetItem(s string) Item {
	return
}

type Item_Sub int

const (
	Item_SubCHARACTER_EXP Item_Sub = iota
	Item_SubEQUIPMENT_EXP
	Item_SubAFFECTION_EXP
	Item_SubCHARACTER_STAMINA
	Item_SubCRAFTING_STAMINA
	Item_SubBATTLE
	Item_SubCNT
)

var (
	Item_Sub_name = map[int32]string{
		0: "CHARACTER_EXP",
		1: "EQUIPMENT_EXP",
		2: "AFFECTION_EXP",
		3: "CHARACTER_STAMINA",
		4: "CRAFTING_STAMINA",
		5: "BATTLE",
		6: "CNT",
	}
	Item_Sub_value = map[string]int32{
		"CHARACTER_EXP":     0,
		"EQUIPMENT_EXP":     1,
		"AFFECTION_EXP":     2,
		"CHARACTER_STAMINA": 3,
		"CRAFTING_STAMINA":  4,
		"BATTLE":            5,
		"CNT":               6,
	}
)

func (e Item_Sub) String() string {
	return
}

func GetItem_Sub(s string) Item_Sub {
	return
}

type Item_Grade int

const (
	Item_GradeNORMAL Item_Grade = iota
	Item_GradeRARE
	Item_GradeEPIC
	Item_GradeLEGEND
	Item_GradeMYTH
	Item_GradeCNT
)

var (
	Item_Grade_name = map[int32]string{
		0: "NORMAL",
		1: "RARE",
		2: "EPIC",
		3: "LEGEND",
		4: "MYTH",
		5: "CNT",
	}
	Item_Grade_value = map[string]int32{
		"NORMAL": 0,
		"RARE":   1,
		"EPIC":   2,
		"LEGEND": 3,
		"MYTH":   4,
		"CNT":    5,
	}
)

func (e Item_Grade) String() string {
	return
}

func GetItem_Grade(s string) Item_Grade {
	return
}

type Equipment_Type int

const (
	Equipment_TypeSTARGEM Equipment_Type = iota
	Equipment_TypeCNT
)

var (
	Equipment_Type_name = map[int32]string{
		0: "STARGEM",
		1: "CNT",
	}
	Equipment_Type_value = map[string]int32{
		"STARGEM": 0,
		"CNT":     1,
	}
)

func (e Equipment_Type) String() string {
	return
}

func GetEquipment_Type(s string) Equipment_Type {
	return
}

type Equipment_Property int

const (
	Equipment_PropertySTARGEM_SHEEP Equipment_Property = iota
	Equipment_PropertySTARGEM_BULL
	Equipment_PropertySTARGEM_TWINS
	Equipment_PropertySTARGEM_CRAB
	Equipment_PropertySTARGEM_LION
	Equipment_PropertySTARGEM_GIRL
	Equipment_PropertySTARGEM_SCALES
	Equipment_PropertySTARGEM_SCORPION
	Equipment_PropertySTARGEM_ARCHER
	Equipment_PropertySTARGEM_GOAT
	Equipment_PropertySTARGEM_WATER
	Equipment_PropertySTARGEM_FISH
	Equipment_PropertySTARGEM_GREATBEAR
	Equipment_PropertySTARGEM_SNAKE
	Equipment_PropertySTARGEM_CRUX
	Equipment_PropertyCNT
)

var (
	Equipment_Property_name = map[int32]string{
		0:  "STARGEM_SHEEP",
		1:  "STARGEM_BULL",
		2:  "STARGEM_TWINS",
		3:  "STARGEM_CRAB",
		4:  "STARGEM_LION",
		5:  "STARGEM_GIRL",
		6:  "STARGEM_SCALES",
		7:  "STARGEM_SCORPION",
		8:  "STARGEM_ARCHER",
		9:  "STARGEM_GOAT",
		10: "STARGEM_WATER",
		11: "STARGEM_FISH",
		12: "STARGEM_GREATBEAR",
		13: "STARGEM_SNAKE",
		14: "STARGEM_CRUX",
		15: "CNT",
	}
	Equipment_Property_value = map[string]int32{
		"STARGEM_SHEEP":     0,
		"STARGEM_BULL":      1,
		"STARGEM_TWINS":     2,
		"STARGEM_CRAB":      3,
		"STARGEM_LION":      4,
		"STARGEM_GIRL":      5,
		"STARGEM_SCALES":    6,
		"STARGEM_SCORPION":  7,
		"STARGEM_ARCHER":    8,
		"STARGEM_GOAT":      9,
		"STARGEM_WATER":     10,
		"STARGEM_FISH":      11,
		"STARGEM_GREATBEAR": 12,
		"STARGEM_SNAKE":     13,
		"STARGEM_CRUX":      14,
		"CNT":               15,
	}
)

func (e Equipment_Property) String() string {
	return
}

func GetEquipment_Property(s string) Equipment_Property {
	return
}

type Equipment_Slot int

const (
	Equipment_SlotSTARGEM_SLOT_0 Equipment_Slot = iota
	Equipment_SlotSTARGEM_SLOT_1
	Equipment_SlotSTARGEM_SLOT_2
	Equipment_SlotSTARGEM_SLOT_3
	Equipment_SlotSTARGEM_SLOT_4
	Equipment_SlotSTARGEM_SLOT_5
	Equipment_SlotCNT
)

var (
	Equipment_Slot_name = map[int32]string{
		0: "STARGEM_SLOT_0",
		1: "STARGEM_SLOT_1",
		2: "STARGEM_SLOT_2",
		3: "STARGEM_SLOT_3",
		4: "STARGEM_SLOT_4",
		5: "STARGEM_SLOT_5",
		6: "CNT",
	}
	Equipment_Slot_value = map[string]int32{
		"STARGEM_SLOT_0": 0,
		"STARGEM_SLOT_1": 1,
		"STARGEM_SLOT_2": 2,
		"STARGEM_SLOT_3": 3,
		"STARGEM_SLOT_4": 4,
		"STARGEM_SLOT_5": 5,
		"CNT":            6,
	}
)

func (e Equipment_Slot) String() string {
	return
}

func GetEquipment_Slot(s string) Equipment_Slot {
	return
}

type Equipment_Grade int

const (
	Equipment_GradeNORMAL Equipment_Grade = iota
	Equipment_GradeRARE
	Equipment_GradeEPIC
	Equipment_GradeLEGEND
	Equipment_GradeMYTH
	Equipment_GradeCNT
)

var (
	Equipment_Grade_name = map[int32]string{
		0: "NORMAL",
		1: "RARE",
		2: "EPIC",
		3: "LEGEND",
		4: "MYTH",
		5: "CNT",
	}
	Equipment_Grade_value = map[string]int32{
		"NORMAL": 0,
		"RARE":   1,
		"EPIC":   2,
		"LEGEND": 3,
		"MYTH":   4,
		"CNT":    5,
	}
)

func (e Equipment_Grade) String() string {
	return
}

func GetEquipment_Grade(s string) Equipment_Grade {
	return
}

type Equipment_Attr int

const (
	Equipment_AttrWEAR Equipment_Attr = iota
	Equipment_AttrOBTAIN
	Equipment_AttrCNT
)

var (
	Equipment_Attr_name = map[int32]string{
		0: "WEAR",
		1: "OBTAIN",
		2: "CNT",
	}
	Equipment_Attr_value = map[string]int32{
		"WEAR":   0,
		"OBTAIN": 1,
		"CNT":    2,
	}
)

func (e Equipment_Attr) String() string {
	return
}

func GetEquipment_Attr(s string) Equipment_Attr {
	return
}

type Stat int

const (
	StatATK Stat = iota
	StatDEF
	StatHP
	StatCRITD
	StatCRIT
	StatTD
	StatREC
	StatCDR
	StatSHI
	StatNEU
	StatEVA
	StatACC
	StatSERES
	StatATKSPD
	StatDM
	StatDMGRES
	StatCRUX
	StatDRAIN
	StatNEUREC
	StatPERSISTANCE
	StatCRITR
	StatCRITDR
	StatBLOCKE
	StatBLOCK
	StatSPD
	StatRANGE
	StatCNT
)

var (
	Stat_name = map[int32]string{
		0:  "ATK",
		1:  "DEF",
		2:  "HP",
		3:  "CRITD",
		4:  "CRIT",
		5:  "TD",
		6:  "REC",
		7:  "CDR",
		8:  "SHI",
		9:  "NEU",
		10: "EVA",
		11: "ACC",
		12: "SERES",
		13: "ATKSPD",
		14: "DM",
		15: "DMGRES",
		16: "CRUX",
		17: "DRAIN",
		18: "NEUREC",
		19: "PERSISTANCE",
		20: "CRITR",
		21: "CRITDR",
		22: "BLOCKE",
		23: "BLOCK",
		24: "SPD",
		25: "RANGE",
		26: "CNT",
	}
	Stat_value = map[string]int32{
		"ATK":         0,
		"DEF":         1,
		"HP":          2,
		"CRITD":       3,
		"CRIT":        4,
		"TD":          5,
		"REC":         6,
		"CDR":         7,
		"SHI":         8,
		"NEU":         9,
		"EVA":         10,
		"ACC":         11,
		"SERES":       12,
		"ATKSPD":      13,
		"DM":          14,
		"DMGRES":      15,
		"CRUX":        16,
		"DRAIN":       17,
		"NEUREC":      18,
		"PERSISTANCE": 19,
		"CRITR":       20,
		"CRITDR":      21,
		"BLOCKE":      22,
		"BLOCK":       23,
		"SPD":         24,
		"RANGE":       25,
		"CNT":         26,
	}
)

func (e Stat) String() string {
	return
}

func GetStat(s string) Stat {
	return
}

type Graph int

const (
	GraphNONE Graph = iota
	GraphBELL_CURVE
	GraphMAX
	GraphMIN
	GraphCNT
)

var (
	Graph_name = map[int32]string{
		0: "NONE",
		1: "BELL_CURVE",
		2: "MAX",
		3: "MIN",
		4: "CNT",
	}
	Graph_value = map[string]int32{
		"NONE":       0,
		"BELL_CURVE": 1,
		"MAX":        2,
		"MIN":        3,
		"CNT":        4,
	}
)

func (e Graph) String() string {
	return
}

func GetGraph(s string) Graph {
	return
}

type Calculation int

const (
	CalculationPLUS Calculation = iota
	CalculationMULT
	CalculationP_MULT
	CalculationCNT
)

var (
	Calculation_name = map[int32]string{
		0: "PLUS",
		1: "MULT",
		2: "P_MULT",
		3: "CNT",
	}
	Calculation_value = map[string]int32{
		"PLUS":   0,
		"MULT":   1,
		"P_MULT": 2,
		"CNT":    3,
	}
)

func (e Calculation) String() string {
	return
}

func GetCalculation(s string) Calculation {
	return
}

type Character_Quest_Trigger int

const (
	Character_Quest_TriggerAUTO_BATTLE Character_Quest_Trigger = iota
	Character_Quest_TriggerTILE_GET
	Character_Quest_TriggerFIRST_STARGEM_GET
	Character_Quest_TriggerCNT
)

var (
	Character_Quest_Trigger_name = map[int32]string{
		0: "AUTO_BATTLE",
		1: "TILE_GET",
		2: "FIRST_STARGEM_GET",
		3: "CNT",
	}
	Character_Quest_Trigger_value = map[string]int32{
		"AUTO_BATTLE":       0,
		"TILE_GET":          1,
		"FIRST_STARGEM_GET": 2,
		"CNT":               3,
	}
)

func (e Character_Quest_Trigger) String() string {
	return
}

func GetCharacter_Quest_Trigger(s string) Character_Quest_Trigger {
	return
}

type Character_Quest_Type int

const (
	Character_Quest_TypeCOLLECT Character_Quest_Type = iota
	Character_Quest_TypeTILE_GET
	Character_Quest_TypeCNT
)

var (
	Character_Quest_Type_name = map[int32]string{
		0: "COLLECT",
		1: "TILE_GET",
		2: "CNT",
	}
	Character_Quest_Type_value = map[string]int32{
		"COLLECT":  0,
		"TILE_GET": 1,
		"CNT":      2,
	}
)

func (e Character_Quest_Type) String() string {
	return
}

func GetCharacter_Quest_Type(s string) Character_Quest_Type {
	return
}

type Equip_State int

const (
	Equip_StateUNEQUIP Equip_State = iota
	Equip_StateEQUIP
	Equip_StateCNT
)

var (
	Equip_State_name = map[int32]string{
		0: "UNEQUIP",
		1: "EQUIP",
		2: "CNT",
	}
	Equip_State_value = map[string]int32{
		"UNEQUIP": 0,
		"EQUIP":   1,
		"CNT":     2,
	}
)

func (e Equip_State) String() string {
	return
}

func GetEquip_State(s string) Equip_State {
	return
}

type Tutorial_Trigger int

const (
	Tutorial_TriggerGAME_START Tutorial_Trigger = iota
	Tutorial_TriggerCITY_MEET
	Tutorial_TriggerCRAFTING_START
	Tutorial_TriggerCRAFTING_END
	Tutorial_TriggerCNT
)

var (
	Tutorial_Trigger_name = map[int32]string{
		0: "GAME_START",
		1: "CITY_MEET",
		2: "CRAFTING_START",
		3: "CRAFTING_END",
		4: "CNT",
	}
	Tutorial_Trigger_value = map[string]int32{
		"GAME_START":     0,
		"CITY_MEET":      1,
		"CRAFTING_START": 2,
		"CRAFTING_END":   3,
		"CNT":            4,
	}
)

func (e Tutorial_Trigger) String() string {
	return
}

func GetTutorial_Trigger(s string) Tutorial_Trigger {
	return
}

type Request_Type int

const (
	Request_TypeASSET Request_Type = iota
	Request_TypeSTARGEM
	Request_TypeITEM
	Request_TypeTILE
	Request_TypeCNT
)

var (
	Request_Type_name = map[int32]string{
		0: "ASSET",
		1: "STARGEM",
		2: "ITEM",
		3: "TILE",
		4: "CNT",
	}
	Request_Type_value = map[string]int32{
		"ASSET":   0,
		"STARGEM": 1,
		"ITEM":    2,
		"TILE":    3,
		"CNT":     4,
	}
)

func (e Request_Type) String() string {
	return
}

func GetRequest_Type(s string) Request_Type {
	return
}

type Battle_Result int

const (
	Battle_ResultNONE Battle_Result = iota
	Battle_ResultLOSE
	Battle_ResultWIN
	Battle_ResultENCOUNTER
	Battle_ResultCNT
)

var (
	Battle_Result_name = map[int32]string{
		0: "NONE",
		1: "LOSE",
		2: "WIN",
		3: "ENCOUNTER",
		4: "CNT",
	}
	Battle_Result_value = map[string]int32{
		"NONE":      0,
		"LOSE":      1,
		"WIN":       2,
		"ENCOUNTER": 3,
		"CNT":       4,
	}
)

func (e Battle_Result) String() string {
	return
}

func GetBattle_Result(s string) Battle_Result {
	return
}

// COA_Worldmap
type Tile_Type int

const (
	Tile_TypeSINGLE Tile_Type = iota
	Tile_TypeCITY
	Tile_TypeRUIN
	Tile_TypeBASE
	Tile_TypeCNT
)

var (
	Tile_Type_name = map[int32]string{
		0: "SINGLE",
		1: "CITY",
		2: "RUIN",
		3: "BASE",
		4: "CNT",
	}
	Tile_Type_value = map[string]int32{
		"SINGLE": 0,
		"CITY":   1,
		"RUIN":   2,
		"BASE":   3,
		"CNT":    4,
	}
)

func (e Tile_Type) String() string {
	return
}

func GetTile_Type(s string) Tile_Type {
	return
}

type Craft_Type int

const (
	Craft_TypeNONE Craft_Type = iota
	Craft_TypeSMITHERY
	Craft_TypeOBSERVATORY
	Craft_TypeJEWELRY
	Craft_TypeALCHEMY
	Craft_TypeCOOKING
	Craft_TypeBASIC
	Craft_TypeCNT
)

var (
	Craft_Type_name = map[int32]string{
		0: "NONE",
		1: "SMITHERY",
		2: "OBSERVATORY",
		3: "JEWELRY",
		4: "ALCHEMY",
		5: "COOKING",
		6: "BASIC",
		7: "CNT",
	}
	Craft_Type_value = map[string]int32{
		"NONE":        0,
		"SMITHERY":    1,
		"OBSERVATORY": 2,
		"JEWELRY":     3,
		"ALCHEMY":     4,
		"COOKING":     5,
		"BASIC":       6,
		"CNT":         7,
	}
)

func (e Craft_Type) String() string {
	return
}

func GetCraft_Type(s string) Craft_Type {
	return
}

type Recipe_Category int

const (
	Recipe_CategoryOFFENSIVE Recipe_Category = iota
	Recipe_CategoryDEFFENSIVE
	Recipe_CategoryESSENTIAL
	Recipe_CategorySPECIAL
	Recipe_CategorySTAMINA
	Recipe_CategoryAFFECTION
	Recipe_CategoryEXP
	Recipe_CategorySTARGEM_EXP
	Recipe_CategoryCNT
)

var (
	Recipe_Category_name = map[int32]string{
		0: "OFFENSIVE",
		1: "DEFFENSIVE",
		2: "ESSENTIAL",
		3: "SPECIAL",
		4: "STAMINA",
		5: "AFFECTION",
		6: "EXP",
		7: "STARGEM_EXP",
		8: "CNT",
	}
	Recipe_Category_value = map[string]int32{
		"OFFENSIVE":   0,
		"DEFFENSIVE":  1,
		"ESSENTIAL":   2,
		"SPECIAL":     3,
		"STAMINA":     4,
		"AFFECTION":   5,
		"EXP":         6,
		"STARGEM_EXP": 7,
		"CNT":         8,
	}
)

func (e Recipe_Category) String() string {
	return
}

func GetRecipe_Category(s string) Recipe_Category {
	return
}

type Crafting_Grade int

const (
	Crafting_GradeNORMAL Crafting_Grade = iota
	Crafting_GradeRARE
	Crafting_GradeEPIC
	Crafting_GradeUNIQUE
	Crafting_GradeMYTH
	Crafting_GradeCNT
)

var (
	Crafting_Grade_name = map[int32]string{
		0: "NORMAL",
		1: "RARE",
		2: "EPIC",
		3: "UNIQUE",
		4: "MYTH",
		5: "CNT",
	}
	Crafting_Grade_value = map[string]int32{
		"NORMAL": 0,
		"RARE":   1,
		"EPIC":   2,
		"UNIQUE": 3,
		"MYTH":   4,
		"CNT":    5,
	}
)

func (e Crafting_Grade) String() string {
	return
}

func GetCrafting_Grade(s string) Crafting_Grade {
	return
}

type Hashtag int

const (
	HashtagSKYSCRAPER Hashtag = iota
	HashtagSIGHT
	HashtagSLUM
	HashtagSILENT
	HashtagNOISY
	HashtagFOOD
	HashtagMYSTERY
	HashtagRUMOR
	HashtagPEACEFUL
	HashtagCNT
)

var (
	Hashtag_name = map[int32]string{
		0: "SKYSCRAPER",
		1: "SIGHT",
		2: "SLUM",
		3: "SILENT",
		4: "NOISY",
		5: "FOOD",
		6: "MYSTERY",
		7: "RUMOR",
		8: "PEACEFUL",
		9: "CNT",
	}
	Hashtag_value = map[string]int32{
		"SKYSCRAPER": 0,
		"SIGHT":      1,
		"SLUM":       2,
		"SILENT":     3,
		"NOISY":      4,
		"FOOD":       5,
		"MYSTERY":    6,
		"RUMOR":      7,
		"PEACEFUL":   8,
		"CNT":        9,
	}
)

func (e Hashtag) String() string {
	return
}

func GetHashtag(s string) Hashtag {
	return
}

type Hashtag_Variable int

const (
	Hashtag_VariableRAIN Hashtag_Variable = iota
	Hashtag_VariableSTORM
	Hashtag_VariableSNOW
	Hashtag_VariableFESTIVAL
	Hashtag_VariableBREEZE
	Hashtag_VariableFIRE
	Hashtag_VariableSTAR_SHOWER
	Hashtag_VariableCNT
)

var (
	Hashtag_Variable_name = map[int32]string{
		0: "RAIN",
		1: "STORM",
		2: "SNOW",
		3: "FESTIVAL",
		4: "BREEZE",
		5: "FIRE",
		6: "STAR_SHOWER",
		7: "CNT",
	}
	Hashtag_Variable_value = map[string]int32{
		"RAIN":        0,
		"STORM":       1,
		"SNOW":        2,
		"FESTIVAL":    3,
		"BREEZE":      4,
		"FIRE":        5,
		"STAR_SHOWER": 6,
		"CNT":         7,
	}
)

func (e Hashtag_Variable) String() string {
	return
}

func GetHashtag_Variable(s string) Hashtag_Variable {
	return
}

// COA_Skill
type Skill_Type int

const (
	Skill_TypeULTIMATE Skill_Type = iota
	Skill_TypeACTIVE
	Skill_TypePASSIVE
	Skill_TypeMOVEMENT
	Skill_TypeBASIC
	Skill_TypeLEADER
	Skill_TypeCONDITIONAL
	Skill_TypeCNT
)

var (
	Skill_Type_name = map[int32]string{
		0: "ULTIMATE",
		1: "ACTIVE",
		2: "PASSIVE",
		3: "MOVEMENT",
		4: "BASIC",
		5: "LEADER",
		6: "CONDITIONAL",
		7: "CNT",
	}
	Skill_Type_value = map[string]int32{
		"ULTIMATE":    0,
		"ACTIVE":      1,
		"PASSIVE":     2,
		"MOVEMENT":    3,
		"BASIC":       4,
		"LEADER":      5,
		"CONDITIONAL": 6,
		"CNT":         7,
	}
)

func (e Skill_Type) String() string {
	return
}

func GetSkill_Type(s string) Skill_Type {
	return
}

type Carrier_Trigger int

const (
	Carrier_TriggerCONNECT Carrier_Trigger = iota
	Carrier_TriggerRELEASE
	Carrier_TriggerCNT
)

var (
	Carrier_Trigger_name = map[int32]string{
		0: "CONNECT",
		1: "RELEASE",
		2: "CNT",
	}
	Carrier_Trigger_value = map[string]int32{
		"CONNECT": 0,
		"RELEASE": 1,
		"CNT":     2,
	}
)

func (e Carrier_Trigger) String() string {
	return
}

func GetCarrier_Trigger(s string) Carrier_Trigger {
	return
}

type Carrier_Velocity int

const (
	Carrier_VelocityFAST Carrier_Velocity = iota
	Carrier_VelocityAVERAGE
	Carrier_VelocitySLOW
	Carrier_VelocityINSTANT
	Carrier_VelocityCONSTANT
	Carrier_VelocityCNT
)

var (
	Carrier_Velocity_name = map[int32]string{
		0: "FAST",
		1: "AVERAGE",
		2: "SLOW",
		3: "INSTANT",
		4: "CONSTANT",
		5: "CNT",
	}
	Carrier_Velocity_value = map[string]int32{
		"FAST":     0,
		"AVERAGE":  1,
		"SLOW":     2,
		"INSTANT":  3,
		"CONSTANT": 4,
		"CNT":      5,
	}
)

func (e Carrier_Velocity) String() string {
	return
}

func GetCarrier_Velocity(s string) Carrier_Velocity {
	return
}

type Enable_Cond int

const (
	Enable_CondNONE Enable_Cond = iota
	Enable_CondTIME
	Enable_CondCRIT
	Enable_CondHIT
	Enable_CondTARGET_HAS_STATUSEFFECT
	Enable_CondSELF_HAS_STATUSEFFECT
	Enable_CondTARGET_HAS_STACKS
	Enable_CondSELF_HAS_STACKS
	Enable_CondRANDOM_CHANCE
	Enable_CondSTACK_COUNT
	Enable_CondTARGET_ALLY_HP_LESS_THAN
	Enable_CondTARGET_HP_LESS_THAN
	Enable_CondLAUNCH
	Enable_CondCNT
)

var (
	Enable_Cond_name = map[int32]string{
		0:  "NONE",
		1:  "TIME",
		2:  "CRIT",
		3:  "HIT",
		4:  "TARGET_HAS_STATUSEFFECT",
		5:  "SELF_HAS_STATUSEFFECT",
		6:  "TARGET_HAS_STACKS",
		7:  "SELF_HAS_STACKS",
		8:  "RANDOM_CHANCE",
		9:  "STACK_COUNT",
		10: "TARGET_ALLY_HP_LESS_THAN",
		11: "TARGET_HP_LESS_THAN",
		12: "LAUNCH",
		13: "CNT",
	}
	Enable_Cond_value = map[string]int32{
		"NONE":                     0,
		"TIME":                     1,
		"CRIT":                     2,
		"HIT":                      3,
		"TARGET_HAS_STATUSEFFECT":  4,
		"SELF_HAS_STATUSEFFECT":    5,
		"TARGET_HAS_STACKS":        6,
		"SELF_HAS_STACKS":          7,
		"RANDOM_CHANCE":            8,
		"STACK_COUNT":              9,
		"TARGET_ALLY_HP_LESS_THAN": 10,
		"TARGET_HP_LESS_THAN":      11,
		"LAUNCH":                   12,
		"CNT":                      13,
	}
)

func (e Enable_Cond) String() string {
	return
}

func GetEnable_Cond(s string) Enable_Cond {
	return
}

type Target int

const (
	TargetSELF Target = iota
	TargetALLY
	TargetENEMY
	TargetNOT_SELF_ALLY
	TargetCNT
)

var (
	Target_name = map[int32]string{
		0: "SELF",
		1: "ALLY",
		2: "ENEMY",
		3: "NOT_SELF_ALLY",
		4: "CNT",
	}
	Target_value = map[string]int32{
		"SELF":          0,
		"ALLY":          1,
		"ENEMY":         2,
		"NOT_SELF_ALLY": 3,
		"CNT":           4,
	}
)

func (e Target) String() string {
	return
}

func GetTarget(s string) Target {
	return
}

type Result_Time int

const (
	Result_TimeSTARTCASTING Result_Time = iota
	Result_TimeENDCASTING
	Result_TimeCNT
)

var (
	Result_Time_name = map[int32]string{
		0: "STARTCASTING",
		1: "ENDCASTING",
		2: "CNT",
	}
	Result_Time_value = map[string]int32{
		"STARTCASTING": 0,
		"ENDCASTING":   1,
		"CNT":          2,
	}
)

func (e Result_Time) String() string {
	return
}

func GetResult_Time(s string) Result_Time {
	return
}

type Target_Condition int

const (
	Target_ConditionSTUN Target_Condition = iota
	Target_ConditionFROZEN
	Target_ConditionLOW_HP
	Target_ConditionSTATUSEFFECT_3_OVER
	Target_ConditionCNT
)

var (
	Target_Condition_name = map[int32]string{
		0: "STUN",
		1: "FROZEN",
		2: "LOW_HP",
		3: "STATUSEFFECT_3_OVER",
		4: "CNT",
	}
	Target_Condition_value = map[string]int32{
		"STUN":                0,
		"FROZEN":              1,
		"LOW_HP":              2,
		"STATUSEFFECT_3_OVER": 3,
		"CNT":                 4,
	}
)

func (e Target_Condition) String() string {
	return
}

func GetTarget_Condition(s string) Target_Condition {
	return
}

type Order_Type int

const (
	Order_TypeCLOSEBY Order_Type = iota
	Order_TypeCNT
)

var (
	Order_Type_name = map[int32]string{
		0: "CLOSEBY",
		1: "CNT",
	}
	Order_Type_value = map[string]int32{
		"CLOSEBY": 0,
		"CNT":     1,
	}
)

func (e Order_Type) String() string {
	return
}

func GetOrder_Type(s string) Order_Type {
	return
}

type Stat_Subtype int

const (
	Stat_SubtypeCURRENT Stat_Subtype = iota
	Stat_SubtypeMAX
	Stat_SubtypePROCESSED
	Stat_SubtypeCNT
)

var (
	Stat_Subtype_name = map[int32]string{
		0: "CURRENT",
		1: "MAX",
		2: "PROCESSED",
		3: "CNT",
	}
	Stat_Subtype_value = map[string]int32{
		"CURRENT":   0,
		"MAX":       1,
		"PROCESSED": 2,
		"CNT":       3,
	}
)

func (e Stat_Subtype) String() string {
	return
}

func GetStat_Subtype(s string) Stat_Subtype {
	return
}

type Affect_Type int

const (
	Affect_TypeINCREASE Affect_Type = iota
	Affect_TypeDECREASE
	Affect_TypeFULL
	Affect_TypeZERO
	Affect_TypeCNT
)

var (
	Affect_Type_name = map[int32]string{
		0: "INCREASE",
		1: "DECREASE",
		2: "FULL",
		3: "ZERO",
		4: "CNT",
	}
	Affect_Type_value = map[string]int32{
		"INCREASE": 0,
		"DECREASE": 1,
		"FULL":     2,
		"ZERO":     3,
		"CNT":      4,
	}
)

func (e Affect_Type) String() string {
	return
}

func GetAffect_Type(s string) Affect_Type {
	return
}

type Skill_Trigger int

const (
	Skill_TriggerNEXT_NODE Skill_Trigger = iota
	Skill_TriggerBASIC_ATTACK
	Skill_TriggerGET_HIT
	Skill_TriggerRANDOM_CHANCE
	Skill_TriggerALLY_LEFT
	Skill_TriggerLEADER
	Skill_TriggerCNT
)

var (
	Skill_Trigger_name = map[int32]string{
		0: "NEXT_NODE",
		1: "BASIC_ATTACK",
		2: "GET_HIT",
		3: "RANDOM_CHANCE",
		4: "ALLY_LEFT",
		5: "LEADER",
		6: "CNT",
	}
	Skill_Trigger_value = map[string]int32{
		"NEXT_NODE":     0,
		"BASIC_ATTACK":  1,
		"GET_HIT":       2,
		"RANDOM_CHANCE": 3,
		"ALLY_LEFT":     4,
		"LEADER":        5,
		"CNT":           6,
	}
)

func (e Skill_Trigger) String() string {
	return
}

func GetSkill_Trigger(s string) Skill_Trigger {
	return
}

type Cost_Type int

const (
	Cost_TypeSTACK Cost_Type = iota
	Cost_TypeCNT
)

var (
	Cost_Type_name = map[int32]string{
		0: "STACK",
		1: "CNT",
	}
	Cost_Type_value = map[string]int32{
		"STACK": 0,
		"CNT":   1,
	}
)

func (e Cost_Type) String() string {
	return
}

func GetCost_Type(s string) Cost_Type {
	return
}

type Effect_Category int

const (
	Effect_CategoryINSTANT Effect_Category = iota
	Effect_CategoryMOVE
	Effect_CategoryLASTING
	Effect_CategoryNEG_STATUS_EFFECT
	Effect_CategoryPOS_STATUS_EFFECT
	Effect_CategorySTAT_INCREASE
	Effect_CategorySTAT_DECREASE
	Effect_CategoryCNT
)

var (
	Effect_Category_name = map[int32]string{
		0: "INSTANT",
		1: "MOVE",
		2: "LASTING",
		3: "NEG_STATUS_EFFECT",
		4: "POS_STATUS_EFFECT",
		5: "STAT_INCREASE",
		6: "STAT_DECREASE",
		7: "CNT",
	}
	Effect_Category_value = map[string]int32{
		"INSTANT":           0,
		"MOVE":              1,
		"LASTING":           2,
		"NEG_STATUS_EFFECT": 3,
		"POS_STATUS_EFFECT": 4,
		"STAT_INCREASE":     5,
		"STAT_DECREASE":     6,
		"CNT":               7,
	}
)

func (e Effect_Category) String() string {
	return
}

func GetEffect_Category(s string) Effect_Category {
	return
}

type Remove_Cond int

const (
	Remove_CondGET_HIT Remove_Cond = iota
	Remove_CondCNT
)

var (
	Remove_Cond_name = map[int32]string{
		0: "GET_HIT",
		1: "CNT",
	}
	Remove_Cond_value = map[string]int32{
		"GET_HIT": 0,
		"CNT":     1,
	}
)

func (e Remove_Cond) String() string {
	return
}

func GetRemove_Cond(s string) Remove_Cond {
	return
}

type Skill_Subtype int

const (
	Skill_SubtypeMELEE Skill_Subtype = iota
	Skill_SubtypePROJECTILE
	Skill_SubtypeEFFECT
	Skill_SubtypeRADIAL
	Skill_SubtypeCNT
)

var (
	Skill_Subtype_name = map[int32]string{
		0: "MELEE",
		1: "PROJECTILE",
		2: "EFFECT",
		3: "RADIAL",
		4: "CNT",
	}
	Skill_Subtype_value = map[string]int32{
		"MELEE":      0,
		"PROJECTILE": 1,
		"EFFECT":     2,
		"RADIAL":     3,
		"CNT":        4,
	}
)

func (e Skill_Subtype) String() string {
	return
}

func GetSkill_Subtype(s string) Skill_Subtype {
	return
}

type Resource_Type int

const (
	Resource_TypeCOMMON_GRADE_BG Resource_Type = iota
	Resource_TypeCOMMON_GRADE_TEXT
	Resource_TypeCNT
)

var (
	Resource_Type_name = map[int32]string{
		0: "COMMON_GRADE_BG",
		1: "COMMON_GRADE_TEXT",
		2: "CNT",
	}
	Resource_Type_value = map[string]int32{
		"COMMON_GRADE_BG":   0,
		"COMMON_GRADE_TEXT": 1,
		"CNT":               2,
	}
)

func (e Resource_Type) String() string {
	return
}

func GetResource_Type(s string) Resource_Type {
	return
}

type Common_Grade int

const (
	Common_GradeNORMAL Common_Grade = iota
	Common_GradeRARE
	Common_GradeEPIC
	Common_GradeLEGEND
	Common_GradeMYTH
	Common_GradeCNT
)

var (
	Common_Grade_name = map[int32]string{
		0: "NORMAL",
		1: "RARE",
		2: "EPIC",
		3: "LEGEND",
		4: "MYTH",
		5: "CNT",
	}
	Common_Grade_value = map[string]int32{
		"NORMAL": 0,
		"RARE":   1,
		"EPIC":   2,
		"LEGEND": 3,
		"MYTH":   4,
		"CNT":    5,
	}
)

func (e Common_Grade) String() string {
	return
}

func GetCommon_Grade(s string) Common_Grade {
	return
}
