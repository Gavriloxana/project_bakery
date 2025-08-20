export default defineNuxtRouteMiddleware(() => {
  if (process.server) return
  const isAdmin = localStorage.getItem('is_admin') === '1'
  if (!isAdmin) {
    return navigateTo('/login')
  }
})