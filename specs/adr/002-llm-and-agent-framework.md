# ADR 002: LLM Provider and Agent Framework Selection

## Status
Accepted

## Context
The Wikipedia Quiz Application requires an LLM-powered agentic system to generate high-quality quiz questions from Wikipedia content. The system implements a 4-stage pipeline:

1. **Topic Resolution** - Disambiguate user queries and find appropriate Wikipedia articles
2. **Content Extraction** - Retrieve and parse relevant Wikipedia content
3. **Question Generation** - Create multiple-choice questions from the content
4. **Quality Validation** - Ensure questions meet quality standards

### Performance Requirements
- Total pipeline execution: <10 seconds
- LLM processing time: <6 seconds
- Support for real-time user interactions

### Project Constraints
- Demo/learning application (cost-conscious)
- Need for rapid development and iteration
- Single developer implementation
- Educational focus requiring high-quality outputs

## Decision

### LLM Provider: **Anthropic Claude (Claude 3.5 Sonnet)**

We will use Anthropic's Claude 3.5 Sonnet as the primary LLM provider.

### Agent Framework: **LangGraph (part of LangChain ecosystem)**

We will use LangGraph for implementing the agent pipeline, with selective use of LangChain components where beneficial.

## Rationale

### LLM Provider Analysis

#### Option 1: OpenAI GPT-4
**Pros:**
- Excellent general performance
- Strong ecosystem and tooling support
- Well-documented with extensive examples
- Fast response times with GPT-4o

**Cons:**
- Higher cost per token ($10-30 per 1M tokens)
- Rate limits can be restrictive for new accounts
- Less strong at following structured instructions compared to Claude

**Cost Estimate:** ~$0.01-0.03 per quiz generation

#### Option 2: Anthropic Claude 3.5 Sonnet ✓ **SELECTED**
**Pros:**
- Excellent instruction following and structured output generation
- Superior performance on reasoning tasks (ideal for question generation)
- Competitive pricing ($3 per 1M input tokens, $15 per 1M output tokens)
- 200K context window (handles long Wikipedia articles)
- Strong at generating educational content
- Better at following complex multi-step instructions
- Fast inference times meeting our <6 second requirement

**Cons:**
- Slightly smaller ecosystem than OpenAI
- Requires separate API key management

**Cost Estimate:** ~$0.005-0.015 per quiz generation

**Why Claude wins:** The superior instruction-following capability is critical for our multi-stage pipeline. Claude's ability to generate well-structured, educational content makes it ideal for quiz question generation. The lower cost and larger context window provide additional benefits for handling comprehensive Wikipedia articles.

#### Option 3: Open-Source Models (Llama 3, Mistral)
**Pros:**
- Zero API costs (only infrastructure)
- Full control and privacy
- No rate limits

**Cons:**
- Requires infrastructure setup and management
- Higher latency (unless using expensive GPU infrastructure)
- Lower quality outputs for complex reasoning tasks
- Significant development overhead
- Doesn't meet <6 second performance requirement without costly infrastructure

**Cost Estimate:** $50-200/month for capable GPU hosting

**Why rejected:** For a demo/learning application, the infrastructure complexity and management overhead outweigh the cost savings. The quality-to-effort ratio doesn't justify the investment.

### Agent Framework Analysis

#### Option 1: LangChain (Traditional Chains)
**Pros:**
- Mature ecosystem with extensive integrations
- Large community and resources
- Well-documented

**Cons:**
- Overly complex for simple use cases
- "Black box" abstractions can hide important details
- Difficult to debug and customize
- Heavy dependencies

#### Option 2: LangGraph ✓ **SELECTED**
**Pros:**
- Purpose-built for agentic workflows and state machines
- Explicit state management (easier debugging)
- Graph-based architecture matches our 4-stage pipeline naturally
- Built on LangChain but more transparent and controllable
- Excellent for conditional routing and error handling
- Supports streaming and checkpointing
- Lighter weight than full LangChain
- Growing community with strong documentation

**Cons:**
- Newer framework (less mature than LangChain)
- Smaller ecosystem than pure LangChain
- Learning curve for graph-based thinking

**Why LangGraph wins:** Our 4-stage pipeline maps perfectly to a directed graph. LangGraph provides explicit control over state transitions, making it easy to implement timeouts, retries, and quality checks. The transparency aids in debugging and optimization, critical for meeting our <10 second requirement.

#### Option 3: LlamaIndex
**Pros:**
- Excellent for RAG (Retrieval-Augmented Generation)
- Strong document parsing capabilities
- Built-in evaluation tools

**Cons:**
- Primarily focused on document retrieval/indexing
- Less suitable for multi-stage agent pipelines
- Overkill for our Wikipedia API integration

**Why rejected:** While LlamaIndex excels at RAG, we're using the Wikipedia API directly rather than building a document index. The framework's strengths don't align with our needs.

#### Option 4: CrewAI
**Pros:**
- Role-based agent paradigm
- Good for multi-agent collaboration
- Simple configuration

**Cons:**
- Opinionated architecture may not fit our linear pipeline
- Less control over execution flow
- Newer and less mature
- Overhead of multi-agent abstraction for our use case

**Why rejected:** Our pipeline is sequential with clear stages, not a collaborative multi-agent scenario. CrewAI's abstractions add complexity without clear benefits.

#### Option 5: Custom Implementation
**Pros:**
- Complete control
- Minimal dependencies
- Optimized for exact needs

**Cons:**
- Significant development time
- Need to implement error handling, retries, state management
- No community support or best practices
- Maintenance burden

**Why rejected:** Building custom infrastructure distracts from the core application logic. LangGraph provides the structure we need without excessive overhead.

## Implementation Plan

### Architecture
```
┌─────────────────┐
│  User Input     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Topic Resolution│ ◄── Claude 3.5 Sonnet
│    (Node 1)     │     (Disambiguate query)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Content Extract  │ ◄── Wikipedia API
│    (Node 2)     │     (Fetch article)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Question Gen     │ ◄── Claude 3.5 Sonnet
│    (Node 3)     │     (Create questions)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Quality Validate │ ◄── Claude 3.5 Sonnet
│    (Node 4)     │     (Validate & refine)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Quiz Output    │
└─────────────────┘
```

### Technology Stack
- **LLM API Client:** Anthropic Python SDK
- **Agent Framework:** LangGraph
- **Supporting Libraries:** 
  - LangChain core utilities (prompt templates, output parsers)
  - Wikipedia API client
  - Pydantic for data validation

### Cost Management
- Implement response caching for repeated queries
- Use prompt optimization to minimize token usage
- Monitor API usage with budget alerts
- Consider implementing graceful degradation (fewer questions if approaching limits)

### Performance Optimization
- Parallel execution where possible (e.g., generating multiple questions simultaneously)
- Streaming responses for better perceived performance
- Timeout handling at each node
- Cached Wikipedia content to avoid re-fetching

## Consequences

### Positive
- High-quality quiz question generation leveraging Claude's strengths
- Clear, debuggable pipeline structure with LangGraph
- Predictable costs suitable for demo/learning project (~$0.005-0.015 per quiz)
- Fast iteration and development cycle
- Meeting performance requirements (<10 second total, <6 second LLM)
- Scalable architecture if needs grow

### Negative
- Dependency on Anthropic API availability
- API costs (though minimal for demo scale)
- Need to manage API keys and secrets
- Potential rate limiting during high usage

### Neutral
- Learning curve for LangGraph (moderate, well-documented)
- Less common stack than OpenAI + traditional LangChain (but growing)

## Alternatives Considered
See detailed analysis above for:
- OpenAI GPT-4 / GPT-4o
- Open-source models (Llama 3, Mistral)
- Traditional LangChain chains
- LlamaIndex
- CrewAI
- Custom implementation

## Success Metrics
- Quiz generation completes in <10 seconds (target: 6-8 seconds)
- Question quality score >4/5 (subjective evaluation)
- Cost per quiz <$0.02
- System uptime >99% (dependent on Anthropic API)
- Successful generation rate >95%

## Review Date
To be reviewed after initial implementation (estimated 4-6 weeks) to assess:
- Actual performance vs. targets
- Cost actuals vs. estimates
- Development experience and productivity
- Question quality in production use

## Amendment: Azure OpenAI Migration (December 11, 2025)

### Status
Superseded by Azure OpenAI implementation

### Context
During implementation, the project requirements evolved to leverage existing Azure infrastructure and enterprise Azure OpenAI subscriptions. This change was driven by:

1. **Enterprise Compatibility**: Existing Azure subscription with OpenAI service already provisioned
2. **Compliance**: Azure OpenAI meets enterprise data residency and compliance requirements
3. **Cost Management**: Centralized billing and cost tracking through Azure
4. **Infrastructure Alignment**: Consistency with other Azure-hosted services

### Changes Made

**LLM Provider:** Changed from Anthropic Claude 3.5 Sonnet to **Azure OpenAI**
- Supports GPT-4, GPT-4 Turbo, GPT-3.5 Turbo deployments
- Uses Azure-hosted models with same capabilities as OpenAI's API
- Configuration via Azure endpoint, API key, API version, and deployment name

**Agent Framework:** LangGraph (unchanged)
- LangGraph supports multiple LLM providers through LangChain's abstraction
- Migration required minimal code changes (swap `ChatAnthropic` to `AzureChatOpenAI`)
- Agent pipeline architecture remains identical

**Configuration Changes:**
```env
# Before (Anthropic)
ANTHROPIC_API_KEY=sk-ant-xxx

# After (Azure OpenAI)
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

**Code Changes:**
- Updated `requirements.txt`: Replaced `anthropic` + `langchain-anthropic` with `openai` + `langchain-openai`
- Updated `quiz_generator.py`: Changed from `ChatAnthropic` to `AzureChatOpenAI`
- Updated environment loading in `main.py`: Added `dotenv` loading before agent initialization

### Consequences

**Positive:**
- ✅ Seamless integration with existing Azure infrastructure
- ✅ Enterprise-grade security and compliance
- ✅ Centralized cost management
- ✅ No changes required to agent pipeline logic
- ✅ Flexibility to use GPT-4, GPT-4 Turbo, or GPT-3.5 Turbo

**Negative:**
- ⚠️ Requires Azure subscription and OpenAI service provisioning
- ⚠️ Slightly more complex configuration (4 env vars vs 1)
- ⚠️ Tied to Azure ecosystem

**Neutral:**
- Question generation quality remains comparable (both are frontier models)
- Performance characteristics similar (both meet <6s LLM requirement)
- Cost varies by deployment type (Azure pricing vs Anthropic pricing)

### Migration Path

The original ADR analysis and decision-making process remains valid. The migration to Azure OpenAI was a deployment-time optimization based on operational requirements rather than a technical deficiency in the original choice.

To revert to Anthropic Claude if needed:
1. Update `requirements.txt`: Replace `openai`/`langchain-openai` with `anthropic`/`langchain-anthropic`
2. Update `quiz_generator.py`: Change `AzureChatOpenAI` back to `ChatAnthropic`
3. Update `.env`: Use single `ANTHROPIC_API_KEY` variable

---

## References
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Wikipedia API Documentation](https://www.mediawiki.org/wiki/API:Main_page)
- [LangChain Documentation](https://python.langchain.com/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)

## Notes
- Consider A/B testing with GPT-4 once initial implementation is complete
- Monitor for Claude API updates (e.g., Claude 4 when available)
- Track LangGraph ecosystem growth for additional capabilities
- May need to implement fallback to GPT-4 for redundancy in production

