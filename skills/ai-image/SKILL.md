---
name: ai-image
description: >
  Generate and edit images with either OpenAI GPT Image 2 (`gpt-image-2`,
  Images API) or Google Gemini (Nano Banana Pro, `gemini-3-pro-image-preview`,
  generateContent API) via direct curl — plus prompt-craft templates and a
  CLI post-processing playbook (grade/grain/sharpen/upscale/bg-removal).
  Supersedes the old gpt-image skill. Use when the user invokes /ai-image or
  asks to generate/edit an image with GPT Image or Gemini.
metadata:
  compatibility: Claude Code, Codex, or OpenCode with curl, python3, and provider credentials
allowed-tools:
  - Bash
  - Read
  - Write
---

# ai-image — multi-provider image generation, editing & finishing

Direct curl calls, no SDK. **The user picks the provider every time** — never
choose silently. If the invocation doesn't name one (gpt / openai vs.
gemini / nano banana), ask before generating.

## Secrets & preflight

Env var first, else the plaintext key file:

```bash
OPENAI_API_KEY="${OPENAI_API_KEY:-$(cat ~/.claude/openai_api_key 2>/dev/null)}"
GEMINI_API_KEY="${GEMINI_API_KEY:-$(cat ~/.claude/gemini_api_key 2>/dev/null)}"
```

If the key for the chosen provider is empty, **fail fast**: stop, do not
call the API, and tell the user how to create one.

- **OpenAI** — mint a key on the OpenAI platform API keys page
  (https://platform.openai.com/api-keys), then either export
  `OPENAI_API_KEY` or save it to `~/.claude/openai_api_key` (`chmod 600`).
  Health: `curl -s -o /dev/null -w "%{http_code}" https://api.openai.com/v1/models/gpt-image-2 -H "Authorization: Bearer $OPENAI_API_KEY"` → `200`.
- **Gemini** — mint a key at https://aistudio.google.com/apikey, then either
  export `GEMINI_API_KEY` or save it to `~/.claude/gemini_api_key`
  (`chmod 600`).
  Health: `curl -s -o /dev/null -w "%{http_code}" "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview" -H "x-goog-api-key: $GEMINI_API_KEY"` → `200`
  (on 404 the model id has rotated — list with `curl -s "https://generativelanguage.googleapis.com/v1beta/models" -H "x-goog-api-key: $GEMINI_API_KEY" | grep -o '"name": "models/gemini[^"]*image[^"]*"'`).

Both providers bill per image. Never echo a key; never commit the key files.

## OpenAI — generate

```bash
curl -s https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"gpt-image-2","prompt":"<prompt>","size":"1024x1024","quality":"high","output_format":"png","n":1}' \
  | python3 -c '
import json, base64, sys
r = json.load(sys.stdin)
if "error" in r: sys.exit(r["error"]["message"])
for i, d in enumerate(r["data"]):
    open(f"out-{i}.png", "wb").write(base64.b64decode(d["b64_json"]))
    print(f"out-{i}.png")'
```

| Param | Values |
|---|---|
| `size` | `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`, `auto` (edges ×16, max 3840, ratio ≤3:1) |
| `quality` | `low` (drafts), `medium`, `high` (finals), `auto` |
| `output_format` | `png`, `jpeg`, `webp` (+ `output_compression` 0–100) |
| `background` | `transparent` for isolated assets, `opaque`, `auto` |

## OpenAI — edit (references / inpainting)

```bash
curl -s https://api.openai.com/v1/images/edits \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F model=gpt-image-2 -F prompt="<edit instruction>" -F image[]=@ref1.png \
  | python3 -c 'import json,base64,sys; r=json.load(sys.stdin); open("edited.png","wb").write(base64.b64decode(r["data"][0]["b64_json"]))'
```

Repeat `-F image[]=@...` for multiple references (up to ~16); add
`-F mask=@mask.png` for inpainting (transparent mask areas are replaced).
State how the references relate — the model won't infer roles.

## Gemini — generate / edit

Same endpoint for both; references go in as extra inline parts:

```bash
B64REF=$(base64 -w0 ref.png)   # omit refs for pure text→image
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -d "{\"contents\":[{\"parts\":[
        {\"text\":\"<prompt>\"},
        {\"inline_data\":{\"mime_type\":\"image/png\",\"data\":\"$B64REF\"}}]}],
      \"generationConfig\":{\"responseModalities\":[\"TEXT\",\"IMAGE\"],
        \"imageConfig\":{\"aspectRatio\":\"1:1\"}}}" \
  | python3 -c '
import json, base64, sys
r = json.load(sys.stdin)
if "error" in r: sys.exit(r["error"]["message"])
n = 0
for p in r["candidates"][0]["content"]["parts"]:
    d = p.get("inlineData") or p.get("inline_data")
    if d:
        open(f"out-{n}.png", "wb").write(base64.b64decode(d["data"])); print(f"out-{n}.png"); n += 1'
```

Aspect ratios: `1:1 3:2 2:3 3:4 4:3 4:5 5:4 9:16 16:9 21:9`; add
`"imageSize":"2K"` (or `4K`) inside `imageConfig` for larger output.
Gemini takes 6+ references — **assign each a role in the prompt** ("use
image 1 for the character's face and body, image 2 for the pose"). Iterate
conversationally (send prior output back as a reference + a short edit
instruction) instead of re-prompting from scratch — that's what holds a
character consistent.

## Prompt craft

Build prompts as a structured brief, filling slots in this order —
**Subject → Action → Setting → Composition/Camera → Lighting →
Style/Medium → Mood → exact text (if any) → constraints** — specific first,
aesthetic last. Expand a terse user idea by filling every slot explicitly,
then show the user the final prompt alongside the image.

**Brief the shot before generating.** If the request leaves the decisive
slots open, ask (one compact round through the host's question tool or ordinary chat)
rather than guessing:

- **Style/medium** — the highest-leverage unknown. Offer concrete options
  ("claymation with fingerprints / flat 2D cel / gouache illustration /
  photoreal product shot"), not adjectives.
- **Destination** → aspect ratio + size (social 9:16 or 4:5, README/web
  16:9, sprite = transparent square).
- **Mood/energy** and any **must-keep details** (brand marks, character
  features, palette).
- Skip the round entirely when the user already named these or is iterating
  on a previous image — then just apply the delta.

**Anti-AI-look rules** (apply unless the user wants the glossy default):
name a specific medium/era/studio anchor, but **at most two** — stacking
more causes style drift; prompt the imperfections a human artisan leaves
(wobbling linework, visible fingerprints, uneven paint, slight
registration offset); ban sheen words ("high quality, beautiful, cinematic,
stunning") — they pull toward the model's generic average; and finish with
the grain/grade post pass below, which does as much as the prompt.

- Natural descriptive sentences, not keyword soup (both models auto-revise;
  rigid literal specs over-trigger). Name concrete style anchors (medium,
  era, studio grammar, film stock) — never "high quality, beautiful,
  cinematic", which produce the generic AI look.
- Character work: always reference-image + edit endpoint, never re-describe
  the character in text. Keep proportions/marks in the prompt anyway
  (belt + suspenders).
- Text-in-image is weak on both. Keep it ≤ a few short words, or render the
  image textless and composite type in post (ImageMagick `-annotate`, or PIL).
- Iterate at `quality: low` / 1K, finalize at `high` / 2K+.

## Post-processing playbook

Order matters: **upscale → color-grade → grain → sharpen → export**
(grain before grading gets re-processed and shifts character).

```bash
# Upscale (Real-ESRGAN; install once: pip install realesrgan / ncnn binary)
realesrgan-ncnn-vulkan -i in.png -o up.png -s 4
# Grade — ffmpeg curves presets: vintage, cross_process, medium_contrast,
# strong_contrast, lighter, darker...
ffmpeg -y -i up.png -vf curves=preset=medium_contrast graded.png
# Grain — alls=10–15 for stills (25 is visibly noisy)
ffmpeg -y -i graded.png -vf "noise=alls=12:allf=t" grained.png
# Sharpen — mild; amounts >1.5 halo
ffmpeg -y -i grained.png -vf "unsharp=5:5:0.8" final.png
```

- **Background removal / sprites**: `rembg i in.png out.png` (batch:
  `rembg p in_dir/ out_dir/`; models: `u2net` default,
  `isnet-general-use` more accurate, `birefnet` for high-res). Kill edge
  halos with `magick out.png -channel A -morphology Erode Disk:1 +channel clean.png`.
  Keep alpha → PNG/WebP, never JPEG.
- **Turnaround sheets**: prompt an explicit equal grid ("four panels in a
  2×2 grid: front, three-quarter, side, back; same character, neutral grey
  background"), then split at fixed offsets:
  `magick sheet.png -crop 2x2@ +repage view_%d.png`.
- **Series consistency**: hold one base prompt constant (style/lighting/
  palette/camera words frozen, only subject varies), then run the identical
  post command over every file. Residual drift: histogram-match to a chosen
  hero frame — `magick drifted.png hero.png -clut matched.png` or normalize
  with `-brightness-contrast`.
- **Export**: social uploads JPEG q75–85 (platforms recompress anyway); web
  AVIF q45–60 with WebP fallback (`magick mogrify -format avif -quality 50 *.png`);
  anything with alpha stays PNG/WebP.

## Conventions

- Show saved file path(s) in the final reply; default outputs to the
  session scratchpad (or CWD outside a project) unless the user wants them
  in a repo.
- Generation can take 30–120s at high quality; use the host's background or resumable shell execution and keep the user updated.
- Report the provider, model id, and rough cost when it's non-trivial
  (many images / 4K).
