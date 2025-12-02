# CHANGELOG

## 02/12/2025 - 12h22

### Docker

**New Features:**
- docker): complete port isolation from other services for VPS deployment
- deploy): add VPS deployment scripts and production config

**Bug Fixes:**
- deploy): update all ports in deploy.sh to match docker-compose changes
- docker): change default ports to avoid conflicts with CityResQ360

**Documentation:**
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]

**Technical Details:**
- Tag: v1.1.0
- Commits: 10
- Released from: main branch
- Release URL: https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/releases/tag/v1.1.0

---

# [Unreleased](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/v1.0.0...aa3b56a518ecc158677b91d4c52b7912db3e3c81) (2025-12-02)


### Bug Fixes

* **deploy:** update all ports in deploy.sh to match docker-compose changes ([9884ffe](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/9884ffe4ba4367ac144438a9a3b24e603eba2e5f))
* **docker:** change default ports to avoid conflicts with CityResQ360 ([a754d60](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/a754d60ee58c5cd505725d0e4ea9bb0771c0b076))


### Features

* **deploy:** add VPS deployment scripts and production config ([78157b7](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/78157b7e45aad48ba450368116917982e352ad6a))
* **docker:** complete port isolation from other services for VPS deployment ([aa3b56a](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/aa3b56a518ecc158677b91d4c52b7912db3e3c81))



# [1.0.0](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/v0.2.0...v1.0.0) (2025-12-02)


### Bug Fixes

* **ci:** add -r 0 flag to regenerate full changelog with unreleased ([00e7991](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/00e7991d3036604c6f98ac11344c8c60447bb7b4))


### Features

* **auth:** implement  user authentication and profile system ([f9a7316](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/f9a73167a897dfe8a17db3e74525bdb2728291c3)), closes [#8](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/issues/8)
* **reviews,testing:** implement user reviews system and E2E testing ([f51d710](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/f51d7108708cbe76f8c6b6ab087917ae9132b419))



# [0.2.0](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/v0.1.0...v0.2.0) (2025-12-01)


### Bug Fixes

* **script:** Sửa file Script Auto git ([a0469c4](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/a0469c4c1602bf01bc3209c9885c691e6f0dc011))


### Features

* **project:** tích hợp bản đồ, tìm kiếm, chi tiết trường học và sửa lỗi hệ thống ([3180677](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/31806776e8bb99b8791328ab20a1f420f21f6216))
* tích hợp bản đồ, tìm kiếm, chi tiết trường học và sửa lỗi hệ thống ([c46eddb](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/c46eddbdefc2fd856398858c34e06ebfedc7938c))



# [0.1.0](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/v0.0.2...v0.1.0) (2025-12-01)


### Bug Fixes

* Architecture Diagram ([d961e50](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/d961e50ed08bcbd9e3bd59efe029045f768f9176))
* Architecture picture ([db99f90](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/db99f90ea7f21f6fcd6ed12b2428c0ca6668568d))
* **ci:** generate dummy package.json for changelog workflow ([66668ba](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/66668baee7f7a9954d389b241f00f14a3996d17a))



## [0.0.2](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/b7e8a61c23e6040a0dfe80220762dbff1c33c06e...v0.0.2) (2025-12-01)


* ﻿refactor(tái cấu trúc dự án theo chuẩn CityResQ360)!: - Dọn dẹp thư mục gốc: chỉ giữ lại file thiết yếu (README, LICENSE, CHANGELOG...) ([600355d](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/600355de957d0df65ad30f3c4cdde2d9e8588d87))


### Bug Fixes

* change CODE_OF_CONDUCT AND CONTRIBITING ([94bd399](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/94bd399b001533cad596da6a82f47dbcd4b6db73))
* Change Readme.md ([f0b156f](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/f0b156f39967326e410bf4258642f232019c9d6c))
* readme ([845f327](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/845f327314e35f95cc5104e2f41f50d5ebc2bdf9))


### Features

* Complete environment service setup and fix critical bugs ([903c607](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/903c607512f0f33572f7fa447b41c103d13d4c13))
* initial setup after refactoring ([b7e8a61](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/b7e8a61c23e6040a0dfe80220762dbff1c33c06e))


### BREAKING CHANGES

* Thay đổi cấu trúc thư mục documentation và scripts.



