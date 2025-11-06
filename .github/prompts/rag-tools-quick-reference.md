# Local RAG MCP Tools Quick Reference

## Overview

The local MCP RAG server contains 11 official LangChain documentation PDFs with 5,010 total chunks. Use these tools to ground all chapter content in authoritative LangChain documentation.

---

## Available Tools

### 1. `mcp_local-rag_query_documents`

**Purpose**: Search through ingested LangChain PDFs using semantic search

**When to use**:
- Looking for official LangChain patterns and examples
- Verifying API usage and syntax
- Finding authoritative explanations of concepts
- Grounding code examples in official documentation

**Parameters**:
```json
{
  "query": "specific technical query",
  "limit": 10
}
```

**Best Practices**:
- Use specific technical queries (e.g., "ReAct agent implementation" vs "agents")
- Start with limit of 5-10, increase to 20 for comprehensive research
- Execute 5-10 different queries per chapter topic
- Cross-reference multiple results for complete understanding

**Example Queries**:
```
"LangChain agent architecture components"
"ReAct reasoning pattern implementation"
"memory management in conversational agents"
"vector store integration patterns"
"LCEL pipe operator syntax examples"
"custom tool BaseTool implementation"
"prompt template variable interpolation"
"output parser Pydantic models"
"sequential chain composition"
"error handling retry logic"
```

**Expected Output**:
```json
{
  "results": [
    {
      "content": "Retrieved passage text...",
      "metadata": {
        "file": "path/to/source.pdf",
        "chunk_index": 123,
        "score": 0.85
      }
    }
  ]
}
```

---

### 2. `mcp_local-rag_humanize_text`

**Purpose**: Transform retrieved documentation into natural, book-style prose

**When to use**:
- After retrieving official documentation passages
- Making technical content more readable
- Adapting formal documentation to book style

**Parameters**:
```json
{
  "text": "Documentation text to humanize",
  "preserveCase": false,
  "addVariation": true
}
```

**Best Practices**:
- Always humanize direct documentation quotes
- Preserve technical accuracy while improving readability
- Use addVariation: true for better flow
- Review humanized output for technical correctness

**Example Usage**:
```
Input: "The LangChain Expression Language (LCEL) is a declarative way to easily compose chains together."

Output: "LCEL provides a declarative approach to composing chains, making it intuitive and productive to build complex workflows without verbose imperative code."
```

---

### 3. `mcp_local-rag_list_files`

**Purpose**: List all ingested documentation files

**When to use**:
- Starting a new chapter to know available resources
- Verifying documentation coverage
- Planning research strategy

**Parameters**: None

**Expected Output**:
```json
{
  "files": [
    {
      "path": "/path/to/langchain-doc1.pdf",
      "chunks": 1128,
      "ingested_at": "2025-11-05T..."
    },
    {
      "path": "/path/to/langchain-doc2.pdf",
      "chunks": 934,
      "ingested_at": "2025-11-05T..."
    }
  ]
}
```

---

### 4. `mcp_local-rag_status`

**Purpose**: Get system status and database information

**When to use**:
- Verifying system health before research
- Understanding documentation coverage scope

**Parameters**: None

**Expected Output**:
```json
{
  "total_documents": 11,
  "total_chunks": 5010,
  "database_size_mb": 27.52,
  "uptime_seconds": 57335
}
```

---

### 5. `mcp_local-rag_ingest_file`

**Purpose**: Add new documentation to the vector database

**When to use**:
- Adding new LangChain documentation PDFs
- Updating existing documentation with new versions
- Adding supplementary reference materials

**Parameters**:
```json
{
  "filePath": "/absolute/path/to/new-doc.pdf"
}
```

**Note**: File path must be absolute

---

### 6. `mcp_local-rag_delete_file`

**Purpose**: Remove documentation from the database

**When to use**:
- Removing outdated documentation versions
- Cleaning up incorrect ingestion

**Parameters**:
```json
{
  "filePath": "/absolute/path/to/doc-to-remove.pdf"
}
```

---

## Available Documentation Sources

Based on previous queries, the RAG server contains these LangChain documentation PDFs:

1. **Auffarth Ben - Generative AI with LangChain** (1,128 chunks)
2. **LangGraph Blueprint** (1,438 chunks)
3. **LangChain Programming for Beginners** (178 chunks)
4. **Building AI Agents with LangChain** (109 chunks)
5. **AI Agents In Action** (934 chunks)
6. **LangChain PrePrints** (varies)
7. **Official LangChain Documentation** (varies)
8-11. Additional LangChain resources (292-600 chunks each)

**Total**: 11 documents, 5,010 chunks, ~27.5 MB

---

## Recommended Research Workflow

### Phase 1: Discovery (List + Status)
```bash
1. mcp_local-rag_list_files()
   → See what documentation is available

2. mcp_local-rag_status()
   → Verify system is operational
```

### Phase 2: Research (Query × 5-10)
```bash
3. For each major chapter topic/section:
   mcp_local-rag_query_documents(query="specific topic", limit=10)
   
   Example for Chapter 2 (Modular Design):
   - Query 1: "modular design chains composition"
   - Query 2: "LCEL declarative syntax"
   - Query 3: "custom tools implementation"
   - Query 4: "prompt template examples"
   - Query 5: "output parser types"
   - Query 6: "sequential chain patterns"
   - Query 7: "error handling chains"
   - Query 8: "testing chain components"
```

### Phase 3: Humanize (Top 3-5 Excerpts)
```bash
4. For most relevant documentation excerpts:
   mcp_local-rag_humanize_text(
     text="excerpt from query results",
     preserveCase=false,
     addVariation=true
   )
```

### Phase 4: Generate Content
```bash
5. Use retrieved and humanized content to:
   - Write technical explanations
   - Create code examples
   - Develop architecture descriptions
   - Include best practices
   - Add real-world examples
```

---

## Query Strategy by Chapter Section

### Introduction
- "[chapter topic] real-world applications"
- "[chapter topic] business value"
- "[chapter topic] use cases"

### Understanding Concepts
- "[core concept] definition LangChain"
- "[component] architecture"
- "[pattern] design principles"
- "[framework feature] benefits"

### Hands-On Implementation
- "[component] implementation example"
- "[API] usage code"
- "[pattern] step by step"
- "[integration] tutorial"

### Best Practices
- "[topic] best practices"
- "[component] production deployment"
- "[feature] optimization"
- "[issue] error handling"

### Common Pitfalls
- "[component] common errors"
- "[feature] troubleshooting"
- "[issue] solutions"
- "[problem] debugging"

---

## Query Quality Tips

### ✅ Good Queries (Specific, Technical)
```
"ReAct agent reasoning pattern implementation"
"LCEL pipe operator chain composition"
"ConversationBufferMemory usage examples"
"Pydantic output parser validation"
"custom tool BaseTool class methods"
```

### ❌ Poor Queries (Too Broad, Vague)
```
"agents"
"LangChain"
"how to use"
"examples"
"help"
```

### Query Refinement Pattern
1. **Start broad**: "LangChain agents"
2. **Get results**: See what's available
3. **Refine specific**: "ReAct agent tool selection process"
4. **Get detailed**: "ReAct agent error recovery patterns"

---

## Integration with Chapter Generation

### Before Writing Any Content
```python
# 1. Research phase
list_results = mcp_local-rag_list_files()
status = mcp_local-rag_status()

# 2. Query for chapter topics (minimum 5 queries)
queries = [
    "topic concept 1",
    "topic concept 2", 
    "topic concept 3",
    "topic implementation patterns",
    "topic best practices"
]

results = []
for query in queries:
    results.append(
        mcp_local-rag_query_documents(query=query, limit=10)
    )

# 3. Humanize top excerpts
humanized = []
for top_result in results[:3]:
    humanized.append(
        mcp_local-rag_humanize_text(
            text=top_result['content'],
            addVariation=True
        )
    )

# 4. Now write chapter using retrieved + humanized content
```

### During Content Generation
- Reference retrieved documentation in explanations
- Base code examples on official patterns from queries
- Use humanized text for natural prose
- Cite sources: "Following the official LangChain documentation..."

### After Content Generation
- Verify all technical claims against query results
- Cross-check API usage with retrieved examples
- Validate architectural patterns match documentation
- Ensure code examples align with official best practices

---

## Troubleshooting

### Problem: Query returns no results
**Solution**:
- Broaden search terms
- Try related concepts or synonyms
- Check documentation with `list_files`

### Problem: Retrieved content too technical
**Solution**:
- Use `humanize_text` with `addVariation: true`
- Combine multiple sources for clearer explanation
- Add practical context and examples

### Problem: Conflicting information
**Solution**:
- Query for more recent documentation
- Cross-reference with official LangChain GitHub
- Note version differences in content

### Problem: Code examples don't work
**Solution**:
- Verify API versions in documentation
- Check for deprecated patterns
- Test with current LangChain installation

---

## Quality Assurance

### Every chapter should:
- [ ] Execute minimum 5 RAG queries
- [ ] Retrieve 50+ documentation passages total
- [ ] Humanize top 3-5 most relevant excerpts
- [ ] Base all code on retrieved official patterns
- [ ] Reference documentation sources appropriately
- [ ] Verify technical accuracy against queries
- [ ] Cross-check API usage with retrieved examples

### Red Flags:
- ❌ No RAG queries executed before writing
- ❌ Code examples not matching official docs
- ❌ Unverified API usage patterns
- ❌ Missing source citations
- ❌ Conflicting information with documentation

---

## Example: Complete RAG Workflow for Chapter 2

```markdown
## Chapter 2: Modular LangChain Architecture

### Research Phase (10 queries executed):

1. query_documents("modular design LangChain chains", limit=10)
   → Found: 10 results, top score: 0.81 (Auffarth book, chain composition)

2. query_documents("LCEL LangChain Expression Language", limit=10)
   → Found: 10 results, top score: 0.82 (Programming book, declarative syntax)

3. query_documents("custom tools BaseTool implementation", limit=10)
   → Found: 10 results, top score: 1.07 (Auffarth book, tool patterns)

4. query_documents("prompt templates ChatPromptTemplate", limit=10)
   → Found: 10 results, top score: 0.90 (Programming book, template examples)

5. query_documents("output parsers JsonOutputParser", limit=10)
   → Found: 10 results, top score: 0.85 (Programming book, parser types)

6. query_documents("sequential chain composition", limit=10)
   → Found: 10 results, top score: 0.79 (Blueprint, multi-step workflows)

7. query_documents("chain error handling retry", limit=10)
   → Found: 10 results, top score: 0.88 (Auffarth book, resilience patterns)

8. query_documents("LCEL pipe operator examples", limit=10)
   → Found: 10 results, top score: 0.91 (Programming book, operator usage)

9. query_documents("chain testing patterns", limit=10)
   → Found: 10 results, top score: 0.76 (AI Agents book, test strategies)

10. query_documents("production chain deployment", limit=10)
    → Found: 10 results, top score: 0.83 (Blueprint, deployment best practices)

### Humanization Phase (3 excerpts):

1. Humanized top result from Query 1 (chain composition)
2. Humanized top result from Query 2 (LCEL syntax)
3. Humanized top result from Query 3 (custom tools)

### Content Generation:
✅ All technical content grounded in retrieved documentation
✅ Code examples based on official patterns
✅ Architecture descriptions match official sources
✅ Best practices validated against documentation
✅ API usage current and correct
```

---

## Support and Resources

- **Documentation Sources**: 11 LangChain PDFs (5,010 chunks)
- **Query Capacity**: Unlimited queries, ~10ms per query
- **Chunk Size**: ~500-1000 tokens per chunk
- **Embedding Model**: Transformers.js (local)
- **Vector Database**: LanceDB (local)
- **Retrieval Method**: Semantic similarity search

**Always use RAG tools before writing to ensure authoritative, accurate content!**
