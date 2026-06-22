# app/domain/value_objects/gender.py
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Gender:
    value: str

    # Definimos las iniciales válidas como regla de formato
    VALID_GENDERS: set[str] = field(default_factory=lambda: {"M", "F"}, init=False)

    def __post_init__(self) -> None:
        upper_value = self.value.upper() if self.value else ""
        if upper_value not in self.VALID_GENDERS:
            raise ValueError(
                f"El género '{self.value}' no es válido. Debe ser 'M' o 'F'."
            )
