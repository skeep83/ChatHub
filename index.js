export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    const path = url.pathname

    if (path !== '/' && !path.includes('.') && !path.endsWith('/')) {
      const htmlUrl = new URL(request.url)
      htmlUrl.pathname = `${path}.html`
      const htmlResponse = await env.ASSETS.fetch(new Request(htmlUrl.toString(), request))
      if (htmlResponse.status < 400) {
        return htmlResponse
      }
    }

    return env.ASSETS.fetch(request)
  }
}
