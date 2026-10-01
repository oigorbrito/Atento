from __future__ import annotations

import json
import sys

from evals.atentoeval.handoff_broker import BrokerContractError, ExplicitHandoffBroker


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise BrokerContractError("broker payload must be an object")
        result = ExplicitHandoffBroker().handoff(payload)
    except (BrokerContractError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2

    print(json.dumps({"ok": True, "envelope": result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
