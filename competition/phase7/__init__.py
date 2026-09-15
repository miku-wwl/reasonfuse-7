"""Independent 1010 Track B / SP-A competition package.

The repository uses a ``src`` layout for the frozen ReasonFuse core.  The
package adds that source directory when the competition package is executed
directly from a clean checkout, so the documented commands do not depend on a
machine-specific PYTHONPATH.
"""

from pathlib import Path
import sys

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_CORE_SOURCE = _REPOSITORY_ROOT / "src"
if str(_CORE_SOURCE) not in sys.path:
    sys.path.insert(0, str(_CORE_SOURCE))

__version__ = "0.1.0"
