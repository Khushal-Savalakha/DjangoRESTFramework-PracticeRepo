from enum import Enum

class StatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

status = "activ"  # Mistyped
if status == StatusEnum.ACTIVE.value:
    print("Status is active.")  # Mistakes are caught early

print("_")