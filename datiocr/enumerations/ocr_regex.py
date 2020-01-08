from enum import Enum


class Annotation(Enum):
    BRF_QUANTITY = '\s[1-9][0-9]{0,2}[.]{0,1}[0-9]{0,3}[,][0]{2,3}\s'
    BRF_MATERIAL = '\s[1-9][0-9]{5}\s'
    BRF_UNIT_PRICE = '\s[0-9]{1,4}[,][0-9]{5}\s'