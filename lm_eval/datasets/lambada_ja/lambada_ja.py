# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: Address all TODOs and remove all explanatory comments
"""LAMBADA (OpenAI) dataset."""

import os
import json

import datasets


_CITATION = """\
@misc{
    author={Paperno, Denis and Kruszewski, Germán and Lazaridou, Angeliki and Pham, Quan Ngoc and Bernardi, Raffaella and Pezzelle, Sandro and Baroni, Marco and Boleda, Gemma and Fernández, Raquel},
    title={The LAMBADA dataset},
    DOI={10.5281/zenodo.2630551},
    publisher={Zenodo},
    year={2016},
    month={Aug}
}
"""

_DESCRIPTION = """\
The LAMBADA dataset as processed by OpenAI. It is used to evaluate the capabilities
of computational models for text understanding by means of a word prediction task.
LAMBADA is a collection of narrative texts sharing the characteristic that human subjects
are able to guess their last word if they are exposed to the whole text, but not
if they only see the last sentence preceding the target word. To succeed on LAMBADA,
computational models cannot simply rely on local context, but must be able to keep track
of information in the broader discourse.

Reference: https://github.com/openai/gpt-2/issues/131#issuecomment-497136199
"""

_HOMEPAGE = "https://zenodo.org/record/2630551#.X4Xzn5NKjUI"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "Modified MIT"

_BASE_URL = (
    "https://huggingface.co/datasets/EleutherAI/lambada_openai/resolve/main/data"
)

JA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "lambada_test_ja.jsonl"
)
_URLS = {
    "default": f"{_BASE_URL}/lambada_test.jsonl",
    "de": f"{_BASE_URL}/lambada_test_de.jsonl",
    "en": f"{_BASE_URL}/lambada_test_en.jsonl",
    "es": f"{_BASE_URL}/lambada_test_es.jsonl",
    "fr": f"{_BASE_URL}/lambada_test_fr.jsonl",
    "it": f"{_BASE_URL}/lambada_test_it.jsonl",
    "ja": "https://gist.githubusercontent.com/mkshing/22b4623233940b2baa2f924e60f9b287/raw/c2c58325f5bc599818fe5f7d6f6b9af3e7699ed6/lambada_test_ja.jsonl",
}


class LambadaOpenAI(datasets.GeneratorBasedBuilder):
    """LAMBADA is a dataset to evaluate the capabilities of computational models for text understanding by means of a word prediction task."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="default",
            version=VERSION,
            description="Pre-processed English LAMBADA dataset from OpenAI",
        ),
        datasets.BuilderConfig(
            name="de",
            version=VERSION,
            description="The German translated LAMBADA OpenAI dataset",
        ),
        datasets.BuilderConfig(
            name="en",
            version=VERSION,
            description="The English translated LAMBADA OpenAI dataset",
        ),
        datasets.BuilderConfig(
            name="es",
            version=VERSION,
            description="The Spanish translated LAMBADA OpenAI dataset",
        ),
        datasets.BuilderConfig(
            name="fr",
            version=VERSION,
            description="The French translated LAMBADA OpenAI dataset",
        ),
        datasets.BuilderConfig(
            name="it",
            version=VERSION,
            description="The Italian translated LAMBADA OpenAI dataset",
        ),
        datasets.BuilderConfig(
            name="ja",
            version=VERSION,
            description="The Japanese translated LAMBADA OpenAI dataset",
        ),
    ]

    DEFAULT_CONFIG_NAME = "default"

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=f"{_DESCRIPTION}\n{self.config.description}",
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "test",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                yield key, {"text": data["text"]}
