"""Exceptions for Your Domain API."""

from __future__ import annotations


class YourDomainApiError(Exception):
    """Base exception for Your Domain API errors."""


class YourDomainApiCommunicationError(YourDomainApiError):
    """Exception for communication errors."""


class YourDomainApiAuthenticationError(YourDomainApiError):
    """Exception for authentication errors."""
