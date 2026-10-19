app/frontend/package.json:

```json
"scripts": {
    "start": "skeleton-webpack serve --env root=. --env servers=../../servers.json --env mode=dev",
    "build": "skeleton-webpack build --env root=. --env servers=../../servers.json --env mode=prod",
    "preview": "npx serve dist"
}
```