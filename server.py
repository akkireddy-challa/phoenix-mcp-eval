"""phoenix-mcp-eval: MCP server for Arize Phoenix LLM observability.

Exposes Phoenix tracing projects, spans, evaluation datasets,
and evaluation results via the Model Context Protocol (MCP).

Author: Akkireddy Challa
License: MIT
"""

import os
import asyncio
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PHOENIX_HOST = os.environ.get("PHOENIX_HOST", "http://localhost:6006").rstrip("/")
PHOENIX_API_KEY = os.environ.get("PHOENIX_API_KEY", "")

HEADERS: dict[str, str] = {"Accept": "application/json"}
if PHOENIX_API_KEY:
    HEADERS["api-key"] = PHOENIX_API_KEY

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
async def phoenix_get(path: str, params: dict | None = None) -> Any:
    """Make a GET request to the Phoenix REST API."""
    async with httpx.AsyncClient(headers=HEADERS, timeout=30.0) as client:
        resp = await client.get(f"{PHOENIX_HOST}{path}", params=params)
        resp.raise_for_status()
        return resp.json()

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
server = Server("phoenix-mcp-eval")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_projects",
            description="List all Phoenix tracing projects.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="get_traces",
            description="Retrieve LLM traces for a project with optional filters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string", "description": "Phoenix project name"},
                    "limit": {"type": "integer", "description": "Max traces to return (default 50)"},
                    "status": {"type": "string", "description": "Filter by status: ok, error"},
                },
                "required": ["project_name"],
            },
        ),
        Tool(
            name="get_spans",
            description="Get individual spans with input, output, and latency data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "trace_id": {"type": "string", "description": "Trace ID to fetch spans for"},
                },
                "required": ["project_name", "trace_id"],
            },
        ),
        Tool(
            name="list_datasets",
            description="List evaluation datasets in Phoenix.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="get_dataset",
            description="Fetch dataset examples for review or eval comparison.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset_id": {"type": "string", "description": "Dataset ID"},
                    "limit": {"type": "integer", "description": "Max examples to return (default 20)"},
                },
                "required": ["dataset_id"],
            },
        ),
        Tool(
            name="list_evaluations",
            description="List evaluation runs and their scores for a project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                },
                "required": ["project_name"],
            },
        ),
        Tool(
            name="get_evaluation_summary",
            description="Get aggregated evaluation metrics (mean score, pass rate, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "eval_name": {"type": "string", "description": "Evaluation name (e.g., 'hallucination', 'qa_correctness')"},
                },
                "required": ["project_name", "eval_name"],
            },
        ),
        Tool(
            name="query_traces",
            description="Run a structured query over trace data by time range or metadata filter.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "start_time": {"type": "string", "description": "ISO8601 start time"},
                    "end_time": {"type": "string", "description": "ISO8601 end time"},
                    "status": {"type": "string", "description": "Filter by status"},
                },
                "required": ["project_name"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Route MCP tool calls to Phoenix REST API."""

    if name == "list_projects":
        data = await phoenix_get("/v1/projects")
        projects = data.get("data", [])
        lines = [f"{p.get('name')} (id={p.get('id')})" for p in projects]
        return [TextContent(type="text", text="\n".join(lines) or "No projects found.")]

    elif name == "get_traces":
        project = arguments["project_name"]
        limit = arguments.get("limit", 50)
        params = {"project_name": project, "limit": limit}
        if status := arguments.get("status"):
            params["status"] = status
        data = await phoenix_get("/v1/traces", params=params)
        traces = data.get("data", [])
        lines = [
            f"trace_id={t.get('context', {}).get('trace_id')} status={t.get('status_code')} latency={t.get('latency_ms')}ms"
            for t in traces
        ]
        return [TextContent(type="text", text="\n".join(lines) or "No traces found.")]

    elif name == "get_spans":
        project = arguments["project_name"]
        trace_id = arguments["trace_id"]
        data = await phoenix_get("/v1/spans", params={"project_name": project, "trace_id": trace_id})
        spans = data.get("data", [])
        lines = [
            f"{s.get('name')} ({s.get('span_kind')}) latency={s.get('latency_ms')}ms status={s.get('status_code')}"
            for s in spans
        ]
        return [TextContent(type="text", text="\n".join(lines) or "No spans found.")]

    elif name == "list_datasets":
        data = await phoenix_get("/v1/datasets")
        datasets = data.get("data", [])
        lines = [f"{d.get('name')} (id={d.get('id')}, examples={d.get('example_count', '?')})" for d in datasets]
        return [TextContent(type="text", text="\n".join(lines) or "No datasets found.")]

    elif name == "get_dataset":
        dataset_id = arguments["dataset_id"]
        limit = arguments.get("limit", 20)
        data = await phoenix_get(f"/v1/datasets/{dataset_id}/examples", params={"limit": limit})
        examples = data.get("data", [])
        lines = [f"Example {i+1}: input={str(e.get('input', ''))[:100]}" for i, e in enumerate(examples)]
        return [TextContent(type="text", text="\n".join(lines) or "No examples found.")]

    elif name == "list_evaluations":
        project = arguments["project_name"]
        data = await phoenix_get("/v1/evaluations", params={"project_name": project})
        evals = data.get("data", [])
        lines = [f"{e.get('name')} score={e.get('score')} label={e.get('label')}" for e in evals]
        return [TextContent(type="text", text="\n".join(lines) or "No evaluations found.")]

    elif name == "get_evaluation_summary":
        project = arguments["project_name"]
        eval_name = arguments["eval_name"]
        data = await phoenix_get("/v1/evaluations/summary", params={"project_name": project, "eval_name": eval_name})
        return [TextContent(type="text", text=str(data))]

    elif name == "query_traces":
        project = arguments["project_name"]
        params: dict = {"project_name": project}
        for field in ["start_time", "end_time", "status"]:
            if val := arguments.get(field):
                params[field] = val
        data = await phoenix_get("/v1/traces", params=params)
        traces = data.get("data", [])
        return [TextContent(type="text", text=f"Found {len(traces)} traces matching query.")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="phoenix-mcp-eval",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
