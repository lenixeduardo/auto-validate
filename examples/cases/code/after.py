"""Correção: comparação monetária numérica preservando strings originais."""
from decimal import Decimal

def sort_prices(prices: list[str]) -> list[str]:
    return sorted(prices, key=lambda price: Decimal(price))
