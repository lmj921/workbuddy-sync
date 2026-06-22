# XGB Prediction Pipeline — Complete Exploration Report

## 1. Project Structure Overview

```
football-betting/
  scripts/
    predict_single.py          # Main CLI entry point (1096 lines) ★ KEY FILE
  src/
    features.py                # v1: 16-factor feature engineering
    features_v2.py             # v2: 72+ factor feature engineering (1448 lines) ★ KEY FILE
    models/
      xgboost_model.py         # XGBoostPredictor class (274 lines) ★ KEY FILE
      ensemble.py              # EnsemblePredictor (Poisson + XGB fusion) (286 lines)
      poisson.py               # PoissonModel core
      calibration.py           # ProbabilityCalibrator (Isotonic/Platt/Adaptive blend)
    decision.py                # EV/Kelly/BetTier decision engine
    backtest.py                # Backtest with XGB_MARKETS fusion logic
    elo.py                     # EloSystem
    market_alerts.py           # Market alert detection
  models/
    E0/, I1/, SP1, CL, CHN/    # Per-league model artifacts
      poisson_params.json       # Attack/defense factors + league averages
      calibrator.pkl            # Pickled sklearn IsotonicRegression
      elo_ratings.json          # Team Elo ratings
      meta.json                 # Training metadata
```

**No pre-trained .pkl XGB models exist on disk.** XGBoost models are trained fresh from CSV each time `--xgb` is passed.

---

## 2. `scripts/predict_single.py` — Full Breakdown

### 2.1 `_build_xgb_feature_row()` (Lines 210–347)

**Purpose:** Synthesizes a single-row DataFrame of XGB features for an upcoming match by combining historical data from both teams' most recent matches.

**Signature (line 210-216):**
```python
def _build_xgb_feature_row(
    home_team: str,
    away_team: str,
    features_df: pd.DataFrame,   # Full v2-featured DataFrame from build_features_v2_from_csv()
    odds: Optional[dict] = None,  # Current market odds dict
    ah_line: Optional[float] = None,
) -> tuple[Optional[pd.DataFrame], dict]:
    """Returns (synth_df, info_dict) or (None, {"error": ...})"""
```

**Column Classification Logic (lines 296-341):**

| Priority | Column Pattern | Source | Fallback |
|----------|---------------|--------|----------|
| 1 | In `market_overrides` dict | Live odds calculation | N/A |
| 2 | Ends with `_home` | Home team's last match as HomeTeam (`home_last`) | N/A |
| 3 | Ends with `_away` | Away team's last match as AwayTeam (`away_last`) | Column median |
| 4 | Starts with `h2h_` or contains `h2h` | Set to NaN (XGB handles) | N/A |
| 5 | All others | Home team's last match (`home_last`) | Column median |

**Market Override Calculations (lines 273-292):**
```python
market_overrides["M19_implied_prob_diff"] = (1.0/home_odds) - (1.0/away_odds)
market_overrides["M01_handicap_line"] = ah_line
market_overrides["handicap_line"] = ah_line
market_overrides["M05_ou_water_over"] = over_odds
market_overrides["ou_water"] = over_odds
market_overrides["M06_ou_water_under"] = under_odds
market_overrides["ah_water"] = (ah_home_odds + ah_away_odds) / 2.0
```

**Diagnostic Output (lines 250-343):**
- `home_feature_source`: {team_as_home, opponent, date} of the home team's source row
- `away_feature_source`: {team_as_away, opponent, date} of away team's source row (or warning if not found)
- `feature_sources`: Counter of how many columns came from each source category
- `synth_method`: Always `"split_home_away_v1"`

---

### 2.2 XGB Raw Predictions (Lines 418-435)

```python
if xgb_model is not None and xgb_features_df is not None:
    synth_row, xgb_match_info = _build_xgb_feature_row(...)
    if synth_row is not None:
        all_xgb = xgb_model.predict_proba(synth_row)   # line 431
        for mkt, arr in all_xgb.items():
            xgb_probs[mkt] = float(arr[0])              # line 433
```
- `xgb_model.predict_proba()` calls `XGBoostPredictor.predict_proba()` (xgboost_model.py:160)
- Returns `dict[str, np.ndarray]` where each value is probability array (shape [1] for single row)
- Extracted to `dict[str, float]` via `float(arr[0])`

---

### 2.3 XGB Shift Calculation (Lines 437-451)

**Key Constants (lines 385-386):**
```python
XGB_MARKETS = {"under_2_5", "draw", "over_2_5", "btts_yes", "btts_no"}  # line 385
XGB_BLEND = xgb_blend  # Default 0.6 (line 386, param default at line 363)
```

**Fusion Formula (lines 440-451):**
```python
for market in calibrated_probs:
    if market in XGB_MARKETS and market in xgb_probs:
        xp = xgb_probs[market]
        if 0.01 < xp < 0.99:
            old = calibrated_probs[market]
            new = (1 - XGB_BLEND) * old + XGB_BLEND * xp   # Weighted blend!
            xgb_shifts[market] = {
                "pre_xgb": round(old, 4),
                "xgb_raw": round(xp, 4),
                "post_xgb": round(new, 4),
                "shift": round(new - old, 4),
            }
            calibrated_probs[market] = new  # IN-PLACE MUTATION
```

**Critical: `home_win` and `away_win` are NOT in XGB_MARKETS — they use pure Poisson+calibration only.**

Blend formula: `P_final = (1 - 0.6) * P_poisson_calibrated + 0.6 * P_xgb_raw`

---

### 2.4 Fusion Logic Summary

The pipeline has **three layers**:

```
Layer 1: Pure Poisson (Dixon-Coles)
    ↓ predict(home, away) → raw_probs {home_win, draw, away_win, over_2_5, under_2_5}
    
Layer 2: Calibration (50/50 blend with Isotonic)
    ↓ calibrated_probs = 0.5 * raw + 0.5 * isotonic(raw)
    → Applies to ALL 5 markets equally
    
Layer 3: XGB Fusion (ONLY for XGB_MARKETS subset)
    ↓ IF --xgb flag AND model trained:
        For under_2_5, draw, over_2_5, btts_yes, btts_no ONLY:
        final = (1 - 0.6) * calibrated + 0.6 * xgb_raw
    → home_win, away_win stay as Layer 2 output only
```

**Note:** There is no "brain" calculation layer in this codebase. The term "brain" appears nowhere in the code. The three-layer system above is the complete logic.

There IS a separate `EnsemblePredictor` class in `/Users/a1_builder/WorkBuddy/football-betting/src/models/ensemble.py` that does a simpler uniform-weight fusion across ALL markets (including home_win/away_win), but it is NOT used by `predict_single.py`. The `predict_single.py` uses its own inline fusion (lines 418-451).

---

### 2.5 JSON Output Structure (Lines 619-623)

```json
{
  "model": {                                    // Lines 468-496
    "home_team": str,
    "away_team": str,
    "lambda_home": float,                       // Poisson attack expectation
    "lambda_away": float,
    "lambda_home_elo": float,                   // Elo-derived lambda
    "lambda_away_elo": float,
    "expected_score": str,                       // e.g. "1.8 - 1.2"
    "home_win": float,                           // Calibrated (+XGB fused if applicable)
    "draw": float,
    "away_win": float,
    "over_2_5": float,
    "under_2_5": float,
    "over_1_5": float,                          // Poisson-only, no calibration/XGB
    "under_1_5": float,
    "over_3_5": float,
    "under_3_5": float,
    "btts_yes": float,                          // Poisson-only
    "btts_no": float,
    "top_scores": [[score, prob], ...],          // Top 5 exact scores
    "home_elo": float,
    "away_elo": float,
    "elo_diff": float,
    "asian_handicap": {                          // Only if ah_line provided
      "line": float,
      "ah_home_cover": float,
      "ah_away_cover": float,
      ...
    }
  },
  "plan": null | {                              // Lines 507-559 (only if odds given)
    "bankroll": float,
    "total_stake": float,
    "total_stake_pct": float,
    "bets": [
      {
        "tier": "core"|"value"|"longshot",
        "market": str,
        "odds": float,
        "model_prob": float,
        "implied_prob": float,
        "ev": float,
        "edge": float,
        "kelly_fraction": float,
        "stake": float
      }
    ],
    "rejected": [...]
  },
  "diagnostics": {                              // Lines 562-617
    "home_atk_factor": float,
    "home_def_factor": float,
    "away_atk_factor": float,
    "away_def_factor": float,
    "league_home_avg": float,
    "league_away_avg": float,
    "lambda_formula": str,
    "calibration_applied": bool,
    "calibration_shift": {                       // Line 576-588
      "home_win": {"raw": f, "calibrated": f, "shift": f},
      ...
    },
    "xgb_applied": bool,                         // Line 591
    "xgb_blend": float | null,                   // Line 592
    "xgb_markets_shifted": {                     // Line 593
      "under_2_5": {"pre_xgb": f, "xgb_raw": f, "post_xgb": f, "shift": f},
      ...
    },
    "xgb_match_source": dict | None,             // Line 594 (from _build_xgb_feature_row)
    "xgb_raw_all": {market: float},              // Line 595 (all XGB predictions)
    "market_alerts": [...]                       // Lines 598-617
  }
}
```

---

### 2.6 Model Loading Flow (Lines 935-1086)

1. **Pre-trained models:** If `--model-dir` exists with `poisson_params.json`, loads Poisson + Calibrator(pkl) + Elo(json)
2. **Train from scratch:** If no model dir or `--train`, trains from CSV
3. **XGB (optional):** If `--xgb` flag, calls `load_xgboost_model(csv_path)` which:
   - Imports `XGBoostPredictor` from `src.models.xgboost_model`
   - Calls `build_features_v2_from_csv(csv_path)` to get full featured DataFrame
   - Creates `XGBoostPredictor()` and calls `.fit(df_v2, markets)`
   - Returns `(xgb_model, df_v2)` or `(None, None)` on failure
4. **Prediction call:** `predict_single_match(..., xgb_model=xgb_model, xgb_features_df=df_v2, xgb_blend=args.xgb_blend)`

---

## 3. `src/features_v2.py` — Feature Engineering (72 Factors)

### 3.1 Factor Categories (Lines 31-103)

| Category | Count | Prefix | Description |
|----------|-------|--------|-------------|
| Attack | 18 | A01-A18 | xG, npxG, shots, conversion, SCA/GCA, key passes |
| Defense | 12 | D01-D12 | xGA, clean sheets, tackles, interceptions, blocks |
| Possession | 9 | P01-P09 | Possession %, progressive passes/carries, completion |
| Tactical | 10 | T01-T10 | PPDA, press success, defensive line, fouls, corners, set piece |
| Player State | 14 | S01-S14 | Fitness, injuries, form trends, key player availability |
| Market | 20 | M01-M29 | Handicap, OU, odds drift, cover rates, streaks, triangle signal |
| Context | 17 | C01-C17 (plus extras) | Home advantage, rest days, derby, H2Elo, referee |
| Reversion | 6 | R01-R06 | Goal/xG overperform, luck factors |

**Total defined: ~100 columns** (72 base + extended M07b-M29 + S01-S05 + C13-C15 + T10-T12 etc.)

### 3.2 CSV-Computable vs External Data (Lines 106-128)

~35 factors computable directly from football-data.co.uk CSV.
Remaining require Understat (xG/PPDA/xPTS), FBRef (advanced tactical), or Transfermarkt data.
Missing factors are filled as **NaN** — XGBoost natively handles missing values.

### 3.3 Key Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| `build_features_v2()` | 131-186 | Main entry point, orchestrates all sub-computers |
| `_compute_market_factors()` | 193-265 | M01-M29: handicap, OU, odds drift, cover rates, reversion |
| `_compute_context_factors()` | 478-508 | C01-C14: home adv, rest days, H2H, season stage |
| `_compute_tactical_from_csv()` | 593-625 | T06-T09: fouls, yellows, corners from CSV |
| `_compute_attack_defense_from_csv()` | 632-678 | A08, A09, A13, D06: shot-based approximations |
| `_compute_reversion_from_csv()` | 685-720 | R01, R02: goal/xG overperformance |
| `_compute_understat_factors()` | 727-811 | T01 PPDA, R05 xPTS, npxG/npxGA, deep completions |
| `_compute_match_detail_factors()` | 1011-1108 | C13 red cards, C14/C15 referee, A14/D07 half-time |
| `_compute_clubelo_factors()` | 1115-1160 | C10-C12 ClubElo ratings |
| `_compute_odds_divergence()` | 1167-1242 | M25-M29 multi-bookmaker odds std/range |
| `_compute_player_creativity()` | 905-1004 | S01-S05 xA aggregation from player-level data |
| `build_features_v2_from_csv()` | 1383-1400 | Convenience wrapper: reads CSV, auto-loads Understat |

### 3.4 Auto Data Loading (Lines 1262-1430)

- `_auto_load_understat()`: Looks for `data/understat/{LEAGUE}_{season}.json`, extracts `teamsData` and `playersData`
- Supports EPL (E0), La Liga (SP1), Serie A (I1) auto-mapping
- Team name mapping dictionary for Understat -> football-data.co.uk conventions

---

## 4. `src/models/xgboost_model.py` — XGB Model

### 4.1 TRAIN_FEATURES List (Lines 35-101) — 73 Features

The actual features used for training/prediction:

**V1 legacy (16):**
`npxG_home`, `npxGA_home`, `form_pts_home`, `goals_scored_home`, `goals_conceded_home`,
`ah_cover_rate_home`, `ou_over_rate_home`, `npxG_away`, `npxGA_away`, `form_pts_away`,
`goals_scored_away`, `goals_conceded_away`, `ah_cover_rate_away`, `ou_over_rate_away`,
`handicap_line`, `ah_water`, `ou_water`, `triangle_signal`, `home_advantage`,
`league_avg_goals`, `h2h_win_rate`

**V2 additions (~52):**
`M01_handicap_line`, `M06_ou_water_under`, `A08_shots_per90`, `M19_implied_prob_diff`,
`M05_ou_water_over`, `A09_shots_on_target_pct`, `T09_corners_per90`,
`R02_concede_xGA_overperform`, `M08_ou_open_vs_close`, `A13_conversion_rate`,
`M10_ou_water_movement`, `C06_season_stage`, `M09_handicap_water_movement`,
`T06_fouls_committed_per90`, `C02_rest_days`, `C03_rest_days_diff`,
`M12_ah_cover_rate_home`, `M14_ou_over_rate_home`, `M16_ah_cover_streak`,
`M17_ou_over_streak`, `D06_clean_sheet_rate`, `T08_yellow_cards_per90`,
`R01_goal_xG_overperform`, `C10_clubelo_home`, `C11_clubelo_away`, `C12_clubelo_diff`,
`M25_odds_std_home` through `M29_max_div_direction` (5 odds divergence features),
`T01_PPDA`, `T01_PPDA_away`, `T01_PPDA_allowed`,
`T10_deep_completions`, `T11_deep_allowed`, `T12_deep_away`,
`R05_points_vs_xPTS`, `M21_walk_rate`, `M22_ah_reversion`, `M23_ou_reversion`,
`M24_cross_streak`, `S01_team_xA` through `S05_team_xGChain` (5 player creativity),
`C13_red_card_rate`, `C14_referee_home_bias`, `C15_referee_card_rate`,
`A14_ht_scoring_rate`, `D07_ht_concede_rate`

### 4.2 Training Hyperparams (Lines 18-31)
```python
DEFAULT_PARAMS = {
    "n_estimators": 100,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 5,
    "reg_alpha": 0.1,     # L1 regularization
    "reg_lambda": 1.0,     # L2 regularization
    "objective": "binary:logistic",
    "eval_metric": "logloss",
    "random_state": 42,
    "verbosity": 0,
}
```

### 4.3 Key Methods

| Method | Lines | Purpose |
|--------|-------|---------|
| `fit(df, markets)` | 113-158 | Trains one XGBClassifier per market; filters NaN rows; requires >=30 samples |
| `predict_proba(df)` | 160-185 | Returns `{market: prob_array}`; fills NaN with column median |
| `predict_single(row)` | 187-204 | Convenience wrapper for single-row prediction |
| `feature_importance(market)` | 206-217 | Returns sorted DataFrame of feature importances |
| `_build_targets(df, markets)` | 224-245 | Creates binary targets: home_win/draw/away_win/over_2_5/under_2_5/over_1_5/btts_yes |

**NaN Handling (line 136):** `X = X.fillna(X.median())` during both training and prediction.

**Markets supported for training (default, line 128):**
`["home_win", "draw", "away_win", "over_2_5", "under_2_5"]`

---

## 5. `src/models/ensemble.py` — Alternative Ensemble (NOT used by predict_single.py)

This class provides a cleaner abstraction but is **not currently wired into `predict_single.py`**. It uses a different fusion strategy:

- Uniform weights across ALL markets (not just XGB_MARKETS subset)
- Calibration applied AFTER fusion (vs predict_single.py applies calibration BEFORE XGB fusion)
- Has Brier-score-based weight optimization capability

**Key difference:** `EnsemblePredictor._predict_row()` (line 167) blends poisson+xgb for ALL markets including home_win/away_win, whereas `predict_single.py` explicitly excludes those from XGB blending.

---

## 6. Models Directory Contents

```
models/
  CHN/  calibrator.pkl, elo_ratings.json, meta.json, poisson_params.json
  CL/   elo_ratings.json, meta.json, poisson_params.json         (no calibrator)
  E0/   calibrator.pkl, elo_ratings.json, meta.json, poisson_params.json
  I1/   calibrator.pkl, elo_ratings.json, meta.json, poisson_params.json
  SP1/  calibrator.pkl, elo_ratings.json, meta.json, poisson_params.json
```

**No `.pkl` files for XGB models exist.** XGBoost is always trained fresh from CSV at prediction time when `--xgb` is passed.

---

## 7. Complete Data Flow Diagram

```
CLI Args (--csv, --home, --away, [--xgb], [--xgb-blend 0.6])
  |
  v
[load_models(model_dir)] OR [fit_poisson_from_csv + calculate_elo + fit_calibrator]
  |
  v (if --xgb)
[build_features_v2_from_csv(csv_path)]
  |-- reads CSV (E0.csv etc.)
  |-- auto-loads understat JSON (if available)
  |-- computes 72+ factor columns
  |-- returns df_v2 (full historical feature matrix)
  |
  v
[XGBoostPredictor().fit(df_v2, markets)]
  |-- filters to TRAIN_FEATURES (73 cols present in df_v2)
  |-- fills NaN with median
  |-- trains 5 separate XGBClassifier models (one per market)
  |
  v
[predict_single_match(home, away, poisson, calibrator, elo, ..., xgb_model, xgb_features_df)]
  |
  +-- Layer 1: poisson.predict(home, away) --> raw_probs (5 markets)
  |
  +-- Layer 2: calibrator.calibrate() (50/50 blend) --> calibrated_probs (5 markets)
  |
  +-- Layer 3 (if xgb):
  |     _build_xgb_feature_row(home, away, xgb_features_df, odds, ah_line)
  |       |-- finds home_team's last row as HomeTeam
  |       |-- finds away_team's last row as AwayTeam  
  |       |-- classifies each column: _home/_away/h2h/market/generic
  |       |-- overrides market cols from live odds
  |       |-- returns single-row DataFrame
  |     
  |     xgb_model.predict_proba(synth_row) --> xgb_probs (all trained markets)
  |     
  |     FOR market in XGB_MARKETS (under_2_5, draw, over_2_5, btts_yes, btts_no):
  |       final = (1 - 0.6) * calibrated + 0.6 * xgb_raw
  |       record shift in diagnostics
  |
  +-- Build model_output dict (with Asian handicap probs if ah_line)
  +-- Build plan_output dict (if odds provided --> EV/Kelly/tier logic)
  +-- Build diagnostics dict (factors, calibration shifts, xgb shifts, alerts)
  |
  v
JSON output (--json) OR human-readable text format
```

---

## 8. Critical Files Summary for Modifications

| File | Path | Lines of Interest |
|------|------|-------------------|
| Main entry | `/Users/a1_builder/WorkBuddy/football-betting/scripts/predict_single.py` | 210-347 (_build_xgb_feature_row), 352-623 (predict_single_match), 384-451 (fusion logic), 468-496 (output struct), 1058-1086 (XGB init) |
| XGB model | `/Users/a1_builder/WorkBuddy/football-betting/src/models/xgboost_model.py` | 35-101 (TRAIN_FEATURES), 104-222 (class), 160-185 (predict_proba) |
| V2 features | `/Users/a1_builder/WorkBuddy/football-betting/src/features_v2.py` | 31-103 (factor lists), 131-186 (main builder), 193-265 (market factors), 1383-1400 (from_csv wrapper) |
| Ensemble (alt) | `/Users/a1_builder/WorkBuddy/football-betting/src/models/ensemble.py` | 26-213 (class), 167-213 (_predict_row fusion) |
| Calibration | `/Users/a1_builder/WorkBuddy/football-betting/src/models/calibration.py` | 122-158 (_blend_calibrate) |
| Decision | `/Users/a1_builder/WorkBuddy/football-betting/src/decision.py` | 1-80 (constants, BetTier, BetCandidate) |
| Backtest | `/Users/a1_builder/WorkBuddy/football-betting/src/backtest.py` | 439-440 (parallel XGB_MARKETS usage) |
