# Custom Fonts

This directory contains custom fonts for use in **external web projects and applications**. 

**Note:** GitHub profile READMEs do not support custom fonts or CSS. These fonts are provided for use in personal websites, portfolio projects, and other applications outside of GitHub.

## Fonts

### IM Fell Double Pica

A classical serif typeface designed for long-form reading. This font brings an elegant, literary quality to text.

**Files:**
- `IMFELLDOUBLEPICA-REGULAR.TTF` - Regular weight
- `IMFELLDOUBLEPICA-ITALIC.TTF` - Italic style

**Usage:**
```css
@font-face {
  font-family: 'IM Fell Double Pica';
  src: url('./IMFELLDOUBLEPICA-REGULAR.TTF') format('truetype');
  font-weight: normal;
  font-style: normal;
}
```

### Portmanteau

A distinctive display font perfect for headings and titles.

**Files:**
- `PORTMANTEAU-REGULAR.OTF` - OpenType format
- `PORTMANTEAU REGULAR.TTF` - TrueType format

**Usage:**
```css
@font-face {
  font-family: 'Portmanteau';
  src: url('./PORTMANTEAU-REGULAR.OTF') format('opentype');
  font-weight: normal;
  font-style: normal;
}
```

## License

These fonts are sourced from the [my_music_page](https://github.com/Rtur2003/my_music_page) repository.
Please refer to the original repository for licensing information.

## Integration

### Web Projects

Include the fonts in your HTML:

```html
<style>
@font-face {
  font-family: 'IM Fell Double Pica';
  src: url('./fonts/IMFELLDOUBLEPICA-REGULAR.TTF') format('truetype');
}

@font-face {
  font-family: 'Portmanteau';
  src: url('./fonts/PORTMANTEAU-REGULAR.OTF') format('opentype');
}

body {
  font-family: 'IM Fell Double Pica', Georgia, serif;
}

h1, h2, h3 {
  font-family: 'Portmanteau', Arial, sans-serif;
}
</style>
```

### Desktop Applications

Install the font files on your system:

**Windows:**
1. Right-click the font file
2. Select "Install" or "Install for all users"

**macOS:**
1. Double-click the font file
2. Click "Install Font" in Font Book

**Linux:**
1. Copy fonts to `~/.local/share/fonts/` or `/usr/share/fonts/`
2. Run `fc-cache -f -v` to refresh font cache
