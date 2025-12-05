# [Unreleased](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/v1.2.0...5d5e854c2935145acd792fdcc7d90fb7f1a3a0fa) (2025-12-05)


### Bug Fixes

* **api:** fix all failed API endpoints and achieve 100% test pass rate ([2a68517](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/2a685178521e484236825e7bd84e721321a1b99b))
* **api:** fix green_resources schema and add init-scripts to seed_database.sh ([5d5e854](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/5d5e854c2935145acd792fdcc7d90fb7f1a3a0fa))
* **api:** resolve route ordering and auth endpoint issues ([07fd488](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/07fd48811d6e40bb55e504bcbb2600bba433d8a6))
* architecture image and overview ([f31a246](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/f31a2460318b9c1a84a7e45a0a54a714493bc7f3))
* change banner and other image ([6ac36ae](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/6ac36aeca20a2d4045a5057eebc080aa1ebc3151))
* **docker:** add NEXT_PUBLIC_API_URL to env configuration ([eb93e8f](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/eb93e8f9b8b823a8d7625b1c5d5955a9233df390))
* **docker:** resolve port 8002 conflict with CityResQ media-service ([2aa4327](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/2aa4327c872a04d7afc0736c159e363bef2c85d1))
* **script:** Fix script ([273bc98](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/273bc98f393f5823fa96cc92be7c364c27ef9202))
* tech stack ([d4e21a2](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/d4e21a2372bef5a2e6d8eadf9cfe25cbf307f618))
* **web-app:**  fix TypeScript errors in CesiumMap component ([6abeeb0](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/6abeeb056d0402b2d44b10c99f655aa3ecc0a069))
* **web-app:** fix TypeScript error in dashboard prediction task ([50043f0](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/50043f0760e6f09bc3a67b1533c97022cb3480c5))
* **web-app:** fix TypeScript error in dashboard prediction task ([8fe9a8c](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/8fe9a8ce2cec7707328fb6d813c719f04d28939f))
* **web-app:** replace remaining Mapbox references with MapTiler ([3a1f8b4](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/3a1f8b4907563cec595560fb29bc0c11f722165f))


### Features

* **deploy:** add VPS deployment scripts and database seeding ([32eeceb](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/32eeceb6dffead57d38d85c6265b0d27cc1fb89c))
* **deploy:** add VPS deployment scripts and database seeding ([7c6c617](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/7c6c617253f1bfbcae02ab1c8e6b336234e30dbe))
* **map:** integrate real API data and fix service endpoints ([adbe432](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/adbe4328dafd3d32069f19d234c1aaae4a1b9bd4))
* **map:** integrate real API data and fix service endpoints ([f5f9c21](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/f5f9c21e11472d53bbf1f11a2d7da473b39b197f))
* **messaging:** integrate RabbitMQ and EMQX message brokers ([290fb5d](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/290fb5d6a9022615a326d0e05b836aee5fd99d3e))



# [1.2.0](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/v1.1.0...v1.2.0) (2025-12-02)


### Bug Fixes

* **deploy:** quote all environment variables to handle special characters ([4758735](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/47587356df9ee7786eb0d86a5c2d3de73e0b49f2))
* **docker:** update web-app port to use WEB_APP_PORT env var (default 4000)" ([3bc4d91](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/commit/3bc4d91c145904da01c167abcb3459064eceadf2))



# [1.1.0](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/compare/v1.0.0...v1.1.0) (2025-12-02)


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



