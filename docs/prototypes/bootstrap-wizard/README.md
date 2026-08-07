# Bootstrap wizard journey prototype

**Question:** Does the proposed stage order and state model make the project
standards bootstrapper understandable and safe in interactive, resumed, and
non-interactive runs?

This is a throwaway prototype for
[Prototype the interactive wizard journey and automation boundary](https://github.com/ironicbuddha/skills-hub/issues/10).
It does not inspect or mutate a repository. It lets a human drive representative
journeys while showing the complete state after every action.

Run it from the repository root:

```sh
python3 docs/prototypes/bootstrap-wizard/prototype.py
```

Try all three scenarios. The useful feedback is where a stage arrives too soon,
asks for the wrong thing, hides important state, or automates something that
should require human authority. Record the verdict in `NOTES.md`; the prototype
is deleted after the issue resolution captures the decision.
