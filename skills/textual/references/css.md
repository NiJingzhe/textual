# Textual CSS (TCSS) Reference

## Table of Contents
- [Tailwind Utility Classes](#tailwind-utility-classes)
- [Selectors](#selectors)
- [Layout Properties](#layout-properties)
- [Sizing Properties](#sizing-properties)
- [Positioning Properties](#positioning-properties)
- [Appearance Properties](#appearance-properties)
- [Text Properties](#text-properties)
- [Scrolling Properties](#scrolling-properties)
- [Animation Properties](#animation-properties)
- [Theme Variables](#theme-variables)
- [Tailwind Palette Variables](#tailwind-palette-variables)
- [Pseudo-classes](#pseudo-classes)

## Tailwind Utility Classes

Textual includes a bundled `tailwind.tcss` utility sheet with Tailwind-inspired classes.

### Loading

```python
from textual import tailwind_tcss

class MyApp(App):
    CSS = tailwind_tcss() + """/* custom CSS */"""
    # or CSS_PATH = "styles/tailwind.tcss"  (exported via: export-twcss ./)
```

### Applying Classes

```python
# Via classes parameter
yield Button("OK", classes="bg-blue-500 text-white hover:bg-blue-700 transition-colors")

# Via widget attribute
widget.add_class("bg-slate-700")
widget.toggle_class("border-round")
```

### Arbitrary Values

Use `[value]` syntax for custom values:

```python
classes="w-[42] bg-[#334155] text-[#f8fafc] opacity-[55%] p-[3]"
classes="min-w-[20] max-h-[30] border-[solid #ff0000]"
```

### Pseudo-class Prefixes

```python
classes="hover:bg-blue-700 focus:border-round dark:hover:bg-slate-700"
classes="disabled:opacity-[50%] focus-within:bg-[#1e293b] odd:bg-[#0f172a]"
```

Prefixes: `hover`, `focus`, `blur`, `focus-within`, `disabled`, `enabled`, `dark`, `light`, `first-child`, `last-child`, `odd`, `even`, `empty`

### Layout Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `block` | `display: block` |
| `hidden` | `display: none` |
| `visible` / `invisible` | `visibility: visible / hidden` |
| `relative` / `absolute` | `position: relative / absolute` |
| `layout-horizontal` | `layout: horizontal` |
| `layout-vertical` | `layout: vertical` |
| `layout-stream` | `layout: stream` |
| `grid` | `layout: grid` |
| `dock-top/right/bottom/left` | `dock: top/right/bottom/left` |

### Overflow Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `overflow-auto` | `overflow: auto auto` |
| `overflow-hidden` | `overflow: hidden hidden` |
| `overflow-scroll` | `overflow: scroll scroll` |
| `overflow-x-auto/hidden/scroll` | `overflow-x: auto/hidden/scroll` |
| `overflow-y-auto/hidden/scroll` | `overflow-y: auto/hidden/scroll` |

### Alignment Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `align-center` | `align: center middle` |
| `align-top-left` | `align: left top` |
| `align-middle-right` | `align: right middle` |
| `align-x-left/center/right` | `align-horizontal: left/center/right` |
| `align-y-top/middle/bottom` | `align-vertical: top/middle/bottom` |
| `content-center` | `content-align: center middle` |
| `content-top-left` | `content-align: left top` |
| `content-x-left/center/right` | `content-align-horizontal: ...` |
| `content-y-top/middle/bottom` | `content-align-vertical: ...` |
| `expand-greedy/optimal` | `expand: greedy/optimal` |

### Spacing Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `p-0/1/2/4` | `padding: 0/1/2/4` |
| `px-0/1/2/4` | `padding-left/right: 0/1/2/4` |
| `py-0/1/2/4` | `padding-top/bottom: 0/1/2/4` |
| `pl-0/1/2/4` | `padding-left: 0/1/2/4` |
| `pr-0/1/2/4` | `padding-right: 0/1/2/4` |
| `pt-0/1/2/4` | `padding-top: 0/1/2/4` |
| `pb-0/1/2/4` | `padding-bottom: 0/1/2/4` |
| `m-0/1/2/4` | `margin: 0/1/2/4` |
| `mx-0/1/2/4` | `margin-left/right: 0/1/2/4` |
| `my-0/1/2/4` | `margin-top/bottom: 0/1/2/4` |
| `ml-0/1/2/4` | `margin-left: 0/1/2/4` |
| `mr-0/1/2/4` | `margin-right: 0/1/2/4` |
| `mt-0/1/2/4` | `margin-top: 0/1/2/4` |
| `mb-0/1/2/4` | `margin-bottom: 0/1/2/4` |

### Sizing Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `w-auto/full/screen/fr` | `width: auto/100%/100vw/1fr` |
| `h-auto/full/screen/fr` | `height: auto/100%/100vh/1fr` |
| `min-w-0` / `min-h-0` | `min-width/min-height: 0` |
| `max-w-full` / `max-h-full` | `max-width/max-height: 100%` |

### Text Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `text-left/center/right/justify/start/end` | `text-align: ...` |
| `text-wrap/nowrap/clip/fold/ellipsis` | `text-wrap/text-overflow: ...` |
| `font-normal/bold/italic` | `text-style: none/bold/italic` |
| `underline` / `line-through` / `reverse` | `text-style: underline/strike/reverse` |
| `font-bold-italic/underline/italic-underline` | `text-style: bold italic/...` |

### Color Utilities

**Background**: `bg-transparent`, `bg-white`, `bg-black`, `bg-slate-50/300/500/700/900`, `bg-blue-500/700`, `bg-emerald-500/700`, `bg-amber-500`, `bg-red-500`

**Text**: `text-white`, `text-black`, `text-slate-50/300/500/700/900`, `text-blue-500/700`, `text-emerald-500/700`, `text-amber-500`, `text-red-500`

**Tint**: `tint-white-10`, `tint-black-10`

### Border & Outline Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `border` | `border: solid $tw-border-neutral` |
| `border-none` | `border: none` |
| `border-dashed/double/heavy/round` | `border: dashed/double/heavy/round $tw-border-neutral` |
| `border-t/r/b/l` | `border-top/right/bottom/left: solid ...` |
| `border-x/y` | `border-left+right / top+bottom: solid ...` |
| `border-slate-300/blue-500/emerald-500/amber-500/red-500` | colored borders |
| `outline/none/dashed/double` | `outline: solid/none/dashed/double $tw-outline-neutral` |

### Grid Utilities

| Class | CSS Equivalent |
|-------|---------------|
| `grid-cols-1/2/3/4` | `grid-size-columns: 1/2/3/4` |
| `grid-rows-1/2/3/4` | `grid-size-rows: 1/2/3/4` |
| `col-span-1/2/3/4` | `column-span: 1/2/3/4` |
| `row-span-1/2/3/4` | `row-span: 1/2/3/4` |
| `gap-0/1/2/4` | `grid-gutter: 0/1/2/4` |
| `gap-x-1/2/4` | `grid-gutter-horizontal: 1/2/4` |
| `gap-y-1/2/4` | `grid-gutter-vertical: 1/2/4` |

### Cursor Utilities

`cursor-default`, `cursor-pointer`, `cursor-text`, `cursor-wait`, `cursor-grab`, `cursor-grabbing`, `cursor-move`

### Transition Utilities

| Class | Transitions |
|-------|-------------|
| `transition-colors` | color, background, tint |
| `transition-opacity` | opacity, text-opacity |
| `transition-offset` | offset |
| `transition-size` | width, height, min/max-width/height |
| `transition-basic` | background, color, opacity, offset |
| `transition-slow-colors` | color, background, tint (slow) |
| `transition-all` | all of the above |

## Selectors

```css
/* Type selector - matches Python class name */
Button { }

/* ID selector */
#sidebar { }

/* Class selector */
.error { }

/* Compound selectors */
Button.primary { }

/* Descendant combinator */
#dialog Button { }

/* Child combinator */
Container > Button { }

/* Multiple selectors */
#submit, #cancel { }
```

## Nested CSS

```css
#container {
    background: $surface;

    .item {
        padding: 1;

        &:hover {
            background: $primary;
        }

        &.-active {
            border: solid green;
        }
    }
}
```

## Layout Properties

```css
layout: vertical;          /* vertical, horizontal, grid */

/* Grid layout */
grid-size: 3 2;           /* columns rows */
grid-columns: 1fr 2fr 1fr;
grid-rows: auto 1fr;
grid-gutter: 1 2;         /* vertical horizontal */
column-span: 2;
row-span: 2;
```

## Sizing Properties

```css
width: 50%;               /* auto, %, fr, cells */
height: 100%;
min-width: 20;
max-width: 80;
min-height: 10;
max-height: 50;

margin: 1 2;              /* vertical horizontal */
margin: 1 2 1 2;          /* top right bottom left */
padding: 1 2;
padding: 1 2 1 2;
```

## Positioning Properties

```css
dock: top;                /* top, right, bottom, left */
offset: 5 10;             /* x y offset */
offset-x: -100%;
offset-y: 50%;
layer: overlay;           /* layer name */
```

### Layers
```css
Screen {
    layers: base overlay modal;
}

#background { layer: base; }
#popup { layer: overlay; }
#dialog { layer: modal; }
```

## Appearance Properties

```css
background: darkblue;
color: white;

/* Borders */
border: solid green;      /* none, solid, double, round, heavy, tall, wide */
border-top: double red;
border-right: solid blue;
border-bottom: heavy green;
border-left: round yellow;

outline: dashed red;
opacity: 0.5;
```

## Text Properties

```css
text-align: center;       /* left, center, right */
content-align: center middle;  /* horizontal vertical */
text-style: bold italic;  /* bold, italic, underline, reverse, strike */
```

## Scrolling Properties

```css
overflow: auto;           /* auto, hidden, scroll */
overflow-x: auto;
overflow-y: scroll;
scrollbar-gutter: stable;
```

## Animation Properties

```css
transition: background 500ms;
transition: offset 200ms ease-in-out;
transition: opacity 300ms linear;

/* Multiple transitions */
transition: background 200ms, offset 300ms;
```

### Easing Functions
- `linear`
- `ease-in`
- `ease-out`
- `ease-in-out`

## Theme Variables

### Core Colors
```css
$primary
$secondary
$success
$warning
$error
$text
$background
$surface
$panel
```

### Color Variants
```css
$primary-lighten-1
$primary-lighten-2
$primary-lighten-3
$primary-darken-1
$primary-darken-2
$primary-darken-3
```

### Custom Variables
```css
$my-color: dodgerblue;
$spacing: 2;

.widget {
    background: $my-color;
    padding: $spacing;
}
```

## Tailwind Palette Variables

These variables are defined in `tailwind.tcss` and available when using the utility sheet:

```css
/* Slate */
$tw-slate-50: #f8fafc;
$tw-slate-300: #cbd5e1;
$tw-slate-500: #64748b;
$tw-slate-700: #334155;
$tw-slate-900: #0f172a;

/* Blue */
$tw-blue-500: #3b82f6;
$tw-blue-700: #1d4ed8;

/* Emerald */
$tw-emerald-500: #10b981;
$tw-emerald-700: #047857;

/* Amber / Red */
$tw-amber-500: #f59e0b;
$tw-red-500: #ef4444;

/* Semantic */
$tw-border-neutral: $tw-slate-700;
$tw-outline-neutral: $tw-slate-500;

/* Transitions */
$tw-transition-fast: 120ms out_cubic 0ms;
$tw-transition-normal: 180ms out_cubic 0ms;
$tw-transition-slow: 280ms in_out_cubic 0ms;
```

Use in custom CSS alongside the utility sheet:

```css
MyWidget {
    background: $tw-slate-900;
    border: solid $tw-blue-500;
    transition: background $tw-transition-fast;
}
```

## Pseudo-classes

### In TCSS Selectors

```css
Button:hover { background: lightblue; }
Button:focus { border: double green; }
Button:disabled { opacity: 0.5; }

/* Custom state classes (prefixed with -) */
.sidebar.-visible { offset-x: 0; }
.item.-selected { background: $primary; }
```

### As Tailwind Utility Prefixes

```css
classes="hover:bg-blue-700 focus:border-round disabled:opacity-[50%]"
classes="dark:hover:bg-slate-700 focus-within:bg-[#1e293b]"
classes="odd:bg-[#0f172a] first-child:m-0"
```

All Textual pseudo-classes work as prefixes: `hover`, `focus`, `blur`, `focus-within`, `disabled`, `enabled`, `dark`, `light`, `first-child`, `last-child`, `odd`, `even`, `empty`.

## Common Patterns

### Animated Sidebar
```css
Sidebar {
    width: 30;
    dock: left;
    offset-x: -100%;
    transition: offset 200ms;

    &.-visible {
        offset-x: 0;
    }
}
```

### Centered Modal
```css
#modal {
    layer: modal;
    width: 60;
    height: 20;
    background: $surface;
    border: thick $primary;
}

Screen {
    align: center middle;
    layers: base modal;
}
```

### Responsive Grid
```css
Grid {
    layout: grid;
    grid-size: 3;
    grid-gutter: 1;
}

@media (max-width: 60) {
    Grid {
        grid-size: 2;
    }
}
```
