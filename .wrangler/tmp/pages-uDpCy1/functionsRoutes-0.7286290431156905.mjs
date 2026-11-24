import { onRequestGet as __api_reviews_remove_js_onRequestGet } from "/home/claude/quran-online-tarteel/functions/api/reviews/remove.js"
import { onRequestPost as __api_reviews_remove_js_onRequestPost } from "/home/claude/quran-online-tarteel/functions/api/reviews/remove.js"
import { onRequestGet as __api_reviews_js_onRequestGet } from "/home/claude/quran-online-tarteel/functions/api/reviews.js"
import { onRequestPost as __api_reviews_js_onRequestPost } from "/home/claude/quran-online-tarteel/functions/api/reviews.js"
import { onRequest as ___middleware_js_onRequest } from "/home/claude/quran-online-tarteel/functions/_middleware.js"

export const routes = [
    {
      routePath: "/api/reviews/remove",
      mountPath: "/api/reviews",
      method: "GET",
      middlewares: [],
      modules: [__api_reviews_remove_js_onRequestGet],
    },
  {
      routePath: "/api/reviews/remove",
      mountPath: "/api/reviews",
      method: "POST",
      middlewares: [],
      modules: [__api_reviews_remove_js_onRequestPost],
    },
  {
      routePath: "/api/reviews",
      mountPath: "/api",
      method: "GET",
      middlewares: [],
      modules: [__api_reviews_js_onRequestGet],
    },
  {
      routePath: "/api/reviews",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_reviews_js_onRequestPost],
    },
  {
      routePath: "/",
      mountPath: "/",
      method: "",
      middlewares: [___middleware_js_onRequest],
      modules: [],
    },
  ]