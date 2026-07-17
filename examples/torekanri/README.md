# トレカンリ生成例 / Torekanri Example

「トレカンリ」の実際のアプリ画面から、App Store／Google Play向けのストア掲載用画像を生成した例です。

This example generates App Store and Google Play listing images from screenshots of the real Torekanri app.

## 生成する / Generate

リポジトリのルートディレクトリで実行します。

Run this command from the repository root:

```bash
python generate.py --config examples/torekanri/config.yaml --overwrite
```

## 出力 / Outputs

- `generated/app-store/ja`: App Store向け・日本語
- `generated/app-store/en`: App Store向け・英語
- `generated/google-play/ja`: Google Play向け・日本語
- `generated/google-play/en`: Google Play向け・英語

## App Store向け・日本語 / App Store, Japanese

<p>
  <img src="generated/app-store/ja/torekanri_ja_01.png" width="31%" alt="取引と収支をカレンダーで確認">
  <img src="generated/app-store/ja/torekanri_ja_02.png" width="31%" alt="仕入も売却もかんたんに記録">
  <img src="generated/app-store/ja/torekanri_ja_03.png" width="31%" alt="収支と在庫をまとめて見える化">
</p>

## Google Play向け・日本語 / Google Play, Japanese

<p>
  <img src="generated/google-play/ja/torekanri_ja_01.png" width="31%" alt="取引と収支をカレンダーで確認">
  <img src="generated/google-play/ja/torekanri_ja_02.png" width="31%" alt="仕入も売却もかんたんに記録">
  <img src="generated/google-play/ja/torekanri_ja_03.png" width="31%" alt="収支と在庫をまとめて見える化">
</p>

## App Store向け・英語 / App Store, English

<p>
  <img src="generated/app-store/en/torekanri_en_01.png" width="31%" alt="See Trades and Profit on Your Calendar">
  <img src="generated/app-store/en/torekanri_en_02.png" width="31%" alt="Log Purchases and Sales with Ease">
  <img src="generated/app-store/en/torekanri_en_03.png" width="31%" alt="See Profit and Inventory at a Glance">
</p>

## Google Play向け・英語 / Google Play, English

<p>
  <img src="generated/google-play/en/torekanri_en_01.png" width="31%" alt="See Trades and Profit on Your Calendar">
  <img src="generated/google-play/en/torekanri_en_02.png" width="31%" alt="Log Purchases and Sales with Ease">
  <img src="generated/google-play/en/torekanri_en_03.png" width="31%" alt="See Profit and Inventory at a Glance">
</p>
