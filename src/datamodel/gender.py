from enum import StrEnum, unique


@unique
class Gender(StrEnum):
    MALE = "男子"
    FEMALE = "女子"
