#!/bin/bash
# Create all missing Material Design icons

cd src/desktop_notify/iconsets/assets/material

# Create remaining icons with simplified SVG content

# Create icon with generic shape
create_icon() {
    local name=$1
    local color=${2:-#757575}
    if [ ! -f "$name.svg" ]; then
        echo "Creating $name.svg"
        cat > "$name.svg" << EOF
<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24" fill="$color">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
</svg>
EOF
    fi
}

# List of all icons we need based on breeze.yaml
for icon in copy cut paste undo redo find clear back forward up down \
    play pause stop next previous record music video microphone camera \
    printer scanner speaker headphones battery users network wifi bluetooth \
    power logout lock browser mail editor terminal calculator document \
    image archive load loading process working busy; do
    create_icon "$icon"
done

# Count total icons
echo "Total Material Design icons: $(ls -1 *.svg | wc -l)"