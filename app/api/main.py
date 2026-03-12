from dotenv import load_dotenv
load_dotenv()

import os
print("OTEL_EXPORTER_OTLP_ENDPOINT =", os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))
print("OTEL_EXPORTER_OTLP_PROTOCOL =", os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL"))
print("OTEL_SERVICE_NAME =", os.getenv("OTEL_SERVICE_NAME"))

# -------------------------------
# OpenTelemetry setup (REQUIRED)
# -------------------------------
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
provider = trace.get_tracer_provider()

import os
if os.getenv("ENABLE_OTEL", "false").lower() == "true":
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint="http://localhost:4317",
                insecure=True
            )
        )
    )

# -------------------------------
# FastAPI app
# -------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="ServiceNow KB RAG API",
    version="1.0.0",
    description="FastAPI wrapper for ServiceNow Knowledge Base RAG system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
