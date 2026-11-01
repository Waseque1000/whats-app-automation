"""Theme constants and color definitions for CustomTkinter."""

# ── Core Background Palette ────────────────────────────────────────────────────
COLOR_BACKGROUND   = "#070B0F"       # Near-black page canvas
COLOR_SIDEBAR      = "#0D1117"       # Sidebar — slightly lighter
COLOR_CARD         = "#111827"       # Card surfaces
COLOR_CARD_HOVER   = "#1A2234"       # Card hover / active row
COLOR_BORDER       = "#1E2A3A"       # Subtle separator borders
COLOR_BORDER_LIGHT = "#253347"       # Brighter border for active states

# ── Accent / Brand Colors ──────────────────────────────────────────────────────
COLOR_PRIMARY        = "#00D46A"     # WhatsApp emerald — primary CTA
COLOR_PRIMARY_HOVER  = "#00F078"     # Brighter on hover
COLOR_PRIMARY_DIM    = "#00D46A22"   # Transparent tint for active nav bg
COLOR_PRIMARY_GLOW   = "#00D46A"     # Used for glow borders

COLOR_SECONDARY      = "#06B6D4"     # Cyan — secondary accent
COLOR_SECONDARY_HOVER= "#22D3EE"

COLOR_ACCENT_PURPLE  = "#8B5CF6"     # Purple — tertiary / messages
COLOR_ACCENT_ORANGE  = "#F59E0B"     # Amber — warnings

# ── Status Colors ──────────────────────────────────────────────────────────────
COLOR_SUCCESS  = "#00D46A"
COLOR_WARNING  = "#F59E0B"
COLOR_DANGER   = "#EF4444"
COLOR_INFO     = "#06B6D4"

# ── Text ───────────────────────────────────────────────────────────────────────
COLOR_TEXT          = "#F0F6FC"      # Primary text — bright white
COLOR_TEXT_MUTED    = "#8B949E"      # Secondary labels
COLOR_TEXT_DISABLED = "#484F58"

# ── Table & Treeview ───────────────────────────────────────────────────────────
COLOR_TABLE_BG      = "#0D1117"
COLOR_TABLE_STRIPE  = "#111827"
COLOR_TABLE_HEADER  = "#090E14"
COLOR_TABLE_SEL_BG  = "#162032"
COLOR_TABLE_SEL_FG  = "#00D46A"

# ── Sidebar ────────────────────────────────────────────────────────────────────
COLOR_NAV_ACTIVE_BG   = "#0F2A1A"   # Active nav item background
COLOR_NAV_ACTIVE_TEXT = "#00D46A"   # Active nav item text
COLOR_NAV_HOVER_BG    = "#131E2B"   # Hover nav background

# ── Font Definitions ───────────────────────────────────────────────────────────
FONT_FAMILY = "Inter"
FONT_MONO   = "JetBrains Mono"

FONT_HEADLINE_XL = (FONT_FAMILY, 24, "bold")
FONT_HEADLINE_LG = (FONT_FAMILY, 18, "bold")
FONT_HEADLINE_MD = (FONT_FAMILY, 15, "bold")
FONT_HEADLINE_SM = (FONT_FAMILY, 12, "bold")

FONT_BODY_LG  = (FONT_FAMILY, 14)
FONT_BODY_MD  = (FONT_FAMILY, 13)
FONT_BODY_SM  = (FONT_FAMILY, 11)
FONT_CAPTION  = (FONT_FAMILY, 10)

FONT_CODE_MD  = (FONT_MONO, 12)
FONT_CODE_SM  = (FONT_MONO, 11)
