# iOS‑style Photo Album App (React Native + TypeScript)

You are a senior full‑stack engineer and AI infra architect. Build an iOS‑Photos‑style React Native photo album app, with a zoomable media grid, strong static typing, and local‑first storage that can later grow into a cloud‑synced system.

## 1. Goal / UX

Create an app that feels like the native Apple Photos app on iOS:

- Main screen: smooth pinch‑to‑zoom media grid where zooming changes how many thumbnails fit on screen (e.g. 16 → 8 → 4 → 2 → 1), with animated transitions.
- Thumbnails automatically resize based on zoom level.
- Photos vs videos are clearly distinguished (play icon overlay + duration label).
- Tapping a thumbnail opens a full‑screen viewer with pinch‑to‑zoom and pan on images.

## 2. Tech Stack and Typing

Use this exact stack:

- **Platform:** React Native (iOS‑first UX, cross‑platform).
- **Language:** TypeScript with strict mode, no `any`.
- **Navigation:** React Navigation (stack).
- **State management:** Redux Toolkit with typed slices OR React Context + hooks with fully typed state.
- **Gestures/animation:** `react-native-gesture-handler` + `react-native-reanimated`.
- **Media picker:** `react-native-image-picker`.
- **Local persistence:** AsyncStorage, SQLite, or MMKV (choose one, implement a service wrapper).
- All domain models, component props, and global state must be strongly typed with TypeScript interfaces/types.

## 3. Core Gallery Behaviour (iOS Photos‑style Zoomable Grid)

Implement an iOS‑Photos‑style zoomable media grid:

**Pinch‑to‑zoom on the grid changes:**
- Number of columns
- Thumbnail size and spacing

**Zoom levels:**
- Many tiny thumbnails (5–6 columns)
- Medium (3–4 columns)
- Large (2–3 columns)
- Single column (1 item per row)

**Technical options (choose best):**
- Option A: Library like `react-native-zoom-grid`.
- Option B: Custom pinch gestures using `react-native-gesture-handler` + Reanimated — maintain a shared zoom/columns Reanimated value driving column count, item size, and spacing. Snap to nearest integer column count when pinch ends (e.g. 6 → 4 → 3 → 2 → 1).

**Required behaviours:**
- Pinch to zoom in/out on the grid.
- As zoom increases, dynamically reduce columns and scale thumbnails.
- Smooth, non‑janky animations during pinch and snap.
- Tap an item to open full‑screen viewer.

## 4. Full‑Screen Viewer (Images + Videos)

**For images:**
- Pinch‑to‑zoom (scale)
- Pan when zoomed in
- Snap back if zoom < 1 or rubber‑band drag
- Use `react-native-gesture-handler` + `react-native-reanimated` or `react-native-image-zoom`

**For videos:**
- Video player with native play/pause/seek controls
- Video may skip pinch‑zoom (prioritise image zoom)
- Close button ("×") top‑right to return to grid

## 5. Media Types and Thumbnails

**Support:** JPEG, PNG, HEIC (photos); MP4, HEVC (videos via `react-native-image-picker`).

**Thumbnails:**
- Photos: use main URI as thumbnail
- Videos: generate thumbnail frame; design `thumbnailService` interface for future plug‑in

**Video overlays:**
- Play icon overlay
- Duration label (e.g. 1:23)

**Interface:**
\`\`\`ts
generateThumbnail(uri: string, isVideo: boolean): Promise<string>
\`\`\`
(Returns original URI if extraction is out of scope; interface must exist and be used.)

## 6. Media Source and Storage

**Acquisition:** `react-native-image-picker` — device gallery and camera (photo/video).

**Storage:** Local‑first for v1 (AsyncStorage / SQLite / MMKV).

**Service layer (typed):**
- `storageService` — load/save albums and media metadata
- `mediaService` — return all media, add new media from picker, call thumbnail service

**Cloud‑sync ready:** code must allow swapping service internals (Firebase, Supabase, custom API) without changing screens/components.

## 7. Data Model (Strong Typing)

\`\`\`ts
export type MediaType = 'photo' | 'video';

export interface MediaItem {
  id: string;
  uri: string;
  type: MediaType;
  createdAt: string;       // ISO timestamp
  duration?: number;       // seconds, for videos
  thumbnailUri: string;
  width: number;
  height: number;
  albumId: string;
}

export interface Album {
  id: string;
  title: string;
  createdAt: string;       // ISO timestamp
}
\`\`\`

- No `any` anywhere
- All component props must have explicit interfaces
- Global state explicitly typed for state shape, actions, and selectors/hooks
- Dedicated service modules: media loading/saving, thumbnail generation/caching, persistence

## 8. Global State

Maintain global state for:
- Albums list
- Media items per album
- Current zoom level / grid configuration

**Options (pick one):**
- **Redux Toolkit:** typed slices (`createSlice` with proper `PayloadAction` types), typed selectors, TypeScript‑configured store
- **React Context + hooks:** `AlbumsProvider` wrapping app, custom hooks `useAlbums`, `useMedia`, internal state typed with interfaces

## 9. Project Structure

\`\`\`
src/
  App.tsx
  navigation/
    RootNavigator.tsx
  screens/
    GalleryScreen.tsx
    ViewerScreen.tsx
  components/
    MediaGrid.tsx
    MediaGridItem.tsx
    VideoOverlay.tsx
  context/          (if Context; else store/)
    AlbumsProvider.tsx
    MediaContext.tsx
  store/            (if Redux; else context/)
    store.ts
    albumsSlice.ts
    mediaSlice.ts
  services/
    mediaService.ts
    storageService.ts
    thumbnailService.ts
  models/
    media.ts
    album.ts
  hooks/
    useAlbums.ts
    useMedia.ts
  utils/
    formatDuration.ts
    constants.ts
package.json       (all required deps)
tsconfig.json      (strict mode, path aliases)
index.js / index.ts
babel.config.js    (if needed for Reanimated)
\`\`\`

## 10. Deliverables

When answering this prompt, provide:

1. Full file/folder tree
2. Full TypeScript/TSX code for all key files
3. `package.json` with dependencies and devDependencies
4. `tsconfig.json`
5. CLI commands: install deps, run on iOS simulator, run on Android
6. Brief explanation (2–3 sentences) of how the pinch‑to‑zoom grid maps pinch → column count and item size

Code should be ready to paste into a new React Native workspace and run with minimal adjustments.

---

## Quick‑use Short Version (for Perplexity / Zo)

Build an iOS‑Photos‑style photo album in React Native + TypeScript. Main screen is a pinch‑to‑zoom grid (5–6 cols → 1 col) with smooth animations. Tap a thumbnail → full‑screen viewer with pinch‑zoom + pan on images, video player for videos. Use `react-native-image-picker` for media acquisition, local persistence (AsyncStorage / SQLite / MMKV) via a typed service layer. Full TypeScript strict mode, no `any`. Structure: screens, components, services, models, hooks, context or Redux store. Cloud‑sync ready via swappable service internals.
