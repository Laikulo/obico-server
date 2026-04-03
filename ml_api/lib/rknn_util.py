from pathlib import Path
from functools import cache
from urllib.request import urlretrieve

_PLATFORMS = {
    "rk2118",
    "rk2118",
    "rk3562",
    "rk3566",
    "rk3568",
    "rk3576",
    "rk3588",
    "rv1126b",
}

@cache
def _get_compats():
    try:
        devicetree_compat = (
            Path("/proc/device-tree/compatible").read_text().removesuffix(chr(0))
        )
    except IOError:
        return set()

    return set(devicetree_compat.split(","))


def detect_rknn_plat():
    if matching_plats := _get_compats().intersection(_PLATFORMS):
        return next(
            iter(matching_plats)
        )  # Don't care if there is more than one, since that would mean an invalid DTB
    else:
        return None


def is_rknn_plat():
    return detect_rknn_plat() is not None


@cache
def _base_url():
    return (Path(__file__).parents[1] / "model" / "model-weights.rknn.url").read_text().strip()

@cache
def model_url(platform=None):
    if not platform:
        platform = detect_rknn_plat()

    if not platform:
        raise RuntimeError("Unable to determine RKNN platform")

    return f"{_base_url()}obico-{platform}-fp.rknn"

def download_model(platform=None, dest="/model_cache/ml_api/rknn/model-weights.rknn"):
    urlretrieve(model_url(platform), dest)
