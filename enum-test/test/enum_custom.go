package test

// R4_Table
type CommonType int

const (
	CommonTypeASSET CommonType = iota
	CommonTypeCHARACTER
	CommonTypeSTARGEM
	CommonTypeITEM
	CommonTypeCRAFTING
	CommonTypeSTORY
	CommonTypeAFFECTION
	CommonTypeCNT
)

func (e CommonType) String() string {
	switch e {
	case CommonTypeASSET:
		return "ASSET"
	case CommonTypeCHARACTER:
		return "CHARACTER"
	case CommonTypeSTARGEM:
		return "STARGEM"
	case CommonTypeITEM:
		return "ITEM"
	case CommonTypeCRAFTING:
		return "CRAFTING"
	case CommonTypeSTORY:
		return "STORY"
	case CommonTypeAFFECTION:
		return "AFFECTION"
	case CommonTypeCNT:
		return "CNT"
	}
	return ""
}

func GetCommonType(s string) CommonType {
	switch s {
	case "ASSET":
		return CommonTypeASSET
	case "CHARACTER":
		return CommonTypeCHARACTER
	case "STARGEM":
		return CommonTypeSTARGEM
	case "ITEM":
		return CommonTypeITEM
	case "CRAFTING":
		return CommonTypeCRAFTING
	case "STORY":
		return CommonTypeSTORY
	case "AFFECTION":
		return CommonTypeAFFECTION
	case "CNT":
		return CommonTypeCNT
	}
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

func (e Asset) String() string {
	switch e {
	case AssetGOLD:
		return "GOLD"
	case AssetCRYSTAL:
		return "CRYSTAL"
	case AssetMINERAL:
		return "MINERAL"
	case AssetESSENCE:
		return "ESSENCE"
	case AssetJEWEL:
		return "JEWEL"
	case AssetMEAT:
		return "MEAT"
	case AssetHERB:
		return "HERB"
	case AssetSTARLIGHT:
		return "STARLIGHT"
	case AssetRARE_MINERAL:
		return "RARE_MINERAL"
	case AssetRARE_ESSENCE:
		return "RARE_ESSENCE"
	case AssetRARE_JEWEL:
		return "RARE_JEWEL"
	case AssetRARE_MEAT:
		return "RARE_MEAT"
	case AssetRARE_HERB:
		return "RARE_HERB"
	case AssetRARE_STARLIGHT:
		return "RARE_STARLIGHT"
	case AssetCNT:
		return "CNT"
	}
	return ""
}

func GetAsset(s string) Asset {
	switch s {
	case "GOLD":
		return AssetGOLD
	case "CRYSTAL":
		return AssetCRYSTAL
	case "MINERAL":
		return AssetMINERAL
	case "ESSENCE":
		return AssetESSENCE
	case "JEWEL":
		return AssetJEWEL
	case "MEAT":
		return AssetMEAT
	case "HERB":
		return AssetHERB
	case "STARLIGHT":
		return AssetSTARLIGHT
	case "RARE_MINERAL":
		return AssetRARE_MINERAL
	case "RARE_ESSENCE":
		return AssetRARE_ESSENCE
	case "RARE_JEWEL":
		return AssetRARE_JEWEL
	case "RARE_MEAT":
		return AssetRARE_MEAT
	case "RARE_HERB":
		return AssetRARE_HERB
	case "RARE_STARLIGHT":
		return AssetRARE_STARLIGHT
	case "CNT":
		return AssetCNT
	}
	return -1
}

type AssetGrade int

const (
	AssetGradeNORMAL AssetGrade = iota
	AssetGradeRARE
	AssetGradeEPIC
	AssetGradeLEGEND
	AssetGradeMYTH
	AssetGradeCNT
)

func (e AssetGrade) String() string {
	switch e {
	case AssetGradeNORMAL:
		return "NORMAL"
	case AssetGradeRARE:
		return "RARE"
	case AssetGradeEPIC:
		return "EPIC"
	case AssetGradeLEGEND:
		return "LEGEND"
	case AssetGradeMYTH:
		return "MYTH"
	case AssetGradeCNT:
		return "CNT"
	}
	return ""
}

func GetAssetGrade(s string) AssetGrade {
	switch s {
	case "NORMAL":
		return AssetGradeNORMAL
	case "RARE":
		return AssetGradeRARE
	case "EPIC":
		return AssetGradeEPIC
	case "LEGEND":
		return AssetGradeLEGEND
	case "MYTH":
		return AssetGradeMYTH
	case "CNT":
		return AssetGradeCNT
	}
	return -1
}

type CharacterSpecies int

const (
	CharacterSpeciesANGEL CharacterSpecies = iota
	CharacterSpeciesDEVIL
	CharacterSpeciesDRAGON
	CharacterSpeciesBEAST
	CharacterSpeciesCNT
)

func (e CharacterSpecies) String() string {
	switch e {
	case CharacterSpeciesANGEL:
		return "ANGEL"
	case CharacterSpeciesDEVIL:
		return "DEVIL"
	case CharacterSpeciesDRAGON:
		return "DRAGON"
	case CharacterSpeciesBEAST:
		return "BEAST"
	case CharacterSpeciesCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterSpecies(s string) CharacterSpecies {
	switch s {
	case "ANGEL":
		return CharacterSpeciesANGEL
	case "DEVIL":
		return CharacterSpeciesDEVIL
	case "DRAGON":
		return CharacterSpeciesDRAGON
	case "BEAST":
		return CharacterSpeciesBEAST
	case "CNT":
		return CharacterSpeciesCNT
	}
	return -1
}

type CharacterClass int

const (
	CharacterClassWARRIOR CharacterClass = iota
	CharacterClassRANGER
	CharacterClassASSASSIN
	CharacterClassKNIGHT
	CharacterClassWIZARD
	CharacterClassPRIEST
	CharacterClassBARD
	CharacterClassBATTLE_MAGE
	CharacterClassCNT
)

func (e CharacterClass) String() string {
	switch e {
	case CharacterClassWARRIOR:
		return "WARRIOR"
	case CharacterClassRANGER:
		return "RANGER"
	case CharacterClassASSASSIN:
		return "ASSASSIN"
	case CharacterClassKNIGHT:
		return "KNIGHT"
	case CharacterClassWIZARD:
		return "WIZARD"
	case CharacterClassPRIEST:
		return "PRIEST"
	case CharacterClassBARD:
		return "BARD"
	case CharacterClassBATTLE_MAGE:
		return "BATTLE_MAGE"
	case CharacterClassCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterClass(s string) CharacterClass {
	switch s {
	case "WARRIOR":
		return CharacterClassWARRIOR
	case "RANGER":
		return CharacterClassRANGER
	case "ASSASSIN":
		return CharacterClassASSASSIN
	case "KNIGHT":
		return CharacterClassKNIGHT
	case "WIZARD":
		return CharacterClassWIZARD
	case "PRIEST":
		return CharacterClassPRIEST
	case "BARD":
		return CharacterClassBARD
	case "BATTLE_MAGE":
		return CharacterClassBATTLE_MAGE
	case "CNT":
		return CharacterClassCNT
	}
	return -1
}

type CharacterProperty int

const (
	CharacterPropertyDARK CharacterProperty = iota
	CharacterPropertyFIRE
	CharacterPropertyWATER
	CharacterPropertyFOREST
	CharacterPropertyELECTRIC
	CharacterPropertyEARTH
	CharacterPropertyLIGHT
	CharacterPropertyCNT
)

func (e CharacterProperty) String() string {
	switch e {
	case CharacterPropertyDARK:
		return "DARK"
	case CharacterPropertyFIRE:
		return "FIRE"
	case CharacterPropertyWATER:
		return "WATER"
	case CharacterPropertyFOREST:
		return "FOREST"
	case CharacterPropertyELECTRIC:
		return "ELECTRIC"
	case CharacterPropertyEARTH:
		return "EARTH"
	case CharacterPropertyLIGHT:
		return "LIGHT"
	case CharacterPropertyCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterProperty(s string) CharacterProperty {
	switch s {
	case "DARK":
		return CharacterPropertyDARK
	case "FIRE":
		return CharacterPropertyFIRE
	case "WATER":
		return CharacterPropertyWATER
	case "FOREST":
		return CharacterPropertyFOREST
	case "ELECTRIC":
		return CharacterPropertyELECTRIC
	case "EARTH":
		return CharacterPropertyEARTH
	case "LIGHT":
		return CharacterPropertyLIGHT
	case "CNT":
		return CharacterPropertyCNT
	}
	return -1
}

type CharacterGrade int

const (
	CharacterGradeNORMAL CharacterGrade = iota
	CharacterGradeRARE
	CharacterGradeEPIC
	CharacterGradeLEGEND
	CharacterGradeMYTH
	CharacterGradeCNT
)

func (e CharacterGrade) String() string {
	switch e {
	case CharacterGradeNORMAL:
		return "NORMAL"
	case CharacterGradeRARE:
		return "RARE"
	case CharacterGradeEPIC:
		return "EPIC"
	case CharacterGradeLEGEND:
		return "LEGEND"
	case CharacterGradeMYTH:
		return "MYTH"
	case CharacterGradeCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterGrade(s string) CharacterGrade {
	switch s {
	case "NORMAL":
		return CharacterGradeNORMAL
	case "RARE":
		return CharacterGradeRARE
	case "EPIC":
		return CharacterGradeEPIC
	case "LEGEND":
		return CharacterGradeLEGEND
	case "MYTH":
		return CharacterGradeMYTH
	case "CNT":
		return CharacterGradeCNT
	}
	return -1
}

type CharacterSkill int

const (
	CharacterSkillCLASS CharacterSkill = iota
	CharacterSkillLEADER
	CharacterSkillBASIC
	CharacterSkillACTIVE
	CharacterSkillULTIMATE
	CharacterSkillPASSIVE
	CharacterSkillCNT
)

func (e CharacterSkill) String() string {
	switch e {
	case CharacterSkillCLASS:
		return "CLASS"
	case CharacterSkillLEADER:
		return "LEADER"
	case CharacterSkillBASIC:
		return "BASIC"
	case CharacterSkillACTIVE:
		return "ACTIVE"
	case CharacterSkillULTIMATE:
		return "ULTIMATE"
	case CharacterSkillPASSIVE:
		return "PASSIVE"
	case CharacterSkillCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterSkill(s string) CharacterSkill {
	switch s {
	case "CLASS":
		return CharacterSkillCLASS
	case "LEADER":
		return CharacterSkillLEADER
	case "BASIC":
		return CharacterSkillBASIC
	case "ACTIVE":
		return CharacterSkillACTIVE
	case "ULTIMATE":
		return CharacterSkillULTIMATE
	case "PASSIVE":
		return CharacterSkillPASSIVE
	case "CNT":
		return CharacterSkillCNT
	}
	return -1
}

type CharacterActivity int

const (
	CharacterActivityNONE CharacterActivity = iota
	CharacterActivityBATTLE
	CharacterActivityGUARD
	CharacterActivityCNT
)

func (e CharacterActivity) String() string {
	switch e {
	case CharacterActivityNONE:
		return "NONE"
	case CharacterActivityBATTLE:
		return "BATTLE"
	case CharacterActivityGUARD:
		return "GUARD"
	case CharacterActivityCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterActivity(s string) CharacterActivity {
	switch s {
	case "NONE":
		return CharacterActivityNONE
	case "BATTLE":
		return CharacterActivityBATTLE
	case "GUARD":
		return CharacterActivityGUARD
	case "CNT":
		return CharacterActivityCNT
	}
	return -1
}

type Item int

const (
	ItemNONBATTLE Item = iota
	ItemBATTLE
	ItemCNT
)

func (e Item) String() string {
	switch e {
	case ItemNONBATTLE:
		return "NONBATTLE"
	case ItemBATTLE:
		return "BATTLE"
	case ItemCNT:
		return "CNT"
	}
	return ""
}

func GetItem(s string) Item {
	switch s {
	case "NONBATTLE":
		return ItemNONBATTLE
	case "BATTLE":
		return ItemBATTLE
	case "CNT":
		return ItemCNT
	}
	return -1
}

type ItemSub int

const (
	ItemSubCHARACTER_EXP ItemSub = iota
	ItemSubEQUIPMENT_EXP
	ItemSubAFFECTION_EXP
	ItemSubCHARACTER_STAMINA
	ItemSubCRAFTING_STAMINA
	ItemSubBATTLE
	ItemSubCNT
)

func (e ItemSub) String() string {
	switch e {
	case ItemSubCHARACTER_EXP:
		return "CHARACTER_EXP"
	case ItemSubEQUIPMENT_EXP:
		return "EQUIPMENT_EXP"
	case ItemSubAFFECTION_EXP:
		return "AFFECTION_EXP"
	case ItemSubCHARACTER_STAMINA:
		return "CHARACTER_STAMINA"
	case ItemSubCRAFTING_STAMINA:
		return "CRAFTING_STAMINA"
	case ItemSubBATTLE:
		return "BATTLE"
	case ItemSubCNT:
		return "CNT"
	}
	return ""
}

func GetItemSub(s string) ItemSub {
	switch s {
	case "CHARACTER_EXP":
		return ItemSubCHARACTER_EXP
	case "EQUIPMENT_EXP":
		return ItemSubEQUIPMENT_EXP
	case "AFFECTION_EXP":
		return ItemSubAFFECTION_EXP
	case "CHARACTER_STAMINA":
		return ItemSubCHARACTER_STAMINA
	case "CRAFTING_STAMINA":
		return ItemSubCRAFTING_STAMINA
	case "BATTLE":
		return ItemSubBATTLE
	case "CNT":
		return ItemSubCNT
	}
	return -1
}

type ItemGrade int

const (
	ItemGradeNORMAL ItemGrade = iota
	ItemGradeRARE
	ItemGradeEPIC
	ItemGradeLEGEND
	ItemGradeMYTH
	ItemGradeCNT
)

func (e ItemGrade) String() string {
	switch e {
	case ItemGradeNORMAL:
		return "NORMAL"
	case ItemGradeRARE:
		return "RARE"
	case ItemGradeEPIC:
		return "EPIC"
	case ItemGradeLEGEND:
		return "LEGEND"
	case ItemGradeMYTH:
		return "MYTH"
	case ItemGradeCNT:
		return "CNT"
	}
	return ""
}

func GetItemGrade(s string) ItemGrade {
	switch s {
	case "NORMAL":
		return ItemGradeNORMAL
	case "RARE":
		return ItemGradeRARE
	case "EPIC":
		return ItemGradeEPIC
	case "LEGEND":
		return ItemGradeLEGEND
	case "MYTH":
		return ItemGradeMYTH
	case "CNT":
		return ItemGradeCNT
	}
	return -1
}

type EquipmentType int

const (
	EquipmentTypeSTARGEM EquipmentType = iota
	EquipmentTypeCNT
)

func (e EquipmentType) String() string {
	switch e {
	case EquipmentTypeSTARGEM:
		return "STARGEM"
	case EquipmentTypeCNT:
		return "CNT"
	}
	return ""
}

func GetEquipmentType(s string) EquipmentType {
	switch s {
	case "STARGEM":
		return EquipmentTypeSTARGEM
	case "CNT":
		return EquipmentTypeCNT
	}
	return -1
}

type EquipmentProperty int

const (
	EquipmentPropertySTARGEM_SHEEP EquipmentProperty = iota
	EquipmentPropertySTARGEM_BULL
	EquipmentPropertySTARGEM_TWINS
	EquipmentPropertySTARGEM_CRAB
	EquipmentPropertySTARGEM_LION
	EquipmentPropertySTARGEM_GIRL
	EquipmentPropertySTARGEM_SCALES
	EquipmentPropertySTARGEM_SCORPION
	EquipmentPropertySTARGEM_ARCHER
	EquipmentPropertySTARGEM_GOAT
	EquipmentPropertySTARGEM_WATER
	EquipmentPropertySTARGEM_FISH
	EquipmentPropertySTARGEM_GREATBEAR
	EquipmentPropertySTARGEM_SNAKE
	EquipmentPropertySTARGEM_CRUX
	EquipmentPropertyCNT
)

func (e EquipmentProperty) String() string {
	switch e {
	case EquipmentPropertySTARGEM_SHEEP:
		return "STARGEM_SHEEP"
	case EquipmentPropertySTARGEM_BULL:
		return "STARGEM_BULL"
	case EquipmentPropertySTARGEM_TWINS:
		return "STARGEM_TWINS"
	case EquipmentPropertySTARGEM_CRAB:
		return "STARGEM_CRAB"
	case EquipmentPropertySTARGEM_LION:
		return "STARGEM_LION"
	case EquipmentPropertySTARGEM_GIRL:
		return "STARGEM_GIRL"
	case EquipmentPropertySTARGEM_SCALES:
		return "STARGEM_SCALES"
	case EquipmentPropertySTARGEM_SCORPION:
		return "STARGEM_SCORPION"
	case EquipmentPropertySTARGEM_ARCHER:
		return "STARGEM_ARCHER"
	case EquipmentPropertySTARGEM_GOAT:
		return "STARGEM_GOAT"
	case EquipmentPropertySTARGEM_WATER:
		return "STARGEM_WATER"
	case EquipmentPropertySTARGEM_FISH:
		return "STARGEM_FISH"
	case EquipmentPropertySTARGEM_GREATBEAR:
		return "STARGEM_GREATBEAR"
	case EquipmentPropertySTARGEM_SNAKE:
		return "STARGEM_SNAKE"
	case EquipmentPropertySTARGEM_CRUX:
		return "STARGEM_CRUX"
	case EquipmentPropertyCNT:
		return "CNT"
	}
	return ""
}

func GetEquipmentProperty(s string) EquipmentProperty {
	switch s {
	case "STARGEM_SHEEP":
		return EquipmentPropertySTARGEM_SHEEP
	case "STARGEM_BULL":
		return EquipmentPropertySTARGEM_BULL
	case "STARGEM_TWINS":
		return EquipmentPropertySTARGEM_TWINS
	case "STARGEM_CRAB":
		return EquipmentPropertySTARGEM_CRAB
	case "STARGEM_LION":
		return EquipmentPropertySTARGEM_LION
	case "STARGEM_GIRL":
		return EquipmentPropertySTARGEM_GIRL
	case "STARGEM_SCALES":
		return EquipmentPropertySTARGEM_SCALES
	case "STARGEM_SCORPION":
		return EquipmentPropertySTARGEM_SCORPION
	case "STARGEM_ARCHER":
		return EquipmentPropertySTARGEM_ARCHER
	case "STARGEM_GOAT":
		return EquipmentPropertySTARGEM_GOAT
	case "STARGEM_WATER":
		return EquipmentPropertySTARGEM_WATER
	case "STARGEM_FISH":
		return EquipmentPropertySTARGEM_FISH
	case "STARGEM_GREATBEAR":
		return EquipmentPropertySTARGEM_GREATBEAR
	case "STARGEM_SNAKE":
		return EquipmentPropertySTARGEM_SNAKE
	case "STARGEM_CRUX":
		return EquipmentPropertySTARGEM_CRUX
	case "CNT":
		return EquipmentPropertyCNT
	}
	return -1
}

type EquipmentSlot int

const (
	EquipmentSlotSTARGEM_SLOT_0 EquipmentSlot = iota
	EquipmentSlotSTARGEM_SLOT_1
	EquipmentSlotSTARGEM_SLOT_2
	EquipmentSlotSTARGEM_SLOT_3
	EquipmentSlotSTARGEM_SLOT_4
	EquipmentSlotSTARGEM_SLOT_5
	EquipmentSlotCNT
)

func (e EquipmentSlot) String() string {
	switch e {
	case EquipmentSlotSTARGEM_SLOT_0:
		return "STARGEM_SLOT_0"
	case EquipmentSlotSTARGEM_SLOT_1:
		return "STARGEM_SLOT_1"
	case EquipmentSlotSTARGEM_SLOT_2:
		return "STARGEM_SLOT_2"
	case EquipmentSlotSTARGEM_SLOT_3:
		return "STARGEM_SLOT_3"
	case EquipmentSlotSTARGEM_SLOT_4:
		return "STARGEM_SLOT_4"
	case EquipmentSlotSTARGEM_SLOT_5:
		return "STARGEM_SLOT_5"
	case EquipmentSlotCNT:
		return "CNT"
	}
	return ""
}

func GetEquipmentSlot(s string) EquipmentSlot {
	switch s {
	case "STARGEM_SLOT_0":
		return EquipmentSlotSTARGEM_SLOT_0
	case "STARGEM_SLOT_1":
		return EquipmentSlotSTARGEM_SLOT_1
	case "STARGEM_SLOT_2":
		return EquipmentSlotSTARGEM_SLOT_2
	case "STARGEM_SLOT_3":
		return EquipmentSlotSTARGEM_SLOT_3
	case "STARGEM_SLOT_4":
		return EquipmentSlotSTARGEM_SLOT_4
	case "STARGEM_SLOT_5":
		return EquipmentSlotSTARGEM_SLOT_5
	case "CNT":
		return EquipmentSlotCNT
	}
	return -1
}

type EquipmentGrade int

const (
	EquipmentGradeNORMAL EquipmentGrade = iota
	EquipmentGradeRARE
	EquipmentGradeEPIC
	EquipmentGradeLEGEND
	EquipmentGradeMYTH
	EquipmentGradeCNT
)

func (e EquipmentGrade) String() string {
	switch e {
	case EquipmentGradeNORMAL:
		return "NORMAL"
	case EquipmentGradeRARE:
		return "RARE"
	case EquipmentGradeEPIC:
		return "EPIC"
	case EquipmentGradeLEGEND:
		return "LEGEND"
	case EquipmentGradeMYTH:
		return "MYTH"
	case EquipmentGradeCNT:
		return "CNT"
	}
	return ""
}

func GetEquipmentGrade(s string) EquipmentGrade {
	switch s {
	case "NORMAL":
		return EquipmentGradeNORMAL
	case "RARE":
		return EquipmentGradeRARE
	case "EPIC":
		return EquipmentGradeEPIC
	case "LEGEND":
		return EquipmentGradeLEGEND
	case "MYTH":
		return EquipmentGradeMYTH
	case "CNT":
		return EquipmentGradeCNT
	}
	return -1
}

type EquipmentAttr int

const (
	EquipmentAttrWEAR EquipmentAttr = iota
	EquipmentAttrOBTAIN
	EquipmentAttrCNT
)

func (e EquipmentAttr) String() string {
	switch e {
	case EquipmentAttrWEAR:
		return "WEAR"
	case EquipmentAttrOBTAIN:
		return "OBTAIN"
	case EquipmentAttrCNT:
		return "CNT"
	}
	return ""
}

func GetEquipmentAttr(s string) EquipmentAttr {
	switch s {
	case "WEAR":
		return EquipmentAttrWEAR
	case "OBTAIN":
		return EquipmentAttrOBTAIN
	case "CNT":
		return EquipmentAttrCNT
	}
	return -1
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

func (e Stat) String() string {
	switch e {
	case StatATK:
		return "ATK"
	case StatDEF:
		return "DEF"
	case StatHP:
		return "HP"
	case StatCRITD:
		return "CRITD"
	case StatCRIT:
		return "CRIT"
	case StatTD:
		return "TD"
	case StatREC:
		return "REC"
	case StatCDR:
		return "CDR"
	case StatSHI:
		return "SHI"
	case StatNEU:
		return "NEU"
	case StatEVA:
		return "EVA"
	case StatACC:
		return "ACC"
	case StatSERES:
		return "SERES"
	case StatATKSPD:
		return "ATKSPD"
	case StatDM:
		return "DM"
	case StatDMGRES:
		return "DMGRES"
	case StatCRUX:
		return "CRUX"
	case StatDRAIN:
		return "DRAIN"
	case StatNEUREC:
		return "NEUREC"
	case StatPERSISTANCE:
		return "PERSISTANCE"
	case StatCRITR:
		return "CRITR"
	case StatCRITDR:
		return "CRITDR"
	case StatBLOCKE:
		return "BLOCKE"
	case StatBLOCK:
		return "BLOCK"
	case StatSPD:
		return "SPD"
	case StatRANGE:
		return "RANGE"
	case StatCNT:
		return "CNT"
	}
	return ""
}

func GetStat(s string) Stat {
	switch s {
	case "ATK":
		return StatATK
	case "DEF":
		return StatDEF
	case "HP":
		return StatHP
	case "CRITD":
		return StatCRITD
	case "CRIT":
		return StatCRIT
	case "TD":
		return StatTD
	case "REC":
		return StatREC
	case "CDR":
		return StatCDR
	case "SHI":
		return StatSHI
	case "NEU":
		return StatNEU
	case "EVA":
		return StatEVA
	case "ACC":
		return StatACC
	case "SERES":
		return StatSERES
	case "ATKSPD":
		return StatATKSPD
	case "DM":
		return StatDM
	case "DMGRES":
		return StatDMGRES
	case "CRUX":
		return StatCRUX
	case "DRAIN":
		return StatDRAIN
	case "NEUREC":
		return StatNEUREC
	case "PERSISTANCE":
		return StatPERSISTANCE
	case "CRITR":
		return StatCRITR
	case "CRITDR":
		return StatCRITDR
	case "BLOCKE":
		return StatBLOCKE
	case "BLOCK":
		return StatBLOCK
	case "SPD":
		return StatSPD
	case "RANGE":
		return StatRANGE
	case "CNT":
		return StatCNT
	}
	return -1
}

type Graph int

const (
	GraphNONE Graph = iota
	GraphBELL_CURVE
	GraphMAX
	GraphMIN
	GraphCNT
)

func (e Graph) String() string {
	switch e {
	case GraphNONE:
		return "NONE"
	case GraphBELL_CURVE:
		return "BELL_CURVE"
	case GraphMAX:
		return "MAX"
	case GraphMIN:
		return "MIN"
	case GraphCNT:
		return "CNT"
	}
	return ""
}

func GetGraph(s string) Graph {
	switch s {
	case "NONE":
		return GraphNONE
	case "BELL_CURVE":
		return GraphBELL_CURVE
	case "MAX":
		return GraphMAX
	case "MIN":
		return GraphMIN
	case "CNT":
		return GraphCNT
	}
	return -1
}

type Calculation int

const (
	CalculationPLUS Calculation = iota
	CalculationMULT
	CalculationP_MULT
	CalculationCNT
)

func (e Calculation) String() string {
	switch e {
	case CalculationPLUS:
		return "PLUS"
	case CalculationMULT:
		return "MULT"
	case CalculationP_MULT:
		return "P_MULT"
	case CalculationCNT:
		return "CNT"
	}
	return ""
}

func GetCalculation(s string) Calculation {
	switch s {
	case "PLUS":
		return CalculationPLUS
	case "MULT":
		return CalculationMULT
	case "P_MULT":
		return CalculationP_MULT
	case "CNT":
		return CalculationCNT
	}
	return -1
}

type CharacterQuestTrigger int

const (
	CharacterQuestTriggerAUTO_BATTLE CharacterQuestTrigger = iota
	CharacterQuestTriggerTILE_GET
	CharacterQuestTriggerFIRST_STARGEM_GET
	CharacterQuestTriggerCNT
)

func (e CharacterQuestTrigger) String() string {
	switch e {
	case CharacterQuestTriggerAUTO_BATTLE:
		return "AUTO_BATTLE"
	case CharacterQuestTriggerTILE_GET:
		return "TILE_GET"
	case CharacterQuestTriggerFIRST_STARGEM_GET:
		return "FIRST_STARGEM_GET"
	case CharacterQuestTriggerCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterQuestTrigger(s string) CharacterQuestTrigger {
	switch s {
	case "AUTO_BATTLE":
		return CharacterQuestTriggerAUTO_BATTLE
	case "TILE_GET":
		return CharacterQuestTriggerTILE_GET
	case "FIRST_STARGEM_GET":
		return CharacterQuestTriggerFIRST_STARGEM_GET
	case "CNT":
		return CharacterQuestTriggerCNT
	}
	return -1
}

type CharacterQuestType int

const (
	CharacterQuestTypeCOLLECT CharacterQuestType = iota
	CharacterQuestTypeTILE_GET
	CharacterQuestTypeCNT
)

func (e CharacterQuestType) String() string {
	switch e {
	case CharacterQuestTypeCOLLECT:
		return "COLLECT"
	case CharacterQuestTypeTILE_GET:
		return "TILE_GET"
	case CharacterQuestTypeCNT:
		return "CNT"
	}
	return ""
}

func GetCharacterQuestType(s string) CharacterQuestType {
	switch s {
	case "COLLECT":
		return CharacterQuestTypeCOLLECT
	case "TILE_GET":
		return CharacterQuestTypeTILE_GET
	case "CNT":
		return CharacterQuestTypeCNT
	}
	return -1
}

type EquipState int

const (
	EquipStateUNEQUIP EquipState = iota
	EquipStateEQUIP
	EquipStateCNT
)

func (e EquipState) String() string {
	switch e {
	case EquipStateUNEQUIP:
		return "UNEQUIP"
	case EquipStateEQUIP:
		return "EQUIP"
	case EquipStateCNT:
		return "CNT"
	}
	return ""
}

func GetEquipState(s string) EquipState {
	switch s {
	case "UNEQUIP":
		return EquipStateUNEQUIP
	case "EQUIP":
		return EquipStateEQUIP
	case "CNT":
		return EquipStateCNT
	}
	return -1
}

type TutorialTrigger int

const (
	TutorialTriggerGAME_START TutorialTrigger = iota
	TutorialTriggerCITY_MEET
	TutorialTriggerCRAFTING_START
	TutorialTriggerCRAFTING_END
	TutorialTriggerCNT
)

func (e TutorialTrigger) String() string {
	switch e {
	case TutorialTriggerGAME_START:
		return "GAME_START"
	case TutorialTriggerCITY_MEET:
		return "CITY_MEET"
	case TutorialTriggerCRAFTING_START:
		return "CRAFTING_START"
	case TutorialTriggerCRAFTING_END:
		return "CRAFTING_END"
	case TutorialTriggerCNT:
		return "CNT"
	}
	return ""
}

func GetTutorialTrigger(s string) TutorialTrigger {
	switch s {
	case "GAME_START":
		return TutorialTriggerGAME_START
	case "CITY_MEET":
		return TutorialTriggerCITY_MEET
	case "CRAFTING_START":
		return TutorialTriggerCRAFTING_START
	case "CRAFTING_END":
		return TutorialTriggerCRAFTING_END
	case "CNT":
		return TutorialTriggerCNT
	}
	return -1
}

type RequestType int

const (
	RequestTypeASSET RequestType = iota
	RequestTypeSTARGEM
	RequestTypeITEM
	RequestTypeTILE
	RequestTypeCNT
)

func (e RequestType) String() string {
	switch e {
	case RequestTypeASSET:
		return "ASSET"
	case RequestTypeSTARGEM:
		return "STARGEM"
	case RequestTypeITEM:
		return "ITEM"
	case RequestTypeTILE:
		return "TILE"
	case RequestTypeCNT:
		return "CNT"
	}
	return ""
}

func GetRequestType(s string) RequestType {
	switch s {
	case "ASSET":
		return RequestTypeASSET
	case "STARGEM":
		return RequestTypeSTARGEM
	case "ITEM":
		return RequestTypeITEM
	case "TILE":
		return RequestTypeTILE
	case "CNT":
		return RequestTypeCNT
	}
	return -1
}

type BattleResult int

const (
	BattleResultNONE BattleResult = iota
	BattleResultLOSE
	BattleResultWIN
	BattleResultENCOUNTER
	BattleResultCNT
)

func (e BattleResult) String() string {
	switch e {
	case BattleResultNONE:
		return "NONE"
	case BattleResultLOSE:
		return "LOSE"
	case BattleResultWIN:
		return "WIN"
	case BattleResultENCOUNTER:
		return "ENCOUNTER"
	case BattleResultCNT:
		return "CNT"
	}
	return ""
}

func GetBattleResult(s string) BattleResult {
	switch s {
	case "NONE":
		return BattleResultNONE
	case "LOSE":
		return BattleResultLOSE
	case "WIN":
		return BattleResultWIN
	case "ENCOUNTER":
		return BattleResultENCOUNTER
	case "CNT":
		return BattleResultCNT
	}
	return -1
}

// COA_Worldmap
type TileType int

const (
	TileTypeSINGLE TileType = iota
	TileTypeCITY
	TileTypeRUIN
	TileTypeBASE
	TileTypeCNT
)

func (e TileType) String() string {
	switch e {
	case TileTypeSINGLE:
		return "SINGLE"
	case TileTypeCITY:
		return "CITY"
	case TileTypeRUIN:
		return "RUIN"
	case TileTypeBASE:
		return "BASE"
	case TileTypeCNT:
		return "CNT"
	}
	return ""
}

func GetTileType(s string) TileType {
	switch s {
	case "SINGLE":
		return TileTypeSINGLE
	case "CITY":
		return TileTypeCITY
	case "RUIN":
		return TileTypeRUIN
	case "BASE":
		return TileTypeBASE
	case "CNT":
		return TileTypeCNT
	}
	return -1
}

type CraftType int

const (
	CraftTypeNONE CraftType = iota
	CraftTypeSMITHERY
	CraftTypeOBSERVATORY
	CraftTypeJEWELRY
	CraftTypeALCHEMY
	CraftTypeCOOKING
	CraftTypeBASIC
	CraftTypeCNT
)

func (e CraftType) String() string {
	switch e {
	case CraftTypeNONE:
		return "NONE"
	case CraftTypeSMITHERY:
		return "SMITHERY"
	case CraftTypeOBSERVATORY:
		return "OBSERVATORY"
	case CraftTypeJEWELRY:
		return "JEWELRY"
	case CraftTypeALCHEMY:
		return "ALCHEMY"
	case CraftTypeCOOKING:
		return "COOKING"
	case CraftTypeBASIC:
		return "BASIC"
	case CraftTypeCNT:
		return "CNT"
	}
	return ""
}

func GetCraftType(s string) CraftType {
	switch s {
	case "NONE":
		return CraftTypeNONE
	case "SMITHERY":
		return CraftTypeSMITHERY
	case "OBSERVATORY":
		return CraftTypeOBSERVATORY
	case "JEWELRY":
		return CraftTypeJEWELRY
	case "ALCHEMY":
		return CraftTypeALCHEMY
	case "COOKING":
		return CraftTypeCOOKING
	case "BASIC":
		return CraftTypeBASIC
	case "CNT":
		return CraftTypeCNT
	}
	return -1
}

type CraftingGrade int

const (
	CraftingGradeNORMAL CraftingGrade = iota
	CraftingGradeRARE
	CraftingGradeEPIC
	CraftingGradeLEGEND
	CraftingGradeMYTH
	CraftingGradeCNT
)

func (e CraftingGrade) String() string {
	switch e {
	case CraftingGradeNORMAL:
		return "NORMAL"
	case CraftingGradeRARE:
		return "RARE"
	case CraftingGradeEPIC:
		return "EPIC"
	case CraftingGradeLEGEND:
		return "LEGEND"
	case CraftingGradeMYTH:
		return "MYTH"
	case CraftingGradeCNT:
		return "CNT"
	}
	return ""
}

func GetCraftingGrade(s string) CraftingGrade {
	switch s {
	case "NORMAL":
		return CraftingGradeNORMAL
	case "RARE":
		return CraftingGradeRARE
	case "EPIC":
		return CraftingGradeEPIC
	case "LEGEND":
		return CraftingGradeLEGEND
	case "MYTH":
		return CraftingGradeMYTH
	case "CNT":
		return CraftingGradeCNT
	}
	return -1
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

func (e Hashtag) String() string {
	switch e {
	case HashtagSKYSCRAPER:
		return "SKYSCRAPER"
	case HashtagSIGHT:
		return "SIGHT"
	case HashtagSLUM:
		return "SLUM"
	case HashtagSILENT:
		return "SILENT"
	case HashtagNOISY:
		return "NOISY"
	case HashtagFOOD:
		return "FOOD"
	case HashtagMYSTERY:
		return "MYSTERY"
	case HashtagRUMOR:
		return "RUMOR"
	case HashtagPEACEFUL:
		return "PEACEFUL"
	case HashtagCNT:
		return "CNT"
	}
	return ""
}

func GetHashtag(s string) Hashtag {
	switch s {
	case "SKYSCRAPER":
		return HashtagSKYSCRAPER
	case "SIGHT":
		return HashtagSIGHT
	case "SLUM":
		return HashtagSLUM
	case "SILENT":
		return HashtagSILENT
	case "NOISY":
		return HashtagNOISY
	case "FOOD":
		return HashtagFOOD
	case "MYSTERY":
		return HashtagMYSTERY
	case "RUMOR":
		return HashtagRUMOR
	case "PEACEFUL":
		return HashtagPEACEFUL
	case "CNT":
		return HashtagCNT
	}
	return -1
}

type HashtagVariable int

const (
	HashtagVariableRAIN HashtagVariable = iota
	HashtagVariableSTORM
	HashtagVariableSNOW
	HashtagVariableFESTIVAL
	HashtagVariableBREEZE
	HashtagVariableFIRE
	HashtagVariableSTAR_SHOWER
	HashtagVariableCNT
)

func (e HashtagVariable) String() string {
	switch e {
	case HashtagVariableRAIN:
		return "RAIN"
	case HashtagVariableSTORM:
		return "STORM"
	case HashtagVariableSNOW:
		return "SNOW"
	case HashtagVariableFESTIVAL:
		return "FESTIVAL"
	case HashtagVariableBREEZE:
		return "BREEZE"
	case HashtagVariableFIRE:
		return "FIRE"
	case HashtagVariableSTAR_SHOWER:
		return "STAR_SHOWER"
	case HashtagVariableCNT:
		return "CNT"
	}
	return ""
}

func GetHashtagVariable(s string) HashtagVariable {
	switch s {
	case "RAIN":
		return HashtagVariableRAIN
	case "STORM":
		return HashtagVariableSTORM
	case "SNOW":
		return HashtagVariableSNOW
	case "FESTIVAL":
		return HashtagVariableFESTIVAL
	case "BREEZE":
		return HashtagVariableBREEZE
	case "FIRE":
		return HashtagVariableFIRE
	case "STAR_SHOWER":
		return HashtagVariableSTAR_SHOWER
	case "CNT":
		return HashtagVariableCNT
	}
	return -1
}

// COA_Skill
type SkillType int

const (
	SkillTypeULTIMATE SkillType = iota
	SkillTypeACTIVE
	SkillTypePASSIVE
	SkillTypeMOVEMENT
	SkillTypeBASIC
	SkillTypeLEADER
	SkillTypeCONDITIONAL
	SkillTypeCNT
)

func (e SkillType) String() string {
	switch e {
	case SkillTypeULTIMATE:
		return "ULTIMATE"
	case SkillTypeACTIVE:
		return "ACTIVE"
	case SkillTypePASSIVE:
		return "PASSIVE"
	case SkillTypeMOVEMENT:
		return "MOVEMENT"
	case SkillTypeBASIC:
		return "BASIC"
	case SkillTypeLEADER:
		return "LEADER"
	case SkillTypeCONDITIONAL:
		return "CONDITIONAL"
	case SkillTypeCNT:
		return "CNT"
	}
	return ""
}

func GetSkillType(s string) SkillType {
	switch s {
	case "ULTIMATE":
		return SkillTypeULTIMATE
	case "ACTIVE":
		return SkillTypeACTIVE
	case "PASSIVE":
		return SkillTypePASSIVE
	case "MOVEMENT":
		return SkillTypeMOVEMENT
	case "BASIC":
		return SkillTypeBASIC
	case "LEADER":
		return SkillTypeLEADER
	case "CONDITIONAL":
		return SkillTypeCONDITIONAL
	case "CNT":
		return SkillTypeCNT
	}
	return -1
}

type CarrierTrigger int

const (
	CarrierTriggerCONNECT CarrierTrigger = iota
	CarrierTriggerRELEASE
	CarrierTriggerCNT
)

func (e CarrierTrigger) String() string {
	switch e {
	case CarrierTriggerCONNECT:
		return "CONNECT"
	case CarrierTriggerRELEASE:
		return "RELEASE"
	case CarrierTriggerCNT:
		return "CNT"
	}
	return ""
}

func GetCarrierTrigger(s string) CarrierTrigger {
	switch s {
	case "CONNECT":
		return CarrierTriggerCONNECT
	case "RELEASE":
		return CarrierTriggerRELEASE
	case "CNT":
		return CarrierTriggerCNT
	}
	return -1
}

type CarrierVelocity int

const (
	CarrierVelocityFAST CarrierVelocity = iota
	CarrierVelocityAVERAGE
	CarrierVelocitySLOW
	CarrierVelocityINSTANT
	CarrierVelocityCONSTANT
	CarrierVelocityCNT
)

func (e CarrierVelocity) String() string {
	switch e {
	case CarrierVelocityFAST:
		return "FAST"
	case CarrierVelocityAVERAGE:
		return "AVERAGE"
	case CarrierVelocitySLOW:
		return "SLOW"
	case CarrierVelocityINSTANT:
		return "INSTANT"
	case CarrierVelocityCONSTANT:
		return "CONSTANT"
	case CarrierVelocityCNT:
		return "CNT"
	}
	return ""
}

func GetCarrierVelocity(s string) CarrierVelocity {
	switch s {
	case "FAST":
		return CarrierVelocityFAST
	case "AVERAGE":
		return CarrierVelocityAVERAGE
	case "SLOW":
		return CarrierVelocitySLOW
	case "INSTANT":
		return CarrierVelocityINSTANT
	case "CONSTANT":
		return CarrierVelocityCONSTANT
	case "CNT":
		return CarrierVelocityCNT
	}
	return -1
}

type EnableCond int

const (
	EnableCondNONE EnableCond = iota
	EnableCondTIME
	EnableCondCRIT
	EnableCondHIT
	EnableCondTARGET_HAS_STATUSEFFECT
	EnableCondSELF_HAS_STATUSEFFECT
	EnableCondTARGET_HAS_STACKS
	EnableCondSELF_HAS_STACKS
	EnableCondRANDOM_CHANCE
	EnableCondSTACK_COUNT
	EnableCondTARGET_ALLY_HP_LESS_THAN
	EnableCondTARGET_HP_LESS_THAN
	EnableCondLAUNCH
	EnableCondCNT
)

func (e EnableCond) String() string {
	switch e {
	case EnableCondNONE:
		return "NONE"
	case EnableCondTIME:
		return "TIME"
	case EnableCondCRIT:
		return "CRIT"
	case EnableCondHIT:
		return "HIT"
	case EnableCondTARGET_HAS_STATUSEFFECT:
		return "TARGET_HAS_STATUSEFFECT"
	case EnableCondSELF_HAS_STATUSEFFECT:
		return "SELF_HAS_STATUSEFFECT"
	case EnableCondTARGET_HAS_STACKS:
		return "TARGET_HAS_STACKS"
	case EnableCondSELF_HAS_STACKS:
		return "SELF_HAS_STACKS"
	case EnableCondRANDOM_CHANCE:
		return "RANDOM_CHANCE"
	case EnableCondSTACK_COUNT:
		return "STACK_COUNT"
	case EnableCondTARGET_ALLY_HP_LESS_THAN:
		return "TARGET_ALLY_HP_LESS_THAN"
	case EnableCondTARGET_HP_LESS_THAN:
		return "TARGET_HP_LESS_THAN"
	case EnableCondLAUNCH:
		return "LAUNCH"
	case EnableCondCNT:
		return "CNT"
	}
	return ""
}

func GetEnableCond(s string) EnableCond {
	switch s {
	case "NONE":
		return EnableCondNONE
	case "TIME":
		return EnableCondTIME
	case "CRIT":
		return EnableCondCRIT
	case "HIT":
		return EnableCondHIT
	case "TARGET_HAS_STATUSEFFECT":
		return EnableCondTARGET_HAS_STATUSEFFECT
	case "SELF_HAS_STATUSEFFECT":
		return EnableCondSELF_HAS_STATUSEFFECT
	case "TARGET_HAS_STACKS":
		return EnableCondTARGET_HAS_STACKS
	case "SELF_HAS_STACKS":
		return EnableCondSELF_HAS_STACKS
	case "RANDOM_CHANCE":
		return EnableCondRANDOM_CHANCE
	case "STACK_COUNT":
		return EnableCondSTACK_COUNT
	case "TARGET_ALLY_HP_LESS_THAN":
		return EnableCondTARGET_ALLY_HP_LESS_THAN
	case "TARGET_HP_LESS_THAN":
		return EnableCondTARGET_HP_LESS_THAN
	case "LAUNCH":
		return EnableCondLAUNCH
	case "CNT":
		return EnableCondCNT
	}
	return -1
}

type Target int

const (
	TargetSELF Target = iota
	TargetALLY
	TargetENEMY
	TargetNOT_SELF_ALLY
	TargetCNT
)

func (e Target) String() string {
	switch e {
	case TargetSELF:
		return "SELF"
	case TargetALLY:
		return "ALLY"
	case TargetENEMY:
		return "ENEMY"
	case TargetNOT_SELF_ALLY:
		return "NOT_SELF_ALLY"
	case TargetCNT:
		return "CNT"
	}
	return ""
}

func GetTarget(s string) Target {
	switch s {
	case "SELF":
		return TargetSELF
	case "ALLY":
		return TargetALLY
	case "ENEMY":
		return TargetENEMY
	case "NOT_SELF_ALLY":
		return TargetNOT_SELF_ALLY
	case "CNT":
		return TargetCNT
	}
	return -1
}

type ResultTime int

const (
	ResultTimeSTARTCASTING ResultTime = iota
	ResultTimeENDCASTING
	ResultTimeCNT
)

func (e ResultTime) String() string {
	switch e {
	case ResultTimeSTARTCASTING:
		return "STARTCASTING"
	case ResultTimeENDCASTING:
		return "ENDCASTING"
	case ResultTimeCNT:
		return "CNT"
	}
	return ""
}

func GetResultTime(s string) ResultTime {
	switch s {
	case "STARTCASTING":
		return ResultTimeSTARTCASTING
	case "ENDCASTING":
		return ResultTimeENDCASTING
	case "CNT":
		return ResultTimeCNT
	}
	return -1
}

type TargetCondition int

const (
	TargetConditionSTUN TargetCondition = iota
	TargetConditionFROZEN
	TargetConditionLOW_HP
	TargetConditionSTATUSEFFECT_3_OVER
	TargetConditionCNT
)

func (e TargetCondition) String() string {
	switch e {
	case TargetConditionSTUN:
		return "STUN"
	case TargetConditionFROZEN:
		return "FROZEN"
	case TargetConditionLOW_HP:
		return "LOW_HP"
	case TargetConditionSTATUSEFFECT_3_OVER:
		return "STATUSEFFECT_3_OVER"
	case TargetConditionCNT:
		return "CNT"
	}
	return ""
}

func GetTargetCondition(s string) TargetCondition {
	switch s {
	case "STUN":
		return TargetConditionSTUN
	case "FROZEN":
		return TargetConditionFROZEN
	case "LOW_HP":
		return TargetConditionLOW_HP
	case "STATUSEFFECT_3_OVER":
		return TargetConditionSTATUSEFFECT_3_OVER
	case "CNT":
		return TargetConditionCNT
	}
	return -1
}

type OrderType int

const (
	OrderTypeCLOSEBY OrderType = iota
	OrderTypeCNT
)

func (e OrderType) String() string {
	switch e {
	case OrderTypeCLOSEBY:
		return "CLOSEBY"
	case OrderTypeCNT:
		return "CNT"
	}
	return ""
}

func GetOrderType(s string) OrderType {
	switch s {
	case "CLOSEBY":
		return OrderTypeCLOSEBY
	case "CNT":
		return OrderTypeCNT
	}
	return -1
}

type StatSubtype int

const (
	StatSubtypeCURRENT StatSubtype = iota
	StatSubtypeMAX
	StatSubtypePROCESSED
	StatSubtypeCNT
)

func (e StatSubtype) String() string {
	switch e {
	case StatSubtypeCURRENT:
		return "CURRENT"
	case StatSubtypeMAX:
		return "MAX"
	case StatSubtypePROCESSED:
		return "PROCESSED"
	case StatSubtypeCNT:
		return "CNT"
	}
	return ""
}

func GetStatSubtype(s string) StatSubtype {
	switch s {
	case "CURRENT":
		return StatSubtypeCURRENT
	case "MAX":
		return StatSubtypeMAX
	case "PROCESSED":
		return StatSubtypePROCESSED
	case "CNT":
		return StatSubtypeCNT
	}
	return -1
}

type AffectType int

const (
	AffectTypeINCREASE AffectType = iota
	AffectTypeDECREASE
	AffectTypeFULL
	AffectTypeZERO
	AffectTypeCNT
)

func (e AffectType) String() string {
	switch e {
	case AffectTypeINCREASE:
		return "INCREASE"
	case AffectTypeDECREASE:
		return "DECREASE"
	case AffectTypeFULL:
		return "FULL"
	case AffectTypeZERO:
		return "ZERO"
	case AffectTypeCNT:
		return "CNT"
	}
	return ""
}

func GetAffectType(s string) AffectType {
	switch s {
	case "INCREASE":
		return AffectTypeINCREASE
	case "DECREASE":
		return AffectTypeDECREASE
	case "FULL":
		return AffectTypeFULL
	case "ZERO":
		return AffectTypeZERO
	case "CNT":
		return AffectTypeCNT
	}
	return -1
}

type SkillTrigger int

const (
	SkillTriggerNEXT_NODE SkillTrigger = iota
	SkillTriggerBASIC_ATTACK
	SkillTriggerGET_HIT
	SkillTriggerRANDOM_CHANCE
	SkillTriggerALLY_LEFT
	SkillTriggerLEADER
	SkillTriggerCNT
)

func (e SkillTrigger) String() string {
	switch e {
	case SkillTriggerNEXT_NODE:
		return "NEXT_NODE"
	case SkillTriggerBASIC_ATTACK:
		return "BASIC_ATTACK"
	case SkillTriggerGET_HIT:
		return "GET_HIT"
	case SkillTriggerRANDOM_CHANCE:
		return "RANDOM_CHANCE"
	case SkillTriggerALLY_LEFT:
		return "ALLY_LEFT"
	case SkillTriggerLEADER:
		return "LEADER"
	case SkillTriggerCNT:
		return "CNT"
	}
	return ""
}

func GetSkillTrigger(s string) SkillTrigger {
	switch s {
	case "NEXT_NODE":
		return SkillTriggerNEXT_NODE
	case "BASIC_ATTACK":
		return SkillTriggerBASIC_ATTACK
	case "GET_HIT":
		return SkillTriggerGET_HIT
	case "RANDOM_CHANCE":
		return SkillTriggerRANDOM_CHANCE
	case "ALLY_LEFT":
		return SkillTriggerALLY_LEFT
	case "LEADER":
		return SkillTriggerLEADER
	case "CNT":
		return SkillTriggerCNT
	}
	return -1
}

type CostType int

const (
	CostTypeSTACK CostType = iota
	CostTypeCNT
)

func (e CostType) String() string {
	switch e {
	case CostTypeSTACK:
		return "STACK"
	case CostTypeCNT:
		return "CNT"
	}
	return ""
}

func GetCostType(s string) CostType {
	switch s {
	case "STACK":
		return CostTypeSTACK
	case "CNT":
		return CostTypeCNT
	}
	return -1
}

type EffectCategory int

const (
	EffectCategoryINSTANT EffectCategory = iota
	EffectCategoryMOVE
	EffectCategoryLASTING
	EffectCategoryNEG_STATUS_EFFECT
	EffectCategoryPOS_STATUS_EFFECT
	EffectCategorySTAT_INCREASE
	EffectCategorySTAT_DECREASE
	EffectCategoryCNT
)

func (e EffectCategory) String() string {
	switch e {
	case EffectCategoryINSTANT:
		return "INSTANT"
	case EffectCategoryMOVE:
		return "MOVE"
	case EffectCategoryLASTING:
		return "LASTING"
	case EffectCategoryNEG_STATUS_EFFECT:
		return "NEG_STATUS_EFFECT"
	case EffectCategoryPOS_STATUS_EFFECT:
		return "POS_STATUS_EFFECT"
	case EffectCategorySTAT_INCREASE:
		return "STAT_INCREASE"
	case EffectCategorySTAT_DECREASE:
		return "STAT_DECREASE"
	case EffectCategoryCNT:
		return "CNT"
	}
	return ""
}

func GetEffectCategory(s string) EffectCategory {
	switch s {
	case "INSTANT":
		return EffectCategoryINSTANT
	case "MOVE":
		return EffectCategoryMOVE
	case "LASTING":
		return EffectCategoryLASTING
	case "NEG_STATUS_EFFECT":
		return EffectCategoryNEG_STATUS_EFFECT
	case "POS_STATUS_EFFECT":
		return EffectCategoryPOS_STATUS_EFFECT
	case "STAT_INCREASE":
		return EffectCategorySTAT_INCREASE
	case "STAT_DECREASE":
		return EffectCategorySTAT_DECREASE
	case "CNT":
		return EffectCategoryCNT
	}
	return -1
}

type RemoveCond int

const (
	RemoveCondGET_HIT RemoveCond = iota
	RemoveCondCNT
)

func (e RemoveCond) String() string {
	switch e {
	case RemoveCondGET_HIT:
		return "GET_HIT"
	case RemoveCondCNT:
		return "CNT"
	}
	return ""
}

func GetRemoveCond(s string) RemoveCond {
	switch s {
	case "GET_HIT":
		return RemoveCondGET_HIT
	case "CNT":
		return RemoveCondCNT
	}
	return -1
}

type SkillSubtype int

const (
	SkillSubtypeMELEE SkillSubtype = iota
	SkillSubtypePROJECTILE
	SkillSubtypeEFFECT
	SkillSubtypeRADIAL
	SkillSubtypeCNT
)

func (e SkillSubtype) String() string {
	switch e {
	case SkillSubtypeMELEE:
		return "MELEE"
	case SkillSubtypePROJECTILE:
		return "PROJECTILE"
	case SkillSubtypeEFFECT:
		return "EFFECT"
	case SkillSubtypeRADIAL:
		return "RADIAL"
	case SkillSubtypeCNT:
		return "CNT"
	}
	return ""
}

func GetSkillSubtype(s string) SkillSubtype {
	switch s {
	case "MELEE":
		return SkillSubtypeMELEE
	case "PROJECTILE":
		return SkillSubtypePROJECTILE
	case "EFFECT":
		return SkillSubtypeEFFECT
	case "RADIAL":
		return SkillSubtypeRADIAL
	case "CNT":
		return SkillSubtypeCNT
	}
	return -1
}

type ResourceType int

const (
	ResourceTypeCOMMON_GRADE_BG ResourceType = iota
	ResourceTypeCOMMON_GRADE_TEXT
	ResourceTypeCNT
)

func (e ResourceType) String() string {
	switch e {
	case ResourceTypeCOMMON_GRADE_BG:
		return "COMMON_GRADE_BG"
	case ResourceTypeCOMMON_GRADE_TEXT:
		return "COMMON_GRADE_TEXT"
	case ResourceTypeCNT:
		return "CNT"
	}
	return ""
}

func GetResourceType(s string) ResourceType {
	switch s {
	case "COMMON_GRADE_BG":
		return ResourceTypeCOMMON_GRADE_BG
	case "COMMON_GRADE_TEXT":
		return ResourceTypeCOMMON_GRADE_TEXT
	case "CNT":
		return ResourceTypeCNT
	}
	return -1
}

type CommonGrade int

const (
	CommonGradeNORMAL CommonGrade = iota
	CommonGradeRARE
	CommonGradeEPIC
	CommonGradeLEGEND
	CommonGradeMYTH
	CommonGradeCNT
)

func (e CommonGrade) String() string {
	switch e {
	case CommonGradeNORMAL:
		return "NORMAL"
	case CommonGradeRARE:
		return "RARE"
	case CommonGradeEPIC:
		return "EPIC"
	case CommonGradeLEGEND:
		return "LEGEND"
	case CommonGradeMYTH:
		return "MYTH"
	case CommonGradeCNT:
		return "CNT"
	}
	return ""
}

func GetCommonGrade(s string) CommonGrade {
	switch s {
	case "NORMAL":
		return CommonGradeNORMAL
	case "RARE":
		return CommonGradeRARE
	case "EPIC":
		return CommonGradeEPIC
	case "LEGEND":
		return CommonGradeLEGEND
	case "MYTH":
		return CommonGradeMYTH
	case "CNT":
		return CommonGradeCNT
	}
	return -1
}
