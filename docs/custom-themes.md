# テーマのカスタマイズ / Custom Themes

[日本語](#日本語) | [English](#english)

## 日本語

付属テーマをコピーし、YAMLの値を変更すると、Pythonコードを書き換えずにデザインを変更できます。

```bash
cp themes/premium-navy.yaml themes/my-brand.yaml
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

色は`#RRGGBB`形式で指定します。大きさの比率は`0`から`1`の小数で指定します。

## English

Copy an included theme and edit its YAML values to customize the design without changing the Python source.

```bash
cp themes/premium-navy.yaml themes/my-brand.yaml
```

Set the new theme path in `config.yaml`:

```yaml
theme: ./themes/my-brand.yaml
```

You can customize background gradients, text colors and sizes, accent colors, screenshot size limits, shadows, and panel styling. Colors use `#RRGGBB`; ratios use decimal values between `0` and `1`.
