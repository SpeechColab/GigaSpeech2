import json
import os
import textgrid
from lhotse.utils import add_durations 


for i in os.listdir("textgrid"):
    tg_path = os.path.join("textgrid", i)
    tg = textgrid.TextGrid()
    tg.read(tg_path)

    manifest_path = i.replace(".TextGrid", "_manifest.jsonl")
    with open("mms/" + manifest_path, "w") as f:
        for interval in tg.tiers[0]:
            if len(interval.mark) == 0:
                continue
            line = {}
            line["audio_filepath"] = os.path.join("/data/shared/Thai_test_merge/wav", i.replace(".TextGrid", ".wav"))
            line["audio_start_sec"] = interval.minTime
            line["duration"] = add_durations(interval.maxTime, -interval.minTime, sampling_rate=16000)
            line["text"] = interval.mark
            f.write(json.dumps(line) + "\n")
