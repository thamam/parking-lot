# Visual Design System for Vibe-K8ds

## Design Principles

### 1. **Clarity Over Complexity**
Every visual element should have a clear purpose. Remove anything that doesn't directly help the child understand or act.

### 2. **Emotion Through Animation**
Static designs are forgotten. Animated characters and interfaces create emotional connections and maintain engagement.

### 3. **Accessibility First**
Design for the widest range of abilities from day one. High contrast, large targets, alternative input methods.

### 4. **Consistency Builds Confidence**
Predictable layouts and interactions help children feel secure and competent.

### 5. **Delight in Details**
Small animations, sound effects, and Easter eggs reward exploration and create memorable experiences.

## Color System

### Primary Palette

**For Ages 4-6**: Bright, saturated colors work best. Avoid pastels (too subtle) and dark colors (intimidating).

```css
/* Primary Action Colors */
--vibek8ds-blue: #2196F3;      /* Primary actions, Codey's color */
--vibek8ds-green: #4CAF50;     /* Success, positive actions */
--vibek8ds-yellow: #FFC107;    /* Attention, highlights */
--vibek8ds-orange: #FF9800;    /* Warnings, hints */
--vibek8ds-purple: #9C27B0;    /* Special, rewards */
--vibek8ds-pink: #E91E63;      /* Alternative character colors */

/* Neutral Colors */
--vibek8ds-white: #FFFFFF;
--vibek8ds-gray-light: #F5F5F5;
--vibek8ds-gray-medium: #E0E0E0;
--vibek8ds-gray-dark: #757575;
--vibek8ds-black: #212121;     /* Use sparingly, only for text */

/* Background Colors */
--vibek8ds-bg-sky: #E3F2FD;    /* World 1 background */
--vibek8ds-bg-grass: #F1F8E9;  /* World 2 background */
--vibek8ds-bg-ocean: #E0F7FA;  /* World 3 background */
--vibek8ds-bg-space: #E8EAF6;  /* World 4 background */
```

### Color Usage Guidelines

**DO**:
- Use color to indicate state (active, completed, locked)
- Combine color with shape/icon (don't rely on color alone)
- Use consistent colors for consistent actions
- Provide high contrast text (WCAG AAA: 7:1 minimum)

**DON'T**:
- Use red for errors (too harsh, scary for kids)
- Use too many colors on one screen (max 3-4)
- Use color gradients that reduce legibility
- Assume child isn't colorblind

### Colorblind-Friendly Mode

```css
/* Deuteranopia/Protanopia Safe Palette */
--vibek8ds-blue-cb: #0173B2;    /* Distinct from green */
--vibek8ds-green-cb: #029E73;   /* Yellower green */
--vibek8ds-yellow-cb: #ECE133;  /* High contrast yellow */
--vibek8ds-orange-cb: #DE8F05;  /* Distinct from green */
--vibek8ds-pink-cb: #CC78BC;    /* Distinct from blue */
```

## Typography

### Font Selection

**Primary Font: "Fredoka" (Google Fonts)**

**Rationale**:
- Friendly, rounded letterforms
- Highly legible at all sizes
- Distinctive characters (no confusing 1/I or O/0)
- Supports multiple weights
- Free, open-source

**Fallback Stack**:
```css
font-family: 'Fredoka', 'Comic Sans MS', 'Chalkboard SE',
             'Arial Rounded MT Bold', sans-serif;
```

### Type Scale

```css
/* Parent Interface (Traditional) */
--font-size-parent-small: 14px;
--font-size-parent-body: 16px;
--font-size-parent-large: 20px;
--font-size-parent-heading: 28px;

/* Child Interface (Minimal Text) */
--font-size-child-label: 24px;   /* If text is needed */
--font-size-child-number: 48px;  /* For counting, ages */
--font-size-child-title: 36px;   /* World titles */

/* Line Heights */
--line-height-tight: 1.2;
--line-height-normal: 1.5;
--line-height-loose: 1.8;
```

### Text Usage in Child Interface

**Minimize Text**:
- Use icons and images instead
- If text needed, keep to 1-3 words maximum
- All-caps for emphasis
- Never paragraphs

**Examples**:

```
❌ BAD:
"Touch the button below to continue to the next activity"

✅ GOOD:
[NEXT button with arrow icon]

---

❌ BAD:
"Completed Activities: 5/10"

✅ GOOD:
⭐⭐⭐⭐⭐ ☆☆☆☆☆

---

❌ BAD:
"Sequencing - Beginner Level - Activity 3"

✅ GOOD:
[World 1 icon] [3 dots, 3rd highlighted]
```

## Iconography

### Icon Style

**Style**: Rounded, friendly, 2-tone

**Specifications**:
- 3px rounded corners on all shapes
- 3-4px stroke weight
- Two-color maximum (outline + fill)
- Consistent visual weight across icon set

### Core Icon Set

```
NAVIGATION:
🏠 Home (house)
🔙 Back (left arrow in circle)
⚙️  Settings (gear) - parents only
❓ Help (question mark)
▶️  Play/Go (right arrow or play button)

COMMANDS (Activity Tiles):
→ Forward (right arrow)
← Backward (left arrow)
↑ Up/Jump (up arrow)
↓ Down (down arrow)
🔄 Turn/Rotate (circular arrow)
🔁 Repeat (loop symbol)

FEEDBACK:
⭐ Star (success, points)
🏆 Trophy (achievement)
💚 Heart (like, favorite)
✓ Checkmark (completed)
🔒 Lock (locked content)

CHARACTERS:
🤖 Codey (robot face)
🐶 Puppy
🐱 Kitty
🦊 Fox
🐻 Bear
```

### Icon Sizes

```css
--icon-small: 32px;   /* Secondary actions */
--icon-medium: 48px;  /* Primary actions */
--icon-large: 64px;   /* Character avatars */
--icon-xlarge: 96px;  /* Hero images, rewards */
```

## Layout System

### Grid System

**Base Unit**: 8px grid

All spacing, sizing, and positioning based on multiples of 8.

```css
--space-xs: 8px;
--space-sm: 16px;
--space-md: 24px;
--space-lg: 32px;
--space-xl: 48px;
--space-xxl: 64px;
```

### Screen Templates

**Template 1: Activity Screen (Most Common)**

```
┌─────────────────────────────────────────┐
│ ┌───┐                         ┌───┐    │ ← Top Bar (32px)
│ │🏠 │                         │⚙️ │    │   Minimal chrome
│ └───┘                         └───┘    │
├─────────────────────────────────────────┤
│                                         │
│         ┌─────────────────┐             │
│         │                 │             │
│         │   Main Play     │             │ ← Play Area
│         │   Area          │             │   (60% of screen)
│         │                 │             │
│         │   [Character]   │             │
│         │   [Environment] │             │
│         └─────────────────┘             │
│                                         │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐   │
│  │   Command Palette               │   │ ← Command Area
│  │   ┌───┐ ┌───┐ ┌───┐ ┌───┐      │   │   (20% of screen)
│  │   │→ │ │← │ │↑ │ │🔄│      │   │
│  │   └───┘ └───┘ └───┘ └───┘      │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│         ┌──────────────┐                │ ← Action Bar
│         │  [▶️ GO!]   │                │   (15% of screen)
│         └──────────────┘                │
└─────────────────────────────────────────┘
```

**Template 2: World Map (Navigation)**

```
┌─────────────────────────────────────────┐
│ ┌───┐         WORLD 1         ┌───┐    │
│ │🏠 │         CODEY'S PARK     │⚙️ │    │
│ └───┘                          └───┘    │
├─────────────────────────────────────────┤
│                                         │
│      ⭐                                  │
│    ┌───┐   path    ⭐                   │
│    │ 1 │─────────┌───┐   path          │
│    └───┘         │ 2 │─────────┌───┐   │
│    ⭐⭐⭐         └───┘         │ 3 │   │
│    Completed     ⭐⭐☆          └───┘   │
│                  In Progress   ☆☆☆     │
│                                Locked   │
│                                         │
│           ⭐                             │
│         ┌───┐   path                    │
│         │ 4 │─────────┌───┐             │
│         └───┘         │ 5 │             │
│         ☆☆☆           └───┘             │
│         Locked        ☆☆☆               │
│                                         │
└─────────────────────────────────────────┘
```

**Template 3: Celebration Screen**

```
┌─────────────────────────────────────────┐
│                                         │
│         ✨ 🎉 ✨ 🎉 ✨                   │
│                                         │
│              YOU DID IT!                │
│                                         │
│         ┌─────────────────┐             │
│         │                 │             │
│         │   [Codey        │             │
│         │    celebrating] │             │
│         │                 │             │
│         └─────────────────┘             │
│                                         │
│              ⭐ ⭐ ⭐                     │
│                                         │
│         ┌──────────────┐                │
│         │  [NEXT]      │                │
│         └──────────────┘                │
│                                         │
│         ✨ 🎊 ✨ 🎊 ✨                   │
└─────────────────────────────────────────┘
```

### Responsive Breakpoints

```css
/* Tablets (Primary) */
@media (min-width: 768px) and (max-width: 1024px) {
  /* iPad, Android tablets */
  /* Landscape mode preferred */
}

/* Large Tablets */
@media (min-width: 1024px) and (max-width: 1366px) {
  /* iPad Pro */
}

/* Phones (Secondary) */
@media (max-width: 767px) {
  /* Portrait mode */
  /* Simplified layouts */
  /* Larger touch targets */
}
```

## Interactive Elements

### Buttons

**Primary Action Button**:

```css
.btn-primary {
  min-width: 120px;
  min-height: 60px;  /* Large for small fingers */
  padding: 16px 32px;
  border-radius: 30px;  /* Fully rounded */
  background: linear-gradient(180deg,
    var(--vibek8ds-blue) 0%,
    #1976D2 100%);
  box-shadow:
    0 4px 0 #1565C0,  /* Bottom shadow for 3D effect */
    0 6px 12px rgba(0,0,0,0.2);
  font-size: 24px;
  font-weight: 600;
  color: white;
  text-transform: uppercase;

  transition: all 0.1s ease;
}

.btn-primary:active {
  transform: translateY(4px);  /* Press down effect */
  box-shadow:
    0 0 0 #1565C0,
    0 2px 8px rgba(0,0,0,0.2);
}

.btn-primary:hover {
  box-shadow:
    0 4px 0 #1565C0,
    0 8px 16px rgba(0,0,0,0.3);
  transform: translateY(-2px);  /* Lift on hover */
}
```

**Command Tile Button**:

```css
.btn-command {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  background: white;
  border: 4px solid var(--vibek8ds-gray-medium);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);

  display: flex;
  align-items: center;
  justify-content: center;

  transition: all 0.2s ease;
}

.btn-command:active {
  transform: scale(0.95);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-command.selected {
  border-color: var(--vibek8ds-blue);
  box-shadow:
    0 0 0 4px rgba(33, 150, 243, 0.2),
    0 4px 8px rgba(0,0,0,0.1);
}

.btn-command:hover {
  border-color: var(--vibek8ds-blue);
  transform: scale(1.05);
}
```

### Touch Targets

**Minimum Sizes**:
```css
--touch-target-min: 60px;   /* Standard minimum */
--touch-target-comfortable: 80px;  /* Preferred */
--touch-target-easy: 100px; /* Accessibility mode */

/* Spacing between targets */
--touch-spacing-min: 20px;
--touch-spacing-comfortable: 24px;
```

### States

All interactive elements must have clear states:

1. **Default**: How it appears normally
2. **Hover**: Mouse over (desktop/trackpad)
3. **Active/Pressed**: Currently being tapped
4. **Focused**: Selected via keyboard/switch control
5. **Disabled**: Cannot be interacted with (grayed out, locked)

**Visual Indicators**:
```
Default:    Normal appearance
Hover:      Slight scale up (1.05x), shadow increase
Active:     Scale down (0.95x), shadow decrease
Focused:    Thick border or outline
Disabled:   Opacity 0.4, grayscale filter
```

## Character Design

### Codey the Robot (Primary Character)

**Design Specifications**:

```
HEAD:
- Rounded square shape (border-radius: 30%)
- Two circular eyes (animated, expressive)
- Small antenna on top
- Screen-like "mouth" that changes shape

BODY:
- Slightly rounded rectangle
- Two arms (simple cylinders with rounded hands)
- Two legs (simple cylinders with rounded feet)
- All joints allow for rotation

COLOR SCHEME:
- Primary: Vibek8ds Blue (#2196F3)
- Accent: White for face screen
- Details: Yellow for antenna tip
```

**Expression System**:

```
HAPPY:
Eyes: ^_^
Mouth: U shape

EXCITED:
Eyes: ⭐_⭐
Mouth: D shape with slight bounce

THINKING:
Eyes: Looking up and right
Mouth: Small o shape
Antenna: Question mark appears

CELEBRATING:
Eyes: Closed happy arcs
Mouth: Wide smile
Arms: Raised up
Body: Slight bounce

SAD/CONCERNED:
Eyes: -_-
Mouth: Inverted U
Body: Slight slump

SURPRISED:
Eyes: O_O
Mouth: O shape
Body: Slight jump back
```

### Supporting Characters

**Puppy**:
- Floppy ears that bounce
- Tail that wags when happy
- Simple dog shape, friendly face
- Color: Golden brown

**Kitty**:
- Pointed ears with pink inside
- Tail that swishes
- Whiskers
- Color: Orange tabby

**Fox**:
- Large triangular ears
- Bushy tail
- Clever, playful expression
- Color: Orange with white accents

**Bear**:
- Round, cuddly shape
- Small round ears
- Gentle expression
- Color: Brown

## Animation Principles

### For Young Children

**Key Principles**:

1. **Exaggeration**: Movements should be clear and obvious (1.5x normal)
2. **Anticipation**: Wind up before action (crouch before jump)
3. **Follow-through**: Complete the motion (don't stop abruptly)
4. **Squash and Stretch**: Characters feel alive and responsive
5. **Slow In/Slow Out**: Ease timing feels natural
6. **Appeal**: Every animation should be pleasant to watch

### Animation Speeds

```css
/* Timing for different action types */
--duration-instant: 0ms;     /* Immediate state changes */
--duration-quick: 150ms;     /* UI feedback (button press) */
--duration-normal: 300ms;    /* Standard transitions */
--duration-slow: 500ms;      /* Character movements */
--duration-celebration: 1000ms; /* Success animations */

/* Easing functions */
--ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-smooth: cubic-bezier(0.25, 0.46, 0.45, 0.94);
```

### Common Animations

**Button Press**:
```javascript
// Scale down + bounce back
{
  scale: [1, 0.95, 1.05, 1],
  duration: 300,
  easing: 'easeInOut'
}
```

**Character Walk**:
```javascript
// Step-by-step movement with bounce
{
  translateX: [0, 100],  // Move right
  rotate: [-5, 5, -5, 5], // Subtle wobble
  duration: 500,
  easing: 'easeInOut'
}
```

**Success Celebration**:
```javascript
// Confetti + scale up + bounce
{
  confetti: {particles: 50, duration: 1000},
  character: {
    scale: [1, 1.2, 1],
    rotate: [0, -10, 10, 0],
    duration: 800
  },
  stars: {
    scale: [0, 1.3, 1],
    opacity: [0, 1, 1],
    rotate: [0, 360],
    duration: 600,
    stagger: 100  // Each star appears 100ms after previous
  }
}
```

**Loading / Waiting**:
```javascript
// Codey's antenna pulses
{
  antenna: {
    scale: [1, 1.2, 1],
    opacity: [1, 0.6, 1],
    duration: 1000,
    loop: true
  }
}
```

### Micro-Interactions

Small animations that provide feedback:

```
TAP FEEDBACK:
- Ripple effect from touch point
- Element scales down then up
- Sound effect plays
Duration: 150ms

DRAG START:
- Element lifts (shadow increases)
- Slight scale up (1.1x)
- Haptic vibration
Duration: 100ms

DROP SUCCESS:
- Element snaps to grid with bounce
- Checkmark animation appears
- Success sound
Duration: 300ms

DROP FAILURE:
- Element bounces back to origin
- Gentle shake animation
- Soft error sound
Duration: 400ms
```

## Accessibility Features

### High Contrast Mode

```css
.high-contrast {
  --vibek8ds-blue: #0D47A1;      /* Darker blue */
  --vibek8ds-green: #2E7D32;     /* Darker green */
  --vibek8ds-yellow: #F57F17;    /* Darker yellow */

  /* Increase border weights */
  --border-default: 4px;

  /* Stronger shadows */
  --shadow-default: 0 4px 12px rgba(0,0,0,0.4);
}
```

### Reduced Motion Mode

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }

  /* Keep essential animations but simplify */
  .character-walk {
    transition: transform 0.3s linear;
    /* Remove bounces and wobbles */
  }
}
```

### Large Touch Target Mode

```css
.accessibility-mode {
  --touch-target-min: 100px;
  --touch-spacing-min: 32px;
  --font-size-child-label: 32px;
}
```

## Design Tokens (Complete Reference)

```javascript
// design-tokens.js
export const tokens = {
  colors: {
    primary: {
      blue: '#2196F3',
      green: '#4CAF50',
      yellow: '#FFC107',
      orange: '#FF9800',
      purple: '#9C27B0',
      pink: '#E91E63'
    },
    neutral: {
      white: '#FFFFFF',
      grayLight: '#F5F5F5',
      grayMedium: '#E0E0E0',
      grayDark: '#757575',
      black: '#212121'
    },
    backgrounds: {
      sky: '#E3F2FD',
      grass: '#F1F8E9',
      ocean: '#E0F7FA',
      space: '#E8EAF6'
    }
  },

  spacing: {
    xs: 8,
    sm: 16,
    md: 24,
    lg: 32,
    xl: 48,
    xxl: 64
  },

  borderRadius: {
    sm: 8,
    md: 12,
    lg: 16,
    xl: 24,
    round: 9999
  },

  shadows: {
    sm: '0 2px 4px rgba(0,0,0,0.1)',
    md: '0 4px 8px rgba(0,0,0,0.1)',
    lg: '0 8px 16px rgba(0,0,0,0.15)',
    xl: '0 12px 24px rgba(0,0,0,0.2)'
  },

  typography: {
    fontSize: {
      parentSmall: 14,
      parentBody: 16,
      parentLarge: 20,
      parentHeading: 28,
      childLabel: 24,
      childNumber: 48,
      childTitle: 36
    },
    lineHeight: {
      tight: 1.2,
      normal: 1.5,
      loose: 1.8
    },
    fontWeight: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700
    }
  },

  animation: {
    duration: {
      instant: 0,
      quick: 150,
      normal: 300,
      slow: 500,
      celebration: 1000
    },
    easing: {
      standard: 'cubic-bezier(0.4, 0.0, 0.2, 1)',
      bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
      smooth: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
    }
  }
};
```

---

**Next Steps**:
1. Create Figma/Sketch design library with all components
2. Build React Native component library
3. Create Lottie animation library for characters
4. Develop accessibility testing checklist
5. Conduct user testing with target age group
