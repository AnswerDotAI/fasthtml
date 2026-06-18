# htmx compatibility checker fixtures

Small scripts for testing `htmx_compat_checker.py`.

Expected behavior with inferred target:

```bash
python ../htmx_compat.py --path v2_compatible.py
python ../htmx_compat.py --path v4_compatible.py
python ../htmx_compat.py --path v2_incompatible_v4_attrs.py
python ../htmx_compat.py --path v4_incompatible_v2_attrs.py
```

The compatible files should exit `0`. The incompatible files should print findings and exit `1`.
