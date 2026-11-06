from typing import Dict, List


def model_catalog(models: List[Dict], *, vision=None, reasoning_levels=False) -> List[Dict]:
    """Model list in the shape the arena and Neby clients expect.

    `vision=None` reads each model's own flag; a bool forces it for all.
    """
    catalog = []
    for m in models:
        capabilities = {
            "chat": True,
            "stream": True,
            "vision": m.get("vision", False) if vision is None else vision,
            "thinking": m.get("reasoning", False),
        }
        if reasoning_levels:
            capabilities["reasoning_levels"] = m.get("reasoning_levels", [])
        capabilities["tools"] = False
        capabilities["web_search"] = m.get("web_search", False)
        catalog.append({"id": m["id"], "name": m["name"], "capabilities": capabilities})
    return catalog
