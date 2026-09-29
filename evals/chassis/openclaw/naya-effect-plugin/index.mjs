import { createControlledEffectTool } from "./effect-protocol.mjs";

export default {
  id: "atento-naya-effect-qualification",
  name: "Atento Nayá Effect Qualification",
  description: "Qualification-only controlled external-effect adapter.",
  register(api) {
    api.registerTool(createControlledEffectTool());
  },
};
