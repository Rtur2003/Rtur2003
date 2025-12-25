# Font Preview & Usage Guide

This document showcases the custom fonts and provides pairing recommendations.

## 📖 IM Fell Double Pica

A classical serif typeface perfect for body text and long-form reading. This elegant font brings a literary quality to documentation.

### Character Set
```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789 !@#$%^&*()_+-=[]{}|;:,.<>?
```

### Sample Text
> The quick brown fox jumps over the lazy dog.
> 
> In the realm of code and creation, where logic meets artistry, we find the perfect balance between structure and expression. This font embodies that harmony with its classical proportions and elegant curves.

### Best Used For
- Documentation paragraphs
- README descriptions
- Long-form technical writing
- Code comments and explanations
- Article body text

---

## 🎨 Portmanteau

A distinctive display font ideal for headings, titles, and attention-grabbing text.

### Character Set
```
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789 !@#$%^&*()_+-=[]{}|;:,.<>?
```

### Sample Text
```
# Welcome to My Profile
## Building the Future
### Code • Create • Compose
```

### Best Used For
- Section headings (H1, H2, H3)
- Banner text
- Logo and branding
- Call-to-action text
- Project titles
- Navigation elements

---

## 🎯 Pairing Guide

### Recommended Combinations

#### Option 1: Classic Hierarchy
- **Headings**: Portmanteau (bold, distinctive)
- **Body**: IM Fell Double Pica (readable, elegant)
- **Code**: Fira Code or JetBrains Mono

```css
h1, h2, h3 { font-family: 'Portmanteau', sans-serif; }
p { font-family: 'IM Fell Double Pica', Georgia, serif; }
code { font-family: 'Fira Code', monospace; }
```

#### Option 2: Subtle Sophistication
- **All text**: IM Fell Double Pica
- **Code**: Consolas or Monaco

```css
body { font-family: 'IM Fell Double Pica', Georgia, serif; }
code { font-family: 'Consolas', monospace; }
```

### Size Recommendations

**Portmanteau:**
- H1: 32-48px
- H2: 24-32px
- H3: 18-24px
- Buttons/CTAs: 16-20px

**IM Fell Double Pica:**
- Body: 16-18px
- Captions: 14-16px
- Fine print: 12-14px
- Line height: 1.6-1.8 for optimal readability

### Color Considerations

Both fonts work well with:
- **Dark on light**: #333333 on #FFFFFF
- **Light on dark**: #FFFFFF on #1a1a1a or #70A5FD background
- **Accent colors**: Blues (#70A5FD), Purples (#9370DB), Teals (#20B2AA)

**Accessibility tip**: Maintain at least 4.5:1 contrast ratio for body text (WCAG AA)

---

## 💻 Usage Examples

### HTML Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="assets/style.css">
  <style>
    h1, h2, h3 {
      font-family: 'Portmanteau', sans-serif;
      color: #70A5FD;
      letter-spacing: 0.02em;
    }
    
    p {
      font-family: 'IM Fell Double Pica', Georgia, serif;
      color: #333;
      line-height: 1.7;
      font-size: 17px;
    }
  </style>
</head>
<body>
  <h1 class="custom-font-heading">Welcome to My Profile</h1>
  <p class="custom-font-body">
    Creating elegant solutions with thoughtful design and clean code.
    Every line of code is an opportunity to build something meaningful.
  </p>
</body>
</html>
```

### Markdown with Inline Styles

```markdown
<div style="font-family: 'Portmanteau', sans-serif; font-size: 32px; color: #70A5FD;">
  🎨 Design Portfolio
</div>

<p style="font-family: 'IM Fell Double Pica', serif; line-height: 1.7;">
  Exploring the intersection of technology and art through 
  code, music composition, and visual design. Each project 
  represents a journey of learning and creative expression.
</p>
```

### React/JSX Example

```jsx
import './assets/style.css';

function ProfileHeader() {
  return (
    <div>
      <h1 className="custom-font-heading">
        Hasan Arthur Altuntaş
      </h1>
      <p className="custom-font-body">
        Full Stack Developer • Music Composer • Robotics Enthusiast
      </p>
    </div>
  );
}
```

---

## 📦 Installation

### For Web Projects

1. **Copy fonts to your project:**
   ```
   project/
   ├── assets/
   │   └── fonts/
   │       ├── IMFELLDOUBLEPICA-REGULAR.TTF
   │       ├── IMFELLDOUBLEPICA-ITALIC.TTF
   │       ├── PORTMANTEAU-REGULAR.OTF
   │       └── PORTMANTEAU REGULAR.TTF
   └── css/
       └── style.css
   ```

2. **Add @font-face declarations:**
   ```css
   @font-face {
     font-family: 'IM Fell Double Pica';
     src: url('../fonts/IMFELLDOUBLEPICA-REGULAR.TTF') format('truetype');
     font-weight: normal;
     font-style: normal;
     font-display: swap;
   }
   
   @font-face {
     font-family: 'Portmanteau';
     src: url('../fonts/PORTMANTEAU-REGULAR.OTF') format('opentype');
     font-weight: normal;
     font-style: normal;
     font-display: swap;
   }
   ```

3. **Apply to elements:**
   ```css
   body {
     font-family: 'IM Fell Double Pica', Georgia, serif;
   }
   
   h1, h2, h3 {
     font-family: 'Portmanteau', sans-serif;
   }
   ```

### For Desktop Use

**Windows:**
1. Right-click font file → "Install" or "Install for all users"
2. Or copy to `C:\Windows\Fonts\`

**macOS:**
1. Double-click font file → "Install Font" in Font Book
2. Or copy to `~/Library/Fonts/`

**Linux:**
1. Copy fonts to `~/.local/share/fonts/` or `/usr/share/fonts/`
2. Run `fc-cache -f -v` to refresh font cache
3. Verify with `fc-list | grep "IM Fell\|Portmanteau"`

---

## 🎭 Design Principles

### When to Use IM Fell Double Pica
✅ Long-form reading  
✅ Professional documentation  
✅ Academic or literary content  
✅ When elegance and readability matter  

❌ Avoid for: Very small text (<12px), UI elements requiring quick scanning

### When to Use Portmanteau
✅ Making a strong visual statement  
✅ Brand identity elements  
✅ Section separators  
✅ Emphasis and hierarchy  

❌ Avoid for: Body text, long paragraphs, small sizes

---

## 🔍 Technical Details

### File Formats
- **TTF (TrueType Font)**: Universal compatibility, good for web and desktop
- **OTF (OpenType Font)**: Advanced features, preferred for professional design

### Browser Support
Both fonts work in all modern browsers:
- Chrome 4+
- Firefox 3.5+
- Safari 3.1+
- Edge (all versions)
- Opera 10+

### Performance Tips
- Use `font-display: swap` to prevent text blocking
- Preload critical fonts: `<link rel="preload" href="font.woff2" as="font">`
- Consider subsetting fonts for better performance
- Load locally rather than from external CDN for privacy

---

## 📄 License

These fonts are sourced from the [my_music_page](https://github.com/Rtur2003/my_music_page) repository. Please refer to the original repository for licensing information.

---

## 🎨 Inspiration

> "Typography is the voice of design. These fonts speak with elegance and distinction."

Use these fonts to create:
- Professional profiles that stand out
- Documentation that's pleasant to read
- Brands with character and sophistication
- Interfaces that respect the craft of typography

---

## 📚 Further Reading

- [assets/fonts/README.md](README.md) - Installation guide
- [DEVELOPMENT.md](../../DEVELOPMENT.md) - Project setup
- [Main README](../../README.md) - See fonts in action

---

*Last updated: December 2025*
