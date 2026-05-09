#!/bin/bash
set -u
cd "$(dirname "$0")"

LOG=output/orchestration.log
mkdir -p output/multiseed output/sensitivity_action_interval
: > "$LOG"

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

log "START Phase 1 orchestration"
log "Machine: $(nproc) cores, load $(uptime | awk -F'load average: ' '{print $2}')"

# WS-3 scalability -- single process, runs alongside everything (uses 1 core)
log "Launching WS-3 scalability (background)"
( .venv/bin/python run_scalability.py --out output/scalability_benchmark.csv \
    >> "$LOG" 2>&1 ) &
SC_PID=$!

# --- WS-1 S1-S4: 4 batches of 5 seeds, 4-way parallel ---
log "Launching WS-1 S1-S4 (4 batches × 5 seeds, 4-way parallel)"
for batch in 1 2 3 4; do
  lo=$(( (batch-1)*5 + 1 )); hi=$(( batch*5 ))
  ( .venv/bin/python run_experiments.py --seeds $(seq $lo $hi) \
      --out-dir "output/multiseed/s1_s4/batch$batch" \
      >> "$LOG" 2>&1 ) &
done
wait
log "WS-1 S1-S4 DONE"

# --- WS-1 bottleneck: 4 batches of 5 seeds, 4-way parallel ---
log "Launching WS-1 bottleneck (4 batches × 5 seeds, 4-way parallel)"
for batch in 1 2 3 4; do
  lo=$(( (batch-1)*5 + 1 )); hi=$(( batch*5 ))
  ( .venv/bin/python run_bottleneck.py --seeds $(seq $lo $hi) \
      --out-dir "output/multiseed/bottleneck/batch$batch" \
      >> "$LOG" 2>&1 ) &
done
wait
log "WS-1 bottleneck DONE"

# --- WS-2 sensitivity: {0.5, 0.25}, 10 seeds, S1-S4 only, 2 batches of 5 seeds × 2 values = 4 parallel ---
log "Launching WS-2 sensitivity (0.5, 0.25; 10 seeds S1-S4)"
for ai in 0.5 0.25; do
  for batch in 1 2; do
    lo=$(( (batch-1)*5 + 1 )); hi=$(( batch*5 ))
    ( .venv/bin/python run_experiments.py --seeds $(seq $lo $hi) \
        --action-interval $ai \
        --out-dir "output/sensitivity_action_interval/ai_${ai}/batch$batch" \
        >> "$LOG" 2>&1 ) &
  done
done
wait
log "WS-2 sensitivity DONE"

# Wait for scalability if still running
if kill -0 $SC_PID 2>/dev/null; then
  log "Waiting for WS-3 scalability to finish..."
  wait $SC_PID
fi
log "WS-3 scalability DONE"

log "ALL PHASE 1 JOBS DONE"
