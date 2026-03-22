"""Domain exceptions for vk."""


class VkError(Exception):
    """Base exception for all vk errors."""


class AuthenticationError(VkError):
    """Raised when authentication fails (401)."""


class NotFoundError(VkError):
    """Raised when a resource is not found (404)."""


class ApiError(VkError):
    """Raised for general API errors (4xx/5xx)."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class ConfigError(VkError):
    """Raised when configuration is missing or invalid."""


class AmbiguousNameError(VkError):
    """Raised when a name matches multiple resources."""

    def __init__(self, name: str, candidates: list[str]) -> None:
        self.name = name
        self.candidates = candidates
        formatted = ", ".join(candidates)
        super().__init__(f"Ambiguous name '{name}': matches {formatted}")
