import inspect
import pkgutil
from importlib import import_module
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Optional

from app.engine_specifics.base import BaseSpecificEngine


def is_engine_specific(obj: Any) -> bool:
    return (
        inspect.isclass(obj)
        and issubclass(obj, BaseSpecificEngine)
        and obj != BaseSpecificEngine
    )


def load_engine_specifics() -> list[type[BaseSpecificEngine]]:
    engine_specs: list[type[BaseSpecificEngine]] = []

    # Load standard engines
    db_engine_spec_dir = str(Path(__file__).parent)
    for module_info in pkgutil.iter_modules([db_engine_spec_dir], prefix="."):
        module = import_module(module_info.name, package=__name__)
        engine_specs.extend(
            getattr(module, attr)
            for attr in module.__dict__
            if is_engine_specific(getattr(module, attr))
        )
    # load additional engines from external modules
    for ep in entry_points(group="superset.db_engine_specs"):
        try:
            engine_spec = ep.load()
        except Exception:
            continue
        engine_specs.append(engine_spec)

    return engine_specs


def get_engine_specific(backend: str, driver: Optional[str] = None) -> type[BaseSpecificEngine]:
    engine_specifics = load_engine_specifics()

    if driver is not None:
        for engine_specific in engine_specifics:
            if engine_specific.supports_backend(backend, driver):
                return engine_specific

    for engine_specific in engine_specifics:
        if engine_specific.supports_backend(backend):
            return engine_specific

    return BaseSpecificEngine
