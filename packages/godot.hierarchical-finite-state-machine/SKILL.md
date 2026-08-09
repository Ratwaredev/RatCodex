---
name: godot-hierarchical-finite-state-machine
description: Reuse the official Godot hierarchical finite state machine core to organize character or gameplay states in GDScript.
---

# Godot hierarchical finite state machine

Use this package when a Godot project has behaviors that are becoming a large conditional script: movement states, attacks, casting, AI modes, menus, interaction modes or other mutually exclusive stateful behavior.

## Included copy-ready files

- `templates/state.gd` — base state interface with `enter`, `exit`, input/update and animation hooks.
- `templates/state_machine.gd` — state machine node that delegates input/physics updates and changes the active state when a state emits `finished`.

Both files are mirrored from the official Godot demo repository and are covered by the package's MIT provenance.

## Integration

1. Copy the two files into a dedicated state-machine folder in the target Godot project.
2. Create state nodes/scripts that extend the base state.
3. Make every concrete state emit `finished(next_state_name)` when it wants a transition.
4. Add the concrete states as children of the state-machine node (or an inherited specialized machine).
5. Populate `states_map` with the names used by transitions.
6. Set `start_state` in the inspector when the first child should not be the initial state.
7. Keep state-specific animation/input/timers inside the state itself rather than growing a central switch statement.

## Important adaptation note

The upstream demo is hierarchical and includes a pushdown-style stack. The two mirrored files are the reusable core, not the full player/demo implementation. A project still needs to define its concrete state map and game-specific states.

If the target architecture does not need a previous-state stack, simplify it deliberately rather than retaining complexity accidentally.

## Forge Studio

This package is allowed in `ai-portable`, `runtime-safe` and `private-full`. Import as a copy-ready template and preserve `NOTICE.md` in project/package attribution records.

## Source of truth

When behavior differs across Godot versions, consult the upstream demo linked in `manifest.json` before inventing compatibility fixes.
