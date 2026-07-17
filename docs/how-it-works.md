# How It Works

[日本語](#日本語) | [English](#english)

## 日本語

このツールは、アプリの実画面、キャッチコピー、テーマ設定を組み合わせて、ストア掲載用PNGを生成します。

1. `config.yaml`から日本語・英語の文章と入力画像を読み込む
2. 出力プリセットからキャンバスサイズを決める
3. テーマの色から背景を生成する
4. 見出しと本文を指定領域に収まるまで自動調整する
5. 入力画像を縦横両方の制限内へ縮小する
6. 影、背景パネル、アプリ名を合成する
7. RGB・アルファなしのPNGとして言語別に出力する

初期リリースでは、日本語と英語、およびApp StoreのiPhone 6.5インチ縦向き`1242 x 2688px`に対応します。

### 入力画像

- PNG、JPEG、WebP
- アプリの現在の画面を正確に示す画像
- 個人情報やテスト用アカウント情報を含まない画像
- 端末フレーム付き透過PNG、または通常の画面キャプチャ

### 設計上の分離

- `generate.py`: 共通の生成処理
- `config.yaml`: アプリ固有の文章、画像、出力設定
- `themes/*.yaml`: 色、文字、端末画像の見せ方

アプリ固有の素材は公開リポジトリへ保存せず、各利用者が自分の環境で管理します。

## English

The generator combines real app captures, localized copy, and a reusable theme into store-ready PNG files.

1. Load Japanese and English content from `config.yaml`.
2. Select the canvas size from an output preset.
3. Render the configured background.
4. Wrap and resize headings and body copy to fit their bounds.
5. Scale the app capture within both width and height limits.
6. Composite the panel, shadow, capture, and app name.
7. Export localized RGB PNG files without alpha channels.

The initial release supports Japanese, English, and the App Store iPhone 6.5-inch portrait size of `1242 x 2688px`.
