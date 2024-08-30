#!/usr/bin/env bash
python tools/mk_pyi.py
llms_txt2ctx nbs/llms.txt > nbs/llms-ctx-full.txt
llms_txt2ctx nbs/llms.txt --optional false > nbs/llms-ctx.txt

