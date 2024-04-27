import { get } from 'svelte/store';
import { state } from "$lib/store.js"

export const load = async ({ fetch }) => {

	let page_name = "home"
	let mem = get(state)
	let i = mem.findIndex(x => x.name == page_name);

	if (i == -1) {
		mem.push({
			name: page_name,
			resp: [],
			loaded: false
		})
		state.set(mem)
		i = mem.findIndex(x => x.name == page_name);
	} else if (mem[i].loaded) {
		return mem[i].resp
	}

	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/home`)
	resp = await resp.json();

	if (resp.status == 200) {
		mem[i].resp = resp
		mem[i].loaded = true
		state.set(mem)

		return resp
	}
}
