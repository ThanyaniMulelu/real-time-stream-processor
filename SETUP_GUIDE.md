# Development Guide

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/ThanyaniMulelu/real-time-stream-processor.git
cd real-time-stream-processor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo_sanitized_system.py
```

### Docker Development
```bash
# Build the image
docker build -t stream-processor .

# Run the container
docker run -d --name processor stream-processor

# View logs
docker logs -f processor

# Stop and remove
docker stop processor
docker rm processor
```

### Using Docker Compose
```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

---

## 🧪 Testing the Demo

### Expected Output
When you run `python demo_sanitized_system.py`, you should see:

```
=== SINGLE SCAN DEMO ===

============================================================
DUAL MARKET SCAN #1
============================================================
[source_1] Signal generated - Confidence: 81.0%, Confluence: 9/10
[source_2] No signal - confluence too low
[source_3] Signal generated - Confidence: 85.5%, Confluence: 7/10
...

=== RESULTS ===
Total results: 3
  - POSITIVE: 81.0% (9/10)
    Factors: Trend aligned, Volume confirmation, Momentum positive, Pattern: REVERSAL_BOTTOM
  - POSITIVE: 85.5% (7/10)
    Factors: Trend aligned, Volume confirmation, Pattern: REVERSAL_TOP
```

---

## 📦 Project Structure

```
.
├── README.md                    # Main documentation
├── demo_sanitized_system.py     # Demo application
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-container setup
├── .gitignore                   # Git exclusions
└── LICENSE                      # MIT License
```

---

## 🔧 Configuration

### Key Parameters

Edit these in `demo_sanitized_system.py`:

```python
# Circuit Breaker
CircuitBreaker(threshold=5, timeout=300)

# Retry Logic
max_retries = 3
initial_backoff = 1.0
max_backoff = 30.0

# Rate Limiting
semaphore = asyncio.Semaphore(3)  # Max concurrent requests

# Analysis Thresholds
min_confluence = 5  # Minimum score for signals
```

---

## 🛠️ Extending the System

### Adding New Data Sources

```python
# Add your source to the list
sources = [
    "source_1",
    "source_2",
    "your_new_source"  # Add here
]

# Implement custom fetcher if needed
async def fetch_custom_data(source: str):
    # Your implementation
    pass
```

### Customizing Analysis Factors

```python
def analyze(self, data: List[DataPoint]):
    # Add your custom factor
    if self._check_custom_indicator(data):
        factors.append("Custom indicator")
        confluence += 2
    
    # ... rest of analysis
```

---

## 📈 Performance Tuning

### Optimizing for High Volume
- Increase `semaphore` limit for more concurrency
- Reduce `rate_limit_delay` if API allows
- Use connection pooling for external APIs

### Reducing Latency
- Decrease `initial_backoff` for faster retries
- Adjust `circuit_breaker.timeout` based on SLA
- Profile with `timer()` context manager

---

## 🐛 Troubleshooting

### Common Issues

**Circuit Breaker Opens Frequently**
- Check network connectivity
- Increase `threshold` if transient failures are common
- Reduce `timeout` for faster recovery

**Low Signal Generation**
- Lower `min_confluence` threshold
- Adjust factor weights in analyzer
- Verify data quality from sources

**High Memory Usage**
- Limit data retention in `DataPoint` objects
- Implement cleanup for old analysis results
- Use streaming for large datasets

---

## 🤝 Contributing

While this is a demonstration project, suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details.

---

**For questions or issues, open a GitHub issue or contact the author.**
