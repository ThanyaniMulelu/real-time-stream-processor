# Real-Time Stream Processor with LLM Integration

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

A production-grade async Python system demonstrating real-time data stream processing with AI-powered validation, circuit breaker patterns, and multi-factor analysis.

## 🎯 Project Overview

This project showcases enterprise-level backend engineering patterns commonly used in real-time data processing systems:

- **Async Data Fetching** with exponential backoff retry
- **Circuit Breaker Pattern** for resilience against cascading failures  
- **LLM Integration** for AI-powered validation
- **Multi-Factor Scoring** with confluence-based decision making
- **Parallel Processing** with semaphore-based rate limiting
- **Performance Monitoring** and optimization

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)

### Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/real-time-stream-processor.git
cd real-time-stream-processor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo_sanitized_system.py
```

### Docker Deployment

```bash
# Build the image
docker build -t stream-processor .

# Run the container
docker run -d --name processor stream-processor

# View logs
docker logs -f processor
```

## 📋 Features

### 1. Circuit Breaker Pattern
Prevents cascade failures by temporarily blocking requests after threshold failures:

```python
circuit_breaker = CircuitBreaker(threshold=5, timeout=300)
if not circuit_breaker.should_allow():
    logger.warning("Circuit open - skipping request")
    return []
```

**Benefits:**
- Automatic failure detection
- Graceful degradation
- Self-healing after timeout

### 2. Exponential Backoff Retry
Intelligent retry mechanism that adapts to transient failures:

```python
backoff = 1.0
for attempt in range(max_retries):
    try:
        return await fetch_data()
    except Exception:
        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, max_backoff)
```

**Key Features:**
- Configurable max retries (default: 3)
- Exponential backoff (1s → 2s → 4s → max 30s)
- Per-source circuit breaker integration

### 3. LLM Integration Pattern
Demonstrates AI validation with graceful fallback:

```python
async def validate(self, result: AnalysisResult) -> bool:
    try:
        response = await self._call_llm(prompt, timeout=5.0)
        return "agree" in response.lower()
    except (TimeoutError, Exception) as e:
        logger.warning(f"LLM unavailable: {e} - defaulting to allow")
        return True  # Graceful degradation
```

**Production Considerations:**
- Timeout protection (5s)
- Error handling with fallback
- Structured prompt engineering
- Async non-blocking calls

### 4. Multi-Factor Confluence Scoring
Decision-making system that combines multiple signals:

```python
factors = []
confluence = 0

if check_trend(data):
    factors.append("Trend aligned")
    confluence += 2

if check_volume(data):
    factors.append("Volume confirmation")
    confluence += 2

if confluence >= min_threshold:
    return AnalysisResult(...)
```

**Configurable Thresholds:**
- Minimum confluence: 5/10 (adjustable)
- Confidence calculation: `min(confluence / 10.0, 1.0) * 0.9`

### 5. Parallel Processing with Rate Limiting
Concurrent processing with controlled resource usage:

```python
semaphore = asyncio.Semaphore(3)  # Max 3 concurrent

async def process_with_limit(source):
    async with semaphore:
        return await process_stream(source)

results = await asyncio.gather(*tasks, return_exceptions=True)
```

**Benefits:**
- Prevents resource exhaustion
- Respects API rate limits
- Error isolation (one failure doesn't crash all)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Stream Processor (Orchestrator)       │
└───────────────┬─────────────────────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼────┐  ┌──▼──────┐  ┌─▼──────────┐
│ Data   │  │ Multi-  │  │    LLM     │
│Fetcher │  │ Factor  │  │ Validator  │
│        │  │Analyzer │  │            │
└───┬────┘  └──┬──────┘  └─┬──────────┘
    │          │            │
    │          │            │
┌───▼──────────▼────────────▼──────────┐
│         Circuit Breakers             │
│   (Failure Detection & Recovery)     │
└──────────────────────────────────────┘
```

## 📊 Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Scan Latency** | < 2s | For 5 sources with 100 data points each |
| **Concurrent Sources** | 3 | Configurable via semaphore |
| **Retry Attempts** | 3 | With exponential backoff |
| **Circuit Reset** | 5 min | After threshold failures |
| **LLM Timeout** | 5s | Prevents blocking |

## 🧪 Testing

```bash
# Run the demo (single scan)
python demo_sanitized_system.py

# Expected output:
# === SINGLE SCAN DEMO ===
# [source_1] Signal generated - Confidence: 81.0%, Confluence: 9/10
# [source_2] No signal - confluence too low
# ...
# === RESULTS ===
# Total results: 3
```

## 🔧 Configuration

Key parameters can be adjusted in the `StreamProcessor` class:

```python
# Circuit breaker settings
CircuitBreaker(threshold=5, timeout=300)

# Retry configuration
max_retries = 3
initial_backoff = 1.0
max_backoff = 30.0

# Rate limiting
semaphore = asyncio.Semaphore(3)  # Max concurrent requests

# Analysis thresholds
min_confluence = 5  # Minimum score for signal generation
```

## 📚 Key Learnings

This project demonstrates solutions to common production challenges:

1. **Cascade Failure Prevention**: Circuit breakers isolate failures
2. **Rate Limit Compliance**: Semaphores control concurrency
3. **Transient Failure Handling**: Exponential backoff adapts to network issues
4. **AI Integration Pitfalls**: Timeouts and fallbacks prevent blocking
5. **Performance Optimization**: Async patterns for I/O-bound operations

## 🎓 Technologies Used

- **Python 3.11+**: Modern async/await syntax
- **asyncio**: Concurrent task execution
- **dataclasses**: Clean data modeling
- **Enum**: Type-safe signal classification
- **typing**: Full type hint coverage

## 📈 Production Deployment

For production deployment, consider:

1. **Monitoring**: Add Prometheus metrics
2. **Logging**: Integrate structured logging (JSON)
3. **Secrets Management**: Environment variables or secrets manager
4. **Horizontal Scaling**: Kubernetes deployment
5. **Observability**: Distributed tracing (OpenTelemetry)

## 🤝 Contributing

This is a demonstration project, but feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Thanyani Mulelu**
- GitHub: [@ThanyaniMulelu](https://github.com/ThanyaniMulelu)
- LinkedIn: [@ThanyaniMulelu]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/thanyani-selby-mulelu-09ba82177?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)

## 🙏 Acknowledgments

This project demonstrates patterns learned from building production systems at scale. Special thanks to the Python async community for excellent documentation and best practices.

---

**Note**: This is a sanitized demonstration project. The architecture patterns shown here are applicable to various domains including financial systems, IoT data processing, real-time analytics, and more.
