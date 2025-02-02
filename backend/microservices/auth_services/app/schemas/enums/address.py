from enum import StrEnum


class AddressType(StrEnum):
    BILLING = "billing"
    SHIPPING = "shipping"
    HOME = "home"
    WORK = "work"
    WAREHOUSE = "warehouse"
