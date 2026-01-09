"""
SANITIZED DEMO: Real-Time Stream Processor with LLM Validation
===============================================================
This is a simplified, generic version of a production system that demonstrates
technical skills without revealing proprietary business logic.

Key Features Demonstrated:
- Async data fetching with retry logic
- Circuit breaker pattern
- LLM integration for validation
- Multi-factor scoring system
- Performance optimization
- Production-ready error handling
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import time
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================
# DOMAIN MODELS
# ============================================================

class SignalType(Enum):
    """Signal classification"""
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


@dataclass
class DataPoint:
    """Represents a single data point from stream"""
    timestamp: int
    value: float
    volume: float
    metadata: Dict = field(default_factory=dict)


@dataclass
class AnalysisResult:
    """Result of multi-factor analysis"""
    signal_type: SignalType
    confidence: float  # 0.0 - 1.0
    confluence_score: int  # 0 - 10
    factors: List[str]
    timestamp: str


# ============================================================
# PERFORMANCE MONITORING
# ============================================================

@contextmanager
def timer(operation: str):
    """Context manager for performance monitoring"""
    start = time.time()
    yield
    elapsed = time.time() - start
    if elapsed > 0.1:  # Log if > 100ms
        logger.warning(f"[PERF] {operation} took {elapsed:.3f}s")


# ============================================================
# CIRCUIT BREAKER PATTERN
# ============================================================

class CircuitBreaker:
    """
    Circuit breaker to prevent cascade failures.
    Opens circuit after threshold failures, resets after timeout.
    """
    
    def __init__(self, threshold: int = 5, timeout: int = 300):
        self.threshold = threshold
        self.timeout = timeout
        self.failures: List[datetime] = []
        self.is_open = False
    
    def record_failure(self):
        """Record a failure"""
        now = datetime.now()
        self.failures.append(now)
        
        # Clean old failures
        cutoff = now - timedelta(seconds=self.timeout)
        self.failures = [f for f in self.failures if f > cutoff]
        
        # Check threshold
        if len(self.failures) >= self.threshold:
            self.is_open = True
            logger.warning(f"[CIRCUIT] OPEN after {len(self.failures)} failures")
    
    def record_success(self):
        """Record a success - reset circuit"""
        if self.is_open:
            logger.info("[CIRCUIT] CLOSED after success")
        self.is_open = False
        self.failures.clear()
    
    def should_allow(self) -> bool:
        """Check if operation should be allowed"""
        if not self.is_open:
            return True
        
        # Check if timeout passed
        if self.failures:
            last_failure = max(self.failures)
            if (datetime.now() - last_failure).total_seconds() > self.timeout:
                logger.info("[CIRCUIT] CLOSED after timeout")
                self.is_open = False
                return True
        
        return False


# ============================================================
# DATA FETCHER WITH RETRY LOGIC
# ============================================================

class DataFetcher:
    """
    Fetches data from external sources with:
    - Exponential backoff retry
    - Circuit breaker protection
    - Rate limiting
    """
    
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(threshold=5, timeout=300)
        self.rate_limit_delay = 0.5  # seconds between calls
        self.max_retries = 3
        self.initial_backoff = 1.0
        self.max_backoff = 30.0
    
    async def fetch_with_retry(self, source: str) -> List[DataPoint]:
        """
        Fetch data with exponential backoff retry.
        
        Demonstrates:
        - Circuit breaker pattern
        - Exponential backoff
        - Error handling
        """
        if not self.circuit_breaker.should_allow():
            logger.warning(f"[CIRCUIT] Skipping {source} - circuit open")
            return []
        
        backoff = self.initial_backoff
        
        for attempt in range(self.max_retries):
            try:
                # Simulate API call
                data = await self._fetch_data_internal(source)
                self.circuit_breaker.record_success()
                return data
                
            except Exception as e:
                self.circuit_breaker.record_failure()
                
                if attempt < self.max_retries - 1:
                    logger.warning(
                        f"[RETRY {attempt+1}/{self.max_retries}] "
                        f"{source} failed: {e}, backoff {backoff:.1f}s"
                    )
                    await asyncio.sleep(backoff)
                    backoff = min(backoff * 2, self.max_backoff)
                else:
                    logger.error(f"[FAILED] {source} after {self.max_retries} attempts")
        
        return []
    
    async def _fetch_data_internal(self, source: str) -> List[DataPoint]:
        """Internal fetch - replace with real API call"""
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # Simulate returning data
        return [
            DataPoint(
                timestamp=int(time.time() * 1000),
                value=100.0 + i,
                volume=1000.0,
                metadata={"source": source}
            )
            for i in range(100)
        ]


# ============================================================
# MULTI-FACTOR ANALYZER
# ============================================================

class MultiFactorAnalyzer:
    """
    Analyzes data using multiple factors and generates confluence score.
    
    Demonstrates:
    - Multi-factor decision making
    - Scoring systems
    - Performance optimization
    """
    
    def __init__(self, min_confluence: int = 5):
        self.min_confluence = min_confluence
    
    def analyze(self, data: List[DataPoint]) -> Optional[AnalysisResult]:
        """
        Analyze data and generate result if confluence threshold met.
        """
        if len(data) < 20:
            return None
        
        with timer("MultiFactorAnalyzer.analyze"):
            factors = []
            confluence = 0
            
            # Factor 1: Trend analysis
            if self._check_trend(data):
                factors.append("Trend aligned")
                confluence += 2
            
            # Factor 2: Volume analysis
            if self._check_volume(data):
                factors.append("Volume confirmation")
                confluence += 2
            
            # Factor 3: Momentum
            if self._check_momentum(data):
                factors.append("Momentum positive")
                confluence += 1
            
            # Factor 4: Pattern recognition
            pattern = self._detect_pattern(data)
            if pattern:
                factors.append(f"Pattern: {pattern}")
                confluence += 2
            
            # Check minimum confluence
            if confluence < self.min_confluence:
                return None
            
            # Calculate confidence
            confidence = min(confluence / 10.0, 1.0) * 0.9  # Max 90%
            
            return AnalysisResult(
                signal_type=SignalType.POSITIVE,
                confidence=confidence,
                confluence_score=confluence,
                factors=factors,
                timestamp=datetime.now().isoformat()
            )
    
    def _check_trend(self, data: List[DataPoint]) -> bool:
        """Check if trend is aligned"""
        recent = [d.value for d in data[-20:]]
        older = [d.value for d in data[-50:-20]]
        
        return sum(recent) / len(recent) > sum(older) / len(older)
    
    def _check_volume(self, data: List[DataPoint]) -> bool:
        """Check volume confirmation"""
        avg_volume = sum(d.volume for d in data[-20:]) / 20
        current_volume = data[-1].volume
        
        return current_volume > avg_volume * 1.5
    
    def _check_momentum(self, data: List[DataPoint]) -> bool:
        """Check momentum"""
        deltas = [data[i].value - data[i-1].value for i in range(-10, 0)]
        positive = sum(1 for d in deltas if d > 0)
        
        return positive >= 7  # 70% positive moves
    
    def _detect_pattern(self, data: List[DataPoint]) -> Optional[str]:
        """Detect patterns in data"""
        # Simplified pattern detection
        recent_high = max(d.value for d in data[-5:])
        recent_low = min(d.value for d in data[-5:])
        current = data[-1].value
        
        if current == recent_low and current < data[-2].value:
            return "REVERSAL_BOTTOM"
        elif current == recent_high and current > data[-2].value:
            return "REVERSAL_TOP"
        
        return None


# ============================================================
# LLM VALIDATOR (Mock)
# ============================================================

class LLMValidator:
    """
    Validates analysis using LLM (Large Language Model).
    
    Demonstrates:
    - LLM integration pattern
    - Async API calls
    - Graceful degradation
    """
    
    def __init__(self):
        self.timeout = 5.0
        self.enabled = True
    
    async def validate(self, result: AnalysisResult) -> bool:
        """
        Validate result using LLM.
        Returns True if LLM agrees, False otherwise.
        """
        if not self.enabled:
            return True  # Graceful degradation
        
        try:
            # Simulate LLM API call
            prompt = self._build_prompt(result)
            response = await self._call_llm(prompt)
            
            return "agree" in response.lower()
            
        except asyncio.TimeoutError:
            logger.warning("[LLM] Timeout - defaulting to allow")
            return True  # Don't block on timeout
            
        except Exception as e:
            logger.error(f"[LLM] Error: {e} - defaulting to allow")
            return True  # Don't block on error
    
    def _build_prompt(self, result: AnalysisResult) -> str:
        """Build structured prompt for LLM"""
        return f"""
        Analyze this signal:
        Type: {result.signal_type.value}
        Confidence: {result.confidence:.1%}
        Factors: {', '.join(result.factors)}
        
        Do you agree with this analysis? (yes/no)
        """
    
    async def _call_llm(self, prompt: str) -> str:
        """Simulate LLM API call"""
        await asyncio.sleep(0.5)  # Simulate network delay
        return "I agree with the analysis"


# ============================================================
# MAIN ORCHESTRATOR
# ============================================================

class StreamProcessor:
    """
    Main orchestrator that ties everything together.
    
    Demonstrates:
    - System architecture
    - Async coordination
    - Error handling
    - Production patterns
    """
    
    def __init__(self):
        self.fetcher = DataFetcher()
        self.analyzer = MultiFactorAnalyzer(min_confluence=5)
        self.validator = LLMValidator()
        self.scan_count = 0
        self.results_generated = 0
    
    async def process_stream(self, source: str) -> Optional[AnalysisResult]:
        """
        Process a single stream source.
        
        Pipeline:
        1. Fetch data with retry
        2. Analyze with multi-factor scoring
        3. Validate with LLM
        4. Return result if all checks pass
        """
        # Step 1: Fetch data
        data = await self.fetcher.fetch_with_retry(source)
        if not data:
            return None
        
        # Step 2: Analyze
        result = self.analyzer.analyze(data)
        if not result:
            logger.debug(f"[{source}] No signal - confluence too low")
            return None
        
        # Step 3: LLM validation
        if not await self.validator.validate(result):
            logger.info(f"[{source}] Rejected by LLM validator")
            return None
        
        logger.info(
            f"[{source}] Signal generated - "
            f"Confidence: {result.confidence:.1%}, "
            f"Confluence: {result.confluence_score}/10"
        )
        
        return result
    
    async def scan_multiple_sources(self, sources: List[str]) -> List[AnalysisResult]:
        """
        Scan multiple sources in parallel with concurrency limit.
        
        Demonstrates:
        - Parallel processing
        - Semaphore for rate limiting
        - Error aggregation
        """
        self.scan_count += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"SCAN #{self.scan_count} - Processing {len(sources)} sources")
        logger.info(f"{'='*60}")
        
        # Limit concurrent requests
        semaphore = asyncio.Semaphore(3)
        
        async def process_with_limit(source: str):
            async with semaphore:
                return await self.process_stream(source)
        
        # Process all sources in parallel
        tasks = [process_with_limit(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful results
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"[{sources[i]}] Failed: {result}")
            elif result is not None:
                valid_results.append(result)
                self.results_generated += 1
        
        logger.info(
            f"[SUMMARY] Scan #{self.scan_count}: "
            f"{len(valid_results)} signals generated"
        )
        logger.info(f"{'='*60}\n")
        
        return valid_results
    
    async def run_continuous(self, sources: List[str], interval: int = 60):
        """
        Run continuous scanning with interval.
        
        Demonstrates:
        - Production deployment pattern
        - Graceful shutdown
        - Error recovery
        """
        logger.info(f"Starting continuous processing (interval: {interval}s)")
        
        try:
            while True:
                results = await self.scan_multiple_sources(sources)
                
                # Process results (send notifications, save to DB, etc.)
                for result in results:
                    logger.info(f"[OUTPUT] {result.signal_type.value} - {result.confidence:.1%}")
                
                await asyncio.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}")


# ============================================================
# DEMO USAGE
# ============================================================

async def main():
    """Demo the system"""
    processor = StreamProcessor()
    
    # Demo sources
    sources = [
        "source_1",
        "source_2", 
        "source_3",
        "source_4",
        "source_5"
    ]
    
    # Single scan demo
    print("\n=== SINGLE SCAN DEMO ===\n")
    results = await processor.scan_multiple_sources(sources)
    
    print(f"\n=== RESULTS ===")
    print(f"Total results: {len(results)}")
    for result in results:
        print(f"  - {result.signal_type.value}: {result.confidence:.1%} ({result.confluence_score}/10)")
        print(f"    Factors: {', '.join(result.factors)}")
    
    # Uncomment to run continuous mode
    # await processor.run_continuous(sources, interval=60)


if __name__ == "__main__":
    asyncio.run(main())
