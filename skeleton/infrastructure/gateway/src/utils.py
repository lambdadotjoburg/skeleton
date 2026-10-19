from pathlib import Path

from skeleton.infrastructure.common.src.context import RuntimeContext

def build_static_dir(context: RuntimeContext) -> Path:
    
    frontend = context.layout.frontend
    lib = context.config.frontend["lib"]

    build_dir = (
        lib["src"]
        if context.mode == "dev"
        else lib["dist"]
    )

    return frontend/build_dir/lib["static"]

def normalize_extensions(
    ext: tuple[str, ...]
) -> tuple[str, ...]:
    
    # store all normalized extensions!
    normalized_ext: list[str] = []

    for item in ext:

        if not isinstance(item, str):
            raise TypeError(f"Extension {item} must be a string")
        
        # remove any leading/trailing whitespace
        item = item.strip()

        # check that extension is not a path
        if "/" in item or "\\" in item:
            raise ValueError(f"Invalid extension {item}")
        
        # check that extension is a proper file type
        if item == ".":
            raise ValueError(f"'.' is not a valid extension/file type")
            
        # if the item does NOT start with . then pre-pend it!
        if not item.startswith("."):
            item = f".{item}"

        # if all is OK!
        normalized_ext.append(item)

    return tuple(normalized_ext)