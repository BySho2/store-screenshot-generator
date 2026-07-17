# 画像生成の仕組み / How It Works

[日本語](#日本語) | [English](#english)

## 日本語

このツールは、アプリ画面のスクリーンショットに見出し、説明文、背景デザインを組み合わせ、App Store／Google Playのストア掲載用画像を生成します。

### 生成の流れ

1. `config.yaml`から、入力するスクリーンショットと日本語・英語の文章を読み込む
2. Apple向け、Google Play向けの出力サイズを決定する
3. 選択したテーマから背景を生成する
4. 見出しと説明文を読みやすい位置へ配置する
5. 文章が表示領域に収まるように、自動で改行と文字サイズを調整する
6. スクリーンショットを縦横比を保ったまま、表示領域に収まる大きさへ調整する
7. 背景パネル、影、スクリーンショット、アプリ名を一枚の画像に合成する
8. 日本語版と英語版を、ストアごとのフォルダへPNG形式で出力する

一度の実行で、次の画像を生成します。

| ストア | 用途 | 出力サイズ |
|---|---|---:|
| App Store | iPhone 6.9インチ・縦向き | `1320 x 2868` |
| Google Play | スマートフォン・縦向き | `1080 x 1920` |

### 用意するもの

- ストア掲載に使いたいアプリ画面のスクリーンショット
- 各画像に掲載する日本語と英語の見出し・説明文
- 使用するテーマ、またはアプリのブランドカラーに合わせた独自テーマ

入力画像にはPNG、JPEG、WebPを使用できます。画面内に個人情報、テスト用アカウント、公開前の機密情報が映り込んでいないことを確認してください。

### ファイルの役割

- `generate.py`：すべてのアプリで共通して使う画像生成処理
- `config.yaml`：アプリごとのスクリーンショット、文章、出力先
- `themes/*.yaml`：背景色、文字色、文字サイズ、画像の配置などのデザイン設定

アプリを追加するときは、`generate.py`を複製したり書き換えたりせず、アプリごとの`config.yaml`とスクリーンショットを用意します。

## English

This tool combines screenshots of your app with headlines, supporting copy, and a visual theme to create App Store and Google Play listing images.

### Generation Pipeline

1. Load the source screenshots and Japanese and English copy from `config.yaml`.
2. Select the Apple and Google Play output dimensions.
3. Render the background from the selected theme.
4. Position the headline and supporting copy.
5. Wrap and resize the text so it fits within the available area.
6. Scale each screenshot to fit while preserving its aspect ratio.
7. Composite the panel, shadow, screenshot, and app name.
8. Export Japanese and English RGB PNG files into separate folders for each store.

One run produces the following outputs:

| Store | Target | Output size |
|---|---|---:|
| App Store | iPhone 6.9-inch portrait | `1320 x 2868` |
| Google Play | Phone portrait | `1080 x 1920` |

### What You Need

- Screenshots of the app screens you want to use in the store listing
- Japanese and English headlines and supporting copy for each image
- One of the included themes or a custom theme based on your app's brand

PNG, JPEG, and WebP source images are supported. Before generating store assets, make sure the screenshots do not contain personal data, test account details, or unreleased confidential information.
