# Changelog

## [2.0.0](https://github.com/LBlend/normantle/compare/v1.1.0...v2.0.0) (2026-11-07)


### ⚠ BREAKING CHANGES

* return top1000 as json

### Features

* add per-ip rate limiting ([97dc941](https://github.com/LBlend/normantle/commit/97dc9410b4504c49a352c6e3fd134b90d354aef5))
* draw hints from the top 10000 closest words ([f434ee2](https://github.com/LBlend/normantle/commit/f434ee23913866c3b52cf6893dc1abd7311aa434))
* only allow dictionary words and pick answers from nouns ([5c7c8fd](https://github.com/LBlend/normantle/commit/5c7c8fd876269fedae0a97b760afd81b3a2c4631))
* return top1000 as json ([9cfd47c](https://github.com/LBlend/normantle/commit/9cfd47c7cc15d54d2ed50d3518ce7645ed5f7bd9))
* shuffle daily word schedule that never repeats ([85ae356](https://github.com/LBlend/normantle/commit/85ae3562ee79413a938227555860fc94aef7b00f))


### Bug Fixes

* add api_root to compose env ([9e4f2c8](https://github.com/LBlend/normantle/commit/9e4f2c820ede73d1036a20b7bc5e3b551ef9bfe1))
* **deps:** add typing_inspect required by fastapi-utils ([daecbdf](https://github.com/LBlend/normantle/commit/daecbdf9625752fad5d2e60c60edcc5c69ea33b3))
* harden API input validation and fix hint, correctness and daily rollover bugs ([3d401ba](https://github.com/LBlend/normantle/commit/3d401ba4aaa974afbd6e3cb375b8a733ee959224))
* normalize unicode in guesses and handle empty or prefixed TZ values ([eceba4e](https://github.com/LBlend/normantle/commit/eceba4eebcbfefe7990b6062fef36ce02313b52b))
* return exact similarity and rank 0 for correct guesses ([99dce7a](https://github.com/LBlend/normantle/commit/99dce7ac0b7ba4e1851d84c846d8c670f8de27c6))
* use correctly ordered model ([773faba](https://github.com/LBlend/normantle/commit/773faba154027a1bcc87c38f26ec5ad43a8ab6be))


### Documentation

* update readme for uv and config options ([128ab47](https://github.com/LBlend/normantle/commit/128ab479f8cac1cbb233139f248b41a080840eba))
