# Custom Themes

Copy an included theme and update the YAML values. Python code changes are not required.

```bash
cp themes/premium-navy.yaml themes/my-brand.yaml
```

Then update `theme` in `config.yaml`.

```yaml
theme: ./themes/my-brand.yaml
```

Customizable values include:

- Background gradient colors
- Headline and body colors
- Maximum and minimum font sizes
- Accent visibility and color
- App capture width and height limits
- Device shadow
- Background panel color and opacity

Colors use the `#RRGGBB` format. Ratios use decimal values between `0` and `1`.
