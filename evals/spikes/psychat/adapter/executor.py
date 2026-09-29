from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

from .contracts import ExecutionRequest, ExecutionResult
from .resilience import retry_with_timeout_boundary


class PsyChatDonorPort(Protocol):
    """Narrow seam around the upstream RAG behavior."""

    def respond(
        self,
        *,
        message: str,
        session_state: dict,
        force_retrieval: bool = False,
    ) -> tuple[str, dict]: ...


def _retrieval_id(doc: Any) -> str | None:
    if not isinstance(doc, Mapping):
        return None

    direct = doc.get("id")
    if direct:
        return str(direct)

    metadata = doc.get("metadata")
    if isinstance(metadata, Mapping):
        for key in ("qa_id", "id", "source"):
            value = metadata.get(key)
            if value:
                return str(value)
    return None


class PsyChatExecutorAdapter:
    capability = "knowledge.rag"
    executor_id = "psychat"

    def __init__(self, donor: PsyChatDonorPort) -> None:
        self._donor = donor

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        request.validate()

        def invoke() -> tuple[str, dict]:
            return self._donor.respond(
                message=request.message,
                session_state=dict(request.state),
                force_retrieval=True,
            )

        response, returned_state = retry_with_timeout_boundary(invoke)
        next_state = dict(returned_state)
        turn_metadata = next_state.pop("_atento_turn", {})
        if not isinstance(turn_metadata, Mapping):
            turn_metadata = {}

        retrieval_docs = next_state.get("last_retrieval_docs", [])
        if not isinstance(retrieval_docs, list):
            retrieval_docs = []
        retrieved_ids = [
            doc_id
            for doc_id in (_retrieval_id(doc) for doc in retrieval_docs)
            if doc_id is not None
        ]

        # This executor is only selected for knowledge.rag and always invokes
        # the donor with force_retrieval=True. A successful execution therefore
        # means retrieval was attempted, even when zero documents were found.
        attempted = True
        used_rag = bool(
            turn_metadata.get("used_rag", bool(retrieval_docs))
        )
        index_info = turn_metadata.get("index", {})
        if not isinstance(index_info, Mapping):
            index_info = {}

        rag_event = {
            "event": "rag.completed",
            "attempted": attempted,
            "used": used_rag,
            "retrieved_count": len(retrieval_docs),
            "retrieved_ids": retrieved_ids,
            "index": {
                key: index_info[key]
                for key in (
                    "name",
                    "index_schema",
                    "embedding_identity",
                    "corpus_identity",
                )
                if key in index_info
            },
        }

        return ExecutionResult(
            response=response,
            executor=self.executor_id,
            capability=self.capability,
            trace=(rag_event,),
            metadata={"next_state": next_state},
        )
