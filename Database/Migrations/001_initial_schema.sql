-- ============================================================================
-- AI Market Intelligence Platform - Initial Database Schema
-- Version: 001
-- Date: 2026-08-02
-- Description: Creates all core tables for market data, features, patterns,
--              predictions, model metrics, and experiment tracking.
-- ============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================================================
-- TABLE: market_candles_raw
-- Purpose: Store raw, unmodified market candle data from exchanges.
-- Rule: NEVER modify data in this table after insertion.
-- ============================================================================
CREATE TABLE IF NOT EXISTS market_candles_raw (
    id                  BIGSERIAL PRIMARY KEY,
    exchange            VARCHAR(50) NOT NULL,
    symbol              VARCHAR(30) NOT NULL,
    interval            VARCHAR(10) NOT NULL,
    open_time           TIMESTAMPTZ NOT NULL,
    close_time          TIMESTAMPTZ NOT NULL,
    open_price          DECIMAL(24, 8) NOT NULL,
    high_price          DECIMAL(24, 8) NOT NULL,
    low_price           DECIMAL(24, 8) NOT NULL,
    close_price         DECIMAL(24, 8) NOT NULL,
    volume              DECIMAL(24, 8) NOT NULL,
    quote_volume        DECIMAL(24, 8),
    trade_count         INTEGER,
    taker_buy_volume    DECIMAL(24, 8),
    taker_buy_quote_vol DECIMAL(24, 8),
    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_hash         VARCHAR(64),

    CONSTRAINT uq_raw_candle UNIQUE (exchange, symbol, interval, open_time)
);

CREATE INDEX IF NOT EXISTS idx_raw_candle_lookup
    ON market_candles_raw (exchange, symbol, interval, open_time DESC);

CREATE INDEX IF NOT EXISTS idx_raw_candle_time
    ON market_candles_raw (open_time DESC);

-- ============================================================================
-- TABLE: market_candles_processed
-- Purpose: Cleaned, validated, and normalized candle data.
-- ============================================================================
CREATE TABLE IF NOT EXISTS market_candles_processed (
    id                  BIGSERIAL PRIMARY KEY,
    raw_candle_id       BIGINT REFERENCES market_candles_raw(id),
    exchange            VARCHAR(50) NOT NULL,
    symbol              VARCHAR(30) NOT NULL,
    interval            VARCHAR(10) NOT NULL,
    open_time           TIMESTAMPTZ NOT NULL,
    close_time          TIMESTAMPTZ NOT NULL,
    open_price          DECIMAL(24, 8) NOT NULL,
    high_price          DECIMAL(24, 8) NOT NULL,
    low_price           DECIMAL(24, 8) NOT NULL,
    close_price         DECIMAL(24, 8) NOT NULL,
    volume              DECIMAL(24, 8) NOT NULL,
    quote_volume        DECIMAL(24, 8),
    trade_count         INTEGER,
    is_gap_filled       BOOLEAN DEFAULT FALSE,
    is_interpolated     BOOLEAN DEFAULT FALSE,
    validation_status   VARCHAR(20) DEFAULT 'valid',
    processed_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_processed_candle UNIQUE (exchange, symbol, interval, open_time)
);

CREATE INDEX IF NOT EXISTS idx_processed_candle_lookup
    ON market_candles_processed (exchange, symbol, interval, open_time DESC);

-- ============================================================================
-- TABLE: market_features
-- Purpose: Store computed features for ML consumption.
-- ============================================================================
CREATE TABLE IF NOT EXISTS market_features (
    id                  BIGSERIAL PRIMARY KEY,
    exchange            VARCHAR(50) NOT NULL,
    symbol              VARCHAR(30) NOT NULL,
    interval            VARCHAR(10) NOT NULL,
    open_time           TIMESTAMPTZ NOT NULL,
    feature_version     VARCHAR(20) NOT NULL DEFAULT 'v1',

    -- Price features
    log_return          DOUBLE PRECISION,
    pct_change          DOUBLE PRECISION,
    price_momentum      DOUBLE PRECISION,
    candle_body_ratio   DOUBLE PRECISION,
    upper_wick_ratio    DOUBLE PRECISION,
    lower_wick_ratio    DOUBLE PRECISION,
    bullish_strength    DOUBLE PRECISION,

    -- Trend features
    ema_9               DOUBLE PRECISION,
    ema_21              DOUBLE PRECISION,
    ema_50              DOUBLE PRECISION,
    ema_200             DOUBLE PRECISION,
    sma_20              DOUBLE PRECISION,
    sma_50              DOUBLE PRECISION,
    sma_200             DOUBLE PRECISION,
    trend_direction     DOUBLE PRECISION,
    trend_strength      DOUBLE PRECISION,
    ma_compression      DOUBLE PRECISION,

    -- Momentum features
    rsi_14              DOUBLE PRECISION,
    macd_line           DOUBLE PRECISION,
    macd_signal         DOUBLE PRECISION,
    macd_histogram      DOUBLE PRECISION,
    stoch_k             DOUBLE PRECISION,
    stoch_d             DOUBLE PRECISION,
    roc_10              DOUBLE PRECISION,
    momentum_divergence DOUBLE PRECISION,

    -- Volatility features
    atr_14              DOUBLE PRECISION,
    historical_vol_20   DOUBLE PRECISION,
    rolling_std_20      DOUBLE PRECISION,
    volatility_regime   DOUBLE PRECISION,
    bb_upper            DOUBLE PRECISION,
    bb_lower            DOUBLE PRECISION,
    bb_width            DOUBLE PRECISION,
    bb_pct              DOUBLE PRECISION,

    -- Volume features
    volume_change       DOUBLE PRECISION,
    volume_sma_20       DOUBLE PRECISION,
    volume_spike        DOUBLE PRECISION,
    volume_divergence   DOUBLE PRECISION,
    obv                 DOUBLE PRECISION,
    vwap                DOUBLE PRECISION,

    -- Market structure
    higher_high         BOOLEAN,
    higher_low          BOOLEAN,
    lower_high          BOOLEAN,
    lower_low           BOOLEAN,
    dist_to_support     DOUBLE PRECISION,
    dist_to_resistance  DOUBLE PRECISION,

    -- Time features
    hour_of_day         SMALLINT,
    day_of_week         SMALLINT,
    is_weekend          BOOLEAN,
    session_type        VARCHAR(20),

    -- ADX
    adx_14              DOUBLE PRECISION,
    plus_di             DOUBLE PRECISION,
    minus_di            DOUBLE PRECISION,

    computed_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_feature UNIQUE (exchange, symbol, interval, open_time, feature_version)
);

CREATE INDEX IF NOT EXISTS idx_features_lookup
    ON market_features (exchange, symbol, interval, open_time DESC);

-- ============================================================================
-- TABLE: market_patterns
-- Purpose: Store discovered market behavior patterns.
-- ============================================================================
CREATE TABLE IF NOT EXISTS market_patterns (
    id                      BIGSERIAL PRIMARY KEY,
    pattern_id              UUID DEFAULT uuid_generate_v4(),
    exchange                VARCHAR(50) NOT NULL,
    symbol                  VARCHAR(30) NOT NULL,
    interval                VARCHAR(10) NOT NULL,
    start_time              TIMESTAMPTZ NOT NULL,
    end_time                TIMESTAMPTZ NOT NULL,
    pattern_type            VARCHAR(50),
    cluster_id              INTEGER,
    embedding_vector        DOUBLE PRECISION[],
    market_state            VARCHAR(50),
    regime_at_discovery     VARCHAR(50),
    historical_occurrences  INTEGER DEFAULT 0,
    avg_outcome_return      DOUBLE PRECISION,
    success_rate            DOUBLE PRECISION,
    confidence_score        DOUBLE PRECISION,
    metadata                JSONB,
    discovered_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    model_version           VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_pattern_lookup
    ON market_patterns (exchange, symbol, interval, start_time DESC);

CREATE INDEX IF NOT EXISTS idx_pattern_cluster
    ON market_patterns (cluster_id);

-- ============================================================================
-- TABLE: market_regimes
-- Purpose: Store classified market regime states.
-- ============================================================================
CREATE TABLE IF NOT EXISTS market_regimes (
    id                  BIGSERIAL PRIMARY KEY,
    exchange            VARCHAR(50) NOT NULL,
    symbol              VARCHAR(30) NOT NULL,
    interval            VARCHAR(10) NOT NULL,
    open_time           TIMESTAMPTZ NOT NULL,
    regime_label        VARCHAR(50) NOT NULL,
    regime_probability  DOUBLE PRECISION NOT NULL,
    alt_regime_label    VARCHAR(50),
    alt_regime_prob     DOUBLE PRECISION,
    model_version       VARCHAR(50) NOT NULL,
    classified_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_regime UNIQUE (exchange, symbol, interval, open_time, model_version)
);

CREATE INDEX IF NOT EXISTS idx_regime_lookup
    ON market_regimes (exchange, symbol, interval, open_time DESC);

-- ============================================================================
-- TABLE: model_predictions
-- Purpose: Store every prediction for evaluation.
-- ============================================================================
CREATE TABLE IF NOT EXISTS model_predictions (
    id                  BIGSERIAL PRIMARY KEY,
    model_name          VARCHAR(100) NOT NULL,
    model_version       VARCHAR(50) NOT NULL,
    exchange            VARCHAR(50) NOT NULL,
    symbol              VARCHAR(30) NOT NULL,
    interval            VARCHAR(10) NOT NULL,
    prediction_time     TIMESTAMPTZ NOT NULL,
    target_time         TIMESTAMPTZ NOT NULL,
    horizon_candles     INTEGER NOT NULL,
    predicted_direction VARCHAR(10),
    direction_prob_up   DOUBLE PRECISION,
    direction_prob_down DOUBLE PRECISION,
    direction_prob_neutral DOUBLE PRECISION,
    predicted_return    DOUBLE PRECISION,
    predicted_volatility DOUBLE PRECISION,
    confidence_score    DOUBLE PRECISION,
    risk_score          DOUBLE PRECISION,
    regime_at_prediction VARCHAR(50),
    pattern_match_id    BIGINT,
    actual_direction    VARCHAR(10),
    actual_return       DOUBLE PRECISION,
    prediction_error    DOUBLE PRECISION,
    is_correct          BOOLEAN,
    evaluated_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_prediction_lookup
    ON model_predictions (model_name, model_version, exchange, symbol, interval, prediction_time DESC);

CREATE INDEX IF NOT EXISTS idx_prediction_evaluation
    ON model_predictions (is_correct, model_name, model_version);

-- ============================================================================
-- TABLE: model_metrics
-- Purpose: Track model performance over time.
-- ============================================================================
CREATE TABLE IF NOT EXISTS model_metrics (
    id                  BIGSERIAL PRIMARY KEY,
    model_name          VARCHAR(100) NOT NULL,
    model_version       VARCHAR(50) NOT NULL,
    evaluation_period   VARCHAR(50) NOT NULL,
    eval_start_time     TIMESTAMPTZ NOT NULL,
    eval_end_time       TIMESTAMPTZ NOT NULL,
    total_predictions   INTEGER NOT NULL,
    accuracy            DOUBLE PRECISION,
    precision_score     DOUBLE PRECISION,
    recall_score        DOUBLE PRECISION,
    f1_score            DOUBLE PRECISION,
    roc_auc             DOUBLE PRECISION,
    mae                 DOUBLE PRECISION,
    rmse                DOUBLE PRECISION,
    directional_accuracy DOUBLE PRECISION,
    profit_factor       DOUBLE PRECISION,
    max_drawdown        DOUBLE PRECISION,
    sharpe_ratio        DOUBLE PRECISION,
    sortino_ratio       DOUBLE PRECISION,
    win_rate            DOUBLE PRECISION,
    avg_win             DOUBLE PRECISION,
    avg_loss            DOUBLE PRECISION,
    metadata            JSONB,
    evaluated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_metrics_model
    ON model_metrics (model_name, model_version, evaluated_at DESC);

-- ============================================================================
-- TABLE: experiments
-- Purpose: Track ML experiments.
-- ============================================================================
CREATE TABLE IF NOT EXISTS experiments (
    id                  BIGSERIAL PRIMARY KEY,
    experiment_id       UUID DEFAULT uuid_generate_v4(),
    experiment_name     VARCHAR(200) NOT NULL,
    description         TEXT,
    dataset_version     VARCHAR(50),
    feature_version     VARCHAR(50),
    model_name          VARCHAR(100),
    model_version       VARCHAR(50),
    parameters          JSONB,
    training_duration_s DOUBLE PRECISION,
    validation_results  JSONB,
    performance_metrics JSONB,
    conclusion          TEXT,
    status              VARCHAR(20) DEFAULT 'running',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMPTZ
);

-- ============================================================================
-- TABLE: data_quality_log
-- Purpose: Track data quality issues.
-- ============================================================================
CREATE TABLE IF NOT EXISTS data_quality_log (
    id                  BIGSERIAL PRIMARY KEY,
    exchange            VARCHAR(50) NOT NULL,
    symbol              VARCHAR(30) NOT NULL,
    interval            VARCHAR(10) NOT NULL,
    issue_type          VARCHAR(50) NOT NULL,
    issue_description   TEXT,
    affected_time_start TIMESTAMPTZ,
    affected_time_end   TIMESTAMPTZ,
    resolution          VARCHAR(50),
    detected_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- TABLE: model_registry
-- Purpose: Model versioning and deployment status.
-- ============================================================================
CREATE TABLE IF NOT EXISTS model_registry (
    id                  BIGSERIAL PRIMARY KEY,
    model_name          VARCHAR(100) NOT NULL,
    model_version       VARCHAR(50) NOT NULL,
    model_type          VARCHAR(50) NOT NULL,
    model_path          TEXT NOT NULL,
    onnx_path           TEXT,
    training_dataset    VARCHAR(200),
    feature_version     VARCHAR(50),
    parameters          JSONB,
    training_date       TIMESTAMPTZ NOT NULL,
    best_metric_name    VARCHAR(50),
    best_metric_value   DOUBLE PRECISION,
    deployment_status   VARCHAR(20) DEFAULT 'candidate',
    deployed_at         TIMESTAMPTZ,
    retired_at          TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_model_version UNIQUE (model_name, model_version)
);

-- ============================================================================
-- Partitioning hint: For production with billions of rows, partition
-- market_candles_raw and market_candles_processed by open_time (monthly).
-- For now, indexes are sufficient.
-- ============================================================================

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO amip_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO amip_admin;
