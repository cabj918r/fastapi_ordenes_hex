from app.domain.entities.order import Order

from .pricing_strategy import PricingStrategy


class BasePriceStrategy(PricingStrategy):
    def calculate(self, order: Order) -> float:
        total = sum(float(item.sale_price) for item in order.items)
        return round(total, 2)

class DiscountStrategy(PricingStrategy):
    def __init__(self, discount_rate: float):
        self.discount_rate = float(discount_rate)

    def calculate(self, order: Order) -> float:
        base = sum(float(item.sale_price) for item in order.items)
        return round(base * (1.0 - self.discount_rate), 2)
