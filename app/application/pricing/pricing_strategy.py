#app/application/pricing/pricing_strategy.py
from abc import ABC, abstractmethod
from app.domain.entities.order import Order

class PricingStrategy(ABC):
    """Contrato para estrategias de cálculo de precio."""
    @abstractmethod
    def calculate(self, order: Order) -> float:
        """Recibe la entidad Order y devuelve el total (float)."""
        ...