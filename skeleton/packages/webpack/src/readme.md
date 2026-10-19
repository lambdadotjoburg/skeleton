# Webpack

Move this project to a standalone package!

### Issues:

1) Tightly coupled to frontend and python reverse proxy gateway server!

This project requires transformer to
pre-process binding expressions to be
consumed by @skeleton/core framework:

{ createTransformer } from "@skeleton/transformer";