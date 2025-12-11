# ADR 003: Caching Strategy

## Status
Accepted

## Context
The Wikipedia Quiz Application needs to cache multiple types of data with different lifetimes:
- **Wikipedia content**: Article text fetched from Wikipedia API (suggested TTL: 7 days)
- **Generated quizzes**: AI-generated quiz questions from articles (suggested TTL: 24 hours)
- **Quiz sessions**: Active user quiz sessions and scores (suggested TTL: 1 hour)

Caching reduces API calls to Wikipedia, minimizes expensive LLM operations, and improves response times. However, we need to balance performance gains against operational complexity for a demo/learning application.

## Decision Drivers
- **Deployment simplicity**: Minimize infrastructure dependencies
- **Developer experience**: Easy to develop and test locally
- **Performance**: Adequate caching for improved UX
- **Cost**: Low operational overhead
- **Scalability**: Sufficient for demo/learning use cases (not production scale)

## Options Considered

### Option 1: Redis (Dedicated Cache Server)
**Pros:**
- Industry-standard caching solution
- Excellent performance and scalability
- Rich feature set (TTL, eviction policies, pub/sub)
- Persistent storage options
- Supports distributed deployments

**Cons:**
- Additional infrastructure dependency
- Requires separate service deployment and management
- More complex local development setup
- Overkill for a demo/learning application
- Additional cost in cloud deployments

### Option 2: In-Memory (Python Dictionary with TTL)
**Pros:**
- Zero external dependencies
- Extremely simple implementation
- Fast access times
- Easy local development
- No additional deployment complexity

**Cons:**
- Data lost on server restart
- Not shared across multiple instances
- Memory consumption grows with cache size
- Need to implement TTL logic manually
- Not suitable for production horizontal scaling

### Option 3: SQLite (File-Based Database)
**Pros:**
- Persistent storage survives restarts
- No separate server required
- Built into Python standard library
- Simple backup and inspection
- Adequate performance for small-scale apps

**Cons:**
- Slower than in-memory solutions
- Single-writer limitation
- Not ideal for high-concurrency scenarios
- More complex than in-memory for cache use case
- Requires file system access

### Option 4: No Caching
**Pros:**
- Simplest possible implementation
- No cache invalidation concerns
- Always fresh data

**Cons:**
- Poor performance (repeated API/LLM calls)
- Higher costs (more LLM API usage)
- Slower user experience
- Unnecessary load on Wikipedia API
- Not practical for real usage

## Decision
**Selected: Option 2 - In-Memory Caching (Python Dictionary with TTL)**

We will implement a simple in-memory caching layer using Python dictionaries with time-to-live (TTL) management.

### Implementation Approach
```python
# Simple cache implementation
class SimpleCache:
    def __init__(self):
        self._cache = {}
        self._expiry = {}
    
    def set(self, key: str, value: Any, ttl_seconds: int):
        self._cache[key] = value
        self._expiry[key] = time.time() + ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            if time.time() < self._expiry[key]:
                return self._cache[key]
            else:
                # Expired, cleanup
                del self._cache[key]
                del self._expiry[key]
        return None
```

### Cache Configuration
- **Wikipedia articles**: 7 days (604800 seconds)
- **Generated quizzes**: 24 hours (86400 seconds)
- **Active quiz sessions**: 1 hour (3600 seconds)

## Rationale
For a demo/learning application, in-memory caching provides the optimal balance:

1. **Simplicity First**: No additional services to deploy, configure, or manage. The application remains self-contained.

2. **Adequate Performance**: In-memory access is extremely fast. Cache hits will be instantaneous, significantly improving UX without complexity.

3. **Development Experience**: Developers can run the entire application locally without installing Redis or managing additional services.

4. **Appropriate Scale**: For a demo/learning app with limited concurrent users, memory consumption will be minimal and data loss on restart is acceptable.

5. **Easy Testing**: Simple to mock and test without external dependencies.

6. **Future Migration Path**: If the application grows beyond demo scope, we can migrate to Redis with minimal code changes by implementing the same cache interface.

## Consequences

### Positive
- Zero infrastructure overhead
- Fast development iteration
- Simple deployment (single container/process)
- No cache server maintenance
- Reduced cloud costs

### Negative
- Cache cleared on application restart
- Not suitable for horizontal scaling (multiple instances)
- Manual TTL implementation required
- Memory consumption proportional to cache size

### Mitigation
- Implement basic cache size limits (LRU eviction)
- Monitor memory usage in production
- Clear migration path to Redis documented if scaling becomes necessary
- Consider Redis upgrade if: 
  - Application becomes production-ready
  - Need to scale horizontally
  - Cache persistence becomes critical

## Related Decisions
- [ADR 002: LLM and Agent Framework](002-llm-and-agent-framework.md) - Affects quiz generation caching
- [ADR 004: Deployment Architecture](004-deployment-architecture.md) - Influences cache viability

## Notes
This decision prioritizes learning and demonstration over production scalability. The simplicity gained significantly lowers the barrier to entry for developers exploring the application architecture.
