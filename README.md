# Falken

**The agent-native application profile** — an open standard for applications that AI agents use on the user's behalf.

In an operating system with an AI agent, an application is no longer, first of all, a screen full of buttons: it is a set of well-defined capabilities over the user's data. Falken describes how those applications declare what they can do, the risk of each action, how the user confirms what cannot be undone, how every action is verified and audited, and how all of it works with small models running offline.

Falken is not a new protocol. It is a profile on top of the [Model Context Protocol (MCP)](https://www.anthropic.com/news/donating%2Dthe%2Dmodel%2Dcontext%2Dprotocol%2Dand%2Destablishing%2Dof%2Dthe%2Dagentic%2Dai%2Dfoundation): a Falken application is an ordinary MCP server, and an agent that knows the profile uses it better and more safely.

## Status

**Draft manifesto.** The specification (v0.1) will be written from real applications built for [AIOS and newos](https://github.com/ccarrillomanzanares/aios-base), the reference implementations.

- [Manifesto (English)](MANIFESTO.md)
- [Manifiesto (español)](MANIFIESTO.md)

## The ten principles

1. Capabilities before screens
2. The data belongs to the user and is in plain sight
3. Every action declares its risk
4. Irreversible actions are confirmed with the user
5. Every action can be verified
6. Everything is logged and can be audited
7. Short, stable responses
8. Interface on demand
9. Any modality
10. Local first

## Contributing

Ideas and objections are welcome as GitHub issues. Changes to the manifesto and, later, to the specification are made by public proposal and discussion in this repository.

## Licence

The manifesto and the specification are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE). Reference code, when published, will be licensed under MIT or Apache 2.0.

*Named after Professor Falken, creator of the AI in WarGames (1983).*
