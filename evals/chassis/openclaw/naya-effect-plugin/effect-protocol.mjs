import fs from "node:fs/promises";
import path from "node:path";

async function readJson(filePath) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    if (error && error.code === "ENOENT") return null;
    throw error;
  }
}

async function writeJsonAtomic(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  const tmp = `${filePath}.tmp-${process.pid}-${Date.now()}`;
  await fs.writeFile(tmp, JSON.stringify(value, null, 2) + "\n", "utf8");
  await fs.rename(tmp, filePath);
}

async function appendJsonLine(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.appendFile(filePath, JSON.stringify(value) + "\n", "utf8");
}

export class SimulatedCrashAfterProvider extends Error {
  constructor() {
    super("simulated crash after provider effect and before local terminal commit");
    this.name = "SimulatedCrashAfterProvider";
  }
}

export class FakeExternalProvider {
  constructor(rootDir) {
    this.rootDir = rootDir;
    this.effectsDir = path.join(rootDir, "effects");
    this.callsPath = path.join(rootDir, "provider-calls.jsonl");
  }

  effectPath(operationId) {
    return path.join(this.effectsDir, `${operationId}.json`);
  }

  async apply(operationId, payload) {
    await appendJsonLine(this.callsPath, {
      operationId,
      payload,
      at: new Date().toISOString(),
    });
    const existing = await readJson(this.effectPath(operationId));
    if (existing) {
      return { ...existing, providerReplay: true };
    }
    const receipt = {
      operationId,
      payload,
      receiptId: `provider:${operationId}`,
    };
    await writeJsonAtomic(this.effectPath(operationId), receipt);
    return receipt;
  }

  async read(operationId) {
    return readJson(this.effectPath(operationId));
  }

  async callCount() {
    try {
      const text = await fs.readFile(this.callsPath, "utf8");
      return text.split("\n").filter(Boolean).length;
    } catch (error) {
      if (error && error.code === "ENOENT") return 0;
      throw error;
    }
  }
}

export class ControlledEffectAdapter {
  constructor({ stateDir, provider }) {
    this.stateDir = stateDir;
    this.provider = provider;
  }

  operationPath(operationId) {
    return path.join(this.stateDir, "operations", `${operationId}.json`);
  }

  async readOperation(operationId) {
    return readJson(this.operationPath(operationId));
  }

  async persistOperation(operationId, value) {
    await writeJsonAtomic(this.operationPath(operationId), value);
  }

  async reconcile(operationId) {
    const operation = await this.readOperation(operationId);
    if (!operation) return { status: "missing", operationId };

    const receipt = await this.provider.read(operationId);
    if (!receipt) {
      return {
        status: "not_sent",
        operationId,
        proof: "authoritative-provider-readback",
      };
    }

    const completed = {
      ...operation,
      status: "completed",
      receipt,
      reconciled: true,
    };
    await this.persistOperation(operationId, completed);
    return completed;
  }

  async execute({ operationId, payload, faultAfterProvider = false }) {
    let operation = await this.readOperation(operationId);
    if (operation?.status === "completed") {
      return { ...operation, replayed: true };
    }

    if (operation?.status === "pending") {
      const reconciled = await this.reconcile(operationId);
      if (reconciled.status === "completed") {
        return { ...reconciled, replayed: true };
      }
      if (reconciled.status !== "not_sent") {
        return reconciled;
      }
    } else {
      operation = {
        operationId,
        payload,
        status: "pending",
        intentPersistedAt: new Date().toISOString(),
      };
      await this.persistOperation(operationId, operation);
    }

    const receipt = await this.provider.apply(operationId, payload);
    if (faultAfterProvider) {
      throw new SimulatedCrashAfterProvider();
    }

    const completed = {
      ...operation,
      status: "completed",
      receipt,
      reconciled: false,
    };
    await this.persistOperation(operationId, completed);
    return completed;
  }
}

export function createControlledEffectTool(options = {}) {
  const root =
    options.rootDir ||
    process.env.ATENTO_NAYA_EFFECT_ROOT ||
    path.join(process.cwd(), ".atento-naya-effect");
  const provider = new FakeExternalProvider(path.join(root, "provider"));
  const adapter = new ControlledEffectAdapter({
    stateDir: path.join(root, "adapter"),
    provider,
  });

  return {
    name: "naya_controlled_effect",
    description:
      "Qualification-only controlled external write using a persisted operation id and provider readback.",
    parameters: {
      type: "object",
      additionalProperties: false,
      required: ["operationId", "value"],
      properties: {
        operationId: { type: "string", minLength: 1 },
        value: { type: "string" },
      },
    },
    async execute(_id, params) {
      const result = await adapter.execute({
        operationId: params.operationId,
        payload: { value: params.value },
      });
      return {
        content: [{ type: "text", text: JSON.stringify(result) }],
        details: result,
      };
    },
  };
}
