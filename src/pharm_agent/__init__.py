from importlib.metadata import version, PackageNotFoundError

__all__ = [
    "__version__",
]

try:
    __version__ = version("pharm_agent")
except PackageNotFoundError:
    __version__ = "0.0.0"

