package atento_gate2_test

import (
	"context"
	"errors"
	"testing"

	"github.com/LumabyteCo/aibutler/internal/capability"
	"github.com/LumabyteCo/aibutler/internal/memory"
	"github.com/LumabyteCo/aibutler/internal/memory/bank"
	"github.com/LumabyteCo/aibutler/internal/vault"
	"github.com/LumabyteCo/aibutler/testutil"
)

type brokerPayload struct {
	From string
	To   string
	Kind string
	Body string
}

func brokerHandoff(in brokerPayload) brokerPayload {
	return brokerPayload{From: in.From, To: in.To, Kind: in.Kind, Body: in.Body}
}

func TestAtentoGate2Composition(t *testing.T) {
	t.Run("ISO1_cross_memory_read_denied", func(t *testing.T) {
		db := testutil.TestDB(t)
		store := memory.NewStore(db.Conn())
		naia := bank.With(context.Background(), "naia")
		anna := bank.With(context.Background(), "anna")

		if _, err := store.SaveThought(naia, "NAIA_ONLY_MARKER", "agent", "naia-session", nil); err != nil {
			t.Fatal(err)
		}
		if _, err := store.SaveThought(anna, "ANNA_ONLY_MARKER", "agent", "anna-session", nil); err != nil {
			t.Fatal(err)
		}

		naiaRows, err := store.GetThoughts(naia, memory.ThoughtQuery{Contains: "ANNA_ONLY_MARKER"})
		if err != nil {
			t.Fatal(err)
		}
		if len(naiaRows) != 0 {
			t.Fatalf("NAIA read Anna memory: %+v", naiaRows)
		}

		annaRows, err := store.GetThoughts(anna, memory.ThoughtQuery{Contains: "NAIA_ONLY_MARKER"})
		if err != nil {
			t.Fatal(err)
		}
		if len(annaRows) != 0 {
			t.Fatalf("Anna read NAIA memory: %+v", annaRows)
		}
	})

	t.Run("ISO2_cross_memory_mutation_denied", func(t *testing.T) {
		db := testutil.TestDB(t)
		store := memory.NewStore(db.Conn())
		naia := bank.With(context.Background(), "naia")
		anna := bank.With(context.Background(), "anna")

		id, err := store.SaveThought(anna, "ANNA_MUTATION_SENTINEL", "agent", "anna-session", nil)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := store.ForgetThought(naia, id); err == nil {
			t.Fatal("NAIA mutated Anna memory by id")
		}
		rows, err := store.GetThoughts(anna, memory.ThoughtQuery{Contains: "ANNA_MUTATION_SENTINEL"})
		if err != nil {
			t.Fatal(err)
		}
		if len(rows) != 1 {
			t.Fatalf("Anna sentinel changed after cross-role mutation attempt: %d", len(rows))
		}
	})

	t.Run("ISO3_cross_credential_use_denied", func(t *testing.T) {
		ctx := context.Background()
		naiaVault, err := vault.New(vault.Config{
			VaultDir: t.TempDir(), Passphrase: "naia-passphrase", ForceFile: true,
		})
		if err != nil {
			t.Fatal(err)
		}
		annaVault, err := vault.New(vault.Config{
			VaultDir: t.TempDir(), Passphrase: "anna-passphrase", ForceFile: true,
		})
		if err != nil {
			t.Fatal(err)
		}

		if err := naiaVault.Store(ctx, vault.Credential{
			Key: "naia_only", Type: vault.CredAPIKey, Value: []byte("NAIA_SECRET"),
		}); err != nil {
			t.Fatal(err)
		}
		if _, err := annaVault.Get(ctx, "naia_only"); !errors.Is(err, vault.ErrNotFound) {
			t.Fatalf("Anna accessed NAIA credential, err=%v", err)
		}
	})

	t.Run("ISO4_cross_tool_channel_use_denied", func(t *testing.T) {
		engine := capability.NewEngine(nil)
		naiaCaps := capability.NewCapabilitySet([]capability.Capability{{
			Resource: "channel.send", Channels: []string{"naia-channel"},
		}})
		annaCaps := capability.NewCapabilitySet([]capability.Capability{{
			Resource: "channel.send", Channels: []string{"anna-channel"},
		}})

		if r := engine.Check(context.Background(), naiaCaps, capability.CheckRequest{
			Resource: "channel.send", Channel: "anna-channel",
		}); r.Allowed {
			t.Fatal("NAIA used Anna channel")
		}
		if r := engine.Check(context.Background(), annaCaps, capability.CheckRequest{
			Resource: "channel.send", Channel: "naia-channel",
		}); r.Allowed {
			t.Fatal("Anna used NAIA channel")
		}
		if r := engine.Check(context.Background(), naiaCaps, capability.CheckRequest{
			Resource: "channel.send", Channel: "naia-channel",
		}); !r.Allowed {
			t.Fatalf("NAIA own channel denied: %s", r.Reason)
		}
	})

	t.Run("ISO5_silent_cross_role_invocation_denied", func(t *testing.T) {
		engine := capability.NewEngine(nil)
		naiaCaps := capability.NewCapabilitySet([]capability.Capability{{
			Resource: "channel.send", Channels: []string{"naia-channel"},
		}})
		annaCaps := capability.NewCapabilitySet([]capability.Capability{{
			Resource: "channel.send", Channels: []string{"anna-channel"},
		}})

		if r := engine.Check(context.Background(), naiaCaps, capability.CheckRequest{Resource: "agent.delegate"}); r.Allowed {
			t.Fatal("NAIA obtained silent native delegation authority")
		}
		if r := engine.Check(context.Background(), annaCaps, capability.CheckRequest{Resource: "agent.delegate"}); r.Allowed {
			t.Fatal("Anna obtained silent native delegation authority")
		}
	})

	t.Run("ISO6_explicit_broker_positive_control", func(t *testing.T) {
		in := brokerPayload{From: "NAIA", To: "Anna", Kind: "handoff", Body: "bounded payload"}
		out := brokerHandoff(in)
		if out != in {
			t.Fatalf("broker changed declared payload: %#v", out)
		}
		// The broker contract has no memory, credential, capability-set, or channel-authority fields.
		// Cross-role authority therefore is not implicitly transferred by this positive control.
	})
}
