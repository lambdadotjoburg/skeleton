// CSS
declare module "*.css";

// CSS modules
declare module "*.module.css" {
    const classes: {
        readonly [key: string]: string;
    };

    export default classes;
}

// Images
declare module "*.png" {
    const src: string;
    export default src;
}

declare module "*.jpg" {
    const src: string;
    export default src;
}

declare module "*.jpeg" {
    const src: string;
    export default src;
}

declare module "*.ico" {
    const src: string;
    export default src;
}

declare module "*.gif" {
    const src: string;
    export default src;
}

// Fonts
declare module "*.woff" {
    const src: string;
    export default src;
}

declare module "*.woff2" {
    const src: string;
    export default src;
}

declare module "*.eot" {
    const src: string;
    export default src;
}

declare module "*.ttf" {
    const src: string;
    export default src;
}

declare module "*.otf" {
    const src: string;
    export default src;
}

// SVG
declare module "*.svg" {
    const src: string;
    export default src;
}
