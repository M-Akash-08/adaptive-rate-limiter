# Adaptive Rate Limiter (FastAPI + Redis)

A backend-focused project that implements a **Token Bucket Rate Limiter** with an **Adaptive Feedback Controller**.  
The system dynamically adjusts request limits based on runtime conditions such as latency and error rate.

This project is built to understand **real-world backend system behavior**, not just static API throttling.

---

## 🚀 Features

- Token Bucket rate limiting (per user / per IP)
- Redis-based shared state (distributed-safe)
- FastAPI middleware (O(1) request path)
- Adaptive controller (feedback-based)
- Graceful handling of edge cases (no refill, overload)
- Retry-After support
- Python-based load testing

---

## 🧠 System Design Overview


