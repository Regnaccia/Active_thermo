from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from entity_config_assembler.assembler.configuration_assembler import ConfigurationAssembler, NamingPolicy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="entity_config_assembler")
    parser.add_argument("--base-path", default=str(Path(__file__).parent.parent), help="Project base path")
    parser.add_argument("--system-file", default="config/00_system/00_system.yaml", help="System YAML path")
    parser.add_argument(
        "--naming-mode",
        default="prefix_parent",
        choices=["keep_local_id", "prefix_parent"],
        help="Entity exported id naming strategy",
    )
    parser.add_argument("--separator", default="_", help="Separator used by naming policy")
    parser.add_argument("--format", default="json", choices=["json", "yaml"], help="Output format")
    parser.add_argument("--output", default="", help="Optional output file path")
    parser.add_argument("--log-mode", default="verbose", choices=["silent", "normal", "verbose"])
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    assembler = ConfigurationAssembler(
        base_path=Path(args.base_path),
        system_file=args.system_file,
        naming_policy=NamingPolicy(mode=args.naming_mode, separator=args.separator),
        log_mode=args.log_mode,
    )
    config = assembler.assemble()
    payload = config.model_dump(mode="json")

    if args.format == "yaml":
        text = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
    else:
        text = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
