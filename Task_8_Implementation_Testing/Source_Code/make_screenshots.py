"""make_screenshots.py - renders source files / console outputs as PNG images for the report."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def render(text_path, out_path, title):
    lines = open(text_path, encoding="utf-8").read().expandtabs(4).splitlines()
    font = ImageFont.truetype(FONT, 14)
    lh, pad = 18, 16
    w = max(900, int(max((font.getlength(l) for l in lines), default=0)) + 2 * pad)
    h = lh * (len(lines) + 2) + 2 * pad
    img = Image.new("RGB", (w, h), (30, 30, 30))
    d = ImageDraw.Draw(img)
    d.text((pad, pad), f"$ {title}", font=font, fill=(120, 200, 120))
    y = pad + lh * 2
    for l in lines:
        d.text((pad, y), l, font=font, fill=(230, 230, 230))
        y += lh
    img.save(out_path)

src = os.path.join(ROOT, "Task_8_Implementation_Testing", "Source_Code")
shots = os.path.join(ROOT, "Report", "Source_Code_Screenshots")
outs = os.path.join(ROOT, "Report", "Output_Screenshots")
for f in ("search_algorithms.py", "test_algorithms.py", "run_experiments.py"):
    render(os.path.join(src, f), os.path.join(shots, f.replace(".py", ".png")), f"cat {f}")
render(os.path.join(outs, "test_output.txt"), os.path.join(outs, "test_output.png"), "python test_algorithms.py")
render(os.path.join(outs, "experiment_output.txt"), os.path.join(outs, "experiment_output.png"), "python run_experiments.py")
print("screenshots done")
