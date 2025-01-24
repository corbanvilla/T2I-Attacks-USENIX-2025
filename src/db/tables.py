"""
This module defines the tables used in the database.

It can be used as a helpful reference for the database schema.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Double,
    ForeignKey,
    Text,
    JSON,
    Numeric,
    ARRAY,
    DateTime,
    UniqueConstraint,
    CheckConstraint,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, timezone

# Define a base class
Base = declarative_base()


class Languages(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True)

    name_short = Column(String(10), unique=True)
    name = Column(String(100), unique=True)

    joshi_et_al = Column(Integer)
    common_crawl_pages = Column(Integer)
    common_crawl_percent = Column(Double)

    # Relationships
    translated_prompts = relationship("TranslatedPrompts", backref="lang")


class PromptPrefixStyles(Base):
    __tablename__ = "prompt_prefix_styles"
    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True)
    prompt_prefix = Column(Text)

    # Relationships
    image_creation_requests = relationship(
        "ImageCreationRequest", backref="prompt_prefix"
    )


class Prompts(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True)

    prompt = Column(Text, index=True)
    dataset = Column(String(100))
    prompt_hash = Column(LargeBinary)

    # Relationships
    translated_prompts = relationship("TranslatedPrompts", backref="translated_prompt")
    image_creation_requests = relationship("ImageCreationRequest", backref="prompt")

    # Require unique prompt/dataset pair
    __table_args__ = (UniqueConstraint("prompt", "dataset", name="uix_prompt_dataset"),)


class TranslatedPrompts(Base):
    __tablename__ = "translated_prompts"
    id = Column(Integer, primary_key=True)

    prompt_translation = Column(Text)
    prompt_translation_hash = Column(LargeBinary)

    # Foreign keys
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))

    # Relationships
    image_creation_requests = relationship(
        "ImageCreationRequest", backref="translated_prompt"
    )

    # Require unique prompt_id/language_id pair
    __table_args__ = (
        UniqueConstraint("prompt_id", "language_id", name="uix_prompt_language"),
    )


# Define a class representing a table
class ImageCreationRequest(Base):
    __tablename__ = "image_creation_requests"
    id = Column(Integer, primary_key=True)
    success = Column(Boolean)
    model = Column(String(100))

    # Timing
    request_start = Column(Double)
    request_end = Column(Double)
    reported_created = Column(Double)
    response_time = Column(Double)
    timing_valid = Column(Boolean, default=True)

    # Returned data
    revised_prompt = Column(Text)
    status_code = Column(Integer)
    error = Column(Text)

    revised_prompt_hash = Column(LargeBinary)

    # Foreign keys
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    translated_prompt_id = Column(Integer, ForeignKey("translated_prompts.id"))
    prompt_prefix_id = Column(Integer, ForeignKey("prompt_prefix_styles.id"))
    image_id = Column(Integer, ForeignKey("images.id"))

    # Require unique translated_prompt_id/prompt_id/model/request_start quartet
    # Require mutually exclusive prompt_id or translated_prompt_id
    __table_args__ = (
        UniqueConstraint(
            "translated_prompt_id",
            "prompt_id",
            "model",
            "request_start",
            name="uix_translated_prompt_model_request_start",
        ),
        CheckConstraint(
            "(CASE WHEN prompt_id IS NOT NULL THEN 1 ELSE 0 END) + "
            "(CASE WHEN translated_prompt_id IS NOT NULL THEN 1 ELSE 0 END) <= 1",
            name="check_prompt_id_translated_prompt_id_mutually_exclusive",
        ),
    )


class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    hash = Column(String(64), unique=True)
    from_b64 = Column(Boolean, index=True)

    bytes = Column(LargeBinary)

    # Relationships
    image_creation_requests = relationship("ImageCreationRequest", backref="image")


class ModerationRequest(Base):
    __tablename__ = "moderation_requests"
    id = Column(Integer, primary_key=True)

    prompt = Column(Text, index=True)
    request_id = Column(String(40))
    model = Column(String(20))

    # Timing
    request_start = Column(Double)
    request_end = Column(Double)
    response_time = Column(Double)

    flagged = Column(Boolean)
    categories = Column(JSON)
    category_scores = Column(ARRAY(Numeric))

    # A second factor to track changes with models
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    prompt_hash = Column(LargeBinary)

    # Require unique prompt/model pair
    __table_args__ = (UniqueConstraint("prompt", "model", name="uix_prompt_model"),)
