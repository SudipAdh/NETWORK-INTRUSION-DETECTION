"""Central configuration for the NID comparative study.

Keeping paths, label maps, and hyperparameters in one place means the rest of
the code stays readable, and tweaking an experiment never requires hunting
through five files.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset" / "archive" / "nsl-kdd"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

TRAIN_FILE = DATASET_DIR / "KDDTrain+.txt"
TEST_FILE = DATASET_DIR / "KDDTest+.txt"

# The NSL-KDD txt files have no header. These are the 41 features + label +
# difficulty score, in order. Names taken from the original KDD Cup '99 docs.
NSL_KDD_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
    "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files",
    "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate",
    "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
    "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate", "label", "difficulty",
]

CATEGORICAL_FEATURES = ["protocol_type", "service", "flag"]

# NSL-KDD uses 22 specific attack names; we group them into 4 attack families
# + Normal, following the standard mapping used in Tavallaee et al. (2009).
ATTACK_TO_CATEGORY = {
    "normal": "Normal",
    # DoS — Denial of Service
    "back": "DoS", "land": "DoS", "neptune": "DoS", "pod": "DoS",
    "smurf": "DoS", "teardrop": "DoS", "mailbomb": "DoS",
    "apache2": "DoS", "processtable": "DoS", "udpstorm": "DoS",
    # Probe — surveillance/scanning
    "ipsweep": "Probe", "nmap": "Probe", "portsweep": "Probe", "satan": "Probe",
    "mscan": "Probe", "saint": "Probe",
    # R2L — Remote-to-Local
    "ftp_write": "R2L", "guess_passwd": "R2L", "imap": "R2L",
    "multihop": "R2L", "phf": "R2L", "spy": "R2L", "warezclient": "R2L",
    "warezmaster": "R2L", "sendmail": "R2L", "named": "R2L", "snmpgetattack": "R2L",
    "snmpguess": "R2L", "xlock": "R2L", "xsnoop": "R2L", "worm": "R2L",
    "httptunnel": "R2L",
    # U2R — User-to-Root
    "buffer_overflow": "U2R", "loadmodule": "U2R", "perl": "U2R",
    "rootkit": "U2R", "ps": "U2R", "sqlattack": "U2R", "xterm": "U2R",
}

CLASS_LABELS = ["Normal", "DoS", "Probe", "R2L", "U2R"]

RANDOM_SEED = 42
CV_FOLDS = 5  # 5-fold instead of 10 — same statistical signal, ~half the runtime
