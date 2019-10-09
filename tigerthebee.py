from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from beefore import diff
from inspectortiger.config_manager import ConfigManager
from inspectortiger.inspects import inspector, load_plugins
from inspectortiger.utils import traverse_paths

__name__ = "inspectortiger"


@dataclass
class Lint:
    code: str
    column: int
    lineno: int
    filename: str

    def add_comment(self, pull_request, commit, position):
        pull_request.create_review_comment(
            body=f"At column {self.column} Inspector Tiger found {self.code}.",
            commit_id=commit.sha,
            path=self.filename,
            position=position,
        )

    @classmethod
    def find(cls, directory, workers=2, ignore=()):
        directory = [Path(directory).resolve()]
        python_files = traverse_paths(directory)
        manager = ConfigManager()
        load_plugins(manager)

        problems = defaultdict(list)
        for plugin, reports in inspector(
            python_files, workers, ignore
        ).items():
            for report in reports:
                problems[report["filename"]] = cls(**report)
        return problems


def check(directory, diff_content, commit, verbosity):
    # Adapted from https://github.com/beeware/beefore/blob/master/src/beefore/checks/pycodestyle.py
    results = []

    lint_results = Lint.find(directory=directory)
    diff_mappings = diff.positions(directory, diff_content)

    for filename, problems in lint_results.items():
        file_seen = False
        if filename in diff_mappings:
            for problem in sorted(problems, key=lambda p: p.lineno):
                try:
                    position = diff_mappings[filename][problem.lineno]
                    if not file_seen:
                        print("  * %s" % filename)
                        file_seen = True
                    print("    - %s" % problem)
                    results.append((problem, position))
                except KeyError:
                    if verbosity:
                        if not file_seen:
                            print("  * %s" % filename)
                            file_seen = True
                        print("    - Line %s not in diff" % problem.lineno)
        else:
            if verbosity:
                if not file_seen:
                    print("  * %s" % filename)
                    file_seen = True
                print("    - file not in diff")

    return results
