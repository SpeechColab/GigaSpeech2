# GigaSpeech 2
<div align="left">
    <img src="https://img.shields.io/badge/Platform-linux-lightgrey" alt="Linux">
    <img src="https://img.shields.io/badge/TorchAudio-2.1.0%2B-orange" alt="TorchAudio">
    <img src="https://img.shields.io/badge/License-Apache2.0-red" alt="Apache2.0">
</div>

This is the official repository of the GigaSpeech 2 dataset. For details of how we created the dataset, please refer to our preprint paper: [TODO]

GigaSpeech 2 version: 2.0 (TODO)

<div align="left">
    <p><img src="https://github.com/yfyeung/GigaSpeech2/blob/main/docs/source/_static/pipeline.png" width=800></p>
</div>

## Download
[TODO]

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
|                      |    Thai    |  Indonesian  | Vietnamese |
|:--------------------:|:----------:|:------------:|:----------:|
| GigaSpeech 2 raw     |  12901.8   | 8112.9       | 7324.0     |
| GigaSpeech 2 refined |  10262.0   | 5714.0       | 6039.0     |

GigaSpeech 2 raw contains all the data from GigaSpeech 2 refined.

### Evaluation Subsets
|                      |    Thai    |  Indonesian  | Vietnamese |
|:--------------------:|:----------:|:------------:|:----------:|
| GigaSpeech 2 dev     |   10.0     | 10.0         | 10.2       |
| GigaSpeech 2 test    |   10.0     | 10.0         | 11.0       |

Evaluation subsets are **annotated by professional human annotators**.

### Preparation Scripts
[TODO]

### Metadata Walkthrough
[TODO]

### Audio Processing
[TODO]

### Text Pre-Processing
[TODO]

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
| [Birch AI](https://birch.ai/) | Computing power |
| [Dataocean AI](https://en.haitianruisheng.com/) | Evaluation data annotation |

## Citation
Please cite our paper if you find this work useful:
[TODO]

## Contact
If you have any concerns, please contact gigaspeech@speechcolab.org.

If you have any technical problems, please contact yifanyeung@sjtu.edu.cn.

## Metadata Changelog
[TODO]
