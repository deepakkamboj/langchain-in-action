# LangChain in Action - Chapter Generation Prompts

This folder contains comprehensive prompts and templates for generating chapters using the local RAG MCP server with official LangChain documentation.

## Files Overview

### 1. `chapter-generation-prompt.md`
**Primary comprehensive prompt** for generating chapters following the authoring guidelines.

**Contains**:
- Complete role and context definition
- Step-by-step RAG research workflow
- Detailed chapter structure requirements (11 sections)
- Code snippet standards and examples
- Enhanced learning element specifications
- Mermaid diagram requirements
- Quality assurance checklist
- Example workflows

**Use this when**: Generating a new chapter from scratch

**Key Features**:
- RAG-first approach (query → humanize → generate)
- Production-ready code focus
- Standard markdown blockquotes (no Callout components)
- 25-30 page target with proper distribution
- Complete validation checklist

---

### 2. `rag-tools-quick-reference.md`
**Quick reference guide** for the local MCP RAG server tools.

**Contains**:
- All 6 MCP RAG tool descriptions
- Parameters and usage examples
- Best practices for each tool
- Query strategy by chapter section
- Troubleshooting guide
- Complete workflow examples

**Use this when**: 
- Learning how to use RAG tools
- Planning research queries
- Debugging RAG integration
- Verifying documentation coverage

**Key Tools**:
- `mcp_local-rag_query_documents` - Semantic search
- `mcp_local-rag_humanize_text` - Content transformation
- `mcp_local-rag_list_files` - Available docs
- `mcp_local-rag_status` - System info
- `mcp_local-rag_ingest_file` - Add documentation
- `mcp_local-rag_delete_file` - Remove documentation

---

### 3. `chapter-template.md`
**Customizable template** for each chapter with step-by-step sections.

**Contains**:
- Quick start guide
- Pre-filled query templates
- Section-by-section generation instructions
- Checklists for each section
- Enhanced learning element placement
- Diagram templates
- Final validation checklist

**Use this when**: 
- Starting a specific chapter
- Need structured guidance
- Want section-by-section workflow
- Ensuring completeness

**Key Sections**:
- Research query templates (10+ queries)
- 11 chapter sections with detailed instructions
- Enhanced learning element distribution
- Code file organization
- Validation checklists

---

## Quick Start Guide

### For First-Time Chapter Generation

1. **Read the main prompt**: Start with `chapter-generation-prompt.md` to understand the complete process

2. **Learn the RAG tools**: Review `rag-tools-quick-reference.md` to understand available tools

3. **Use the template**: Copy `chapter-template.md` and customize for your specific chapter

4. **Follow the workflow**:
   ```
   Research (RAG queries) 
   → Humanize (top excerpts)
   → Generate (following structure)
   → Validate (against checklist)
   ```

### For Experienced Users

1. Copy the chapter template
2. Customize the query list
3. Execute RAG research
4. Generate content section-by-section
5. Validate with final checklist

---

## Available Documentation

The local RAG server contains **11 official LangChain documentation PDFs**:

1. Auffarth Ben - Generative AI with LangChain (1,128 chunks)
2. LangGraph Blueprint (1,438 chunks)
3. LangChain Programming for Beginners (178 chunks)
4. Building AI Agents with LangChain (109 chunks)
5. AI Agents In Action (934 chunks)
6. LangChain PrePrints (various)
7-11. Additional LangChain resources (292-600 chunks each)

**Total**: 5,010 chunks, ~27.5 MB of documentation

---

## Workflow Overview

### Phase 1: Research
```bash
# List available docs
mcp_local-rag_list_files()

# Execute 10+ queries
mcp_local-rag_query_documents(query="specific topic", limit=10)

# Repeat for all chapter topics
```

### Phase 2: Humanize
```bash
# Transform top excerpts
mcp_local-rag_humanize_text(
    text="documentation excerpt",
    addVariation=true
)
```

### Phase 3: Generate
```bash
# Follow chapter structure:
1. Introduction (2-3 pages)
2. What You Will Learn (0.5 pages)
3. Understanding Concepts (4-5 pages)
4. Hands-On Implementation (12-15 pages)
   - Basic (4-5 pages)
   - Enhanced (4-5 pages)
   - Advanced (4-5 pages)
5. Architecture (3-4 pages)
6. Best Practices (2-3 pages)
7. Common Pitfalls (2-3 pages)
8. Real-World Application (3-4 pages)
9. Implementation Exercise (2-3 pages)
10. Summary (1 page)
11. Technical References (0.5 pages)
```

### Phase 4: Validate
```bash
# Check against quality standards:
- RAG queries executed (min 5)
- Content grounded in docs
- Code examples tested
- Diagrams have captions
- Page count: 25-30
- Enhanced elements distributed
- No Callout components
```

---

## Chapter Structure Quick Reference

| Section                      | Pages  | % of Total | Key Elements                        |
| ---------------------------- | ------ | ---------- | ----------------------------------- |
| Introduction                 | 2-3    | 10%        | Context, value, preview             |
| What You Will Learn          | 0.5    | 2%         | 5-6 measurable outcomes             |
| Understanding Concepts       | 4-5    | 17%        | Theory, definitions, architecture   |
| Hands-On Implementation      | 12-15  | 50%        | Code snippets (basic→enhanced→adv) |
| Architecture & Design        | 3-4    | 13%        | Diagrams, patterns, decisions       |
| Best Practices               | 2-3    | -          | Actionable guidelines + code        |
| Common Pitfalls              | 2-3    | -          | Problem-solution pairs              |
| Real-World Application       | 3-4    | 13%        | Complete use case                   |
| Implementation Exercise      | 2-3    | 10%        | Guided project                      |
| Summary                      | 1      | 4%         | Key achievements, next steps        |
| Technical References         | 0.5    | 2%         | Links, packages, resources          |
| **Total**                    | **25-30** | **100%**  |                                     |

---

## Enhanced Learning Elements Distribution

| Element                  | Count per Chapter | Usage                           |
| ------------------------ | ----------------- | ------------------------------- |
| TIP                      | 8-12              | Practical advice                |
| IMPORTANT                | 4-6               | Critical information            |
| THINGS TO REMEMBER       | 2-3               | Key concept summaries           |
| DEFINITION               | 5-8               | Technical term definitions      |
| EXPERT INSIGHT           | 1-2               | Industry perspectives           |
| WARNING                  | 2-4               | Potential issues                |
| BEST PRACTICE            | 6-10              | Industry-standard approaches    |
| REAL-WORLD EXAMPLE       | 3-5               | Practical applications          |
| PERFORMANCE NOTE         | 2-4               | Optimization insights           |
| SECURITY CONSIDERATION   | 2-3               | Safety guidance                 |

**Format**: Always use markdown blockquotes
```markdown
> **LABEL**: Content here
```

**Never use**: Callout components (React/Nextra specific)

---

## Code File Organization

### Python Code Files
```
codes/
└── chapterXX/
    ├── 01_basic_[topic].py
    ├── 02_enhanced_[topic].py
    ├── 03_advanced_[topic].py
    └── utils.py
```

### Jupyter Notebooks
```
notebooks/
└── chapterXX/
    ├── 01_[descriptive_name].ipynb
    ├── 02_[descriptive_name].ipynb
    └── 03_[descriptive_name].ipynb
```

### Chapter Content
```
pages/
└── part[N]-[section]/
    └── chapterX.mdx
```

---

## Quality Standards

### Every Chapter Must:

**RAG Integration**:
- [ ] Execute minimum 5 RAG queries (recommended 10-15)
- [ ] Retrieve 50+ documentation passages
- [ ] Humanize top 3-5 excerpts
- [ ] Base all technical content on retrieved docs
- [ ] Verify API usage against documentation

**Content Structure**:
- [ ] Follow 11-section mandatory structure
- [ ] Meet 25-30 page target
- [ ] Proper section distribution (10%, 17%, 50%, 13%, 10%)
- [ ] Progressive complexity (basic → enhanced → advanced)

**Code Quality**:
- [ ] All snippets tested and functional
- [ ] Based on official LangChain patterns
- [ ] Include error handling
- [ ] Follow PEP 8 style
- [ ] Inline comments present
- [ ] Production-ready examples

**Visual Elements**:
- [ ] 3-4 Mermaid diagrams with captions
- [ ] 2-3 comparison tables with captions
- [ ] All figures numbered (X.Y format)
- [ ] All tables numbered (X.Y format)

**Enhanced Learning**:
- [ ] Proper distribution of all 10 element types
- [ ] Use markdown blockquotes only
- [ ] No Callout components
- [ ] Strategic placement throughout

---

## Example Usage

### Generate Chapter 5: Computer Vision Integration

```markdown
I need to generate Chapter 5: Computer Vision Integration.

Please follow this process:

1. **Research Phase** (use rag-tools-quick-reference.md):
   - List available documentation
   - Execute these queries:
     * "computer vision models CLIP GPT-4V"
     * "image understanding classification detection"
     * "OCR document intelligence"
     * "vision API integration LangChain"
     * "image-to-text workflows"
     * "video stream processing"
     * "vision-language agent architecture"
     * [5 more queries...]

2. **Humanization Phase**:
   - Humanize top 5 most relevant excerpts
   - Preserve technical accuracy
   - Add natural variation

3. **Generation Phase** (use chapter-template.md):
   - Follow 11-section structure
   - Include code snippets for:
     * Basic vision model integration
     * Enhanced with error handling
     * Advanced multi-modal workflows
   - Add Mermaid diagrams:
     * Vision pipeline architecture
     * Image processing flow
     * Vision-language interaction sequence
   - Include real-world application:
     * Medical imaging analysis use case

4. **Validation Phase**:
   - Check all requirements from chapter-generation-prompt.md
   - Verify 25-30 page length
   - Confirm all enhanced elements present
   - Test all code examples

Target: 25-30 pages, production-ready content, grounded in official docs.
```

---

## Troubleshooting

### Problem: Not enough RAG results
**Solution**: 
- Broaden query terms
- Try related concepts
- Execute more queries (increase from 5 to 10-15)

### Problem: Code examples don't match docs
**Solution**:
- Re-query for specific API usage
- Cross-reference multiple documentation sources
- Verify current LangChain version

### Problem: Content too technical/formal
**Solution**:
- Use humanize_text with addVariation: true
- Combine multiple sources
- Add practical context and examples

### Problem: Missing chapter sections
**Solution**:
- Use chapter-template.md as checklist
- Follow 11-section mandatory structure
- Validate against section distribution percentages

---

## Additional Resources

### Related Files
- `.github/instructions/langchain_authoring_guidelines.instructions.md` - Complete authoring rules
- `docs/langchain_book_outline.md` - Full 15-chapter outline
- `pages/part1-foundations/chapter2.mdx` - Example completed chapter

### Book Information
- **Title**: LangChain in Action
- **Subtitle**: Building Intelligent Multi-Modal and Context-Aware AI Agents
- **Publisher**: BPB Publications
- **Target Audience**: AI engineers, ML developers, data scientists
- **Language**: Python
- **Prerequisites**: Intermediate Python, APIs, basic ML concepts

---

## Contribution Guidelines

When adding new prompts or templates:

1. Follow existing formatting standards
2. Include practical examples
3. Add checklists for validation
4. Reference RAG tools where appropriate
5. Maintain consistency with authoring guidelines
6. Test with actual chapter generation
7. Update this README with new files

---

## Version History

- **v1.0** (2025-11-06): Initial prompt collection
  - chapter-generation-prompt.md
  - rag-tools-quick-reference.md
  - chapter-template.md
  - README.md

---

## Support

For questions or issues:
1. Review the main authoring guidelines
2. Check the RAG tools quick reference
3. Consult the chapter template
4. Validate against quality checklists

**Remember**: Always use RAG tools to ground content in official LangChain documentation!
