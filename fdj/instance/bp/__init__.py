from .analyze import bp_analyze
from .compare import bp_compare
from .contour import bp_contour
from .theory import bp_theory
from .cas import bp_cas
from .history import bp_history
from .public import bp_public

bps = [bp_theory, bp_contour, bp_compare, bp_analyze,
       bp_cas, bp_history, bp_public]
