import { error } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, url, parent }) => {
	let a = await parent();
	if (!a.locals.user.permissions.includes("voucher:view")) {
		throw error(400, "unauthorized access")
	}

	let page_name = "vouchers"
	let mem = get(state)
	let i = mem.findIndex(x => x.name == page_name);
	
	if (i == -1) {
		mem.push({
			name: page_name,
			search: url.search,
			resp: [],
			loaded: false
		})
		state.set(mem)
		i = mem.findIndex(x => x.name == page_name);
	} else if (mem[i].loaded) {
		return mem[i].resp
	}
	
	let backend = new URL(`${import.meta.env.VITE_BACKEND}/voucher`)
	backend.search = mem[i].search
	let resp = await fetch(backend.href, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.set(false)

	if (resp.status == 200) {
		resp.page_name = page_name

		mem[i].resp = resp
		mem[i].loaded = true
		state.set(mem)

		return resp
	}
}