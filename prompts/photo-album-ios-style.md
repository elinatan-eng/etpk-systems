# iOS‑Style Photo Album — Master Prompt

Build an iOS‑Photos‑style React Native photo album app with a pinch‑to‑zoom grid, strong static typing, and local‑first storage ready to grow into cloud sync.

## Tech Stack

- React Native + TypeScript strict mode (no `any`)
- React Navigation (stack)
- Redux Toolkit with typed slices OR React Context + hooks with fully typed state
- `react-native-gesture-handler` + `react-native-reanimated` for gestures
- `react-native-image-picker` for media acquisition
- AsyncStorage / SQLite / MMKV via typed service wrapper

## Core UX

- **Zoomable grid:** pinch on the grid changes column count (6 → 4 → 3 → 2 → 1), smoothly animating thumbnail sizes like iOS Photos
- **Full‑screen viewer:** pinch‑to‑zoom + pan on images; native video player for videos; close button to return
- **Video overlay:** play icon + duration label on video thumbnails
- **No `any` anywhere.** All models, props, state, and actions must be explicitly typed

## Data Model

```ts
type MediaType = 'photo' | 'video';
interface MediaItem { id: string; uri: string; type: MediaType; thumbnailUri: string; createdAt: string; width: number; height: number; albumId: string; duration?: number; }
interface Album { id: string; title: string; createdAt: string; }
```

## Service Layer

- `storageService`: load/save albums + media (local‑first, swappable for cloud)
- `mediaService`: pick from library, capture with camera, get/add media items
- `thumbnailService`: `ensureThumbnail(media): Promise<MediaItem>` interface (pass‑through for v1, plug‑in later)

## Project Structure

```
src/
  App.tsx
  navigation/RootNavigator.tsx
  screens/MediaGridScreen.tsx / MediaViewerScreen.tsx
  components/MediaGrid.tsx / MediaThumbnail.tsx / FullscreenImageViewer.tsx / FullscreenVideoViewer.tsx
  store/index.ts + mediaSlice.ts   (or context/)
  services/mediaService.ts / storageService.ts / thumbnailService.ts
  models/media.ts / album.ts
  hooks/useMedia.ts
  utils/formatDuration.ts / constants.ts
package.json / tsconfig.json / babel.config.js / index.js
```

## Deliverables

1. Full file/folder tree
2. Full TSX/TS code for every file above
3. `package.json` with all deps + devDeps
4. `tsconfig.json` with strict mode + path aliases
5. CLI: `npm install && npx react-native run-ios` (and Android equivalent)
6. 2–3 sentence explanation of how pinch → columns/item‑size mapping works

Code must paste into a fresh RN workspace and run with minimal tweaks.
