# vrc-pilot-test

VRChat上の自動操作を小さな実験単位で検証するPython実験リポジトリです。各実験は `exp/` に分離し、`Taskfile.yml` を実行入口にします。

現在の実験:

- `task explorer` — VRChat explorer experiment
- `task mass-photographer` — 複数worldを対象にしたphoto experiment
- `task reflex-test` — 0ms reaction speed demonstration
- `task world-pioneer` — automated world exploration / crate opening experiment

AI操作と人間操作を同時に行う場合は、AI用VRChat profileをDesktop modeで分離して使う運用を前提にしています。詳細は `AGENTS.md` と `docs/MANUAL_MULTI_ACCOUNT.md` を参照してください。
