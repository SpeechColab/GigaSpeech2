# GigaSpeech 2
[![arXiv](https://img.shields.io/badge/arXiv-Paper-COLOR.svg)](https://arxiv.org/pdf/2406.11546)  [![hf](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Dataset-yellow)](https://huggingface.co/datasets/speechcolab/gigaspeech2)  [![GitHub](https://img.shields.io/badge/GitHub-Repo-green)](https://github.com/SpeechColab/GigaSpeech2)  [![demo](https://img.shields.io/badge/WebPage-Demo-red)](https://huggingface.co/spaces/k2-fsa/automatic-speech-recognition)

This is the official repository of the GigaSpeech 2 dataset. For details of how we created the dataset, please refer to our [arXiv preprint paper](https://arxiv.org/pdf/2406.11546).

GigaSpeech 2 version: 2.0 (2024/06/19)

<div align="left">
    <p><img src="https://github.com/yfyeung/GigaSpeech2/blob/main/docs/source/_static/pipeline.png" width=800></p>
</div>

## Download
* The dataset is available at [HuggingFace](https://huggingface.co/datasets/speechcolab/gigaspeech2) and [ModelScope](https://modelscope.cn/datasets/AI-ModelScope/gigaspeech2).
* The pre-trained models are available at [Thai](https://huggingface.co/yfyeung/icefall-asr-gigaspeech2-th-zipformer-2024-06-20) and [Vietnamese](https://huggingface.co/zzasdf/icefall-asr-gigaspeech2-vi-zipformer).

## Leaderboard

| **Contributor**| **Toolkit**       | **Train Recipe**     | **Train Data** | **Inference**     |**Test CER/WER**    |
|:---------------|:------------------|:------------------|:------------------|:------------------|:------------------:|
|||||
| <em>Baseline</em>   | [Icefall](https://github.com/k2-fsa/icefall) | Zipformer/Stateless pruned RNN-T | GigaSpeech 2.0 th | TODO | 12.46 | 
| <em>Baseline</em>   | [Icefall](https://github.com/k2-fsa/icefall) | Zipformer/Stateless pruned RNN-T | GigaSpeech 2.0 id | TODO | 14.92 | 
| <em>Baseline</em>   | [Icefall](https://github.com/k2-fsa/icefall) | Zipformer/Stateless pruned RNN-T | GigaSpeech 2.0 vi | TODO | 12.83 | 
| <em>Baseline</em>    | [ESPNet](https://github.com/espnet/espnet) | Conformer/Transformer CTC/AED | GigaSpeech 2.0 th | TODO | 13.70 |
| <em>Baseline</em>    | [ESPNet](https://github.com/espnet/espnet) | Conformer/Transformer CTC/AED | GigaSpeech 2.0 id | TODO | 15.50 |
| <em>Baseline</em>    | [ESPNet](https://github.com/espnet/espnet) | Conformer/Transformer CTC/AED | GigaSpeech 2.0 vi | TODO | 15.60 |

## Dataset

### Audio Source
* Language: Thai, Indonesian, Vietnamese
* GigaSpeech 2 raw: 30,000 hours of automatically transcribed speech across Thai, Indonesian, and Vietnamese.
* GigaSpeech 2 refined: 10,000 hours of Thai, 6,000 hours each for Indonesian and Vietnamese.
* GigaSpeech 2 DEV & TEST: 10 hours for DEV and 10 hours for TEST per language, **transcribed by professional human annotators**, challenging and realistic.

### Training Subsets
|                      | Thai (hours) | Indonesian (hours) | Vietnamese (hours) |
|:--------------------:|:------------:|:------------------:|:------------------:|
| GigaSpeech 2 raw     |    12901.8   |      8112.9        |      7324.0        |
| GigaSpeech 2 refined |    10262.0   |      5714.0        |      6039.0        |

GigaSpeech 2 raw contains all the data from GigaSpeech 2 refined.

### Evaluation Subsets
|                      | Thai (hours) | Indonesian (hours) | Vietnamese (hours) |
|:--------------------:|:------------:|:------------------:|:------------------:|
| GigaSpeech 2 DEV     |     10.0     |       10.0         |       10.2         |
| GigaSpeech 2 TEST    |     10.0     |       10.0         |       11.0         |

Evaluation subsets are **annotated by professional human annotators**.

### Preparation Scripts
Soon available at [Lhotse](https://github.com/lhotse-speech/lhotse) and [ESPNet](https://github.com/espnet/espnet).

### Metadata Walkthrough
Soon available.

### Audio Processing
GigaSpeech 2 audio files are resampled to 16 kHz and converted to single-channel WAV format. For detailed implementation, refer to [pipeline/convert_transcribe/convert_and_transcribe.py](https://github.com/yfyeung/GigaSpeech2/blob/main/pipeline/convert_transcribe/convert_and_transcribe.py#L45).

### Text Pre-Processing
Transcripts are normalized by applying NFKC, converting all characters to uppercase, removing punctuation, and mapping Arabic numerals to words in the respective languages.

### Text Post-Processing (before scoring)
We standardize by applying NFKC, converting all characters to uppercase, removing punctuation, and merging consecutive whitespace or removing all whitespace from both hypothesis and reference text before CER/WER scoring to ensure apple-to-apple performance comparisons across different toolkits or commercial services.

We also provide the following code snippet, which is used in all the experiments reported in our paper and leaderboard.

```python
import string
import unicodedata

def text_post_processing(text):
    text = unicodedata.normalize("NFKC", text)  # apply NFKC
    text = text.upper()  # convert to uppercase
    text = text.replace("-", " ")  # remove hyphen
    text = re.sub("[{}]".format(string.punctuation), "", text)  # remove punctuation
    text = re.sub(r"\s+", "", text).strip()  # remove all whitespace for Thai
    return text
```

## Collaboration
We are a group of volunteers trying to make speech technologies easier to use. We welcome any kind of contributions. Currently, we are exploring the following directions. If you are interested in one of the directions and you think you will be able to help, please contact gigaspeech@speechcolab.org.

* Inference architecture for different pre-trained models
* Adding diverse audio source
* Benchmarking speech algorithms/services
* Building and releasing pre-trained models
* Supporting more languages
* Making new datasets with permissive licenses

## Institutional Contributors
|  Institution | Contribution |
|:------|:-----|
| [Shanghai Jiao Tong University](https://www.seiee.sjtu.edu.cn/) | Computing power; Data host; Researchers |
| [The Chinese University of Hong Kong](https://www.cuhk.edu.hk/chinese/index.html) | Researchers |
| [Tsinghua University](https://www.ee.tsinghua.edu.cn/en/) | Researchers |
| [Seasalt AI](https://seasalt.ai/) | Researchers |
| [Birch AI](https://birch.ai/) | Researchers |
| [Peng Cheng Laboratory](https://data-starcloud.pcl.ac.cn/) | Computing power |
| [Dataocean AI](https://en.haitianruisheng.com/) | Evaluation data annotation |

## Citation
Please cite our paper if you find this work useful:
```
@article{gigaspeech2,
  title={GigaSpeech 2: An Evolving, Large-Scale and Multi-domain ASR Corpus for Low-Resource Languages with Automated Crawling, Transcription and Refinement},
  author={Yifan Yang and Zheshu Song and Jianheng Zhuo and Mingyu Cui and Jinpeng Li and Bo Yang and Yexing Du and Ziyang Ma and Xunying Liu and Ziyuan Wang and Ke Li and Shuai Fan and Kai Yu and Wei-Qiang Zhang and Guoguo Chen and Xie Chen},
  journal={arXiv preprint arXiv:2406.11546},
  year={2024},
}
```

## Contact
If you have any concerns, please contact gigaspeech@speechcolab.org.

If you have any technical problems, please contact yifanyeung@sjtu.edu.cn.

## Metadata Changelog
- 2024/06/19 v2.0: Initial release.
