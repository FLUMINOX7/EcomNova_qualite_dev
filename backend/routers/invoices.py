"""Invoice endpoints"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.dependencies import get_session
from backend.schemas.invoice import InvoiceResponse, InvoiceLineResponse
from backend.repositories.invoice import InvoiceRepository
from backend.auth.jwt import get_current_user_id

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Get an invoice by ID"""
    repo = InvoiceRepository(db)
    invoice = repo.get_by_id(invoice_id)
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Verify ownership
    if invoice.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this invoice"
        )
    
    # Build response with lines
    lines_response = [
        InvoiceLineResponse(
            id=line.id,
            product_id=line.product_id,
            name=line.name,
            unit_price_cents=line.unit_price_cents,
            quantity=line.quantity,
            line_total_cents=line.line_total_cents
        )
        for line in invoice.lines
    ]
    
    return InvoiceResponse(
        id=invoice.id,
        order_id=invoice.order_id,
        user_id=invoice.user_id,
        total_cents=invoice.total_cents,
        issued_at=invoice.issued_at,
        lines=lines_response
    )
