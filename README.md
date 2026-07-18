# phoenix-mcp-eval

> MCP server for Arize Phoenix — LLM tracing, evaluation, and dataset management via AI agents.

![python](https://img.shields.io/badge/python-3.11+-blue) ![Phoenix](https://img.shields.io/badge/Arize-Phoenix-purple) ![MCP](https://img.shields.io/badge/MCP-compatible-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## What is this?

`phoenix-mcp-eval` is an MCP (Model Context Protocol) server that exposes Arize Phoenix's LLM observability capabilities to AI agents. It enables AI-driven analysis of traces, evaluation of LLM outputs, and management of evaluation datasets — directly from an MCP-compatible agent.

Built for platform engineers and ML teams running LLM pipelines on AI Foundry, LangChain, or LlamaIndex who need automated quality assurance and tracing.

---

## Available Tools

| Tool | Description |
|---|---|
| `list_projects` | List all Phoenix tracing projects |
| `get_traces` | Retrieve LLM traces for a project with filters |
| `get_spans` | Get individual spans with input/output/latency data |
| `list_datasets` | List evaluation datasets in Phoenix |
| `get_dataset` | Fetch dataset examples for review or comparison |
| `list_evaluations` | List evaluation runs and their scores |
| `get_evaluation_summary` | Get aggregated evaluation metrics (precision, recall, etc.) |
| `query_traces` | Run structured queries over trace data |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Arize Phoenix instance (self-hosted or cloud)
- Phoenix API key or local server URL

### Installation

```bash
git clone https://github.com/akkireddy-challa/phoenix-mcp-eval
cd phoenix-mcp-eval
pip install -r requirements.txt
```

### Configuration

```bash
export PHOENIX_HOST=http://localhost:6006
export PHOENIX_API_KEY=<your-api-key>  # if using cloud
```

### Run

```bash
python server.py
```

### MCP Client Config (Claude Desktop)

```json
{
  "mcpServers": {
    "phoenix": {
      "command": "python",
      "args": ["/path/to/phoenix-mcp-eval/server.py"],
      "env": {
        "PHOENIX_HOST": "http://localhost:6006"
      }
    }
  }
}
```

---

## Security Model

- Connects to Phoenix via API key or local network only
- All operations are **read-only** by default (trace/eval retrieval)
- No model weights, prompts, or PII are transmitted outside Phoenix
- API key stored in environment variables, never in code
- Designed for internal network use within a Kubernetes cluster

---

## Use Cases at Telia

This pattern is used to allow AI agents to:

- Automatically review LLM trace quality after AI Foundry deployments
- Surface failing evaluation metrics to on-call engineers without manual Phoenix access
- Compare evaluation datasets across model versions
- Trigger re-evaluation jobs based on trace anomaly detection

---

## Roadmap

- [ ] `run_evaluation` — trigger evaluation jobs programmatically
- [ ] `create_dataset` — export traces to evaluation datasets
- [ ] `get_prompt_templates` — retrieve versioned prompts from Phoenix
- [ ] Integration with Azure AI Foundry deployment events
- [ ] GitHub Actions workflow for CI validation

---

## Related Projects

| Repo | Purpose |
|---|---|
| [k8s-mcp-server](https://github.com/akkireddy-challa/k8s-mcp-server) | Kubernetes cluster diagnostics via MCP |
| [azure-mcp-platform](https://github.com/akkireddy-challa/azure-mcp-platform) | Azure resource management via MCP |
| [grafana-mcp-observability](https://github.com/akkireddy-challa/grafana-mcp-observability) | Grafana dashboards and alerts via MCP |

---

## License

MIT License. See [LICENSE](LICENSE) for details.
