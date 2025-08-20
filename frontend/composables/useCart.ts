import { ref, computed } from 'vue'

const items = ref<Array<{id:string; name:string; price:number; image_url?:string; quantity:number}>>([])

export function useCart() {
  const add = (p: {id:string; name:string; price:number; image_url?:string}, qty = 1) => {
    const found = items.value.find(i => i.id === p.id)
    if (found) found.quantity += qty
    else items.value.push({ id: p.id, name: p.name, price: p.price, image_url: p.image_url, quantity: qty })
  }
  const remove = (id: string) => { items.value = items.value.filter(i => i.id !== id) }
  const clear = () => { items.value = [] }
  const setQty = (id: string, qty: number) => {
    const it = items.value.find(i => i.id === id)
    if (it) it.quantity = Math.max(1, qty)
  }
  const total = computed(() => items.value.reduce((s,i)=> s + i.price*i.quantity, 0))

  return { items, add, remove, clear, setQty, total }
}
