#!/bin/bash

set -e # exit if any command fails

echo "📦 Installing dotfiles..."

# Function to safely create symlinks
link_file() {
  local src=$1
  local dest=$2

  echo "🔗 Linking $src → $dest"

  # Remove existing file, folder, or symlink
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "🗑️ Removing existing $dest"
    rm -rf "$dest"
  fi

  mkdir -p "$(dirname "$dest")"
  ln -sfn "$src" "$dest"
}

# Link all files in ~/.config/
for item in "$HOME/dotfiles/config/"*; do
  if [ -f "$item" ] || [ -d "$item" ]; then
    link_file "$item" "$HOME/.config/$(basename "$item")"
  fi
done

# Link all files in $HOME directly
for file in "$HOME/dotfiles/home/"*; do
  if [ -f "$file" ]; then
    link_file "$file" "$HOME/$(basename "$file")"
  fi
done

echo "✅ Dotfiles installed successfully."
