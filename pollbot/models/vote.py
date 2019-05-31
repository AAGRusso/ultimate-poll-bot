"""The sqlalchemy model for a vote."""
from sqlalchemy import (
    Column,
    func,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.types import (
    BigInteger,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from pollbot.db import base


class Vote(base):
    """The model for a Vote."""

    __tablename__ = 'vote'
    __table_args__ = (
        UniqueConstraint('user_id', 'poll_id', 'poll_option_id'),
    )

    id = Column(Integer, primary_key=True)
    type = Column(String)
    vote_count = Column(Integer)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # ManyToOne
    poll_option_id = Column(Integer, ForeignKey('poll_option.id', ondelete='cascade'), nullable=False, index=True)
    poll_option = relationship('PollOption')

    poll_id = Column(Integer, ForeignKey('poll.id', ondelete='cascade'), nullable=False, index=True)
    poll = relationship('Poll')

    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='cascade'), nullable=False, index=True)
    user = relationship('User')

    def __init__(self, vote_type, user, poll_option):
        """Create a new vote."""
        self.type = vote_type
        self.user = user
        self.vote_count = 0
        self.poll_option = poll_option
        self.poll = poll_option.poll