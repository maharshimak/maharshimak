# 🎬 Multimodal AI Studio

A safe public prototype of a **prompt-to-edit planning engine** for intelligent photo/video workflows.

The current implementation focuses on planning, validation and effect-graph generation rather than pretending to perform heavyweight media generation that is not yet implemented.

## Implemented

- edit-intent schema
- prompt parser for common cinematic operations
- ordered effect graph
- validation rules
- JSON export
- unit tests

## Example

Input:

`"cinematic teal look, slow motion, remove background noise, add subtitles"`

Output: an ordered plan containing color grade, retiming, denoise and subtitle nodes.
