# app/domain/value_objects/order_status.py
from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderStatus:
    value: str

    # Definimos los estados válidos como una regla de negocio del dominio
    VALID_STATUSES: set[str] = field(
        default_factory=lambda: {
            "Complete",
            "Cancelled",
            "Processing",
            "Returned",
            "Shipped",
        },
        init=False,
    )

    def __post_init__(self) -> None:
        if self.value not in self.VALID_STATUSES:
            raise ValueError(f"'{self.value}' no es un estado válido para la orden.")
