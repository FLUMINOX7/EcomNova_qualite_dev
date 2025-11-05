"""Payment service with gateway simulation"""

from __future__ import annotations

import uuid


class PaymentGateway:
    """
    Simulation d'une passerelle de paiement (mock de Stripe/Adyen)

    Règle de simulation :
    - Carte se terminant par '0000' => REFUSÉE
    - Toutes les autres cartes => ACCEPTÉE
    """

    def charge_card(
        self,
        card_number: str,
        exp_month: int,
        exp_year: int,
        cvc: str,
        amount_cents: int,
        idempotency_key: str,
    ) -> dict:
        """
        Simuler une charge de carte bancaire

        Returns:
            {
                "success": bool,
                "transaction_id": str | None,
                "failure_reason": str | None
            }
        """
        # Nettoyer le numéro de carte (enlever espaces)
        clean_card = card_number.replace(" ", "").replace("-", "")

        # Simulation : refuser si la carte finit par 0000
        if clean_card.endswith("0000"):
            return {
                "success": False,
                "transaction_id": None,
                "failure_reason": "CARTE_REFUSEE",
            }

        # Sinon, accepter le paiement
        return {
            "success": True,
            "transaction_id": f"txn_{uuid.uuid4().hex[:16].upper()}",
            "failure_reason": None,
        }

    def refund(self, transaction_id: str, amount_cents: int) -> dict:
        """
        Simuler un remboursement

        Returns:
            {
                "success": bool,
                "refund_id": str
            }
        """
        return {"success": True, "refund_id": f"rfnd_{uuid.uuid4().hex[:16].upper()}"}


class PaymentService:
    """Service for handling payment operations"""

    def __init__(self, gateway: PaymentGateway | None = None):
        self.gateway = gateway or PaymentGateway()

    def process_payment(
        self,
        order_id: str,
        card_number: str,
        exp_month: int,
        exp_year: int,
        cvc: str,
        amount_cents: int,
    ) -> dict:
        """
        Process a payment for an order

        Returns the result from the gateway
        """
        return self.gateway.charge_card(
            card_number=card_number,
            exp_month=exp_month,
            exp_year=exp_year,
            cvc=cvc,
            amount_cents=amount_cents,
            idempotency_key=order_id,
        )

    def process_refund(self, transaction_id: str, amount_cents: int) -> dict:
        """Process a refund"""
        return self.gateway.refund(transaction_id, amount_cents)
