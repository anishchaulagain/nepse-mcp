"""SQLAlchemy model for stock data persistence."""

from sqlalchemy import Column, Integer, Float, String, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, default=0)
    amount = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint("symbol", "timestamp", name="uq_symbol_timestamp"),
    )

    def __repr__(self):
        return f"<StockPrice(symbol={self.symbol}, date={self.timestamp}, close={self.close})>"
