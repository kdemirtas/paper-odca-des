#!/bin/bash
# Every simulated result of the manuscript: the multi-seed runs, the single-run figures' inputs
# (bottleneck, incident, demand sweep), then the timed runs (single-seed S1-S4 and scalability)
# on a quiet machine.
# One job per (scenario, seed), run by a pool of JOBS processes; aggregate_multiseed.py then
# writes the CSVs. Seed sets come from config.py (D-2026-09-19-4).
#   ./run_all_phase1.sh [JOBS]      (default: cores - 1)
set -u
cd "$(dirname "$0")"

JOBS=${1:-$(( $(nproc) - 1 ))}
LOG=output/orchestration.log
S1_S4=output/multiseed/s1_s4/batch1
BOTTLENECK=output/multiseed/bottleneck/batch1
SENSITIVITY=output/sensitivity_action_interval
mkdir -p "$S1_S4" "$BOTTLENECK" "$SENSITIVITY"
: > "$LOG"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
seeds() { .venv/bin/python -c "import config; print(*config.$1)"; }

# stale per-seed files from older runs would be aggregated too, so start clean
rm -rf output/multiseed/s1_s4/batch* output/multiseed/bottleneck/batch* "$SENSITIVITY"/ai_*
mkdir -p "$S1_S4" "$BOTTLENECK"

log "START: $JOBS parallel jobs on $(nproc) cores"
{
  # single runs first: the longest jobs
  echo "run_bottleneck.py"
  echo "run_incident.py"
  echo "run_demand_sweep.py --lanes 1"
  echo "run_demand_sweep.py --lanes 4"
  for seed in $(seeds REPLICATION_SEEDS); do
    for scenario in S1_baseline S2_low_av S3_med_av S4_high_av; do
      echo "run_experiments.py --scenarios $scenario --seeds $seed --out-dir $S1_S4"
    done
    echo "run_bottleneck.py --seeds $seed --out-dir $BOTTLENECK"
  done
  # sensitivity: S1 only (D-2026-04-20-2)
  for ai in 0.5 0.25; do
    for seed in $(seeds SENSITIVITY_SEEDS); do
      echo "run_experiments.py --scenarios S1_baseline --seeds $seed --action-interval $ai" \
           "--out-dir $SENSITIVITY/ai_${ai}/batch1"
    done
  done
} | xargs -P "$JOBS" -I{} sh -c \
    '.venv/bin/python {} >> '"$LOG"' 2>&1 || echo "FAILED: {}" >> '"$LOG"
log "multi-seed runs DONE ($(grep -c '^FAILED' "$LOG") failed)"

.venv/bin/python aggregate_multiseed.py >> "$LOG" 2>&1 && log "aggregation DONE"

# wall times are the result here, so nothing else runs alongside
.venv/bin/python run_experiments.py >> "$LOG" 2>&1
log "single-seed S1-S4 DONE"
.venv/bin/python run_scalability.py --out output/scalability_benchmark.csv >> "$LOG" 2>&1
log "scalability DONE"
log "ALL PHASE 1 JOBS DONE"
