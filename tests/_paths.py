"""Put each skill's scripts folder on sys.path so tests can import the tools."""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for skill in ("linkedin-post", "linkedin-hooks", "linkedin-dm", "linkedin-audit", "linkedin-carousel"):
    path = os.path.join(ROOT, "skills", skill, "scripts")
    if path not in sys.path:
        sys.path.insert(0, path)
