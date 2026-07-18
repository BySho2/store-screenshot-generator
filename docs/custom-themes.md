# テーマのカスタマイズ / Custom Themes

[日本語](#日本語) | [English](#english)

## 日本語

付属テーマをコピーし、YAMLの値を変更すると、Pythonコードを書き換えずにデザインを変更できます。

READMEの[テーマギャラリー](../README.md#デザインテーマを選ぶ)では、同じスクリーンショットから生成した6テーマを比較できます。

- `modern-gradient.yaml`：幅広いアプリ向けの標準テーマ
- `minimal-light.yaml`：業務・管理系向けの明るいテーマ
- `premium-navy.yaml`：金融・ビジネス系向けの落ち着いたテーマ
- `sunny-yellow.yaml`：生活・カジュアル系向けの明るいテーマ
- `dark-neon.yaml`：開発者・テック系向けのダークテーマ
- `soft-pastel.yaml`：ライフスタイル系向けの柔らかなテーマ

```bash
cp themes/modern-gradient.yaml themes/my-brand.yaml
```

次に、`config.yaml`の`theme`へ作成したファイルを指定します。

```yaml
theme: ./themes/my-brand.yaml
```

変更できる主な項目：

- 背景のグラデーションカラー
- 見出しと説明文の色
- 文字サイズの上限・下限
- アクセントラインの表示と色
- スクリーンショットの最大幅・最大高
- スクリーンショットの影
- 背景パネルの色と透明度
- スクリーンショットの角丸、汎用端末枠、外部フレーム素材
- 背景の複数の光彩とその位置
- アプリ名フッターの表示

色は`#RRGGBB`形式で指定します。大きさの比率は`0`から`1`の小数で指定します。

### 白いパネルと影を消す

```yaml
panel:
  enabled: false

device:
  frame: rounded
  shadow:
    enabled: false
```

`panel`と`shadow`は独立しているため、どちらか一方だけを残すこともできます。

### スクリーンショットの表示方式

`device.frame`では次の4種類を指定できます。

- `raw`：加工せずに配置する
- `rounded`：スクリーンショットを角丸に切り抜く
- `generic`：特定メーカーを表現しない汎用端末枠へ入れる
- `asset`：利用者が用意した透過PNGフレームへ入れる

モダンテーマ単体の既定値は`rounded`ですが、付属の設定テンプレートでは両ストアに黒い汎用端末枠を使用し、iPhone向けをAndroid向けより丸くしています。ストアごとに表示方式を変える場合は、`config.yaml`の各出力へ上書きを追加します。

```yaml
outputs:
  - name: app-store
    preset: app-store-iphone-6.9
    directory: ./output/app-store
    device:
      frame: generic
      corner_radius_ratio: 0.105
      bezel_ratio: 0.022

  - name: google-play
    preset: google-play-phone-portrait
    directory: ./output/google-play
    device:
      frame: generic
      corner_radius_ratio: 0.065
      bezel_ratio: 0.022
```

### 外部フレーム素材を使う

フレーム素材は透明な画面領域を持つPNGにしてください。`screen_rect`には、元のフレーム画像上でスクリーンショットを配置する`[左, 上, 幅, 高さ]`をピクセルで指定します。

```yaml
device:
  frame: asset
  frame_asset: ./frames/device-frame.png
  screen_rect: [72, 68, 1176, 2548]
```

外部素材はリポジトリに同梱されません。Apple、Google、端末メーカーなどの素材を使用する場合は、利用者自身で正規に取得し、用途とライセンス条件を確認してください。

### 影を調整する

```yaml
device:
  shadow:
    enabled: true
    opacity: 62
    blur_ratio: 0.032
    offset_y_ratio: 0.016
    padding_ratio: 0.045
```

## English

Copy an included theme and edit its YAML values to customize the design without changing the Python source.

See the [theme gallery](../README.en.md#choose-a-design-theme) to compare six themes generated from the same screenshot.

- `modern-gradient.yaml`: versatile recommended default
- `minimal-light.yaml`: clean theme for productivity apps
- `premium-navy.yaml`: refined theme for finance and business apps
- `sunny-yellow.yaml`: friendly theme for everyday apps
- `dark-neon.yaml`: dark theme for developer and technology apps
- `soft-pastel.yaml`: gentle theme for lifestyle apps

```bash
cp themes/modern-gradient.yaml themes/my-brand.yaml
```

Set the new theme path in `config.yaml`:

```yaml
theme: ./themes/my-brand.yaml
```

You can customize background gradients and glows, text colors and sizes, accent colors, screenshot size limits, frames, shadows, panel styling, and footer visibility. Colors use `#RRGGBB`; ratios use decimal values between `0` and `1`.

### Remove the panel and shadow

```yaml
panel:
  enabled: false

device:
  frame: rounded
  shadow:
    enabled: false
```

The panel and shadow are independent and can be enabled separately.

### Screenshot presentation modes

Set `device.frame` to one of four modes:

- `raw`: place the screenshot without clipping or a frame
- `rounded`: clip the screenshot to rounded corners
- `generic`: add a neutral device frame with no manufacturer-specific details
- `asset`: composite the screenshot behind a transparent PNG supplied by the user

Each output can override the theme's device settings:

The modern theme itself defaults to `rounded`. The included configuration template overrides both stores to a black neutral device frame and gives the iPhone output a stronger corner radius than the Android output:

```yaml
outputs:
  - name: app-store
    preset: app-store-iphone-6.9
    directory: ./output/app-store
    device:
      frame: generic
      corner_radius_ratio: 0.105
      bezel_ratio: 0.022

  - name: google-play
    preset: google-play-phone-portrait
    directory: ./output/google-play
    device:
      frame: generic
      corner_radius_ratio: 0.065
      bezel_ratio: 0.022
```

### Use an external frame asset

The PNG should have a transparent screen opening. `screen_rect` specifies `[left, top, width, height]` in pixels within the original frame image.

```yaml
device:
  frame: asset
  frame_asset: ./frames/device-frame.png
  screen_rect: [72, 68, 1176, 2548]
```

Frame artwork is not bundled. Obtain it through an authorized source and verify the license and intended use before using Apple, Google, or manufacturer artwork.

### Tune the shadow

```yaml
device:
  shadow:
    enabled: true
    opacity: 62
    blur_ratio: 0.032
    offset_y_ratio: 0.016
    padding_ratio: 0.045
```
